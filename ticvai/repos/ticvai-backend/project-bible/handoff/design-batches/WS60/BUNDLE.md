# WS60 — Ticket Media   Credential Management board 2

**10 screens · 17 operations · 24 schemas · 5 permissions**

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

- **Every control that can be refused must be gated.** 5 permissions apply here:
  `ACCESS_POINT_CONFIGURE, ORDER_REPRINT, PRODUCT_CONFIGURE, PRODUCT_VIEW, SCOPE_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-344` | Media Design Studio Command Center | commandCentre | 4 | 0 | — |
| `BO-345` | Digital QR & Barcode Ticket Designer | configEditor | 1 | 0 | — |
| `BO-346` | PDF, Printable & POS Ticket Designer | configEditor | 5 | 0 | — |
| `BO-347` | Apple Wallet Pass Designer | configEditor | 1 | 0 | — |
| `BO-348` | Google Wallet Pass Designer | configEditor | 1 | 0 | — |
| `BO-349` | RFID, NFC, Card & Wristband Media Designer | configEditor | 1 | 0 | — |
| `BO-350` | Digital Card, Membership & Wearable Designer | configEditor | 1 | 0 | — |
| `BO-351` | Dynamic Fields, Data Mapping & Content Builder | configEditor | 1 | 0 | — |
| `BO-352` | Branding, Localization & Template Inheritance | listDetail | 2 | 0 | — |
| `BO-353` | Multi-Media Preview, Testing, Approval & Publication | listDetail | 1 | 0 | — |

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "BO-344",
  "name": "Media Design Studio Command Center",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Ticket_Media___Credential_Management_Reference.pdf",
   "board": "2",
   "number": "15.2.1",
   "page": 23
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/media-design-studio-command-center-bo-344",
   "component": "apps/venue-management-web/src/routes/access-venue/MediaDesignStudioCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-100"
   ],
   "exitTo": [
    "BO-100",
    "BO-345",
    "BO-346",
    "BO-347",
    "BO-348",
    "BO-349",
    "BO-350",
    "BO-351",
    "BO-352",
    "BO-353"
   ],
   "inferred": false,
   "notes": "**The board's hub.** The workshop specified this module as boards of ten and opened each with a command centre; the other nine screens are that board's detail, so they are reached from here and return here.",
   "transitions": [
    {
     "to": "BO-100",
     "trigger": "Venue Home",
     "provenance": "derived — BO-100 declares entryState.params  and BO-344 holds none of them, so the edge carries nothing and BO-100 opens cold"
    },
    {
     "to": "BO-345",
     "trigger": "Works in Digital QR & Barcode Ticket Designer",
     "provenance": "flow F169 step 1→2",
     "operation": "listMediaDesign"
    },
    {
     "to": "BO-347",
     "trigger": "Works in Apple Wallet Pass Designer",
     "provenance": "flow F169 step 5→6",
     "operation": "listMediaDesign"
    },
    {
     "to": "BO-348",
     "trigger": "Works in Google Wallet Pass Designer",
     "provenance": "flow F169 step 7→8",
     "operation": "listMediaDesign"
    },
    {
     "to": "BO-349",
     "trigger": "Works in RFID, NFC, Card & Wristband Media Designer",
     "provenance": "flow F169 step 9→10",
     "operation": "listMediaDesign"
    },
    {
     "to": "BO-350",
     "trigger": "Works in Digital Card, Membership & Wearable Designer",
     "provenance": "flow F169 step 11→12",
     "operation": "listMediaDesign"
    },
    {
     "to": "BO-351",
     "trigger": "Works in Dynamic Fields, Data Mapping & Content Builder",
     "provenance": "flow F169 step 13→14",
     "operation": "listMediaDesign"
    },
    {
     "to": "BO-352",
     "trigger": "Works in Branding, Localization & Template Inheritance",
     "provenance": "flow F169 step 15→16",
     "operation": "listMediaDesign"
    },
    {
     "to": "BO-353",
     "trigger": "Works in Multi-Media Preview, Testing, Approval & Publication",
     "provenance": "flow F169 step 17→18",
     "operation": "listMediaDesign"
    },
    {
     "to": "BO-346",
     "trigger": "Works in PDF, Printable & POS Ticket Designer",
     "provenance": "flow F169 step 3→4",
     "operation": "listMediaDesign",
     "carries": [
      "templateId"
     ]
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Administrators can locate, create and manage every ticket-media template from one centralized Media Design Studio.",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen both a metric directory (§Display) and a per-row directory (§Each template should show) — counts over a population, then the population",
  "purpose": "Provide administrators with the central workspace for creating and managing all ticket and credential media templates. This should be the entry point for the entire no-code Media Design Studio.",
  "gaps": [
   {
    "operation": null,
    "why": "**Media Design Studio Command Center declares no operation that writes anything** — its only declared call is `listMediaDesign`, a read. The name promises authoring and the contract offers none, so either the write operations are missing or this screen is a view of something another screen builds.",
    "source": "contract — the screen's declared operations"
   }
  ],
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Total Media Templates",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 23 §Display",
       "bindsTo": "MediaDesignStudioCommandCenterViewSummary.totalMediaTemplates"
      },
      {
       "kind": "metricTile",
       "label": "Published",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 23 §Display",
       "bindsTo": "MediaDesignStudioCommandCenterViewSummary.published"
      },
      {
       "kind": "metricTile",
       "label": "Draft",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 23 §Display",
       "bindsTo": "MediaDesignStudioCommandCenterViewSummary.draft"
      },
      {
       "kind": "metricTile",
       "label": "Pending Approval",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 23 §Display",
       "bindsTo": "MediaDesignStudioCommandCenterViewSummary.pendingApproval"
      },
      {
       "kind": "metricTile",
       "label": "Scheduled",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 23 §Display",
       "bindsTo": "MediaDesignStudioCommandCenterViewSummary.scheduled"
      },
      {
       "kind": "metricTile",
       "label": "Archived",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 23 §Display",
       "bindsTo": "MediaDesignStudioCommandCenterViewSummary.archived"
      },
      {
       "kind": "metricTile",
       "label": "QR / Digital Templates",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 23 §Display",
       "bindsTo": "MediaDesignStudioCommandCenterViewSummary.qrDigitalTemplates"
      },
      {
       "kind": "metricTile",
       "label": "PDF / Print Templates",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 23 §Display",
       "bindsTo": "MediaDesignStudioCommandCenterViewSummary.pdfPrintTemplates"
      },
      {
       "kind": "metricTile",
       "label": "Apple Wallet Templates",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 23 §Display",
       "bindsTo": "MediaDesignStudioCommandCenterViewSummary.appleWalletTemplates"
      },
      {
       "kind": "metricTile",
       "label": "Google Wallet Templates",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 23 §Display",
       "bindsTo": "MediaDesignStudioCommandCenterViewSummary.googleWalletTemplates"
      },
      {
       "kind": "metricTile",
       "label": "RFID / NFC Templates",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 23 §Display",
       "bindsTo": "MediaDesignStudioCommandCenterViewSummary.rfidNfcTemplates"
      },
      {
       "kind": "metricTile",
       "label": "Card / Wristband Templates",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 23 §Display",
       "bindsTo": "MediaDesignStudioCommandCenterViewSummary.cardWristbandTemplates"
      },
      {
       "kind": "metricTile",
       "label": "Templates Requiring Review",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 23 §Display",
       "bindsTo": "MediaDesignStudioCommandCenterViewSummary.templatesRequiringReview"
      },
      {
       "kind": "metricTile",
       "label": "Templates with Validation Errors",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 23 §Display",
       "bindsTo": "MediaDesignStudioCommandCenterViewSummary.templatesWithValidationErrors"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "moduleTiles",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every media design",
       "columns": [
        "MediaDesignStudioCommandCenterView.templateId",
        "MediaDesignStudioCommandCenterView.templateName",
        "MediaDesignStudioCommandCenterView.mediaType",
        "MediaDesignStudioCommandCenterView.brand",
        "MediaDesignStudioCommandCenterView.venue",
        "MediaDesignStudioCommandCenterView.productEventAssociation",
        "MediaDesignStudioCommandCenterView.language",
        "MediaDesignStudioCommandCenterView.version",
        "MediaDesignStudioCommandCenterView.effectiveFrom",
        "MediaDesignStudioCommandCenterView.effectiveTo",
        "MediaDesignStudioCommandCenterView.status",
        "MediaDesignStudioCommandCenterView.owner",
        "MediaDesignStudioCommandCenterView.lastModified"
       ],
       "bindsTo": "MediaDesignStudioCommandCenterView",
       "operation": "listMediaDesign",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 23 §Each template should show"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected media design",
       "bindsTo": "MediaDesignStudioCommandCenterView",
       "columns": [
        "MediaDesignStudioCommandCenterView.templateId",
        "MediaDesignStudioCommandCenterView.templateName",
        "MediaDesignStudioCommandCenterView.mediaType",
        "MediaDesignStudioCommandCenterView.brand",
        "MediaDesignStudioCommandCenterView.venue",
        "MediaDesignStudioCommandCenterView.productEventAssociation",
        "MediaDesignStudioCommandCenterView.language",
        "MediaDesignStudioCommandCenterView.version",
        "MediaDesignStudioCommandCenterView.effectiveFrom",
        "MediaDesignStudioCommandCenterView.effectiveTo",
        "MediaDesignStudioCommandCenterView.status",
        "MediaDesignStudioCommandCenterView.owner",
        "MediaDesignStudioCommandCenterView.lastModified"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Primary action”, “Digital”, “Print”, “Wallet”, “Physical”.",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 23 §Each template should show"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Duplicate Existing",
       "operation": "cloneTicketTemplate",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 23 §Allow"
      },
      {
       "kind": "secondaryButton",
       "label": "Use Venue Template",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 23 §Allow"
      },
      {
       "kind": "secondaryButton",
       "label": "Use Product Template",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 23 §Allow"
      },
      {
       "kind": "secondaryButton",
       "label": "Import supported template definition",
       "operation": "importTicketTemplate",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 23 §Allow"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The media design list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the media design untouched.",
   "emptyFirstRun": "No media design yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the media design are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listMediaDesign",
    "contract": "access",
    "purpose": "Media Design Studio Command Center",
    "trigger": "onLoad"
   },
   {
    "operationId": "listTicketTemplates",
    "contract": "orders",
    "purpose": "The ticket templates to duplicate or start from",
    "trigger": "onLoad"
   },
   {
    "operationId": "cloneTicketTemplate",
    "contract": "orders",
    "purpose": "Duplicate",
    "trigger": "onAction"
   },
   {
    "operationId": "importTicketTemplate",
    "contract": "orders",
    "purpose": "Import",
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-344",
   "workshopBoard": "wireframes/WS166 Ticket Media   Credential Management Board 2.dc.html#bo-344"
  },
  "apisNote": "Regenerated 9 September 2026 from Ticket_Media___Credential_Management_Reference.pdf page 23. 27 of 27 labels bound to a contract property; 31 of 59 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Pack actions reconciled 29 September (VM close-out):** still owed by a contract change: `importTicketTemplate`, `cloneTicketTemplate`.",
  "entryState": {
   "params": [
    {
     "name": "templateId",
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
  "id": "BO-345",
  "name": "Digital QR & Barcode Ticket Designer",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Ticket_Media___Credential_Management_Reference.pdf",
   "board": "2",
   "number": "15.2.2",
   "page": 24
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/digital-qr-barcode-ticket-designer-bo-345",
   "component": "apps/venue-management-web/src/routes/access-venue/DigitalQrBarcodeTicketDesigner.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-344"
   ],
   "exitTo": [
    "BO-344"
   ],
   "inferred": false,
   "notes": "**Reached from BO-344, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-344",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F169 step 2→3",
     "operation": "setDigitalBarcodeTicket",
     "carries": [
      "templateId"
     ]
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Authorized administrators can visually design and configure customer-facing QR/barcode tickets without development.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure; Barcode Configuration) and no display directory — it is settings, not a population",
  "purpose": "Provide a visual no-code designer specifically for digital QR and barcode tickets.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Static QR",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 24 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Dynamic QR",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 24 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Signed QR",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 24 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Tokenized QR",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 24 §Configure"
      },
      {
       "kind": "textField",
       "label": "Rotation behavior where supported",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 24 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Size",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 24 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Position",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 24 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Quiet zone",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 24 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Error correction",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 24 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Expiration",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 24 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Refresh behavior",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 24 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Barcode type",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 24 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Orientation",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 24 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Human-readable value",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 24 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Hide/show encoded reference",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 24 §Configure"
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
       "provenance": "contract operation setDigitalBarcodeTicket"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The digital barcode ticket configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the digital barcode ticket untouched.",
   "emptyFirstRun": "No digital barcode ticket configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setDigitalBarcodeTicket",
    "contract": "access",
    "purpose": "Digital QR & Barcode Ticket Designer",
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-345",
   "workshopBoard": "wireframes/WS166 Ticket Media   Credential Management Board 2.dc.html#bo-345"
  },
  "apisNote": "Regenerated 9 September 2026 from Ticket_Media___Credential_Management_Reference.pdf page 24. 0 of 0 labels bound to a contract property; 15 of 48 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-346",
  "name": "PDF, Printable & POS Ticket Designer",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Ticket_Media___Credential_Management_Reference.pdf",
   "board": "2",
   "number": "15.2.3",
   "page": 26
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/pdf-printable-pos-ticket-designer-bo-346",
   "component": "apps/venue-management-web/src/routes/access-venue/PdfPrintablePosTicketDesigner.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-344"
   ],
   "exitTo": [
    "BO-344"
   ],
   "inferred": false,
   "notes": "**Reached from BO-344, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-344",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F169 step 4→5",
     "operation": "setPdfPrintablePos",
     "carries": [
      "templateId"
     ]
    }
   ]
  },
  "density": "compact",
  "purposeNote": "and operational environments.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure; Configure/reference) and no display directory — it is settings, not a population",
  "purpose": "Design tickets intended for printing, PDF generation, POS, box office and other physical/document outputs.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Orientation",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 26 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Margins",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 26 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Header",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 26 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Footer",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 26 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Background",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 26 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Logo",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 26 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Images",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 26 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Text",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 26 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Dynamic fields",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 26 §Configure"
      },
      {
       "kind": "selectField",
       "label": "QR/barcode",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 26 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Terms",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 26 §Configure"
      },
      {
       "kind": "textField",
       "label": "Perforation indicators where applicable",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 26 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Print-safe zones",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 26 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Printer profile",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 26 §Configure/reference"
      },
      {
       "kind": "selectField",
       "label": "DPI",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 26 §Configure/reference"
      },
      {
       "kind": "selectField",
       "label": "Paper/stock type",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 26 §Configure/reference"
      },
      {
       "kind": "selectField",
       "label": "Thermal layout",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 26 §Configure/reference"
      },
      {
       "kind": "selectField",
       "label": "Cut behavior",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 26 §Configure/reference"
      },
      {
       "kind": "selectField",
       "label": "Print margins",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 26 §Configure/reference"
      },
      {
       "kind": "selectField",
       "label": "Supported printer integration",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 26 §Configure/reference"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "POS receipt",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 26 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Thermal ticket",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 26 §Support"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The pdf printable pos configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the pdf printable pos untouched.",
   "emptyFirstRun": "No pdf printable pos configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listTicketTemplates",
    "contract": "orders",
    "purpose": "The templates this venue issues from",
    "trigger": "onLoad"
   },
   {
    "operationId": "createTicketTemplate",
    "contract": "orders",
    "purpose": "Create a template",
    "trigger": "onAction",
    "invalidates": [
     "listTicketTemplates"
    ]
   },
   {
    "operationId": "updateTicketTemplate",
    "contract": "orders",
    "purpose": "Change or retire a template",
    "trigger": "onAction",
    "invalidates": [
     "listTicketTemplates"
    ]
   },
   {
    "operationId": "printTicketProof",
    "contract": "orders",
    "purpose": "Print a sample without selling anything",
    "trigger": "onAction"
   },
   {
    "operationId": "setPdfPrintablePos",
    "contract": "access",
    "purpose": "PDF, Printable & POS Ticket Designer",
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-346",
   "workshopBoard": "wireframes/WS166 Ticket Media   Credential Management Board 2.dc.html#bo-346"
  },
  "apisNote": "Regenerated 9 September 2026 from Ticket_Media___Credential_Management_Reference.pdf page 26. 0 of 0 labels bound to a contract property; 22 of 35 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Pack actions reconciled 29 September (VM close-out):** Thermal ticket are choices sent by `setPdfPrintablePos`.",
  "entryState": {
   "params": [
    {
     "name": "templateId",
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
  "id": "BO-347",
  "name": "Apple Wallet Pass Designer",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Ticket_Media___Credential_Management_Reference.pdf",
   "board": "2",
   "number": "15.2.4",
   "page": 27
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/apple-wallet-pass-designer-bo-347",
   "component": "apps/venue-management-web/src/routes/access-venue/AppleWalletPassDesigner.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-344"
   ],
   "exitTo": [
    "BO-344"
   ],
   "inferred": false,
   "notes": "**Reached from BO-344, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-344",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F169 step 6→7",
     "operation": "setAppleWalletPass",
     "carries": [
      "templateId"
     ]
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Administrators can configure, preview, test and publish Apple Wallet presentations of TICVAI Virtual Tickets using supported wallet capabilities.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Pass Configuration; Configure the appropriate; Configure/reference) and no display directory — it is settings, not a population",
  "purpose": "Provide an Apple Wallet-specific configuration experience for eligible TICVAI credentials. This should not simply be a PDF ticket rendered inside a wallet.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Pass identity",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 27 §Pass Configuration"
      },
      {
       "kind": "selectField",
       "label": "Organization",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 27 §Pass Configuration"
      },
      {
       "kind": "selectField",
       "label": "Description",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 27 §Pass Configuration"
      },
      {
       "kind": "selectField",
       "label": "Logo",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 27 §Pass Configuration"
      },
      {
       "kind": "selectField",
       "label": "Icon",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 27 §Pass Configuration"
      },
      {
       "kind": "selectField",
       "label": "Images where supported",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 27 §Pass Configuration"
      },
      {
       "kind": "selectField",
       "label": "Background appearance",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 27 §Pass Configuration"
      },
      {
       "kind": "selectField",
       "label": "Foreground appearance",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 27 §Pass Configuration"
      },
      {
       "kind": "selectField",
       "label": "Label appearance",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 27 §Pass Configuration"
      },
      {
       "kind": "selectField",
       "label": "Primary fields",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 27 §Pass Configuration"
      },
      {
       "kind": "selectField",
       "label": "Secondary fields",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 27 §Pass Configuration"
      },
      {
       "kind": "selectField",
       "label": "Auxiliary fields",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 27 §Pass Configuration"
      },
      {
       "kind": "selectField",
       "label": "Header fields",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 27 §Pass Configuration"
      },
      {
       "kind": "selectField",
       "label": "Back fields",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 27 §Pass Configuration"
      },
      {
       "kind": "selectField",
       "label": "QR",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 27 §Configure the appropriate"
      },
      {
       "kind": "selectField",
       "label": "Barcode",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 27 §Configure the appropriate"
      },
      {
       "kind": "selectField",
       "label": "Token/reference",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 27 §Configure the appropriate"
      },
      {
       "kind": "selectField",
       "label": "Dynamic updates",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 27 §Configure/reference"
      },
      {
       "kind": "selectField",
       "label": "Event changes",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 27 §Configure/reference"
      },
      {
       "kind": "selectField",
       "label": "Seat changes",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 27 §Configure/reference"
      },
      {
       "kind": "selectField",
       "label": "Ticket status changes",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 27 §Configure/reference"
      },
      {
       "kind": "selectField",
       "label": "Relevant notification/update behavior",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 27 §Configure/reference"
      },
      {
       "kind": "selectField",
       "label": "Expiry",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 27 §Configure/reference"
      },
      {
       "kind": "textField",
       "label": "Revocation/invalidation behavior where supported",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 27 §Configure/reference"
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
       "provenance": "contract operation setAppleWalletPass"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The apple wallet pass configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the apple wallet pass untouched.",
   "emptyFirstRun": "No apple wallet pass configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setAppleWalletPass",
    "contract": "access",
    "purpose": "Apple Wallet Pass Designer",
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-347",
   "workshopBoard": "wireframes/WS166 Ticket Media   Credential Management Board 2.dc.html#bo-347"
  },
  "apisNote": "Regenerated 9 September 2026 from Ticket_Media___Credential_Management_Reference.pdf page 27. 0 of 0 labels bound to a contract property; 24 of 33 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-348",
  "name": "Google Wallet Pass Designer",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Ticket_Media___Credential_Management_Reference.pdf",
   "board": "2",
   "number": "15.2.5",
   "page": 29
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/google-wallet-pass-designer-bo-348",
   "component": "apps/venue-management-web/src/routes/access-venue/GoogleWalletPassDesigner.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-344"
   ],
   "exitTo": [
    "BO-344"
   ],
   "inferred": false,
   "notes": "**Reached from BO-344, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-344",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F169 step 8→9",
     "operation": "setGoogleWalletPass",
     "carries": [
      "templateId"
     ]
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Administrators can independently configure and govern Google Wallet ticket presentations while retaining the same underlying Virtual Ticket architecture.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure supported; Configure) and no display directory — it is settings, not a population",
  "purpose": "Provide a dedicated Google Wallet configuration environment.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Pass class/template",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 29 §Configure supported"
      },
      {
       "kind": "selectField",
       "label": "Issuer",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 29 §Configure supported"
      },
      {
       "kind": "selectField",
       "label": "Title",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 29 §Configure supported"
      },
      {
       "kind": "selectField",
       "label": "Logo",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 29 §Configure supported"
      },
      {
       "kind": "textField",
       "label": "Hero/image assets where applicable",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 29 §Configure supported"
      },
      {
       "kind": "selectField",
       "label": "Event information",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 29 §Configure supported"
      },
      {
       "kind": "selectField",
       "label": "Venue",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 29 §Configure supported"
      },
      {
       "kind": "selectField",
       "label": "Date/time",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 29 §Configure supported"
      },
      {
       "kind": "selectField",
       "label": "Ticket holder",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 29 §Configure supported"
      },
      {
       "kind": "selectField",
       "label": "Seat",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 29 §Configure supported"
      },
      {
       "kind": "selectField",
       "label": "Ticket type",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 29 §Configure supported"
      },
      {
       "kind": "selectField",
       "label": "Custom fields",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 29 §Configure supported"
      },
      {
       "kind": "selectField",
       "label": "Status",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 29 §Configure supported"
      },
      {
       "kind": "selectField",
       "label": "Links",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 29 §Configure supported"
      },
      {
       "kind": "selectField",
       "label": "Additional information",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 29 §Configure supported"
      },
      {
       "kind": "selectField",
       "label": "QR",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 29 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Barcode",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 29 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Credential/token reference",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 29 §Configure"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Event time change",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 29 §Support/reference updates such as"
      },
      {
       "kind": "secondaryButton",
       "label": "Venue change",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 29 §Support/reference updates such as"
      },
      {
       "kind": "secondaryButton",
       "label": "Ticket status change",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 29 §Support/reference updates such as"
      },
      {
       "kind": "secondaryButton",
       "label": "Relevant ticket information changes",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 29 §Support/reference updates such as"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The google wallet pass configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the google wallet pass untouched.",
   "emptyFirstRun": "No google wallet pass configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setGoogleWalletPass",
    "contract": "access",
    "purpose": "Google Wallet Pass Designer",
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-348",
   "workshopBoard": "wireframes/WS166 Ticket Media   Credential Management Board 2.dc.html#bo-348"
  },
  "apisNote": "Regenerated 9 September 2026 from Ticket_Media___Credential_Management_Reference.pdf page 29. 0 of 0 labels bound to a contract property; 22 of 30 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Pack actions reconciled 29 September (VM close-out):** Event time change, Venue change, Ticket status change, Relevant ticket information changes are choices sent by `setGoogleWalletPass`.",
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
  "id": "BO-349",
  "name": "RFID, NFC, Card & Wristband Media Designer",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Ticket_Media___Credential_Management_Reference.pdf",
   "board": "2",
   "number": "15.2.6",
   "page": 30
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/rfid-nfc-card-wristband-media-designer-bo-349",
   "component": "apps/venue-management-web/src/routes/access-venue/RfidNfcCardWristbandMediaDesigner.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-344"
   ],
   "exitTo": [
    "BO-344"
   ],
   "inferred": false,
   "notes": "**Reached from BO-344, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-344",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F169 step 10→11",
     "operation": "setRfidNfcCard",
     "carries": [
      "templateId"
     ]
    }
   ]
  },
  "density": "compact",
  "purposeNote": "cards, wristbands and supported wearable media.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure; Configure/reference) and no display directory — it is settings, not a population",
  "purpose": "Configure both the visual and technical profile of physical electronic credentials. This is important because RFID/NFC media are not merely artwork.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Media dimensions",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 30 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Front",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 30 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Back",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 30 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Printable area",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 30 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Logo",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 30 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Customer name",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 30 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Photo",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 30 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Membership tier",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 30 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Expiry",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 30 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Serial number",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 30 §Configure"
      },
      {
       "kind": "selectField",
       "label": "QR/barcode if combined",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 30 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Custom artwork",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 30 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Sponsor/venue branding",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 30 §Configure"
      },
      {
       "kind": "selectField",
       "label": "RFID/NFC technology",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 30 §Configure/reference"
      },
      {
       "kind": "selectField",
       "label": "Chip/profile",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 30 §Configure/reference"
      },
      {
       "kind": "selectField",
       "label": "UID/reference handling",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 30 §Configure/reference"
      },
      {
       "kind": "selectField",
       "label": "Encoding profile",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 30 §Configure/reference"
      },
      {
       "kind": "selectField",
       "label": "Provider",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 30 §Configure/reference"
      },
      {
       "kind": "selectField",
       "label": "Reader compatibility",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 30 §Configure/reference"
      },
      {
       "kind": "selectField",
       "label": "Printer/encoder integration",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 30 §Configure/reference"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "RFID Card",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 30 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "NFC Card",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 30 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Membership Card",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 30 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Staff/guest card where applicable",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 30 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Size where applicable",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 30 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Deposit/reference where applicable",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 30 §Support"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The rfid nfc card configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the rfid nfc card untouched.",
   "emptyFirstRun": "No rfid nfc card configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setRfidNfcCard",
    "contract": "access",
    "purpose": "RFID, NFC, Card & Wristband Media Designer",
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-349",
   "workshopBoard": "wireframes/WS166 Ticket Media   Credential Management Board 2.dc.html#bo-349"
  },
  "apisNote": "Regenerated 9 September 2026 from Ticket_Media___Credential_Management_Reference.pdf page 30. 0 of 0 labels bound to a contract property; 26 of 41 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Pack actions reconciled 29 September (VM close-out):** Membership Card, Staff/guest card where applicable, Size where applicable, Deposit/reference where applicable are choices sent by `setRfidNfcCard`.",
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
  "id": "BO-350",
  "name": "Digital Card, Membership & Wearable Designer",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Ticket_Media___Credential_Management_Reference.pdf",
   "board": "2",
   "number": "15.2.7",
   "page": 31
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/digital-card-membership-wearable-designer-bo-350",
   "component": "apps/venue-management-web/src/routes/access-venue/DigitalCardMembershipWearableDesigner.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-344"
   ],
   "exitTo": [
    "BO-344"
   ],
   "inferred": false,
   "notes": "**Reached from BO-344, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-344",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F169 step 12→13",
     "operation": "setDigitalCardMembership",
     "carries": [
      "templateId"
     ]
    }
   ]
  },
  "density": "compact",
  "purposeNote": "templates linked to persistent Virtual Tickets or applicable entitlement identities.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Provide specialized configuration for persistent credentials that may represent longer-lived relationships rather than a single event ticket.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Brand",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 31 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Card artwork",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 31 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Member photograph",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 31 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Member name",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 31 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Membership number",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 31 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Tier",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 31 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Validity",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 31 §Configure"
      },
      {
       "kind": "selectField",
       "label": "QR/barcode",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 31 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Status",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 31 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Benefits summary",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 31 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Dynamic messaging",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 31 §Configure"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Tier designs",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 31 §Support different"
      },
      {
       "kind": "secondaryButton",
       "label": "Membership types",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 31 §Support different"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The digital card membership configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the digital card membership untouched.",
   "emptyFirstRun": "No digital card membership configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setDigitalCardMembership",
    "contract": "access",
    "purpose": "Digital Card, Membership & Wearable Designer",
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-350",
   "workshopBoard": "wireframes/WS166 Ticket Media   Credential Management Board 2.dc.html#bo-350"
  },
  "apisNote": "Regenerated 9 September 2026 from Ticket_Media___Credential_Management_Reference.pdf page 31. 0 of 0 labels bound to a contract property; 13 of 36 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Pack actions reconciled 29 September (VM close-out):** Tier designs are choices sent by `setDigitalCardMembership`.",
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
  "id": "BO-351",
  "name": "Dynamic Fields, Data Mapping & Content Builder",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Ticket_Media___Credential_Management_Reference.pdf",
   "board": "2",
   "number": "15.2.8",
   "page": 32
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/dynamic-fields-data-mapping-content-builder-bo-351",
   "component": "apps/venue-management-web/src/routes/access-venue/DynamicFieldsDataMappingContentBuilder.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-344"
   ],
   "exitTo": [
    "BO-344"
   ],
   "inferred": false,
   "notes": "**Reached from BO-344, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-344",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F169 step 14→15",
     "operation": "setDynamicFieldData"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "All media designers consume a governed reusable field/data-mapping framework rather than independently hard-coding ticket information.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Custom Fields; Configure) and no display directory — it is settings, not a population",
  "purpose": "Create a centralized reusable field library so development team does not hard-code ticket fields separately into every media designer. This is another important architecture screen.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Date formats",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 32 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Time formats",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 32 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Currency",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 32 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Number formatting",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 32 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Text transformation",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 32 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Character limit",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 32 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Conditional visibility",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 32 §Configure"
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
       "provenance": "contract operation setDynamicFieldData"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The dynamic fields data configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the dynamic fields data untouched.",
   "emptyFirstRun": "No dynamic fields data configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setDynamicFieldData",
    "contract": "access",
    "purpose": "Dynamic Fields, Data Mapping & Content Builder",
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-351",
   "workshopBoard": "wireframes/WS166 Ticket Media   Credential Management Board 2.dc.html#bo-351"
  },
  "apisNote": "Regenerated 9 September 2026 from Ticket_Media___Credential_Management_Reference.pdf page 32. 0 of 0 labels bound to a contract property; 7 of 64 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-352",
  "name": "Branding, Localization & Template Inheritance",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Ticket_Media___Credential_Management_Reference.pdf",
   "board": "2",
   "number": "15.2.9",
   "page": 34
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/branding-localization-template-inheritance-bo-352",
   "component": "apps/venue-management-web/src/routes/access-venue/BrandingLocalizationTemplateInheritance.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-344"
   ],
   "exitTo": [
    "BO-344"
   ],
   "inferred": false,
   "notes": "**Reached from BO-344, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-344",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F169 step 16→17",
     "operation": "listBrandingLocalizationTemplate"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "controlled inheritance and media-specific overrides.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Track) and no metric row",
  "purpose": "Allow TICVAI's multi-tenant clients to control branding and localization without rebuilding every ticket template.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every branding localization template",
       "columns": [
        "BrandingLocalizationTemplateInheritanceView.sourceLanguage",
        "BrandingLocalizationTemplateInheritanceView.translation",
        "BrandingLocalizationTemplateInheritanceView.translationStatus",
        "BrandingLocalizationTemplateInheritanceView.reviewer",
        "BrandingLocalizationTemplateInheritanceView.approval",
        "BrandingLocalizationTemplateInheritanceView.version"
       ],
       "bindsTo": "BrandingLocalizationTemplateInheritanceView",
       "operation": "listBrandingLocalizationTemplate",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 34 §Track"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected branding localization template",
       "bindsTo": "BrandingLocalizationTemplateInheritanceView",
       "columns": [
        "BrandingLocalizationTemplateInheritanceView.sourceLanguage",
        "BrandingLocalizationTemplateInheritanceView.translation",
        "BrandingLocalizationTemplateInheritanceView.translationStatus",
        "BrandingLocalizationTemplateInheritanceView.reviewer",
        "BrandingLocalizationTemplateInheritanceView.approval",
        "BrandingLocalizationTemplateInheritanceView.version"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Tenant / Corporate”, “Brand”, “Venue”, “Event”, “Product”, “Inheritance Example”.",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 34 §Track"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Additional configured languages",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 34 §Support"
      },
      {
       "kind": "primaryButton",
       "label": "Save branding and languages",
       "operation": "setBrandingLocalizationTemplate",
       "provenance": "contract access.yaml PUT /branding-localization-template (decided 29 September, VM close-out)"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The branding localization template list.",
   "error": "Could not load. Names which read failed and leaves the branding localization template untouched.",
   "emptyFirstRun": "No branding localization template yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the branding localization template are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listBrandingLocalizationTemplate",
    "contract": "access",
    "purpose": "Branding, Localization & Template Inheritance",
    "trigger": "onLoad"
   },
   {
    "operationId": "setBrandingLocalizationTemplate",
    "contract": "access",
    "purpose": "Save branding and languages",
    "trigger": "onAction"
   }
  ],
  "entryState": {
   "preloaded": [
    "BrandingLocalizationTemplateInheritanceView.sourceLanguage",
    "BrandingLocalizationTemplateInheritanceView.translation",
    "BrandingLocalizationTemplateInheritanceView.translationStatus",
    "BrandingLocalizationTemplateInheritanceView.reviewer",
    "BrandingLocalizationTemplateInheritanceView.approval",
    "BrandingLocalizationTemplateInheritanceView.version"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-352",
   "workshopBoard": "wireframes/WS166 Ticket Media   Credential Management Board 2.dc.html#bo-352"
  },
  "apisNote": "Regenerated 9 September 2026 from Ticket_Media___Credential_Management_Reference.pdf page 34. 6 of 6 labels bound to a contract property; 16 of 35 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Pack actions reconciled 29 September (VM close-out):** still owed by a contract change: `setBrandingLocalizationTemplate`.",
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
  "id": "BO-353",
  "name": "Multi-Media Preview, Testing, Approval & Publication",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Ticket_Media___Credential_Management_Reference.pdf",
   "board": "2",
   "number": "15.2.10",
   "page": 36
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/multi-media-preview-testing-approval-publication-bo-353",
   "component": "apps/venue-management-web/src/routes/access-venue/MultiMediaPreviewTestingApprovalPublication.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-344"
   ],
   "exitTo": [
    "BO-344"
   ],
   "inferred": false,
   "notes": "**Reached from BO-344, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-344",
     "trigger": "Media Design Studio Command Center",
     "carries": [
      "templateId"
     ],
     "provenance": "derived — BO-344 declares entryState.params templateId and BO-353 holds templateId, so an edge into it carries them"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Administrators can preview, test, approve, version and publish every supported ticket-media configuration before it becomes available for production issuance. Board 2 — Final Screen Register",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Provide the final quality and governance gate before any media template becomes operational. This should be a particularly visual screen. Board 1 established the Virtual Ticket as the authoritative ticket identity and the one- Virtual-Ticket-to-many-media architecture. Board 2 established how administrators design and configure each media type. Board 3 manages what happens to the actual credential instances in production after a Virtual Ticket has been created.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Ticket_Media___Credential_Management_Reference.pdf, page 36"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Ticket_Media___Credential_Management_Reference.pdf, page 36"
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
       "label": "Publish Now",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 36 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Schedule",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 36 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Selected Brands",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 36 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Selected Venues",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 36 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Selected Products",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 36 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Selected Channels",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 36 §Support"
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
   "loading": "The multi-media preview testing list.",
   "error": "Could not load. Names which read failed and leaves the multi-media preview testing untouched.",
   "emptyFirstRun": "No multi-media preview testing yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the multi-media preview testing are still there. The pack's own statuses are if Required → Expire → Audit — the state names which is selected.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "approveMultiMediaPreview",
    "contract": "access",
    "purpose": "Multi-Media Preview, Testing, Approval & Publication",
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-353",
   "workshopBoard": "wireframes/WS166 Ticket Media   Credential Management Board 2.dc.html#bo-353"
  },
  "apisNote": "Regenerated 9 September 2026 from Ticket_Media___Credential_Management_Reference.pdf page 36. 0 of 0 labels bound to a contract property; 7 of 126 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Pack actions reconciled 29 September (VM close-out):** Publish Now, Schedule, Selected Brands, Selected Venues, Selected Products, Selected Channels are choices sent by `approveMultiMediaPreview`.",
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
 "approveMultiMediaPreview": {
  "method": "PUT",
  "path": "/multi-media-preview",
  "contract": "access",
  "summary": "Multi-Media Preview, Testing, Approval & Publication",
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
  "requestBody": "MultiMediaPreviewTestingApprovalPublicationInput",
  "responds": "MultiMediaPreviewTestingApprovalPublicationView"
 },
 "cloneTicketTemplate": {
  "method": "POST",
  "path": "/ticket-templates/{templateId}/clone",
  "contract": "orders",
  "summary": "Create a ticket template from an existing one",
  "permission": "PRODUCT_CONFIGURE",
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
  "requestBody": "CloneTicketTemplateInput",
  "responds": "TicketTemplate"
 },
 "createTicketTemplate": {
  "method": "POST",
  "path": "/ticket-templates",
  "contract": "orders",
  "summary": "Create a ticket template",
  "permission": "PRODUCT_CONFIGURE",
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
  "requestBody": "TicketTemplateRequest",
  "responds": "TicketTemplate"
 },
 "importTicketTemplate": {
  "method": "POST",
  "path": "/ticket-templates/imports",
  "contract": "orders",
  "summary": "Import a ticket template definition",
  "permission": "PRODUCT_CONFIGURE",
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
  "requestBody": "TicketTemplateImportInput",
  "responds": "TicketTemplate"
 },
 "listBrandingLocalizationTemplate": {
  "method": "GET",
  "path": "/branding-localization-template",
  "contract": "access",
  "summary": "Branding, Localization & Template Inheritance",
  "permission": "SCOPE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "BrandingLocalizationTemplateInheritanceView"
 },
 "listMediaDesign": {
  "method": "GET",
  "path": "/media-design",
  "contract": "access",
  "summary": "Media Design Studio Command Center",
  "permission": "SCOPE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "mediaType",
    "in": "query",
    "required": false
   },
   {
    "name": "status",
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
 "listTicketTemplates": {
  "method": "GET",
  "path": "/ticket-templates",
  "contract": "orders",
  "summary": "The ticket templates a venue issues from",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "mediaType",
    "in": "query",
    "required": false
   },
   {
    "name": "includeInactive",
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
 "printTicketProof": {
  "method": "POST",
  "path": "/ticket-templates/{templateId}/proof",
  "contract": "orders",
  "summary": "Print a sample without selling anything",
  "permission": "ORDER_REPRINT",
  "offlineCapable": true,
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
  "responds": "TicketProof"
 },
 "setAppleWalletPass": {
  "method": "PUT",
  "path": "/apple-wallet-pass",
  "contract": "access",
  "summary": "Apple Wallet Pass Designer",
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
  "requestBody": "AppleWalletPassDesignerInput",
  "responds": "AppleWalletPassDesignerView"
 },
 "setBrandingLocalizationTemplate": {
  "method": "PUT",
  "path": "/branding-localization-template",
  "contract": "access",
  "summary": "Save branding and languages for a level",
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
  "requestBody": "BrandingLocalizationTemplateInheritanceInput",
  "responds": "BrandingLocalizationTemplateInheritanceView"
 },
 "setDigitalBarcodeTicket": {
  "method": "PUT",
  "path": "/digital-barcode-ticket",
  "contract": "access",
  "summary": "Digital QR & Barcode Ticket Designer",
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
  "requestBody": "DigitalQrBarcodeTicketDesignerInput",
  "responds": "DigitalQrBarcodeTicketDesignerView"
 },
 "setDigitalCardMembership": {
  "method": "PUT",
  "path": "/digital-card-membership",
  "contract": "access",
  "summary": "Digital Card, Membership & Wearable Designer",
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
  "requestBody": "DigitalCardMembershipWearableDesignerInput",
  "responds": "DigitalCardMembershipWearableDesignerView"
 },
 "setDynamicFieldData": {
  "method": "PUT",
  "path": "/dynamic-field-data",
  "contract": "access",
  "summary": "Dynamic Fields, Data Mapping & Content Builder",
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
  "requestBody": "DynamicFieldsDataMappingContentBuilderInput",
  "responds": "DynamicFieldsDataMappingContentBuilderView"
 },
 "setGoogleWalletPass": {
  "method": "PUT",
  "path": "/google-wallet-pass",
  "contract": "access",
  "summary": "Google Wallet Pass Designer",
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
  "requestBody": "GoogleWalletPassDesignerInput",
  "responds": "GoogleWalletPassDesignerView"
 },
 "setPdfPrintablePos": {
  "method": "PUT",
  "path": "/pdf-printable-pos",
  "contract": "access",
  "summary": "PDF, Printable & POS Ticket Designer",
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
  "requestBody": "PdfPrintablePosTicketDesignerInput",
  "responds": "PdfPrintablePosTicketDesignerView"
 },
 "setRfidNfcCard": {
  "method": "PUT",
  "path": "/rfid-nfc-card",
  "contract": "access",
  "summary": "RFID, NFC, Card & Wristband Media Designer",
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
  "requestBody": "RfidNfcCardWristbandMediaDesignerInput",
  "responds": "RfidNfcCardWristbandMediaDesignerView"
 },
 "updateTicketTemplate": {
  "method": "PATCH",
  "path": "/ticket-templates/{templateId}",
  "contract": "orders",
  "summary": "Change or retire a ticket template",
  "permission": "PRODUCT_CONFIGURE",
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
  "requestBody": "TicketTemplateRequest",
  "responds": "TicketTemplate"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "AppleWalletPassDesignerInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Apple Wallet Pass Designer submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "templateId": {
    "type": "string",
    "description": "Media template being designed"
   },
   "passIdentity": {
    "type": "string",
    "description": "Pass identity"
   },
   "organization": {
    "type": "string",
    "description": "Organization"
   },
   "description": {
    "type": "string",
    "description": "Description"
   },
   "logo": {
    "type": "string",
    "description": "Logo"
   },
   "icon": {
    "type": "string",
    "description": "Icon"
   },
   "imagesWhereSupported": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Images where supported"
   },
   "backgroundAppearance": {
    "type": "string",
    "description": "Background appearance"
   },
   "foregroundAppearance": {
    "type": "string",
    "description": "Foreground appearance"
   },
   "labelAppearance": {
    "type": "string",
    "description": "Label appearance"
   },
   "primaryFields": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Primary fields"
   },
   "secondaryFields": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Secondary fields"
   },
   "auxiliaryFields": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Auxiliary fields"
   },
   "headerFields": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Header fields"
   },
   "backFields": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Back fields"
   },
   "credentialEncoding": {
    "type": "string",
    "enum": [
     "qr",
     "barcode",
     "tokenReference"
    ],
    "description": "How the credential is carried on the pass, per the credential profile"
   },
   "dynamicUpdates": {
    "type": "boolean",
    "description": "Issued passes receive updates"
   },
   "updateTriggers": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "eventChange",
      "seatChange",
      "ticketStatusChange"
     ]
    },
    "description": "Changes that push an update to issued passes"
   },
   "relevantNotificationUpdateBehavior": {
    "type": "string",
    "description": "Relevant notification/update behavior"
   },
   "expiry": {
    "type": "string",
    "description": "Expiry rule for the pass, e.g. end of validity"
   },
   "revocationInvalidationBehaviorWhereSupported": {
    "type": "string",
    "description": "Revocation/invalidation behavior where supported"
   }
  },
  "required": [
   "templateId"
  ]
 },
 "AppleWalletPassDesignerView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Apple Wallet Pass Designer displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "templateId": {
    "type": "string",
    "description": "Media template being designed"
   },
   "passIdentity": {
    "type": "string",
    "description": "Pass identity"
   },
   "organization": {
    "type": "string",
    "description": "Organization"
   },
   "description": {
    "type": "string",
    "description": "Description"
   },
   "logo": {
    "type": "string",
    "description": "Logo"
   },
   "icon": {
    "type": "string",
    "description": "Icon"
   },
   "imagesWhereSupported": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Images where supported"
   },
   "backgroundAppearance": {
    "type": "string",
    "description": "Background appearance"
   },
   "foregroundAppearance": {
    "type": "string",
    "description": "Foreground appearance"
   },
   "labelAppearance": {
    "type": "string",
    "description": "Label appearance"
   },
   "primaryFields": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Primary fields"
   },
   "secondaryFields": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Secondary fields"
   },
   "auxiliaryFields": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Auxiliary fields"
   },
   "headerFields": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Header fields"
   },
   "backFields": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Back fields"
   },
   "credentialEncoding": {
    "type": "string",
    "enum": [
     "qr",
     "barcode",
     "tokenReference"
    ],
    "description": "How the credential is carried on the pass, per the credential profile"
   },
   "dynamicUpdates": {
    "type": "boolean",
    "description": "Issued passes receive updates"
   },
   "updateTriggers": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "eventChange",
      "seatChange",
      "ticketStatusChange"
     ]
    },
    "description": "Changes that push an update to issued passes"
   },
   "relevantNotificationUpdateBehavior": {
    "type": "string",
    "description": "Relevant notification/update behavior"
   },
   "expiry": {
    "type": "string",
    "description": "Expiry rule for the pass, e.g. end of validity"
   },
   "revocationInvalidationBehaviorWhereSupported": {
    "type": "string",
    "description": "Revocation/invalidation behavior where supported"
   }
  },
  "required": [
   "templateId"
  ]
 },
 "BrandingLocalizationTemplateInheritanceInput": {
  "type": "object",
  "x-ticvai-persistence": "none — request only; the write configures the rules the matching View reads back (decided 29 September, VM close-out)",
  "description": "**What Branding, Localization & Template Inheritance submits** (decided 29 September, VM close-out). The writable fields of its View; the figures the screen computes are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "required": [
   "level",
   "scopeId",
   "sourceLanguage"
  ],
  "properties": {
   "level": {
    "type": "string",
    "enum": [
     "tenant",
     "brand",
     "venue",
     "event",
     "product",
     "mediaTemplate"
    ]
   },
   "scopeId": {
    "type": "string"
   },
   "parentScopeId": {
    "type": "string",
    "description": "The level above this one inherits from; empty at tenant"
   },
   "logo": {
    "type": "string",
    "description": "Asset library reference"
   },
   "colors": {
    "type": "array",
    "items": {
     "type": "string",
     "pattern": "^#[0-9A-Fa-f]{6}$"
    }
   },
   "typography": {
    "type": "string"
   },
   "backgrounds": {
    "type": "string"
   },
   "headerFooter": {
    "type": "string"
   },
   "legalFooter": {
    "type": "string"
   },
   "supportInformation": {
    "type": "string"
   },
   "sponsorPlacement": {
    "type": "string"
   },
   "images": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "sourceLanguage": {
    "type": "string",
    "maxLength": 35,
    "description": "BCP 47 tag"
   },
   "languages": {
    "type": "array",
    "items": {
     "type": "string",
     "maxLength": 35
    },
    "description": "Additional configured languages (BCP 47)"
   },
   "rtl": {
    "type": "boolean",
    "default": false,
    "description": "Right-to-left layout for the RTL languages in `languages`"
   },
   "fieldOverrides": {
    "type": "object",
    "additionalProperties": {
     "type": "string"
    },
    "description": "Field-level overrides of the inherited template, keyed by field name"
   }
  }
 },
 "BrandingLocalizationTemplateInheritanceView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Branding, Localization & Template Inheritance displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "parentScopeId": {
    "type": "string",
    "description": "The level above this one inherits from; empty at tenant (decided 29 September, VM close-out)"
   },
   "rtl": {
    "type": "boolean",
    "description": "Right-to-left layout for the RTL languages in `languages` (decided 29 September, VM close-out)"
   },
   "scopeId": {
    "type": "string",
    "description": "ID of the tenant, brand, venue, event, product or template at that level"
   },
   "level": {
    "type": "string",
    "enum": [
     "tenant",
     "brand",
     "venue",
     "event",
     "product",
     "mediaTemplate"
    ],
    "description": "Inheritance level"
   },
   "logo": {
    "type": "string",
    "description": "Logo"
   },
   "colors": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Colors"
   },
   "typography": {
    "type": "string",
    "description": "Typography"
   },
   "backgrounds": {
    "type": "string",
    "description": "Backgrounds"
   },
   "headerFooter": {
    "type": "string",
    "description": "Header/footer"
   },
   "legalFooter": {
    "type": "string",
    "description": "Legal footer"
   },
   "supportInformation": {
    "type": "string",
    "description": "Support information"
   },
   "sponsorPlacement": {
    "type": "string",
    "description": "Sponsor placement"
   },
   "images": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Images"
   },
   "sourceLanguage": {
    "type": "string",
    "description": "Source language"
   },
   "translation": {
    "type": "string",
    "description": "Translation"
   },
   "translationStatus": {
    "type": "string",
    "enum": [
     "notStarted",
     "inProgress",
     "inReview",
     "approved"
    ],
    "description": "Translation status"
   },
   "reviewer": {
    "type": "string",
    "description": "Reviewer"
   },
   "approval": {
    "type": "string",
    "description": "Approval"
   },
   "version": {
    "type": "string",
    "description": "Version"
   },
   "languages": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Language codes; English and Arabic at minimum, plus configured languages"
   }
  },
  "required": [
   "level",
   "scopeId"
  ]
 },
 "CloneTicketTemplateInput": {
  "type": "object",
  "x-ticvai-persistence": "none — request only",
  "description": "What `cloneTicketTemplate` takes (decided 29 September, readiness close-out).",
  "required": [
   "name",
   "source"
  ],
  "properties": {
   "name": {
    "type": "string",
    "maxLength": 120
   },
   "source": {
    "type": "string",
    "description": "What the template in the path is (decided 29 September, readiness close-out).",
    "enum": [
     "existingTemplate",
     "venueTemplate",
     "productTemplate"
    ]
   },
   "venueId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The venue whose template is copied. Required for `venueTemplate`."
   },
   "productId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The product the template issues for. Required for `productTemplate`."
   }
  }
 },
 "DigitalCardMembershipWearableDesignerInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Digital Card, Membership & Wearable Designer submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "templateId": {
    "type": "string",
    "description": "Media template being designed"
   },
   "brand": {
    "type": "string",
    "description": "Brand"
   },
   "cardArtwork": {
    "type": "string",
    "description": "Card artwork"
   },
   "memberPhotograph": {
    "type": "string",
    "description": "Member photograph"
   },
   "memberName": {
    "type": "string",
    "description": "Member name"
   },
   "membershipNumber": {
    "type": "string",
    "description": "Membership number"
   },
   "tier": {
    "type": "string",
    "description": "Tier"
   },
   "validity": {
    "type": "string",
    "description": "Validity"
   },
   "qrBarcode": {
    "type": "string",
    "description": "QR/barcode"
   },
   "status": {
    "type": "string",
    "description": "Status"
   },
   "benefitsSummary": {
    "type": "string",
    "description": "Benefits summary"
   },
   "dynamicMessaging": {
    "type": "string",
    "description": "Dynamic messaging"
   },
   "tierDesigns": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Artwork per tier, e.g. Silver, Gold, Platinum"
   },
   "membershipTypes": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Membership types"
   },
   "brands": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Brands"
   },
   "venues": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Venues"
   },
   "ageCategories": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Age categories"
   },
   "stateTriggers": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "membershipRenewal",
      "tierChange",
      "expiry",
      "suspension",
      "benefitStatus"
     ]
    },
    "description": "Changes that alter how the persistent card is presented"
   }
  },
  "required": [
   "templateId"
  ]
 },
 "DigitalCardMembershipWearableDesignerView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Digital Card, Membership & Wearable Designer displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "templateId": {
    "type": "string",
    "description": "Media template being designed"
   },
   "brand": {
    "type": "string",
    "description": "Brand"
   },
   "cardArtwork": {
    "type": "string",
    "description": "Card artwork"
   },
   "memberPhotograph": {
    "type": "string",
    "description": "Member photograph"
   },
   "memberName": {
    "type": "string",
    "description": "Member name"
   },
   "membershipNumber": {
    "type": "string",
    "description": "Membership number"
   },
   "tier": {
    "type": "string",
    "description": "Tier"
   },
   "validity": {
    "type": "string",
    "description": "Validity"
   },
   "qrBarcode": {
    "type": "string",
    "description": "QR/barcode"
   },
   "status": {
    "type": "string",
    "description": "Status"
   },
   "benefitsSummary": {
    "type": "string",
    "description": "Benefits summary"
   },
   "dynamicMessaging": {
    "type": "string",
    "description": "Dynamic messaging"
   },
   "tierDesigns": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Artwork per tier, e.g. Silver, Gold, Platinum"
   },
   "membershipTypes": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Membership types"
   },
   "brands": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Brands"
   },
   "venues": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Venues"
   },
   "ageCategories": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Age categories"
   },
   "stateTriggers": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "membershipRenewal",
      "tierChange",
      "expiry",
      "suspension",
      "benefitStatus"
     ]
    },
    "description": "Changes that alter how the persistent card is presented"
   }
  },
  "required": [
   "templateId"
  ]
 },
 "DigitalQrBarcodeTicketDesignerInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Digital QR & Barcode Ticket Designer submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "templateId": {
    "type": "string",
    "description": "Media template being designed"
   },
   "components": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "logo",
      "eventImage",
      "eventName",
      "ticketType",
      "customerName",
      "participantName",
      "date",
      "time",
      "venue",
      "entrance",
      "section",
      "row",
      "seat",
      "price",
      "orderReference",
      "virtualTicketId",
      "qr",
      "barcode",
      "terms",
      "instructions",
      "waiverLinkStatus",
      "sponsor",
      "customFields"
     ]
    },
    "description": "Components placed on the layout; values come from the dynamic-field library"
   },
   "qrMode": {
    "type": "string",
    "enum": [
     "staticQr",
     "dynamicQr",
     "signedQr",
     "tokenizedQr"
    ],
    "description": "QR payload profile"
   },
   "rotationBehaviorWhereSupported": {
    "type": "string",
    "description": "Rotation behavior where supported"
   },
   "size": {
    "type": "string",
    "description": "Size"
   },
   "position": {
    "type": "string",
    "description": "Position"
   },
   "quietZone": {
    "type": "string",
    "description": "Quiet zone"
   },
   "errorCorrection": {
    "type": "string",
    "enum": [
     "l",
     "m",
     "q",
     "h"
    ],
    "description": "QR error-correction level"
   },
   "expiration": {
    "type": "string",
    "description": "Expiration"
   },
   "refreshBehavior": {
    "type": "string",
    "description": "Refresh behavior"
   },
   "barcodeType": {
    "type": "string",
    "description": "Barcode type"
   },
   "orientation": {
    "type": "string",
    "description": "Orientation"
   },
   "humanReadableValue": {
    "type": "boolean",
    "description": "Human-readable value"
   },
   "hideShowEncodedReference": {
    "type": "boolean",
    "description": "Show the encoded reference"
   },
   "showPriceOnOff": {
    "type": "boolean",
    "description": "Show price on the ticket"
   }
  },
  "required": [
   "templateId"
  ]
 },
 "DigitalQrBarcodeTicketDesignerView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Digital QR & Barcode Ticket Designer displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "templateId": {
    "type": "string",
    "description": "Media template being designed"
   },
   "components": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "logo",
      "eventImage",
      "eventName",
      "ticketType",
      "customerName",
      "participantName",
      "date",
      "time",
      "venue",
      "entrance",
      "section",
      "row",
      "seat",
      "price",
      "orderReference",
      "virtualTicketId",
      "qr",
      "barcode",
      "terms",
      "instructions",
      "waiverLinkStatus",
      "sponsor",
      "customFields"
     ]
    },
    "description": "Components placed on the layout; values come from the dynamic-field library"
   },
   "qrMode": {
    "type": "string",
    "enum": [
     "staticQr",
     "dynamicQr",
     "signedQr",
     "tokenizedQr"
    ],
    "description": "QR payload profile"
   },
   "rotationBehaviorWhereSupported": {
    "type": "string",
    "description": "Rotation behavior where supported"
   },
   "size": {
    "type": "string",
    "description": "Size"
   },
   "position": {
    "type": "string",
    "description": "Position"
   },
   "quietZone": {
    "type": "string",
    "description": "Quiet zone"
   },
   "errorCorrection": {
    "type": "string",
    "enum": [
     "l",
     "m",
     "q",
     "h"
    ],
    "description": "QR error-correction level"
   },
   "expiration": {
    "type": "string",
    "description": "Expiration"
   },
   "refreshBehavior": {
    "type": "string",
    "description": "Refresh behavior"
   },
   "barcodeType": {
    "type": "string",
    "description": "Barcode type"
   },
   "orientation": {
    "type": "string",
    "description": "Orientation"
   },
   "humanReadableValue": {
    "type": "boolean",
    "description": "Human-readable value"
   },
   "hideShowEncodedReference": {
    "type": "boolean",
    "description": "Show the encoded reference"
   },
   "showPriceOnOff": {
    "type": "boolean",
    "description": "Show price on the ticket"
   }
  },
  "required": [
   "templateId"
  ]
 },
 "DynamicFieldsDataMappingContentBuilderInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table covers these fields** — the closest is access.entitlement at 3%, so this is not an update to anything the package stores today and no new table has been decided",
  "description": "**What Dynamic Fields, Data Mapping & Content Builder submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "category": {
    "type": "string",
    "enum": [
     "customer",
     "participant",
     "order",
     "virtualTicket",
     "productEvent",
     "seating",
     "commercial",
     "membership",
     "compliance",
     "credential",
     "custom"
    ],
    "description": "Field group"
   },
   "fieldKey": {
    "type": "string",
    "description": "Token used in templates, e.g. ticket.seat"
   },
   "standardField": {
    "type": "string",
    "enum": [
     "customerName",
     "customerId",
     "mobile",
     "email",
     "photo",
     "participantName",
     "dobAgeCategory",
     "participantId",
     "orderId",
     "bookingReference",
     "purchaseDate",
     "channel",
     "virtualTicketId",
     "ticketType",
     "status",
     "validity",
     "usageStatus",
     "product",
     "event",
     "performance",
     "date",
     "time",
     "venue",
     "entrance",
     "section",
     "block",
     "row",
     "seat",
     "faceValue",
     "paidPrice",
     "discount",
     "currency",
     "membershipId",
     "tier",
     "expiry",
     "waiverStatus",
     "waiverLink",
     "qr",
     "barcode",
     "credentialReference"
    ],
    "description": "Standard source field; empty for a tenant-defined custom field"
   },
   "dateFormats": {
    "type": "string",
    "description": "Date format pattern"
   },
   "timeFormat": {
    "type": "string",
    "description": "Time format pattern"
   },
   "numberFormat": {
    "type": "string",
    "description": "Number formatting"
   },
   "textTransformation": {
    "type": "string",
    "description": "Text transformation"
   },
   "characterLimit": {
    "type": "integer",
    "description": "Character limit"
   },
   "conditionalVisibility": {
    "type": "string",
    "description": "Condition under which the field shows, e.g. seat assigned"
   },
   "allowedMedia": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Media types that may display this field"
   },
   "sensitive": {
    "type": "boolean",
    "description": "Personal or sensitive data; not permitted on media by default"
   }
  },
  "required": [
   "fieldKey",
   "category"
  ]
 },
 "DynamicFieldsDataMappingContentBuilderView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Dynamic Fields, Data Mapping & Content Builder displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "category": {
    "type": "string",
    "enum": [
     "customer",
     "participant",
     "order",
     "virtualTicket",
     "productEvent",
     "seating",
     "commercial",
     "membership",
     "compliance",
     "credential",
     "custom"
    ],
    "description": "Field group"
   },
   "fieldKey": {
    "type": "string",
    "description": "Token used in templates, e.g. ticket.seat"
   },
   "standardField": {
    "type": "string",
    "enum": [
     "customerName",
     "customerId",
     "mobile",
     "email",
     "photo",
     "participantName",
     "dobAgeCategory",
     "participantId",
     "orderId",
     "bookingReference",
     "purchaseDate",
     "channel",
     "virtualTicketId",
     "ticketType",
     "status",
     "validity",
     "usageStatus",
     "product",
     "event",
     "performance",
     "date",
     "time",
     "venue",
     "entrance",
     "section",
     "block",
     "row",
     "seat",
     "faceValue",
     "paidPrice",
     "discount",
     "currency",
     "membershipId",
     "tier",
     "expiry",
     "waiverStatus",
     "waiverLink",
     "qr",
     "barcode",
     "credentialReference"
    ],
    "description": "Standard source field; empty for a tenant-defined custom field"
   },
   "dateFormats": {
    "type": "string",
    "description": "Date format pattern"
   },
   "timeFormat": {
    "type": "string",
    "description": "Time format pattern"
   },
   "numberFormat": {
    "type": "string",
    "description": "Number formatting"
   },
   "textTransformation": {
    "type": "string",
    "description": "Text transformation"
   },
   "characterLimit": {
    "type": "integer",
    "description": "Character limit"
   },
   "conditionalVisibility": {
    "type": "string",
    "description": "Condition under which the field shows, e.g. seat assigned"
   },
   "allowedMedia": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Media types that may display this field"
   },
   "sensitive": {
    "type": "boolean",
    "description": "Personal or sensitive data; not permitted on media by default"
   }
  },
  "required": [
   "fieldKey",
   "category"
  ]
 },
 "GoogleWalletPassDesignerInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Google Wallet Pass Designer submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "templateId": {
    "type": "string",
    "description": "Media template being designed"
   },
   "passClass": {
    "type": "string",
    "description": "Pass class"
   },
   "passTemplate": {
    "type": "string",
    "description": "Pass template"
   },
   "issuer": {
    "type": "string",
    "description": "Issuer"
   },
   "title": {
    "type": "string",
    "description": "Title"
   },
   "logo": {
    "type": "string",
    "description": "Logo"
   },
   "heroImageAssetsWhereApplicable": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Hero/image assets where applicable"
   },
   "eventInformation": {
    "type": "string",
    "description": "Event information"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "dateTime": {
    "type": "string",
    "description": "Field key mapped to the event date/time"
   },
   "ticketHolder": {
    "type": "string",
    "description": "Ticket holder"
   },
   "seat": {
    "type": "string",
    "description": "Seat"
   },
   "ticketType": {
    "type": "string",
    "description": "Ticket type"
   },
   "customFields": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Custom fields"
   },
   "status": {
    "type": "string",
    "description": "Status"
   },
   "links": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Links"
   },
   "additionalInformation": {
    "type": "string",
    "description": "Additional information"
   },
   "credentialEncoding": {
    "type": "string",
    "enum": [
     "qr",
     "barcode",
     "credentialTokenReference"
    ],
    "description": "How the credential is carried on the pass"
   },
   "updateTriggers": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "eventTimeChange",
      "venueChange",
      "seatReassignment",
      "ticketStatusChange",
      "otherTicketInformationChange"
     ]
    },
    "description": "Changes that push an update to issued passes"
   }
  },
  "required": [
   "templateId"
  ]
 },
 "GoogleWalletPassDesignerView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Google Wallet Pass Designer displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "templateId": {
    "type": "string",
    "description": "Media template being designed"
   },
   "passClass": {
    "type": "string",
    "description": "Pass class"
   },
   "passTemplate": {
    "type": "string",
    "description": "Pass template"
   },
   "issuer": {
    "type": "string",
    "description": "Issuer"
   },
   "title": {
    "type": "string",
    "description": "Title"
   },
   "logo": {
    "type": "string",
    "description": "Logo"
   },
   "heroImageAssetsWhereApplicable": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Hero/image assets where applicable"
   },
   "eventInformation": {
    "type": "string",
    "description": "Event information"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "dateTime": {
    "type": "string",
    "description": "Field key mapped to the event date/time"
   },
   "ticketHolder": {
    "type": "string",
    "description": "Ticket holder"
   },
   "seat": {
    "type": "string",
    "description": "Seat"
   },
   "ticketType": {
    "type": "string",
    "description": "Ticket type"
   },
   "customFields": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Custom fields"
   },
   "status": {
    "type": "string",
    "description": "Status"
   },
   "links": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Links"
   },
   "additionalInformation": {
    "type": "string",
    "description": "Additional information"
   },
   "credentialEncoding": {
    "type": "string",
    "enum": [
     "qr",
     "barcode",
     "credentialTokenReference"
    ],
    "description": "How the credential is carried on the pass"
   },
   "updateTriggers": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "eventTimeChange",
      "venueChange",
      "seatReassignment",
      "ticketStatusChange",
      "otherTicketInformationChange"
     ]
    },
    "description": "Changes that push an update to issued passes"
   }
  },
  "required": [
   "templateId"
  ]
 },
 "MultiMediaPreviewTestingApprovalPublicationInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Multi-Media Preview, Testing, Approval & Publication submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "publishMode": {
    "type": "string",
    "enum": [
     "publishNow",
     "schedule"
    ],
    "description": "Publish now or on a schedule"
   },
   "templateId": {
    "type": "string",
    "description": "Media template being published"
   },
   "validationChecks": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "dynamicFields",
      "missingFields",
      "qrReadability",
      "barcodeReadability",
      "walletConfiguration",
      "printBoundaries",
      "localization",
      "rtl",
      "branding",
      "imageResolution",
      "credentialPayload",
      "virtualTicketResolution",
      "providerConfiguration"
     ]
    },
    "description": "Pre-publication checks run"
   },
   "previewTargets": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "desktop",
      "mobile",
      "tablet",
      "printer",
      "pos",
      "wallet",
      "encoder"
     ]
    },
    "description": "Targets previewed"
   },
   "selectedBrands": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Selected Brands"
   },
   "selectedVenues": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Selected Venues"
   },
   "selectedProducts": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Selected Products"
   },
   "selectedChannels": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Selected Channels"
   },
   "controlledRollout": {
    "type": "boolean",
    "description": "Controlled rollout"
   },
   "templateVersion": {
    "type": "string",
    "description": "Version created by this publication"
   },
   "scheduledAt": {
    "type": "string",
    "format": "date-time",
    "description": "Publication time when scheduled"
   }
  },
  "required": [
   "templateId",
   "publishMode"
  ]
 },
 "MultiMediaPreviewTestingApprovalPublicationView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Multi-Media Preview, Testing, Approval & Publication displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "publishMode": {
    "type": "string",
    "enum": [
     "publishNow",
     "schedule"
    ],
    "description": "Publish now or on a schedule"
   },
   "templateId": {
    "type": "string",
    "description": "Media template being published"
   },
   "validationChecks": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "dynamicFields",
      "missingFields",
      "qrReadability",
      "barcodeReadability",
      "walletConfiguration",
      "printBoundaries",
      "localization",
      "rtl",
      "branding",
      "imageResolution",
      "credentialPayload",
      "virtualTicketResolution",
      "providerConfiguration"
     ]
    },
    "description": "Pre-publication checks run"
   },
   "previewTargets": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "desktop",
      "mobile",
      "tablet",
      "printer",
      "pos",
      "wallet",
      "encoder"
     ]
    },
    "description": "Targets previewed"
   },
   "selectedBrands": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Selected Brands"
   },
   "selectedVenues": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Selected Venues"
   },
   "selectedProducts": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Selected Products"
   },
   "selectedChannels": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Selected Channels"
   },
   "controlledRollout": {
    "type": "boolean",
    "description": "Controlled rollout"
   },
   "templateVersion": {
    "type": "string",
    "description": "Version created by this publication"
   },
   "scheduledAt": {
    "type": "string",
    "format": "date-time",
    "description": "Publication time when scheduled"
   }
  },
  "required": [
   "templateId",
   "publishMode"
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
 "PdfPrintablePosTicketDesignerInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What PDF, Printable & POS Ticket Designer submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "templateId": {
    "type": "string",
    "description": "Media template being designed"
   },
   "outputFormat": {
    "type": "string",
    "enum": [
     "pdf",
     "a4",
     "a5",
     "customDimensions",
     "posReceipt",
     "thermalTicket",
     "boxOfficeStock",
     "prePrintedStock"
    ],
    "description": "Print output this template produces"
   },
   "pageSize": {
    "type": "string",
    "description": "Page size"
   },
   "orientation": {
    "type": "string",
    "description": "Orientation"
   },
   "margins": {
    "type": "string",
    "description": "Margins"
   },
   "header": {
    "type": "string",
    "description": "Header"
   },
   "footer": {
    "type": "string",
    "description": "Footer"
   },
   "background": {
    "type": "string",
    "description": "Background"
   },
   "logo": {
    "type": "string",
    "description": "Logo"
   },
   "images": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Images"
   },
   "text": {
    "type": "string",
    "description": "Text"
   },
   "dynamicFields": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Field keys from the dynamic-field library"
   },
   "qrBarcode": {
    "type": "string",
    "description": "QR/barcode"
   },
   "terms": {
    "type": "string",
    "description": "Terms"
   },
   "perforationIndicatorsWhereApplicable": {
    "type": "string",
    "description": "Perforation indicators where applicable"
   },
   "printSafeZones": {
    "type": "string",
    "description": "Print-safe zones"
   },
   "printerProfile": {
    "type": "string",
    "description": "Printer profile"
   },
   "dpi": {
    "type": "integer",
    "description": "DPI"
   },
   "paperStockType": {
    "type": "string",
    "description": "Paper/stock type"
   },
   "thermalLayout": {
    "type": "string",
    "description": "Thermal layout"
   },
   "cutBehavior": {
    "type": "string",
    "description": "Cut behavior"
   },
   "supportedPrinterIntegration": {
    "type": "string",
    "description": "Supported printer integration"
   }
  },
  "required": [
   "templateId",
   "outputFormat"
  ]
 },
 "PdfPrintablePosTicketDesignerView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What PDF, Printable & POS Ticket Designer displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "templateId": {
    "type": "string",
    "description": "Media template being designed"
   },
   "outputFormat": {
    "type": "string",
    "enum": [
     "pdf",
     "a4",
     "a5",
     "customDimensions",
     "posReceipt",
     "thermalTicket",
     "boxOfficeStock",
     "prePrintedStock"
    ],
    "description": "Print output this template produces"
   },
   "pageSize": {
    "type": "string",
    "description": "Page size"
   },
   "orientation": {
    "type": "string",
    "description": "Orientation"
   },
   "margins": {
    "type": "string",
    "description": "Margins"
   },
   "header": {
    "type": "string",
    "description": "Header"
   },
   "footer": {
    "type": "string",
    "description": "Footer"
   },
   "background": {
    "type": "string",
    "description": "Background"
   },
   "logo": {
    "type": "string",
    "description": "Logo"
   },
   "images": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Images"
   },
   "text": {
    "type": "string",
    "description": "Text"
   },
   "dynamicFields": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Field keys from the dynamic-field library"
   },
   "qrBarcode": {
    "type": "string",
    "description": "QR/barcode"
   },
   "terms": {
    "type": "string",
    "description": "Terms"
   },
   "perforationIndicatorsWhereApplicable": {
    "type": "string",
    "description": "Perforation indicators where applicable"
   },
   "printSafeZones": {
    "type": "string",
    "description": "Print-safe zones"
   },
   "printerProfile": {
    "type": "string",
    "description": "Printer profile"
   },
   "dpi": {
    "type": "integer",
    "description": "DPI"
   },
   "paperStockType": {
    "type": "string",
    "description": "Paper/stock type"
   },
   "thermalLayout": {
    "type": "string",
    "description": "Thermal layout"
   },
   "cutBehavior": {
    "type": "string",
    "description": "Cut behavior"
   },
   "supportedPrinterIntegration": {
    "type": "string",
    "description": "Supported printer integration"
   }
  },
  "required": [
   "templateId",
   "outputFormat"
  ]
 },
 "RfidNfcCardWristbandMediaDesignerInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What RFID, NFC, Card & Wristband Media Designer submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "templateId": {
    "type": "string",
    "description": "Media template being designed"
   },
   "mediaKind": {
    "type": "string",
    "enum": [
     "rfidCard",
     "rfidWristband",
     "nfcCard",
     "nfcWristband",
     "membershipCard",
     "staffGuestCard",
     "customWearable"
    ],
    "description": "Physical medium"
   },
   "reusability": {
    "type": "string",
    "enum": [
     "disposable",
     "reusable"
    ],
    "description": "Disposable or reusable medium"
   },
   "printed": {
    "type": "boolean",
    "description": "Printed"
   },
   "encoded": {
    "type": "boolean",
    "description": "Encoded"
   },
   "colorCategory": {
    "type": "string",
    "description": "Color/category"
   },
   "sizeWhereApplicable": {
    "type": "string",
    "description": "Size where applicable"
   },
   "activationAtCollection": {
    "type": "boolean",
    "description": "Activation at collection"
   },
   "depositReferenceWhereApplicable": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Deposit/reference where applicable"
   },
   "mediaDimensions": {
    "type": "string",
    "description": "Media dimensions"
   },
   "front": {
    "type": "string",
    "description": "Front"
   },
   "back": {
    "type": "string",
    "description": "Back"
   },
   "printableArea": {
    "type": "string",
    "description": "Printable area"
   },
   "logo": {
    "type": "string",
    "description": "Logo"
   },
   "printedFields": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "customerName",
      "photo",
      "membershipTier",
      "expiry",
      "serialNumber",
      "qrBarcode"
     ]
    },
    "description": "Personal and reference fields printed on the medium"
   },
   "customArtwork": {
    "type": "string",
    "description": "Custom artwork"
   },
   "sponsorVenueBranding": {
    "type": "string",
    "description": "Sponsor/venue branding"
   },
   "rfidNfcTechnology": {
    "type": "string",
    "description": "RFID/NFC technology"
   },
   "chipProfile": {
    "type": "string",
    "description": "Chip/profile"
   },
   "uidReferenceHandling": {
    "type": "string",
    "description": "UID/reference handling"
   },
   "encodingProfile": {
    "type": "string",
    "description": "Encoding profile"
   },
   "provider": {
    "type": "string",
    "description": "Provider"
   },
   "readerCompatibility": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Reader compatibility"
   },
   "printerEncoderIntegration": {
    "type": "string",
    "description": "Printer/encoder integration"
   }
  },
  "required": [
   "templateId",
   "mediaKind"
  ]
 },
 "RfidNfcCardWristbandMediaDesignerView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What RFID, NFC, Card & Wristband Media Designer displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "templateId": {
    "type": "string",
    "description": "Media template being designed"
   },
   "mediaKind": {
    "type": "string",
    "enum": [
     "rfidCard",
     "rfidWristband",
     "nfcCard",
     "nfcWristband",
     "membershipCard",
     "staffGuestCard",
     "customWearable"
    ],
    "description": "Physical medium"
   },
   "reusability": {
    "type": "string",
    "enum": [
     "disposable",
     "reusable"
    ],
    "description": "Disposable or reusable medium"
   },
   "printed": {
    "type": "boolean",
    "description": "Printed"
   },
   "encoded": {
    "type": "boolean",
    "description": "Encoded"
   },
   "colorCategory": {
    "type": "string",
    "description": "Color/category"
   },
   "sizeWhereApplicable": {
    "type": "string",
    "description": "Size where applicable"
   },
   "activationAtCollection": {
    "type": "boolean",
    "description": "Activation at collection"
   },
   "depositReferenceWhereApplicable": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Deposit/reference where applicable"
   },
   "mediaDimensions": {
    "type": "string",
    "description": "Media dimensions"
   },
   "front": {
    "type": "string",
    "description": "Front"
   },
   "back": {
    "type": "string",
    "description": "Back"
   },
   "printableArea": {
    "type": "string",
    "description": "Printable area"
   },
   "logo": {
    "type": "string",
    "description": "Logo"
   },
   "printedFields": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "customerName",
      "photo",
      "membershipTier",
      "expiry",
      "serialNumber",
      "qrBarcode"
     ]
    },
    "description": "Personal and reference fields printed on the medium"
   },
   "customArtwork": {
    "type": "string",
    "description": "Custom artwork"
   },
   "sponsorVenueBranding": {
    "type": "string",
    "description": "Sponsor/venue branding"
   },
   "rfidNfcTechnology": {
    "type": "string",
    "description": "RFID/NFC technology"
   },
   "chipProfile": {
    "type": "string",
    "description": "Chip/profile"
   },
   "uidReferenceHandling": {
    "type": "string",
    "description": "UID/reference handling"
   },
   "encodingProfile": {
    "type": "string",
    "description": "Encoding profile"
   },
   "provider": {
    "type": "string",
    "description": "Provider"
   },
   "readerCompatibility": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Reader compatibility"
   },
   "printerEncoderIntegration": {
    "type": "string",
    "description": "Printer/encoder integration"
   }
  },
  "required": [
   "templateId",
   "mediaKind"
  ]
 },
 "TicketProof": {
  "type": "object",
  "x-ticvai-persistence": "none — rendered on request, nothing is stored",
  "description": "A sample ticket from a template, **marked as a proof on the artefact itself** so it cannot be presented at a gate.",
  "required": [
   "templateId",
   "mediaType",
   "contentRef"
  ],
  "properties": {
   "templateId": {
    "type": "string",
    "format": "uuid"
   },
   "mediaType": {
    "type": "string",
    "enum": [
     "thermalTicket",
     "a4Pdf",
     "wristband",
     "rfidCard",
     "walletPass",
     "qrOnly",
     "sms"
    ]
   },
   "locale": {
    "type": "string",
    "nullable": true
   },
   "contentRef": {
    "type": "string",
    "format": "uri",
    "description": "Where the rendered proof can be fetched or sent to the printer from."
   }
  }
 },
 "TicketTemplate": {
  "type": "object",
  "x-ticvai-persistence": "orders.ticket_template + orders.ticket_template_channel",
  "description": "BL-102. **A venue changing its ticket artwork had no path that was not a code change.**\n2.16.6 asks to print a proof without processing a sale — the equivalent of `white-label.createPreview`, and the same reason: **artwork is checked by looking at it, and the only way to look at it was to sell something.**\n",
  "required": [
   "id",
   "name",
   "mediaType",
   "isActive"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "name": {
    "type": "string"
   },
   "isRecyclable": {
    "type": "boolean",
    "default": false,
    "description": "BL-103. **An RFID wristband handed back at the exit is stock, not waste** — and nothing released it, so a venue reissuing one had a card serving two entitlements.\n**Replacement disables the previous medium automatically**, following the F23 rule: a guest issued a replacement wristband must not walk in on the old one, and relying on somebody remembering to blacklist it is how they do.\n"
   },
   "recycleAfterDays": {
    "type": "integer",
    "nullable": true,
    "description": "**A quarantine before reissue.** A wristband returned today and reissued tomorrow to a different guest is a support call waiting to happen when the first guest's app still shows it.\n"
   },
   "mediaType": {
    "type": "string",
    "enum": [
     "thermalTicket",
     "a4Pdf",
     "wristband",
     "rfidCard",
     "walletPass",
     "qrOnly",
     "sms"
    ]
   },
   "appliesToProductKinds": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "appliesToChannels": {
    "type": "array",
    "items": {
     "$ref": "../shared/common.yaml#/components/schemas/SalesChannel"
    }
   },
   "selectionPriority": {
    "type": "integer",
    "default": 100,
    "description": "2.16.x. **Automatic media-type selection**, which was absent — a kiosk with no printer and a guest with no smartphone need different answers, and neither should be chosen by the caller.\n"
   },
   "layoutRef": {
    "type": "string"
   },
   "localeVariants": {
    "type": "object",
    "additionalProperties": {
     "type": "string"
    }
   },
   "isActive": {
    "type": "boolean"
   }
  }
 },
 "TicketTemplateImportInput": {
  "type": "object",
  "x-ticvai-persistence": "none — request only",
  "description": "What `importTicketTemplate` takes (decided 29 September, readiness close-out).",
  "required": [
   "format",
   "fileRef",
   "name"
  ],
  "properties": {
   "format": {
    "type": "string",
    "maxLength": 30,
    "description": "The definition format of the file. One the service does not read is a 422."
   },
   "fileRef": {
    "type": "string",
    "format": "uuid",
    "description": "The uploaded definition file."
   },
   "name": {
    "type": "string",
    "maxLength": 120
   }
  }
 },
 "TicketTemplateRequest": {
  "type": "object",
  "description": "Request only; persisted as `TicketTemplate`. On update every field is optional and absent means unchanged. On create, `name` and `mediaType` are required and the operation enforces it.",
  "properties": {
   "name": {
    "type": "string",
    "maxLength": 200
   },
   "mediaType": {
    "type": "string",
    "enum": [
     "thermalTicket",
     "a4Pdf",
     "wristband",
     "rfidCard",
     "walletPass",
     "qrOnly",
     "sms"
    ]
   },
   "isRecyclable": {
    "type": "boolean"
   },
   "recycleAfterDays": {
    "type": "integer",
    "minimum": 0,
    "nullable": true
   },
   "appliesToProductKinds": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "appliesToChannels": {
    "type": "array",
    "items": {
     "$ref": "../shared/common.yaml#/components/schemas/SalesChannel"
    }
   },
   "selectionPriority": {
    "type": "integer"
   },
   "layoutRef": {
    "type": "string",
    "description": "The artwork, as a media-asset reference."
   },
   "localeVariants": {
    "type": "object",
    "additionalProperties": {
     "type": "string"
    }
   },
   "isActive": {
    "type": "boolean"
   }
  }
 }
}
```
