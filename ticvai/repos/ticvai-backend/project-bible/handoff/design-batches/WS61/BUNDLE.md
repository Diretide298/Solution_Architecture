# WS61 — Ticket Media   Credential Management board 3

**10 screens · 10 operations · 12 schemas · 2 permissions**

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
| `BO-354` | Credential Operations Command Center | commandCentre | 1 | 0 | — |
| `BO-355` | Virtual Ticket & Credential 360° Workspace | commandCentre | 1 | 0 | — |
| `BO-356` | Credential Generation & Issuance Monitor | listDetail | 1 | 0 | — |
| `BO-357` | Credential Delivery & Distribution Operations | listDetail | 1 | 0 | — |
| `BO-358` | Media Binding, Activation & Assignment Operations | listDetail | 1 | 0 | — |
| `BO-359` | Credential Replacement, Reissue, Revocation & Recovery | configEditor | 1 | 0 | — |
| `BO-360` | Failed Generation, Delivery & Credential Exception Management | listDetail | 1 | 0 | — |
| `BO-361` | Credential Usage & Cross-Media Traceability | configEditor | 1 | 0 | — |
| `BO-362` | Credential Security, Audit & Operational Evidence | listDetail | 1 | 0 | — |
| `BO-363` | Ticket Media Analytics & AI Operations Intelligence | listDetail | 1 | 0 | — |

## Thin screens in this batch

**BO-362 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "BO-354",
  "name": "Credential Operations Command Center",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Ticket_Media___Credential_Management_Reference.pdf",
   "board": "3",
   "number": "15.3.1",
   "page": 41
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/credential-operations-command-center-bo-354",
   "component": "apps/venue-management-web/src/routes/access-venue/CredentialOperationsCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-100"
   ],
   "exitTo": [
    "BO-100",
    "BO-355",
    "BO-356",
    "BO-357",
    "BO-358",
    "BO-359",
    "BO-360",
    "BO-361",
    "BO-362",
    "BO-363"
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
     "to": "BO-355",
     "trigger": "Works in Virtual Ticket & Credential 360° Workspace",
     "provenance": "flow F170 step 1→2",
     "operation": "listCredential"
    },
    {
     "to": "BO-356",
     "trigger": "Works in Credential Generation & Issuance Monitor",
     "provenance": "flow F170 step 3→4",
     "operation": "listCredential"
    },
    {
     "to": "BO-357",
     "trigger": "Works in Credential Delivery & Distribution Operations",
     "provenance": "flow F170 step 5→6",
     "operation": "listCredential"
    },
    {
     "to": "BO-358",
     "trigger": "Works in Media Binding, Activation & Assignment Operations",
     "provenance": "flow F170 step 7→8",
     "operation": "listCredential"
    },
    {
     "to": "BO-359",
     "trigger": "Works in Credential Replacement, Reissue, Revocation & Recovery",
     "provenance": "flow F170 step 9→10",
     "operation": "listCredential"
    },
    {
     "to": "BO-360",
     "trigger": "Works in Failed Generation, Delivery & Credential Exception Management",
     "provenance": "flow F170 step 11→12",
     "operation": "listCredential"
    },
    {
     "to": "BO-361",
     "trigger": "Works in Credential Usage & Cross-Media Traceability",
     "provenance": "flow F170 step 13→14",
     "operation": "listCredential"
    },
    {
     "to": "BO-362",
     "trigger": "Works in Credential Security, Audit & Operational Evidence",
     "provenance": "flow F170 step 15→16",
     "operation": "listCredential"
    },
    {
     "to": "BO-363",
     "trigger": "Works in Ticket Media Analytics & AI Operations Intelligence",
     "provenance": "flow F170 step 17→18",
     "operation": "listCredential"
    }
   ]
  },
  "density": "compact",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen both a metric directory (§Display) and a per-row directory (§Each record should show) — counts over a population, then the population",
  "purpose": "Provide Operations, Ticketing, Customer Service and Technical teams with a real-time command center covering all issued credential media. This is the operational starting point for Area 15.",
  "purposeNote": "Operations can understand the health, status and exceptions of all issued credentials from one central workspace.",
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "filters",
     "components": [
      {
       "kind": "searchField",
       "label": "Search credential operations",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 41 §Filter by"
      },
      {
       "kind": "multiSelect",
       "label": "Filter by",
       "columns": [
        "Brand",
        "Venue",
        "CredentialOperationsCommandCenterView.event",
        "CredentialOperationsCommandCenterView.product",
        "Date",
        "Media",
        "CredentialOperationsCommandCenterView.provider",
        "Status",
        "Channel",
        "CredentialOperationsCommandCenterView.exception",
        "Customer"
       ],
       "notes": "The pack filters this screen by brand, venue, event, product, date, media and 5 more — which are present is a decision the pack already made.",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 41 §Filter by"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Virtual Tickets Issued",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 41 §Display",
       "bindsTo": "CredentialOperationsCommandCenterView.virtualTicketsIssued"
      },
      {
       "kind": "metricTile",
       "label": "Credentials Generated",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 41 §Display",
       "bindsTo": "CredentialOperationsCommandCenterView.credentialsGenerated"
      },
      {
       "kind": "metricTile",
       "label": "Active Credentials",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 41 §Display",
       "bindsTo": "CredentialOperationsCommandCenterView.activeCredentials"
      },
      {
       "kind": "metricTile",
       "label": "Pending Generation",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 41 §Display",
       "bindsTo": "CredentialOperationsCommandCenterView.pendingGeneration"
      },
      {
       "kind": "metricTile",
       "label": "Pending Delivery",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 41 §Display",
       "bindsTo": "CredentialOperationsCommandCenterView.pendingDelivery"
      },
      {
       "kind": "metricTile",
       "label": "Pending Binding",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 41 §Display",
       "bindsTo": "CredentialOperationsCommandCenterView.pendingBinding"
      },
      {
       "kind": "metricTile",
       "label": "Pending Activation",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 41 §Display",
       "bindsTo": "CredentialOperationsCommandCenterView.pendingActivation"
      },
      {
       "kind": "metricTile",
       "label": "Suspended",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 41 §Display",
       "bindsTo": "CredentialOperationsCommandCenterView.suspended"
      },
      {
       "kind": "metricTile",
       "label": "Revoked",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 41 §Display",
       "bindsTo": "CredentialOperationsCommandCenterView.revoked"
      },
      {
       "kind": "metricTile",
       "label": "Expired",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 41 §Display",
       "bindsTo": "CredentialOperationsCommandCenterView.expired"
      },
      {
       "kind": "metricTile",
       "label": "Failed Generation",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 41 §Display",
       "bindsTo": "CredentialOperationsCommandCenterView.failedGeneration"
      },
      {
       "kind": "metricTile",
       "label": "Failed Delivery",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 41 §Display",
       "bindsTo": "CredentialOperationsCommandCenterView.failedDelivery"
      },
      {
       "kind": "metricTile",
       "label": "Synchronization Exceptions",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 41 §Display",
       "bindsTo": "CredentialOperationsCommandCenterView.synchronizationExceptions"
      },
      {
       "kind": "metricTile",
       "label": "Multi-Media Virtual Tickets",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 41 §Display",
       "bindsTo": "CredentialOperationsCommandCenterView.multiMediaVirtualTickets"
      },
      {
       "kind": "metricTile",
       "label": "Virtual Tickets Without Active Media",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 41 §Display"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "moduleTiles",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every credential operations",
       "columns": [
        "CredentialOperationsCommandCenterView.virtualTicketId",
        "CredentialOperationsCommandCenterView.credentialId",
        "CredentialOperationsCommandCenterView.mediaType",
        "CredentialOperationsCommandCenterView.customerParticipant",
        "CredentialOperationsCommandCenterView.product",
        "CredentialOperationsCommandCenterView.event",
        "CredentialOperationsCommandCenterView.credentialStatus",
        "CredentialOperationsCommandCenterView.deliveryStatus",
        "CredentialOperationsCommandCenterView.activationStatus",
        "CredentialOperationsCommandCenterView.bindingStatus",
        "CredentialOperationsCommandCenterView.provider",
        "CredentialOperationsCommandCenterView.lastActivity",
        "CredentialOperationsCommandCenterView.exception",
        "CredentialOperationsCommandCenterView.owner"
       ],
       "bindsTo": "CredentialOperationsCommandCenterView",
       "operation": "listCredential",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 41 §Each record should show"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected credential operations",
       "bindsTo": "CredentialOperationsCommandCenterView",
       "columns": [
        "CredentialOperationsCommandCenterView.virtualTicketId",
        "CredentialOperationsCommandCenterView.credentialId",
        "CredentialOperationsCommandCenterView.mediaType",
        "CredentialOperationsCommandCenterView.customerParticipant",
        "CredentialOperationsCommandCenterView.product",
        "CredentialOperationsCommandCenterView.event",
        "CredentialOperationsCommandCenterView.credentialStatus",
        "CredentialOperationsCommandCenterView.deliveryStatus",
        "CredentialOperationsCommandCenterView.activationStatus",
        "CredentialOperationsCommandCenterView.bindingStatus",
        "CredentialOperationsCommandCenterView.provider",
        "CredentialOperationsCommandCenterView.lastActivity",
        "CredentialOperationsCommandCenterView.exception",
        "CredentialOperationsCommandCenterView.owner"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Display credentials by”, “Provide indicators such as”.",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 41 §Each record should show"
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
       "notes": "**The pack separates these permissions and no action on the screen claims them yet:** Open Virtual Ticket, Generate Credential, Resend, Activate, Suspend Media, Replace, Revoke, Diagnose, View History. Each needs attaching to the control it gates, or the screen needs the control.",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 41 §Authorized users can"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The credential operations list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the credential operations untouched.",
   "emptyFirstRun": "No credential operations yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the credential operations are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listCredential",
    "contract": "access",
    "purpose": "Credential Operations Command Center",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-354"
  },
  "apisNote": "Regenerated 9 September 2026 from Ticket_Media___Credential_Management_Reference.pdf page 41. 32 of 39 labels bound to a contract property; 49 of 72 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-355",
  "name": "Virtual Ticket & Credential 360° Workspace",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Ticket_Media___Credential_Management_Reference.pdf",
   "board": "3",
   "number": "15.3.2",
   "page": 43
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/virtual-ticket-credential-360-workspace-bo-355",
   "component": "apps/venue-management-web/src/routes/access-venue/VirtualTicketCredential360Workspace.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-354"
   ],
   "exitTo": [
    "BO-354"
   ],
   "inferred": false,
   "notes": "**Reached from BO-354, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-354",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F170 step 2→3",
     "operation": "setVirtualTicketCredential"
    }
   ]
  },
  "density": "compact",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen both a metric directory (§Display; Identify) and a per-row directory (§For each media show) — counts over a population, then the population",
  "purpose": "Provide a complete operational view of one Virtual Ticket and every media credential currently or historically associated with it. This is one of the most important operational screens.",
  "purposeNote": "Staff can view and manage the complete multi-media credential history of a Virtual Ticket without treating each credential as a separate ticket.",
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Virtual Ticket ID",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 43 §Display",
       "bindsTo": "VirtualTicketCredential360WorkspaceView.virtualTicketId"
      },
      {
       "kind": "metricTile",
       "label": "Ticket Holder",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 43 §Display",
       "bindsTo": "VirtualTicketCredential360WorkspaceView.ticketHolder"
      },
      {
       "kind": "metricTile",
       "label": "Participant",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 43 §Display",
       "bindsTo": "VirtualTicketCredential360WorkspaceView.participant"
      },
      {
       "kind": "metricTile",
       "label": "Product",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 43 §Display",
       "bindsTo": "VirtualTicketCredential360WorkspaceView.product"
      },
      {
       "kind": "metricTile",
       "label": "Event",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 43 §Display",
       "bindsTo": "VirtualTicketCredential360WorkspaceView.event"
      },
      {
       "kind": "metricTile",
       "label": "Performance",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 43 §Display",
       "bindsTo": "VirtualTicketCredential360WorkspaceView.performance"
      },
      {
       "kind": "metricTile",
       "label": "Venue",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 43 §Display",
       "bindsTo": "VirtualTicketCredential360WorkspaceView.venue"
      },
      {
       "kind": "metricTile",
       "label": "Seat",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 43 §Display",
       "bindsTo": "VirtualTicketCredential360WorkspaceView.seat"
      },
      {
       "kind": "metricTile",
       "label": "Order",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 43 §Display",
       "bindsTo": "VirtualTicketCredential360WorkspaceView.order"
      },
      {
       "kind": "metricTile",
       "label": "Ticket Status",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 43 §Display",
       "bindsTo": "VirtualTicketCredential360WorkspaceView.ticketStatus"
      },
      {
       "kind": "metricTile",
       "label": "Usage Status",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 43 §Display",
       "bindsTo": "VirtualTicketCredential360WorkspaceView.usageStatus"
      },
      {
       "kind": "metricTile",
       "label": "Validity",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 43 §Display",
       "bindsTo": "VirtualTicketCredential360WorkspaceView.validity"
      },
      {
       "kind": "metricTile",
       "label": "Entitlements",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 43 §Display",
       "bindsTo": "VirtualTicketCredential360WorkspaceView.entitlements"
      },
      {
       "kind": "metricTile",
       "label": "Primary",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 43 §Identify",
       "bindsTo": "VirtualTicketCredential360WorkspaceView.primary"
      },
      {
       "kind": "metricTile",
       "label": "Secondary",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 43 §Identify",
       "bindsTo": "VirtualTicketCredential360WorkspaceView.secondary"
      },
      {
       "kind": "metricTile",
       "label": "Fallback",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 43 §Identify",
       "bindsTo": "VirtualTicketCredential360WorkspaceView.fallback"
      },
      {
       "kind": "metricTile",
       "label": "Temporary",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 43 §Identify",
       "bindsTo": "VirtualTicketCredential360WorkspaceView.temporary"
      },
      {
       "kind": "metricTile",
       "label": "Revoked historical media",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 43 §Identify",
       "bindsTo": "VirtualTicketCredential360WorkspaceView.revokedHistoricalMedia"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "moduleTiles",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every virtual ticket credential",
       "columns": [
        "VirtualTicketCredential360WorkspaceView.bindingId",
        "VirtualTicketCredential360WorkspaceView.mediaType",
        "VirtualTicketCredential360WorkspaceView.provider",
        "VirtualTicketCredential360WorkspaceView.issued",
        "VirtualTicketCredential360WorkspaceView.delivered",
        "VirtualTicketCredential360WorkspaceView.activated",
        "Valid From/To",
        "VirtualTicketCredential360WorkspaceView.lastUpdate",
        "Last presentation/use",
        "VirtualTicketCredential360WorkspaceView.deviceReferenceWhereAppropriate",
        "VirtualTicketCredential360WorkspaceView.status"
       ],
       "bindsTo": "VirtualTicketCredential360WorkspaceView",
       "operation": "setVirtualTicketCredential",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 43 §For each media show"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected virtual ticket credential",
       "bindsTo": "VirtualTicketCredential360WorkspaceView",
       "columns": [
        "VirtualTicketCredential360WorkspaceView.bindingId",
        "VirtualTicketCredential360WorkspaceView.mediaType",
        "VirtualTicketCredential360WorkspaceView.provider",
        "VirtualTicketCredential360WorkspaceView.issued",
        "VirtualTicketCredential360WorkspaceView.delivered",
        "VirtualTicketCredential360WorkspaceView.activated",
        "Valid From/To",
        "VirtualTicketCredential360WorkspaceView.lastUpdate",
        "Last presentation/use",
        "VirtualTicketCredential360WorkspaceView.deviceReferenceWhereAppropriate",
        "VirtualTicketCredential360WorkspaceView.status"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Credential Wallet”, “Media Status”, “Dynamic QR Active”, “Apple Wallet Active”, “Old RFID RF-88410”, “Provide one chronological timeline”.",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 43 §For each media show"
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
       "provenance": "contract operation setVirtualTicketCredential"
      },
      {
       "kind": "banner",
       "label": "Permissions this screen separates",
       "notes": "**The pack separates these permissions and no action on the screen claims them yet:** Generate Additional Media, Bind RFID, Add Wallet Pass, Initiate Face Enrollment, Replace Media, Suspend, Revoke, Resend, Refresh, Diagnose. Each needs attaching to the control it gates, or the screen needs the control.",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 43 §Depending on permission"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The virtual ticket credential list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the virtual ticket credential untouched.",
   "emptyFirstRun": "No virtual ticket credential yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the virtual ticket credential are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setVirtualTicketCredential",
    "contract": "access",
    "purpose": "Virtual Ticket & Credential 360° Workspace",
    "trigger": "onAction",
    "invalidates": [
     "setVirtualTicketCredential"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-355"
  },
  "apisNote": "Regenerated 9 September 2026 from Ticket_Media___Credential_Management_Reference.pdf page 43. 27 of 29 labels bound to a contract property; 39 of 53 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-356",
  "name": "Credential Generation & Issuance Monitor",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Ticket_Media___Credential_Management_Reference.pdf",
   "board": "3",
   "number": "15.3.3",
   "page": 45
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/credential-generation-issuance-monitor-bo-356",
   "component": "apps/venue-management-web/src/routes/access-venue/CredentialGenerationIssuanceMonitor.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-354"
   ],
   "exitTo": [
    "BO-354"
   ],
   "inferred": false,
   "notes": "**Reached from BO-354, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-354",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F170 step 4→5",
     "operation": "listCredentialGenerationIssuance"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Show; Display) and no metric row",
  "purpose": "Manage and monitor generation of credential instances from approved Board 2 media templates.",
  "purposeNote": "operational visibility into successful and failed issuance.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 5 actions on this screen and the screen declares 1 operation.** Unserved: Automatic Retry, Manual Retry, Retry Selected, Retry All Eligible, Escalate. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Ticket_Media___Credential_Management_Reference.pdf, page 45 §Support"
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
       "label": "Every credential generation issuance",
       "columns": [
        "→ Bound → Ready → Delivered",
        "CredentialGenerationIssuanceMonitorView.requestId",
        "CredentialGenerationIssuanceMonitorView.virtualTicket",
        "CredentialGenerationIssuanceMonitorView.media",
        "CredentialGenerationIssuanceMonitorView.template",
        "CredentialGenerationIssuanceMonitorView.templateVersion",
        "CredentialGenerationIssuanceMonitorView.product",
        "CredentialGenerationIssuanceMonitorView.customer",
        "Trigger",
        "CredentialGenerationIssuanceMonitorView.provider",
        "CredentialGenerationIssuanceMonitorView.requestedAt",
        "CredentialGenerationIssuanceMonitorView.generatedAt",
        "CredentialGenerationIssuanceMonitorView.status",
        "CredentialGenerationIssuanceMonitorView.error"
       ],
       "bindsTo": "CredentialGenerationIssuanceMonitorView",
       "operation": "listCredentialGenerationIssuance",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 45 §Show"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected credential generation issuance",
       "bindsTo": "CredentialGenerationIssuanceMonitorView",
       "columns": [
        "→ Bound → Ready → Delivered",
        "CredentialGenerationIssuanceMonitorView.requestId",
        "CredentialGenerationIssuanceMonitorView.virtualTicket",
        "CredentialGenerationIssuanceMonitorView.media",
        "CredentialGenerationIssuanceMonitorView.template",
        "CredentialGenerationIssuanceMonitorView.templateVersion",
        "CredentialGenerationIssuanceMonitorView.product",
        "CredentialGenerationIssuanceMonitorView.customer",
        "Trigger",
        "CredentialGenerationIssuanceMonitorView.provider",
        "CredentialGenerationIssuanceMonitorView.requestedAt",
        "CredentialGenerationIssuanceMonitorView.generatedAt",
        "CredentialGenerationIssuanceMonitorView.status",
        "CredentialGenerationIssuanceMonitorView.error"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Generation Sources”, “Template Resolution”, “Bulk Generation”, “Failures may include”.",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 45 §Show"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Automatic Retry",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 45 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Manual Retry",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 45 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Retry Selected",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 45 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Retry All Eligible",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 45 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Escalate",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 45 §Support"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The credential generation issuance list.",
   "error": "Could not load. Names which read failed and leaves the credential generation issuance untouched.",
   "emptyFirstRun": "No credential generation issuance yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the credential generation issuance are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listCredentialGenerationIssuance",
    "contract": "access",
    "purpose": "Credential Generation & Issuance Monitor",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "→ Bound → Ready → Delivered",
    "CredentialGenerationIssuanceMonitorView.requestId",
    "CredentialGenerationIssuanceMonitorView.virtualTicket",
    "CredentialGenerationIssuanceMonitorView.media",
    "CredentialGenerationIssuanceMonitorView.template",
    "CredentialGenerationIssuanceMonitorView.templateVersion"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-356"
  },
  "apisNote": "Regenerated 9 September 2026 from Ticket_Media___Credential_Management_Reference.pdf page 45. 12 of 14 labels bound to a contract property; 19 of 57 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-357",
  "name": "Credential Delivery & Distribution Operations",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Ticket_Media___Credential_Management_Reference.pdf",
   "board": "3",
   "number": "15.3.4",
   "page": 47
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/credential-delivery-distribution-operations-bo-357",
   "component": "apps/venue-management-web/src/routes/access-venue/CredentialDeliveryDistributionOperations.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-354"
   ],
   "exitTo": [
    "BO-354"
   ],
   "inferred": false,
   "notes": "**Reached from BO-354, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-354",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F170 step 6→7",
     "operation": "listCredentialDeliveryDistribution"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Show) and no metric row",
  "purpose": "Manage how generated ticket media are delivered or made available to customers, participants and operational staff.",
  "purposeNote": "delivery tracking.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 6 actions on this screen and the screen declares 1 operation.** Unserved: SMS Link, Send All, Send Selected, Resend Failed, Send Group, Export Status. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Ticket_Media___Credential_Management_Reference.pdf, page 47 §Support as applicable"
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
       "label": "Every credential delivery distribution",
       "columns": [
        "CredentialDeliveryDistributionOperationsView.virtualTicket",
        "CredentialDeliveryDistributionOperationsView.media",
        "CredentialDeliveryDistributionOperationsView.recipient",
        "CredentialDeliveryDistributionOperationsView.channel",
        "CredentialDeliveryDistributionOperationsView.destination",
        "CredentialDeliveryDistributionOperationsView.sentAt",
        "CredentialDeliveryDistributionOperationsView.deliveredAt",
        "CredentialDeliveryDistributionOperationsView.openedDownloaded",
        "CredentialDeliveryDistributionOperationsView.attempt",
        "CredentialDeliveryDistributionOperationsView.status"
       ],
       "bindsTo": "CredentialDeliveryDistributionOperationsView",
       "operation": "listCredentialDeliveryDistribution",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 47 §Show"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected credential delivery distribution",
       "bindsTo": "CredentialDeliveryDistributionOperationsView",
       "columns": [
        "CredentialDeliveryDistributionOperationsView.virtualTicket",
        "CredentialDeliveryDistributionOperationsView.media",
        "CredentialDeliveryDistributionOperationsView.recipient",
        "CredentialDeliveryDistributionOperationsView.channel",
        "CredentialDeliveryDistributionOperationsView.destination",
        "CredentialDeliveryDistributionOperationsView.sentAt",
        "CredentialDeliveryDistributionOperationsView.deliveredAt",
        "CredentialDeliveryDistributionOperationsView.openedDownloaded",
        "CredentialDeliveryDistributionOperationsView.attempt",
        "CredentialDeliveryDistributionOperationsView.status"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Alternative states”, “Where allowed, support”.",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 47 §Show"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "SMS Link",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 47 §Support as applicable"
      },
      {
       "kind": "secondaryButton",
       "label": "Send All",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 47 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Send Selected",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 47 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Resend Failed",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 47 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Send Group",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 47 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Export Status",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 47 §Support"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The credential delivery distribution list.",
   "error": "Could not load. Names which read failed and leaves the credential delivery distribution untouched.",
   "emptyFirstRun": "No credential delivery distribution yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the credential delivery distribution are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listCredentialDeliveryDistribution",
    "contract": "access",
    "purpose": "Credential Delivery & Distribution Operations",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "CredentialDeliveryDistributionOperationsView.virtualTicket",
    "CredentialDeliveryDistributionOperationsView.media",
    "CredentialDeliveryDistributionOperationsView.recipient",
    "CredentialDeliveryDistributionOperationsView.channel",
    "CredentialDeliveryDistributionOperationsView.destination",
    "CredentialDeliveryDistributionOperationsView.sentAt"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-357"
  },
  "apisNote": "Regenerated 9 September 2026 from Ticket_Media___Credential_Management_Reference.pdf page 47. 10 of 10 labels bound to a contract property; 22 of 50 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-358",
  "name": "Media Binding, Activation & Assignment Operations",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Ticket_Media___Credential_Management_Reference.pdf",
   "board": "3",
   "number": "15.3.5",
   "page": 48
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/media-binding-activation-assignment-operations-bo-358",
   "component": "apps/venue-management-web/src/routes/access-venue/MediaBindingActivationAssignmentOperations.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-354"
   ],
   "exitTo": [
    "BO-354"
   ],
   "inferred": false,
   "notes": "**Reached from BO-354, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-354",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F170 step 8→9",
     "operation": "setMediaBindingActivation"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Manage credentials that require operational assignment or activation after ticket issuance.",
  "purposeNote": "Operational staff can securely assign and activate supported physical, digital and biometric credential media against the correct Virtual Ticket.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 4 actions on this screen and the screen declares 1 operation.** Unserved: Activate Now, Schedule, Activate on First Use, Activate on Collection. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Ticket_Media___Credential_Management_Reference.pdf, page 48 §Allow"
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
       "label": "Every media binding activation",
       "columns": [
        "MediaBindingActivationAssignmentOperationsView.virtualTicket",
        "MediaBindingActivationAssignmentOperationsView.customer",
        "MediaBindingActivationAssignmentOperationsView.product",
        "MediaBindingActivationAssignmentOperationsView.existingMedia",
        "MediaBindingActivationAssignmentOperationsView.newMediaType",
        "MediaBindingActivationAssignmentOperationsView.credentialIdUid",
        "MediaBindingActivationAssignmentOperationsView.provider",
        "MediaBindingActivationAssignmentOperationsView.activation",
        "MediaBindingActivationAssignmentOperationsView.validity",
        "MediaBindingActivationAssignmentOperationsView.bindingRule"
       ],
       "bindsTo": "MediaBindingActivationAssignmentOperationsView",
       "operation": "setMediaBindingActivation",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 48 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected media binding activation",
       "bindsTo": "MediaBindingActivationAssignmentOperationsView",
       "columns": [
        "MediaBindingActivationAssignmentOperationsView.virtualTicket",
        "MediaBindingActivationAssignmentOperationsView.customer",
        "MediaBindingActivationAssignmentOperationsView.product",
        "MediaBindingActivationAssignmentOperationsView.existingMedia",
        "MediaBindingActivationAssignmentOperationsView.newMediaType",
        "MediaBindingActivationAssignmentOperationsView.credentialIdUid",
        "MediaBindingActivationAssignmentOperationsView.provider",
        "MediaBindingActivationAssignmentOperationsView.activation",
        "MediaBindingActivationAssignmentOperationsView.validity",
        "MediaBindingActivationAssignmentOperationsView.bindingRule"
       ],
       "notes": "The pack groups this record's detail under its own headings: “This is especially important for”, “Scan Virtual Ticket QR”, “Scan Wristband UID”, “Resolve Virtual Ticket”, “Bind”, “Activate”.",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 48 §Display"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Activate Now",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 48 §Allow"
      },
      {
       "kind": "secondaryButton",
       "label": "Schedule",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 48 §Allow"
      },
      {
       "kind": "secondaryButton",
       "label": "Activate on First Use",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 48 §Allow"
      },
      {
       "kind": "secondaryButton",
       "label": "Activate on Collection",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 48 §Allow"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The media binding activation list.",
   "error": "Could not load. Names which read failed and leaves the media binding activation untouched.",
   "emptyFirstRun": "No media binding activation yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the media binding activation are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setMediaBindingActivation",
    "contract": "access",
    "purpose": "Media Binding, Activation & Assignment Operations",
    "trigger": "onAction",
    "invalidates": [
     "setMediaBindingActivation"
    ]
   }
  ],
  "entryState": {
   "preloaded": [
    "MediaBindingActivationAssignmentOperationsView.virtualTicket",
    "MediaBindingActivationAssignmentOperationsView.customer",
    "MediaBindingActivationAssignmentOperationsView.product",
    "MediaBindingActivationAssignmentOperationsView.existingMedia",
    "MediaBindingActivationAssignmentOperationsView.newMediaType",
    "MediaBindingActivationAssignmentOperationsView.credentialIdUid"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-358"
  },
  "apisNote": "Regenerated 9 September 2026 from Ticket_Media___Credential_Management_Reference.pdf page 48. 10 of 10 labels bound to a contract property; 15 of 40 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-359",
  "name": "Credential Replacement, Reissue, Revocation & Recovery",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Ticket_Media___Credential_Management_Reference.pdf",
   "board": "3",
   "number": "15.3.6",
   "page": 50
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/credential-replacement-reissue-revocation-recovery-bo-359",
   "component": "apps/venue-management-web/src/routes/access-venue/CredentialReplacementReissueRevocationRecovery.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-354"
   ],
   "exitTo": [
    "BO-354"
   ],
   "inferred": false,
   "notes": "**Reached from BO-354, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-354",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F170 step 10→11",
     "operation": "listCredentialReplacementReissue"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure/reference) and no display directory — it is settings, not a population",
  "purpose": "Manage operational credential changes while preserving the underlying Virtual Ticket.",
  "purposeNote": "Ticket and without losing historical traceability.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 1 actions on this screen and the screen declares 1 operation.** Unserved: Customer changed phone. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Ticket_Media___Credential_Management_Reference.pdf, page 50 §Support"
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
       "label": "Immediate old-media revocation",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 50 §Configure/reference"
      },
      {
       "kind": "selectField",
       "label": "Grace period",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 50 §Configure/reference"
      },
      {
       "kind": "selectField",
       "label": "Maximum replacements",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 50 §Configure/reference"
      },
      {
       "kind": "selectField",
       "label": "Identity verification",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 50 §Configure/reference"
      },
      {
       "kind": "selectField",
       "label": "Supervisor approval",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 50 §Configure/reference"
      },
      {
       "kind": "selectField",
       "label": "Reason codes",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 50 §Configure/reference"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Customer changed phone",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 50 §Support"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The credential replacement reissue configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the credential replacement reissue untouched.",
   "emptyFirstRun": "No credential replacement reissue configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listCredentialReplacementReissue",
    "contract": "access",
    "purpose": "Credential Replacement, Reissue, Revocation & Recovery",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-359"
  },
  "apisNote": "Regenerated 9 September 2026 from Ticket_Media___Credential_Management_Reference.pdf page 50. 0 of 0 labels bound to a contract property; 7 of 37 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-360",
  "name": "Failed Generation, Delivery & Credential Exception Management",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Ticket_Media___Credential_Management_Reference.pdf",
   "board": "3",
   "number": "15.3.7",
   "page": 51
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/failed-generation-delivery-credential-exception-manageme-bo-360",
   "component": "apps/venue-management-web/src/routes/access-venue/FailedGenerationDeliveryCredentialExceptionManag.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-354"
   ],
   "exitTo": [
    "BO-354"
   ],
   "inferred": false,
   "notes": "**Reached from BO-354, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-354",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F170 step 12→13",
     "operation": "listFailedGenerationDelivery"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Provide one dedicated operational queue for credential-related failures.",
  "purposeNote": "Credential failures are centrally identified, prioritized and resolved before unnecessarily impacting customer admission or fulfillment.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 4 actions on this screen and the screen declares 1 operation.** Unserved: Retry, Escalate, Assign Owner, Open Technical Case. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Ticket_Media___Credential_Management_Reference.pdf, page 51 §Allow"
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
       "label": "Every failed generation delivery",
       "columns": [
        "FailedGenerationDeliveryCredentialExceptionManagemenView.severity",
        "FailedGenerationDeliveryCredentialExceptionManagemenView.virtualTicket",
        "FailedGenerationDeliveryCredentialExceptionManagemenView.credential",
        "FailedGenerationDeliveryCredentialExceptionManagemenView.media",
        "FailedGenerationDeliveryCredentialExceptionManagemenView.customer",
        "FailedGenerationDeliveryCredentialExceptionManagemenView.event",
        "FailedGenerationDeliveryCredentialExceptionManagemenView.failure",
        "FailedGenerationDeliveryCredentialExceptionManagemenView.time",
        "FailedGenerationDeliveryCredentialExceptionManagemenView.operationalImpact",
        "Retry Status",
        "FailedGenerationDeliveryCredentialExceptionManagemenView.owner"
       ],
       "bindsTo": "FailedGenerationDeliveryCredentialExceptionManagemenView",
       "operation": "listFailedGenerationDelivery",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 51 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected failed generation delivery",
       "bindsTo": "FailedGenerationDeliveryCredentialExceptionManagemenView",
       "columns": [
        "FailedGenerationDeliveryCredentialExceptionManagemenView.severity",
        "FailedGenerationDeliveryCredentialExceptionManagemenView.virtualTicket",
        "FailedGenerationDeliveryCredentialExceptionManagemenView.credential",
        "FailedGenerationDeliveryCredentialExceptionManagemenView.media",
        "FailedGenerationDeliveryCredentialExceptionManagemenView.customer",
        "FailedGenerationDeliveryCredentialExceptionManagemenView.event",
        "FailedGenerationDeliveryCredentialExceptionManagemenView.failure",
        "FailedGenerationDeliveryCredentialExceptionManagemenView.time",
        "FailedGenerationDeliveryCredentialExceptionManagemenView.operationalImpact",
        "Retry Status",
        "FailedGenerationDeliveryCredentialExceptionManagemenView.owner"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Include”, “Consider”.",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 51 §Display"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Retry",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 51 §Allow"
      },
      {
       "kind": "secondaryButton",
       "label": "Escalate",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 51 §Allow"
      },
      {
       "kind": "secondaryButton",
       "label": "Assign Owner",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 51 §Allow"
      },
      {
       "kind": "secondaryButton",
       "label": "Open Technical Case",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 51 §Allow"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The failed generation delivery list.",
   "error": "Could not load. Names which read failed and leaves the failed generation delivery untouched.",
   "emptyFirstRun": "No failed generation delivery yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the failed generation delivery are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listFailedGenerationDelivery",
    "contract": "access",
    "purpose": "Failed Generation, Delivery & Credential Exception Management",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "FailedGenerationDeliveryCredentialExceptionManagemenView.severity",
    "FailedGenerationDeliveryCredentialExceptionManagemenView.virtualTicket",
    "FailedGenerationDeliveryCredentialExceptionManagemenView.credential",
    "FailedGenerationDeliveryCredentialExceptionManagemenView.media",
    "FailedGenerationDeliveryCredentialExceptionManagemenView.customer",
    "FailedGenerationDeliveryCredentialExceptionManagemenView.event"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-360"
  },
  "apisNote": "Regenerated 9 September 2026 from Ticket_Media___Credential_Management_Reference.pdf page 51. 10 of 11 labels bound to a contract property; 15 of 48 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-361",
  "name": "Credential Usage & Cross-Media Traceability",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Ticket_Media___Credential_Management_Reference.pdf",
   "board": "3",
   "number": "15.3.8",
   "page": 53
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/credential-usage-cross-media-traceability-bo-361",
   "component": "apps/venue-management-web/src/routes/access-venue/CredentialUsageCrossMediaTraceability.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-354"
   ],
   "exitTo": [
    "BO-354"
   ],
   "inferred": false,
   "notes": "**Reached from BO-354, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-354",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F170 step 14→15",
     "operation": "listCredentialUsageCross"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Capture/reference) and no display directory — it is settings, not a population",
  "purpose": "Provide end-to-end visibility into how the different media attached to one Virtual Ticket have been presented or used. This screen is for credential traceability, while Area 16 remains responsible for the actual access-control decision.",
  "purposeNote": "authoritative admission decision engine.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 1 actions on this screen and the screen declares 1 operation.** Unserved: What happened to the master entitlement?. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Ticket_Media___Credential_Management_Reference.pdf, page 53 §Allow administrators to understand"
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
       "label": "Virtual Ticket",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 53 §Capture/reference"
      },
      {
       "kind": "selectField",
       "label": "Credential",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 53 §Capture/reference"
      },
      {
       "kind": "selectField",
       "label": "Media",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 53 §Capture/reference"
      },
      {
       "kind": "selectField",
       "label": "Presentation timestamp",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 53 §Capture/reference"
      },
      {
       "kind": "selectField",
       "label": "Location",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 53 §Capture/reference"
      },
      {
       "kind": "selectField",
       "label": "Device",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 53 §Capture/reference"
      },
      {
       "kind": "selectField",
       "label": "External system",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 53 §Capture/reference"
      },
      {
       "kind": "selectField",
       "label": "Transaction type",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 53 §Capture/reference"
      },
      {
       "kind": "selectField",
       "label": "Result",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 53 §Capture/reference"
      },
      {
       "kind": "selectField",
       "label": "Entitlement impact",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 53 §Capture/reference"
      },
      {
       "kind": "selectField",
       "label": "Synchronization status",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 53 §Capture/reference"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "What happened to the master entitlement?",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 53 §Allow administrators to understand"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The credential usage cross-media configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the credential usage cross-media untouched.",
   "emptyFirstRun": "No credential usage cross-media configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listCredentialUsageCross",
    "contract": "access",
    "purpose": "Credential Usage & Cross-Media Traceability",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-361"
  },
  "apisNote": "Regenerated 9 September 2026 from Ticket_Media___Credential_Management_Reference.pdf page 53. 0 of 0 labels bound to a contract property; 12 of 33 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-362",
  "name": "Credential Security, Audit & Operational Evidence",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Ticket_Media___Credential_Management_Reference.pdf",
   "board": "3",
   "number": "15.3.9",
   "page": 54
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/credential-security-audit-operational-evidence-bo-362",
   "component": "apps/venue-management-web/src/routes/access-venue/CredentialSecurityAuditOperationalEvidence.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-354"
   ],
   "exitTo": [
    "BO-354"
   ],
   "inferred": false,
   "notes": "**Reached from BO-354, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-354",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F170 step 16→17",
     "operation": "listCredentialSecurityOperational"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Identify) and no metric row",
  "purpose": "Maintain complete evidence of credential creation and lifecycle activity.",
  "purposeNote": "Every significant credential lifecycle action is traceable with sufficient evidence to reconstruct who did what, when, why and to which Virtual Ticket.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every credential security audit",
       "columns": [
        "CredentialSecurityAuditOperationalEvidenceView.excessiveRegeneration",
        "CredentialSecurityAuditOperationalEvidenceView.repeatedReplacement",
        "CredentialSecurityAuditOperationalEvidenceView.suspiciousRebinding",
        "CredentialSecurityAuditOperationalEvidenceView.multipleCredentialAssignments",
        "CredentialSecurityAuditOperationalEvidenceView.unexpectedProviderTokenChanges",
        "CredentialSecurityAuditOperationalEvidenceView.unauthorizedAdministrativeActions"
       ],
       "bindsTo": "CredentialSecurityAuditOperationalEvidenceView",
       "operation": "listCredentialSecurityOperational",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 54 §Identify"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected credential security audit",
       "bindsTo": "CredentialSecurityAuditOperationalEvidenceView",
       "columns": [
        "CredentialSecurityAuditOperationalEvidenceView.excessiveRegeneration",
        "CredentialSecurityAuditOperationalEvidenceView.repeatedReplacement",
        "CredentialSecurityAuditOperationalEvidenceView.suspiciousRebinding",
        "CredentialSecurityAuditOperationalEvidenceView.multipleCredentialAssignments",
        "CredentialSecurityAuditOperationalEvidenceView.unexpectedProviderTokenChanges",
        "CredentialSecurityAuditOperationalEvidenceView.unauthorizedAdministrativeActions"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Record”, “RFID-1001”, “Access Control”, “Evidence Export”.",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 54 §Identify"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The credential security audit list.",
   "error": "Could not load. Names which read failed and leaves the credential security audit untouched.",
   "emptyFirstRun": "No credential security audit yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the credential security audit are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listCredentialSecurityOperational",
    "contract": "access",
    "purpose": "Credential Security, Audit & Operational Evidence",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "CredentialSecurityAuditOperationalEvidenceView.excessiveRegeneration",
    "CredentialSecurityAuditOperationalEvidenceView.repeatedReplacement",
    "CredentialSecurityAuditOperationalEvidenceView.suspiciousRebinding",
    "CredentialSecurityAuditOperationalEvidenceView.multipleCredentialAssignments",
    "CredentialSecurityAuditOperationalEvidenceView.unexpectedProviderTokenChanges",
    "CredentialSecurityAuditOperationalEvidenceView.unauthorizedAdministrativeActions"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-362"
  },
  "apisNote": "Regenerated 9 September 2026 from Ticket_Media___Credential_Management_Reference.pdf page 54. 6 of 6 labels bound to a contract property; 21 of 55 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-363",
  "name": "Ticket Media Analytics & AI Operations Intelligence",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Ticket_Media___Credential_Management_Reference.pdf",
   "board": "3",
   "number": "15.3.10",
   "page": 56
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/ticket-media-analytics-ai-operations-intelligence-bo-363",
   "component": "apps/venue-management-web/src/routes/access-venue/TicketMediaAnalyticsAiOperationsIntelligence.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-354"
   ],
   "exitTo": [
    "BO-354"
   ],
   "inferred": false,
   "notes": "**Reached from BO-354, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation."
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Analyze; Compare) and no metric row",
  "purpose": "Provide management and operations with analytics and AI intelligence across Virtual Tickets and credential media. This should be a serious operational intelligence layer—not simply a chatbot.",
  "purposeNote": "and operational performance without transferring authoritative ticket or security decisions to generative AI. Board 3 — Final Screen Register",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "filters",
     "components": [
      {
       "kind": "searchField",
       "label": "Search ticket media analytics",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 56 §Analyze by"
      },
      {
       "kind": "multiSelect",
       "label": "Filter by",
       "columns": [
        "Brand",
        "Venue",
        "Event",
        "Product",
        "Channel",
        "Media",
        "Provider",
        "Device",
        "Customer segment",
        "Time period"
       ],
       "notes": "The pack filters this screen by brand, venue, event, product, channel, media and 4 more — which are present is a decision the pack already made.",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 56 §Analyze by"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every ticket media analytics",
       "columns": [
        "TicketMediaAnalyticsAiOperationsIntelligenceView.credentialsGenerated",
        "TicketMediaAnalyticsAiOperationsIntelligenceView.generationSuccess",
        "TicketMediaAnalyticsAiOperationsIntelligenceView.deliverySuccess",
        "TicketMediaAnalyticsAiOperationsIntelligenceView.activation",
        "TicketMediaAnalyticsAiOperationsIntelligenceView.walletAdoption",
        "TicketMediaAnalyticsAiOperationsIntelligenceView.rfidAdoption",
        "TicketMediaAnalyticsAiOperationsIntelligenceView.faceCredentialAdoption",
        "TicketMediaAnalyticsAiOperationsIntelligenceView.multiMediaAdoption",
        "TicketMediaAnalyticsAiOperationsIntelligenceView.replacementRate",
        "TicketMediaAnalyticsAiOperationsIntelligenceView.revocationRate",
        "TicketMediaAnalyticsAiOperationsIntelligenceView.generationFailure",
        "TicketMediaAnalyticsAiOperationsIntelligenceView.deliveryFailure",
        "TicketMediaAnalyticsAiOperationsIntelligenceView.averageGenerationTime",
        "TicketMediaAnalyticsAiOperationsIntelligenceView.averageResolutionTime",
        "TicketMediaAnalyticsAiOperationsIntelligenceView.mediaUsageDistribution",
        "TicketMediaAnalyticsAiOperationsIntelligenceView.providerUptime",
        "TicketMediaAnalyticsAiOperationsIntelligenceView.generationFailures",
        "TicketMediaAnalyticsAiOperationsIntelligenceView.encodingFailures",
        "TicketMediaAnalyticsAiOperationsIntelligenceView.deliveryFailures",
        "TicketMediaAnalyticsAiOperationsIntelligenceView.synchronizationDelay",
        "TicketMediaAnalyticsAiOperationsIntelligenceView.replacementFrequency"
       ],
       "bindsTo": "TicketMediaAnalyticsAiOperationsIntelligenceView",
       "operation": "listTicketMedia",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 56 §Analyze"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected ticket media analytics",
       "bindsTo": "TicketMediaAnalyticsAiOperationsIntelligenceView",
       "columns": [
        "TicketMediaAnalyticsAiOperationsIntelligenceView.credentialsGenerated",
        "TicketMediaAnalyticsAiOperationsIntelligenceView.generationSuccess",
        "TicketMediaAnalyticsAiOperationsIntelligenceView.deliverySuccess",
        "TicketMediaAnalyticsAiOperationsIntelligenceView.activation",
        "TicketMediaAnalyticsAiOperationsIntelligenceView.walletAdoption",
        "TicketMediaAnalyticsAiOperationsIntelligenceView.rfidAdoption",
        "TicketMediaAnalyticsAiOperationsIntelligenceView.faceCredentialAdoption",
        "TicketMediaAnalyticsAiOperationsIntelligenceView.multiMediaAdoption",
        "TicketMediaAnalyticsAiOperationsIntelligenceView.replacementRate",
        "TicketMediaAnalyticsAiOperationsIntelligenceView.revocationRate",
        "TicketMediaAnalyticsAiOperationsIntelligenceView.generationFailure",
        "TicketMediaAnalyticsAiOperationsIntelligenceView.deliveryFailure",
        "TicketMediaAnalyticsAiOperationsIntelligenceView.averageGenerationTime",
        "TicketMediaAnalyticsAiOperationsIntelligenceView.averageResolutionTime",
        "TicketMediaAnalyticsAiOperationsIntelligenceView.mediaUsageDistribution",
        "TicketMediaAnalyticsAiOperationsIntelligenceView.providerUptime",
        "TicketMediaAnalyticsAiOperationsIntelligenceView.generationFailures",
        "TicketMediaAnalyticsAiOperationsIntelligenceView.encodingFailures",
        "TicketMediaAnalyticsAiOperationsIntelligenceView.deliveryFailures",
        "TicketMediaAnalyticsAiOperationsIntelligenceView.synchronizationDelay",
        "TicketMediaAnalyticsAiOperationsIntelligenceView.replacementFrequency"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Eligible customers”, “Backend Screen”, “Credential Operations Command Center”, “Operational exceptions”, “ONE VIRTUAL TICKET”.",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 56 §Analyze"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The ticket media analytics list.",
   "error": "Could not load. Names which read failed and leaves the ticket media analytics untouched.",
   "emptyFirstRun": "No ticket media analytics yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the ticket media analytics are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listTicketMedia",
    "contract": "access",
    "purpose": "Ticket Media Analytics & AI Operations Intelligence",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "TicketMediaAnalyticsAiOperationsIntelligenceView.credentialsGenerated",
    "TicketMediaAnalyticsAiOperationsIntelligenceView.generationSuccess",
    "TicketMediaAnalyticsAiOperationsIntelligenceView.deliverySuccess",
    "TicketMediaAnalyticsAiOperationsIntelligenceView.activation",
    "TicketMediaAnalyticsAiOperationsIntelligenceView.walletAdoption",
    "TicketMediaAnalyticsAiOperationsIntelligenceView.rfidAdoption"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-363"
  },
  "apisNote": "Regenerated 9 September 2026 from Ticket_Media___Credential_Management_Reference.pdf page 56. 21 of 31 labels bound to a contract property; 31 of 133 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
 "listCredential": {
  "method": "GET",
  "path": "/credential",
  "contract": "access",
  "summary": "Credential Operations Command Center",
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
    "name": "date",
    "in": "query",
    "required": false
   },
   {
    "name": "media",
    "in": "query",
    "required": false
   },
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
    "name": "customer",
    "in": "query",
    "required": false
   }
  ],
  "requestBody": null,
  "responds": "CredentialOperationsCommandCenterView"
 },
 "listCredentialDeliveryDistribution": {
  "method": "GET",
  "path": "/credential-delivery-distribution",
  "contract": "access",
  "summary": "Credential Delivery & Distribution Operations",
  "permission": "SCOPE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "CredentialDeliveryDistributionOperationsView"
 },
 "listCredentialGenerationIssuance": {
  "method": "GET",
  "path": "/credential-generation-issuance",
  "contract": "access",
  "summary": "Credential Generation & Issuance Monitor",
  "permission": "SCOPE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "CredentialGenerationIssuanceMonitorView"
 },
 "listCredentialReplacementReissue": {
  "method": "GET",
  "path": "/credential-replacement-reissue",
  "contract": "access",
  "summary": "Credential Replacement, Reissue, Revocation & Recovery",
  "permission": "SCOPE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "CredentialReplacementReissueRevocationRecoveryView"
 },
 "listCredentialSecurityOperational": {
  "method": "GET",
  "path": "/credential-security-operational",
  "contract": "access",
  "summary": "Credential Security, Audit & Operational Evidence",
  "permission": "SCOPE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "CredentialSecurityAuditOperationalEvidenceView"
 },
 "listCredentialUsageCross": {
  "method": "GET",
  "path": "/credential-usage-cross",
  "contract": "access",
  "summary": "Credential Usage & Cross-Media Traceability",
  "permission": "SCOPE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "CredentialUsageCrossMediaTraceabilityView"
 },
 "listFailedGenerationDelivery": {
  "method": "GET",
  "path": "/failed-generation-delivery",
  "contract": "access",
  "summary": "Failed Generation, Delivery & Credential Exception Management",
  "permission": "SCOPE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "FailedGenerationDeliveryCredentialExceptionManagemenView"
 },
 "listTicketMedia": {
  "method": "GET",
  "path": "/ticket-media",
  "contract": "access",
  "summary": "Ticket Media Analytics & AI Operations Intelligence",
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
    "name": "product",
    "in": "query",
    "required": false
   },
   {
    "name": "channel",
    "in": "query",
    "required": false
   },
   {
    "name": "media",
    "in": "query",
    "required": false
   },
   {
    "name": "provider",
    "in": "query",
    "required": false
   },
   {
    "name": "device",
    "in": "query",
    "required": false
   }
  ],
  "requestBody": null,
  "responds": "TicketMediaAnalyticsAiOperationsIntelligenceView"
 },
 "setMediaBindingActivation": {
  "method": "PUT",
  "path": "/media-binding-activation",
  "contract": "access",
  "summary": "Media Binding, Activation & Assignment Operations",
  "permission": "ACCESS_POINT_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": "MediaBindingActivationAssignmentOperationsInput",
  "responds": "MediaBindingActivationAssignmentOperationsView"
 },
 "setVirtualTicketCredential": {
  "method": "PUT",
  "path": "/virtual-ticket-credential",
  "contract": "access",
  "summary": "Virtual Ticket & Credential 360° Workspace",
  "permission": "ACCESS_POINT_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": "VirtualTicketCredential360WorkspaceInput",
  "responds": "VirtualTicketCredential360WorkspaceView"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "CredentialDeliveryDistributionOperationsView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Credential Delivery & Distribution Operations displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "email": {
    "type": "string",
    "description": "Email"
   },
   "smsLink": {
    "type": "string",
    "description": "SMS Link"
   },
   "whatsappIntegration": {
    "type": "string",
    "description": "WhatsApp integration"
   },
   "b2cAccount": {
    "type": "string",
    "description": "B2C Account"
   },
   "mobileApp": {
    "type": "string",
    "description": "Mobile App"
   },
   "appleWallet": {
    "type": "string",
    "description": "Apple Wallet"
   },
   "googleWallet": {
    "type": "string",
    "description": "Google Wallet"
   },
   "pos": {
    "type": "string",
    "description": "POS"
   },
   "boxOffice": {
    "type": "string",
    "description": "Box Office"
   },
   "kiosk": {
    "type": "string",
    "description": "Kiosk"
   },
   "groupPortal": {
    "type": "string",
    "description": "Group Portal"
   },
   "api": {
    "type": "string",
    "description": "API"
   },
   "physicalCollection": {
    "type": "string",
    "description": "Physical Collection"
   },
   "statesType": {
    "type": "string",
    "enum": [
     "failed",
     "bounced",
     "expired",
     "cancelled"
    ],
    "description": "Vocabulary listed under Alternative states."
   },
   "virtualTicket": {
    "type": "string",
    "description": "Virtual Ticket"
   },
   "media": {
    "type": "string",
    "description": "Media"
   },
   "recipient": {
    "type": "string",
    "description": "Recipient"
   },
   "channel": {
    "type": "string",
    "description": "Channel"
   },
   "destination": {
    "type": "string",
    "description": "Destination"
   },
   "sentAt": {
    "type": "string",
    "description": "Sent At"
   },
   "deliveredAt": {
    "type": "string",
    "description": "Delivered At"
   },
   "openedDownloaded": {
    "type": "string",
    "description": "Opened/Downloaded"
   },
   "attempt": {
    "type": "string",
    "description": "Attempt"
   },
   "status": {
    "type": "integer",
    "description": "Status"
   },
   "purchaser": {
    "type": "string",
    "description": "Purchaser"
   },
   "ticketHolder": {
    "type": "string",
    "description": "Ticket Holder"
   },
   "participant": {
    "type": "string",
    "description": "Participant"
   },
   "guardian": {
    "type": "string",
    "description": "Guardian"
   },
   "groupLeader": {
    "type": "string",
    "description": "Group Leader"
   },
   "authorizedRecipient": {
    "type": "string",
    "description": "Authorized recipient"
   },
   "authentication": {
    "type": "string",
    "description": "Authentication"
   },
   "singleMultipleUse": {
    "type": "string",
    "description": "Single/multiple use"
   },
   "customerIdentity": {
    "type": "string",
    "description": "Customer identity"
   },
   "tokenSecurity": {
    "type": "string",
    "description": "Token security"
   },
   "dataMasking": {
    "type": "string",
    "description": "Data masking"
   }
  }
 },
 "CredentialGenerationIssuanceMonitorView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Credential Generation & Issuance Monitor displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "orderConfirmation": {
    "type": "string",
    "description": "Order Confirmation"
   },
   "ticketIssuance": {
    "type": "string",
    "description": "Ticket Issuance"
   },
   "membershipActivation": {
    "type": "string",
    "description": "Membership Activation"
   },
   "customerRequest": {
    "type": "string",
    "description": "Customer Request"
   },
   "staffAction": {
    "type": "string",
    "description": "Staff Action"
   },
   "rfidCollection": {
    "type": "string",
    "description": "RFID Collection"
   },
   "walletRequest": {
    "type": "string",
    "description": "Wallet Request"
   },
   "faceEnrollment": {
    "type": "string",
    "description": "Face Enrollment"
   },
   "api": {
    "type": "string",
    "description": "API"
   },
   "bulkOperation": {
    "type": "string",
    "description": "Bulk Operation"
   },
   "scheduledProcess": {
    "type": "string",
    "format": "date-time",
    "description": "Scheduled Process"
   },
   "requestId": {
    "type": "string",
    "description": "Request ID"
   },
   "virtualTicket": {
    "type": "string",
    "description": "Virtual Ticket"
   },
   "media": {
    "type": "string",
    "description": "Media"
   },
   "template": {
    "type": "string",
    "description": "Template"
   },
   "templateVersion": {
    "type": "string",
    "description": "Template Version"
   },
   "product": {
    "type": "string",
    "description": "Product"
   },
   "customer": {
    "type": "string",
    "description": "Customer"
   },
   "provider": {
    "type": "string",
    "description": "Provider"
   },
   "requestedAt": {
    "type": "string",
    "description": "Requested At"
   },
   "generatedAt": {
    "type": "string",
    "description": "Generated At"
   },
   "status": {
    "type": "integer",
    "description": "Status"
   },
   "error": {
    "type": "string",
    "description": "Error"
   },
   "brand": {
    "type": "string",
    "description": "Brand"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "event": {
    "type": "string",
    "description": "Event"
   },
   "channel": {
    "type": "string",
    "description": "Channel"
   },
   "language": {
    "type": "string",
    "description": "Language"
   },
   "customerContext": {
    "type": "string",
    "description": "Customer context"
   },
   "supportControlledBulkOperations": {
    "type": "string",
    "description": "Support controlled bulk operations"
   },
   "templateMissing": {
    "type": "string",
    "description": "Template missing"
   },
   "requiredDataMissing": {
    "type": "string",
    "description": "Required data missing"
   },
   "providerUnavailable": {
    "type": "string",
    "description": "Provider unavailable"
   },
   "invalidPayload": {
    "type": "string",
    "description": "Invalid payload"
   },
   "tokenGenerationFailure": {
    "type": "string",
    "description": "Token generation failure"
   },
   "walletGenerationFailure": {
    "type": "string",
    "description": "Wallet generation failure"
   },
   "encoderUnavailable": {
    "type": "string",
    "description": "Encoder unavailable"
   },
   "automaticRetry": {
    "type": "string",
    "description": "Automatic Retry"
   },
   "manualRetry": {
    "type": "string",
    "description": "Manual Retry"
   }
  }
 },
 "CredentialOperationsCommandCenterView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Credential Operations Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "virtualTicketsIssued": {
    "type": "string",
    "description": "Virtual Tickets Issued"
   },
   "credentialsGenerated": {
    "type": "string",
    "description": "Credentials Generated"
   },
   "activeCredentials": {
    "type": "integer",
    "description": "Active Credentials"
   },
   "pendingGeneration": {
    "type": "integer",
    "description": "Pending Generation"
   },
   "pendingDelivery": {
    "type": "integer",
    "description": "Pending Delivery"
   },
   "pendingBinding": {
    "type": "integer",
    "description": "Pending Binding"
   },
   "pendingActivation": {
    "type": "integer",
    "description": "Pending Activation"
   },
   "suspended": {
    "type": "string",
    "description": "Suspended"
   },
   "revoked": {
    "type": "string",
    "description": "Revoked"
   },
   "expired": {
    "type": "integer",
    "description": "Expired"
   },
   "failedGeneration": {
    "type": "integer",
    "description": "Failed Generation"
   },
   "failedDelivery": {
    "type": "integer",
    "description": "Failed Delivery"
   },
   "synchronizationExceptions": {
    "type": "integer",
    "description": "Synchronization Exceptions"
   },
   "multiMediaVirtualTickets": {
    "type": "integer",
    "description": "Multi-Media Virtual Tickets"
   },
   "dynamicQr": {
    "type": "string",
    "description": "Dynamic QR"
   },
   "barcode": {
    "type": "string",
    "description": "Barcode"
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
   "rfid": {
    "type": "string",
    "description": "RFID"
   },
   "nfc": {
    "type": "string",
    "description": "NFC"
   },
   "faceRecognitionReference": {
    "type": "string",
    "description": "Face Recognition Reference"
   },
   "card": {
    "type": "string",
    "description": "Card"
   },
   "wristband": {
    "type": "string",
    "description": "Wristband"
   },
   "virtualTicketId": {
    "type": "string",
    "description": "Virtual Ticket ID"
   },
   "credentialId": {
    "type": "string",
    "description": "Credential ID"
   },
   "mediaType": {
    "type": "string",
    "description": "Media Type"
   },
   "customerParticipant": {
    "type": "string",
    "description": "Customer / Participant"
   },
   "product": {
    "type": "string",
    "description": "Product"
   },
   "event": {
    "type": "string",
    "description": "Event"
   },
   "credentialStatus": {
    "type": "integer",
    "description": "Credential Status"
   },
   "deliveryStatus": {
    "type": "integer",
    "description": "Delivery Status"
   },
   "activationStatus": {
    "type": "integer",
    "description": "Activation Status"
   },
   "bindingStatus": {
    "type": "integer",
    "description": "Binding Status"
   },
   "provider": {
    "type": "string",
    "description": "Provider"
   },
   "lastActivity": {
    "type": "string",
    "format": "date-time",
    "description": "Last Activity"
   },
   "exception": {
    "type": "string",
    "description": "Exception"
   },
   "owner": {
    "type": "string",
    "description": "Owner"
   },
   "qrGeneration9998Healthy": {
    "type": "number",
    "description": "QR Generation — 99.98% Healthy"
   },
   "rfidEncoding987Healthy": {
    "type": "number",
    "description": "RFID Encoding — 98.7% Healthy"
   }
  }
 },
 "CredentialReplacementReissueRevocationRecoveryView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Credential Replacement, Reissue, Revocation & Recovery displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "lost": {
    "type": "string",
    "description": "Lost"
   },
   "stolen": {
    "type": "string",
    "description": "Stolen"
   },
   "damaged": {
    "type": "string",
    "description": "Damaged"
   },
   "compromised": {
    "type": "string",
    "description": "Compromised"
   },
   "customerChangedPhone": {
    "type": "string",
    "description": "Customer changed phone"
   },
   "rfidFailure": {
    "type": "string",
    "description": "RFID failure"
   },
   "wristbandReplacement": {
    "type": "string",
    "description": "Wristband replacement"
   },
   "qrCompromise": {
    "type": "string",
    "description": "QR compromise"
   },
   "walletReplacement": {
    "type": "string",
    "description": "Wallet replacement"
   },
   "faceReEnrollment": {
    "type": "string",
    "description": "Face re-enrollment"
   },
   "incorrectAssignment": {
    "type": "string",
    "description": "Incorrect assignment"
   },
   "vt009821Active": {
    "type": "integer",
    "description": "VT-009821 — ACTIVE"
   },
   "rf88721Revoked": {
    "type": "string",
    "description": "RF-88721 — REVOKED"
   },
   "rf99211Active": {
    "type": "integer",
    "description": "RF-99211 — ACTIVE"
   },
   "qr": {
    "type": "string",
    "description": "QR"
   },
   "qr55128Active": {
    "type": "integer",
    "description": "QR-55128 — ACTIVE"
   },
   "theVirtualTicketRemainsUnchanged": {
    "type": "string",
    "description": "The Virtual Ticket remains unchanged"
   },
   "calculationsHere": {
    "type": "string",
    "description": "calculations here"
   },
   "immediateOldMediaRevocation": {
    "type": "string",
    "description": "Immediate old-media revocation"
   },
   "gracePeriod": {
    "type": "string",
    "format": "date-time",
    "description": "Grace period"
   },
   "maximumReplacements": {
    "type": "string",
    "description": "Maximum replacements"
   },
   "identityVerification": {
    "type": "string",
    "description": "Identity verification"
   },
   "supervisorApproval": {
    "type": "string",
    "description": "Supervisor approval"
   },
   "reasonCodes": {
    "type": "string",
    "description": "Reason codes"
   }
  }
 },
 "CredentialSecurityAuditOperationalEvidenceView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Credential Security, Audit & Operational Evidence displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "credentialRequested": {
    "type": "string",
    "description": "Credential Requested"
   },
   "generated": {
    "type": "string",
    "description": "Generated"
   },
   "bound": {
    "type": "string",
    "description": "Bound"
   },
   "delivered": {
    "type": "string",
    "description": "Delivered"
   },
   "activated": {
    "type": "string",
    "description": "Activated"
   },
   "updated": {
    "type": "string",
    "format": "date-time",
    "description": "Updated"
   },
   "presented": {
    "type": "string",
    "description": "Presented"
   },
   "suspended": {
    "type": "string",
    "description": "Suspended"
   },
   "reactivated": {
    "type": "string",
    "description": "Reactivated"
   },
   "replaced": {
    "type": "string",
    "description": "Replaced"
   },
   "revoked": {
    "type": "string",
    "description": "Revoked"
   },
   "expired": {
    "type": "integer",
    "description": "Expired"
   },
   "rebound": {
    "type": "string",
    "description": "Rebound"
   },
   "regenerated": {
    "type": "string",
    "description": "Regenerated"
   },
   "deletedWhereLegallyPermissiblyApplicable": {
    "type": "string",
    "description": "Deleted where legally/permissibly applicable"
   },
   "virtualTicket": {
    "type": "string",
    "description": "Virtual Ticket"
   },
   "credential": {
    "type": "string",
    "description": "Credential"
   },
   "media": {
    "type": "string",
    "description": "Media"
   },
   "action": {
    "type": "string",
    "description": "Action"
   },
   "before": {
    "type": "string",
    "description": "Before"
   },
   "after": {
    "type": "string",
    "description": "After"
   },
   "actor": {
    "type": "string",
    "description": "Actor"
   },
   "source": {
    "type": "string",
    "description": "Source"
   },
   "device": {
    "type": "string",
    "description": "Device"
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
   "providerReference": {
    "type": "string",
    "description": "Provider reference"
   },
   "relatedTransaction": {
    "type": "string",
    "description": "Related transaction"
   },
   "lost": {
    "type": "string",
    "description": "↓ Lost"
   },
   "rfid1001Revoked": {
    "type": "string",
    "description": "RFID-1001 — Revoked"
   },
   "replacement": {
    "type": "string",
    "description": "↓ Replacement"
   },
   "rfid1057Active": {
    "type": "integer",
    "description": "RFID-1057 — Active"
   },
   "excessiveRegeneration": {
    "type": "string",
    "description": "Excessive regeneration"
   },
   "repeatedReplacement": {
    "type": "string",
    "description": "Repeated replacement"
   },
   "suspiciousRebinding": {
    "type": "string",
    "description": "Suspicious rebinding"
   },
   "multipleCredentialAssignments": {
    "type": "string",
    "description": "Multiple credential assignments"
   },
   "unexpectedProviderTokenChanges": {
    "type": "string",
    "description": "Unexpected provider/token changes"
   },
   "unauthorizedAdministrativeActions": {
    "type": "string",
    "description": "Unauthorized administrative actions"
   },
   "role": {
    "type": "string",
    "description": "Role"
   }
  }
 },
 "CredentialUsageCrossMediaTraceabilityView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Credential Usage & Cross-Media Traceability displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "virtualTicket": {
    "type": "string",
    "description": "Virtual Ticket"
   },
   "credential": {
    "type": "string",
    "description": "Credential"
   },
   "media": {
    "type": "string",
    "description": "Media"
   },
   "presentationTimestamp": {
    "type": "string",
    "format": "date-time",
    "description": "Presentation timestamp"
   },
   "location": {
    "type": "string",
    "description": "Location"
   },
   "device": {
    "type": "string",
    "description": "Device"
   },
   "externalSystem": {
    "type": "string",
    "description": "External system"
   },
   "transactionType": {
    "type": "string",
    "description": "Transaction type"
   },
   "result": {
    "type": "string",
    "description": "Result"
   },
   "entitlementImpact": {
    "type": "string",
    "description": "Entitlement impact"
   },
   "synchronizationStatus": {
    "type": "string",
    "description": "Synchronization status"
   },
   "where": {
    "type": "string",
    "description": "Where?"
   },
   "area16DecidesAdmission": {
    "type": "string",
    "description": "Area 16 decides admission"
   },
   "rfidRf10028Vt009821": {
    "type": "string",
    "description": "RFID RF-10028 → VT-009821"
   }
  }
 },
 "FailedGenerationDeliveryCredentialExceptionManagemenView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Failed Generation, Delivery & Credential Exception Management displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "generationFailed": {
    "type": "integer",
    "description": "Generation Failed"
   },
   "bindingFailed": {
    "type": "integer",
    "description": "Binding Failed"
   },
   "activationFailed": {
    "type": "integer",
    "description": "Activation Failed"
   },
   "deliveryFailed": {
    "type": "integer",
    "description": "Delivery Failed"
   },
   "walletFailure": {
    "type": "string",
    "description": "Wallet Failure"
   },
   "rfidEncodingFailure": {
    "type": "string",
    "description": "RFID Encoding Failure"
   },
   "invalidToken": {
    "type": "string",
    "description": "Invalid Token"
   },
   "providerFailure": {
    "type": "string",
    "description": "Provider Failure"
   },
   "synchronizationFailure": {
    "type": "string",
    "description": "Synchronization Failure"
   },
   "missingTemplate": {
    "type": "string",
    "description": "Missing Template"
   },
   "missingRequiredData": {
    "type": "string",
    "description": "Missing Required Data"
   },
   "expiredCredential": {
    "type": "integer",
    "description": "Expired Credential"
   },
   "mappingFailure": {
    "type": "string",
    "description": "Mapping Failure"
   },
   "unknownCredential": {
    "type": "string",
    "description": "Unknown Credential"
   },
   "severity": {
    "type": "string",
    "description": "Severity"
   },
   "virtualTicket": {
    "type": "string",
    "description": "Virtual Ticket"
   },
   "credential": {
    "type": "string",
    "description": "Credential"
   },
   "media": {
    "type": "string",
    "description": "Media"
   },
   "customer": {
    "type": "string",
    "description": "Customer"
   },
   "event": {
    "type": "string",
    "description": "Event"
   },
   "failure": {
    "type": "string",
    "description": "Failure"
   },
   "time": {
    "type": "string",
    "format": "date-time",
    "description": "Time"
   },
   "operationalImpact": {
    "type": "string",
    "description": "Operational Impact"
   },
   "owner": {
    "type": "string",
    "description": "Owner"
   },
   "eventProximity": {
    "type": "string",
    "description": "Event proximity"
   },
   "customerArrivalTime": {
    "type": "string",
    "format": "date-time",
    "description": "Customer arrival time"
   },
   "numberOfAffectedTickets": {
    "type": "integer",
    "description": "Number of affected tickets"
   },
   "noAlternativeMedia": {
    "type": "string",
    "description": "No alternative media"
   },
   "vipCustomerServiceImpact": {
    "type": "string",
    "description": "VIP/customer-service impact"
   },
   "accessImpact": {
    "type": "string",
    "description": "Access impact"
   },
   "providerOutage": {
    "type": "string",
    "description": "Provider outage"
   },
   "regenerate": {
    "type": "string",
    "description": "Regenerate"
   },
   "rebind": {
    "type": "string",
    "description": "Rebind"
   },
   "switchMedia": {
    "type": "string",
    "description": "Switch Media"
   },
   "useFallback": {
    "type": "string",
    "description": "Use Fallback"
   }
  }
 },
 "MediaBindingActivationAssignmentOperationsInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Media Binding, Activation & Assignment Operations submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "rfid": {
    "type": "string",
    "description": "RFID"
   },
   "nfc": {
    "type": "string",
    "description": "NFC"
   },
   "wristbands": {
    "type": "string",
    "description": "Wristbands"
   },
   "physicalCards": {
    "type": "string",
    "description": "Physical cards"
   },
   "faceRecognition": {
    "type": "string",
    "description": "Face recognition"
   },
   "temporaryCredentials": {
    "type": "string",
    "description": "Temporary credentials"
   },
   "scan": {
    "type": "string",
    "description": "Scan"
   },
   "tap": {
    "type": "string",
    "description": "Tap"
   },
   "manualLookupWhereAuthorized": {
    "type": "string",
    "description": "Manual lookup where authorized"
   },
   "batchAssignment": {
    "type": "string",
    "description": "Batch assignment"
   },
   "encoderAssignment": {
    "type": "string",
    "description": "Encoder assignment"
   },
   "rawBiometricData": {
    "type": "string",
    "description": "raw biometric data"
   },
   "temporaryActivation": {
    "type": "string",
    "description": "Temporary Activation"
   }
  }
 },
 "MediaBindingActivationAssignmentOperationsView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Media Binding, Activation & Assignment Operations displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "rfid": {
    "type": "string",
    "description": "RFID"
   },
   "nfc": {
    "type": "string",
    "description": "NFC"
   },
   "wristbands": {
    "type": "string",
    "description": "Wristbands"
   },
   "physicalCards": {
    "type": "string",
    "description": "Physical cards"
   },
   "faceRecognition": {
    "type": "string",
    "description": "Face recognition"
   },
   "temporaryCredentials": {
    "type": "string",
    "description": "Temporary credentials"
   },
   "virtualTicket": {
    "type": "string",
    "description": "Virtual Ticket"
   },
   "customer": {
    "type": "string",
    "description": "Customer"
   },
   "product": {
    "type": "string",
    "description": "Product"
   },
   "existingMedia": {
    "type": "string",
    "description": "Existing Media"
   },
   "newMediaType": {
    "type": "integer",
    "description": "New Media Type"
   },
   "credentialIdUid": {
    "type": "string",
    "description": "Credential ID / UID"
   },
   "provider": {
    "type": "string",
    "description": "Provider"
   },
   "activation": {
    "type": "string",
    "description": "Activation"
   },
   "validity": {
    "type": "string",
    "description": "Validity"
   },
   "bindingRule": {
    "type": "string",
    "description": "Binding Rule"
   },
   "scan": {
    "type": "string",
    "description": "Scan"
   },
   "tap": {
    "type": "string",
    "description": "Tap"
   },
   "manualLookupWhereAuthorized": {
    "type": "string",
    "description": "Manual lookup where authorized"
   },
   "batchAssignment": {
    "type": "string",
    "description": "Batch assignment"
   },
   "encoderAssignment": {
    "type": "string",
    "description": "Encoder assignment"
   },
   "rawBiometricData": {
    "type": "string",
    "description": "raw biometric data"
   },
   "temporaryActivation": {
    "type": "string",
    "description": "Temporary Activation"
   }
  }
 },
 "TicketMediaAnalyticsAiOperationsIntelligenceView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Ticket Media Analytics & AI Operations Intelligence displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "credentialsGenerated": {
    "type": "string",
    "description": "Credentials Generated"
   },
   "generationSuccess": {
    "type": "number",
    "description": "Generation Success %"
   },
   "deliverySuccess": {
    "type": "number",
    "description": "Delivery Success %"
   },
   "activation": {
    "type": "number",
    "description": "Activation %"
   },
   "walletAdoption": {
    "type": "string",
    "description": "Wallet Adoption"
   },
   "rfidAdoption": {
    "type": "string",
    "description": "RFID Adoption"
   },
   "faceCredentialAdoption": {
    "type": "string",
    "description": "Face Credential Adoption"
   },
   "multiMediaAdoption": {
    "type": "string",
    "description": "Multi-Media Adoption"
   },
   "replacementRate": {
    "type": "number",
    "description": "Replacement Rate"
   },
   "revocationRate": {
    "type": "number",
    "description": "Revocation Rate"
   },
   "generationFailure": {
    "type": "number",
    "description": "Generation Failure %"
   },
   "deliveryFailure": {
    "type": "number",
    "description": "Delivery Failure %"
   },
   "averageGenerationTime": {
    "type": "string",
    "format": "date-time",
    "description": "Average Generation Time"
   },
   "averageResolutionTime": {
    "type": "string",
    "format": "date-time",
    "description": "Average Resolution Time"
   },
   "mediaUsageDistribution": {
    "type": "string",
    "description": "Media Usage Distribution"
   },
   "mobileQr78": {
    "type": "number",
    "description": "Mobile QR — 78%"
   },
   "appleWallet31": {
    "type": "number",
    "description": "Apple Wallet — 31%"
   },
   "googleWallet22": {
    "type": "number",
    "description": "Google Wallet — 22%"
   },
   "rfid18": {
    "type": "number",
    "description": "RFID — 18%"
   },
   "face12": {
    "type": "number",
    "description": "Face — 12%"
   },
   "providerUptime": {
    "type": "string",
    "description": "Provider uptime"
   },
   "generationFailures": {
    "type": "string",
    "description": "Generation failures"
   },
   "encodingFailures": {
    "type": "string",
    "description": "Encoding failures"
   },
   "deliveryFailures": {
    "type": "string",
    "description": "Delivery failures"
   },
   "synchronizationDelay": {
    "type": "string",
    "description": "Synchronization delay"
   },
   "replacementFrequency": {
    "type": "string",
    "description": "Replacement frequency"
   },
   "credentialFailureRisk": {
    "type": "string",
    "description": "Credential failure risk"
   },
   "deliveryFailureProbability": {
    "type": "string",
    "description": "Delivery failure probability"
   },
   "mediaDemandForUpcomingEvents": {
    "type": "string",
    "description": "Media demand for upcoming events"
   },
   "rfidWristbandStockRequirements": {
    "type": "string",
    "description": "RFID/wristband stock requirements"
   },
   "operationalWorkload": {
    "type": "string",
    "description": "Operational workload"
   },
   "likelyOnSiteReplacementVolumes": {
    "type": "string",
    "description": "Likely on-site replacement volumes"
   },
   "qrDynamicQr": {
    "type": "string",
    "description": "↙ QR / Dynamic QR"
   },
   "appleWallet": {
    "type": "string",
    "description": "↙ Apple Wallet"
   },
   "googleWallet": {
    "type": "string",
    "description": "↙ Google Wallet"
   },
   "rfidNfc": {
    "type": "string",
    "description": "↙ RFID / NFC"
   },
   "cardWristband": {
    "type": "string",
    "description": "↙ Card / Wristband"
   },
   "faceRecognitionReference": {
    "type": "string",
    "description": "↙ Face Recognition Reference"
   },
   "futureMedia": {
    "type": "string",
    "description": "↙ Future Media"
   },
   "sameTicket": {
    "type": "string",
    "description": "same ticket"
   }
  }
 },
 "VirtualTicketCredential360WorkspaceInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table covers these fields** — the closest is access.entitlement at 9%, so this is not an update to anything the package stores today and no new table has been decided",
  "description": "**What Virtual Ticket & Credential 360° Workspace submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.\n\n**The pack defines this as a record**, under *For each media show* - one of only 13 drafted writes that does. That is the client writing a row rather than a screen, and it is where the table conversation should start.",
  "properties": {
   "showAllAssociatedCredentials": {
    "type": "string",
    "description": "Show all associated credentials"
   },
   "al": {
    "type": "string",
    "description": "al"
   },
   "primary": {
    "type": "string",
    "description": "Primary"
   },
   "secondary": {
    "type": "string",
    "description": "Secondary"
   },
   "fallback": {
    "type": "string",
    "description": "Fallback"
   },
   "temporary": {
    "type": "string",
    "description": "Temporary"
   },
   "revokedHistoricalMedia": {
    "type": "string",
    "description": "Revoked historical media"
   },
   "bindingId": {
    "type": "string",
    "description": "Binding ID"
   },
   "mediaType": {
    "type": "string",
    "description": "Media type"
   },
   "provider": {
    "type": "string",
    "description": "Provider"
   },
   "issued": {
    "type": "string",
    "description": "Issued"
   },
   "delivered": {
    "type": "string",
    "description": "Delivered"
   },
   "activated": {
    "type": "string",
    "description": "Activated"
   },
   "validFrom": {
    "type": "string",
    "description": "Valid From"
   },
   "validTo": {
    "type": "string",
    "description": "Valid To"
   },
   "lastUpdate": {
    "type": "string",
    "format": "date-time",
    "description": "Last update"
   },
   "lastPresentation": {
    "type": "string",
    "format": "date-time",
    "description": "Last presentation"
   },
   "lastUse": {
    "type": "string",
    "format": "date-time",
    "description": "Last use"
   },
   "deviceReferenceWhereAppropriate": {
    "type": "string",
    "description": "Device/reference where appropriate"
   },
   "status": {
    "type": "string",
    "description": "Status"
   },
   "bindRfid": {
    "type": "string",
    "description": "Bind RFID"
   },
   "initiateFaceEnrollment": {
    "type": "string",
    "description": "Initiate Face Enrollment"
   },
   "refresh": {
    "type": "string",
    "description": "Refresh"
   },
   "diagnose": {
    "type": "string",
    "description": "Diagnose"
   }
  },
  "x-ticvai-record-definition": "For each media show"
 },
 "VirtualTicketCredential360WorkspaceView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Virtual Ticket & Credential 360° Workspace displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "virtualTicketId": {
    "type": "string",
    "description": "Virtual Ticket ID"
   },
   "ticketHolder": {
    "type": "string",
    "description": "Ticket Holder"
   },
   "participant": {
    "type": "string",
    "description": "Participant"
   },
   "product": {
    "type": "string",
    "description": "Product"
   },
   "event": {
    "type": "string",
    "description": "Event"
   },
   "performance": {
    "type": "string",
    "description": "Performance"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "seat": {
    "type": "string",
    "description": "Seat"
   },
   "order": {
    "type": "string",
    "description": "Order"
   },
   "ticketStatus": {
    "type": "integer",
    "description": "Ticket Status"
   },
   "usageStatus": {
    "type": "integer",
    "description": "Usage Status"
   },
   "validity": {
    "type": "string",
    "description": "Validity"
   },
   "entitlements": {
    "type": "integer",
    "description": "Entitlements"
   },
   "showAllAssociatedCredentials": {
    "type": "string",
    "description": "Show all associated credentials"
   },
   "al": {
    "type": "string",
    "description": "al"
   },
   "dynamicQrActive": {
    "type": "integer",
    "description": "Dynamic QR Active (the pack shows 88721)"
   },
   "appleWalletActive": {
    "type": "integer",
    "description": "Apple Wallet Active (the pack shows 55321, 43 | Pag e)"
   },
   "primary": {
    "type": "string",
    "description": "Primary"
   },
   "secondary": {
    "type": "string",
    "description": "Secondary"
   },
   "fallback": {
    "type": "string",
    "description": "Fallback"
   },
   "temporary": {
    "type": "string",
    "description": "Temporary"
   },
   "revokedHistoricalMedia": {
    "type": "string",
    "description": "Revoked historical media"
   },
   "bindingId": {
    "type": "string",
    "description": "Binding ID"
   },
   "mediaType": {
    "type": "string",
    "description": "Media type"
   },
   "provider": {
    "type": "string",
    "description": "Provider"
   },
   "issued": {
    "type": "string",
    "description": "Issued"
   },
   "delivered": {
    "type": "string",
    "description": "Delivered"
   },
   "activated": {
    "type": "string",
    "description": "Activated"
   },
   "validFrom": {
    "type": "string",
    "description": "Valid From"
   },
   "validTo": {
    "type": "string",
    "description": "Valid To"
   },
   "lastUpdate": {
    "type": "string",
    "format": "date-time",
    "description": "Last update"
   },
   "lastPresentation": {
    "type": "string",
    "format": "date-time",
    "description": "Last presentation"
   },
   "lastUse": {
    "type": "string",
    "format": "date-time",
    "description": "Last use"
   },
   "deviceReferenceWhereAppropriate": {
    "type": "string",
    "description": "Device/reference where appropriate"
   },
   "status": {
    "type": "string",
    "description": "Status"
   },
   "bindRfid": {
    "type": "string",
    "description": "Bind RFID"
   },
   "initiateFaceEnrollment": {
    "type": "string",
    "description": "Initiate Face Enrollment"
   },
   "refresh": {
    "type": "string",
    "description": "Refresh"
   },
   "diagnose": {
    "type": "string",
    "description": "Diagnose"
   }
  }
 }
}
```
