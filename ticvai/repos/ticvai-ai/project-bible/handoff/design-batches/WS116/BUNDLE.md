# WS116 — AI Configuration Assistant board 1

**10 screens · 8 operations · 12 schemas · 1 permissions**

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

- **Every control that can be refused must be gated.** 1 permissions apply here:
  `AI_USE`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `ADM-469` | AI Configuration Home & Start | listDetail | 3 | 0 | — |
| `ADM-470` | Setup Type & Business Intent Discovery | configEditor | 4 | 0 | — |
| `ADM-471` | Venue & Business Model Discovery | configEditor | 2 | 0 | — |
| `ADM-472` | Guided Question & Answer Workspace | listDetail | 2 | 0 | — |
| `ADM-473` | Product & Admission Model Discovery | listDetail | 2 | 0 | — |
| `ADM-474` | Operational Requirement Discovery | listDetail | 2 | 0 | — |
| `ADM-475` | Commercial Requirement Discovery | listDetail | 2 | 0 | — |
| `ADM-476` | Required, Recommended & Optional Decisions | configEditor | 2 | 0 | — |
| `ADM-477` | Missing Information & Clarification Center | commandCentre | 5 | 0 | — |
| `ADM-478` | Configuration Blueprint & Dependency Map | listDetail | 2 | 0 | — |

## Thin screens in this batch

**ADM-472, ADM-473, ADM-474, ADM-475, ADM-478 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "ADM-469",
  "name": "AI Configuration Home & Start",
  "module": "Platform",
  "requiresModule": "ai",
  "wave": 3,
  "source": {
   "pack": "AI_Configuration_Assistant_Reference.pdf",
   "board": "1",
   "number": "1",
   "page": 4
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/ai-configuration-home-start-adm-469",
   "component": "apps/ticvai-web/src/routes/platform/AiConfigurationHomeStart.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-002"
   ],
   "exitTo": [
    "ADM-002",
    "ADM-470",
    "ADM-471",
    "ADM-472",
    "ADM-473",
    "ADM-474",
    "ADM-475",
    "ADM-476",
    "ADM-477",
    "ADM-478"
   ],
   "transitions": [
    {
     "to": "ADM-002",
     "trigger": "Back to Platform Dashboard",
     "provenance": "structural — pack board 1 wiring, 19 September 2026",
     "back": true
    },
    {
     "to": "ADM-470",
     "trigger": "Setup Type & Business Intent Discovery",
     "provenance": "structural — pack board 1 wiring, 19 September 2026"
    },
    {
     "to": "ADM-471",
     "trigger": "Venue & Business Model Discovery",
     "provenance": "structural — pack board 1 wiring, 19 September 2026"
    },
    {
     "to": "ADM-472",
     "trigger": "Guided Question & Answer Workspace",
     "provenance": "structural — pack board 1 wiring, 19 September 2026"
    },
    {
     "to": "ADM-473",
     "trigger": "Product & Admission Model Discovery",
     "provenance": "structural — pack board 1 wiring, 19 September 2026"
    },
    {
     "to": "ADM-474",
     "trigger": "Operational Requirement Discovery",
     "provenance": "structural — pack board 1 wiring, 19 September 2026"
    },
    {
     "to": "ADM-475",
     "trigger": "Commercial Requirement Discovery",
     "provenance": "structural — pack board 1 wiring, 19 September 2026"
    },
    {
     "to": "ADM-476",
     "trigger": "Required, Recommended & Optional Decisions",
     "provenance": "structural — pack board 1 wiring, 19 September 2026"
    },
    {
     "to": "ADM-477",
     "trigger": "Missing Information & Clarification Center",
     "provenance": "structural — pack board 1 wiring, 19 September 2026"
    },
    {
     "to": "ADM-478",
     "trigger": "Configuration Blueprint & Dependency Map",
     "provenance": "structural — pack board 1 wiring, 19 September 2026"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Show intelligent cards such as; Show) and no metric row",
  "purpose": "Provide one intelligent starting point for creating or modifying TICVAI configuration through AI.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 4 actions on this screen and the screen declares 0 operations.** Unserved: Create New Configuration, Modify Existing Configuration, Extend Existing Configuration, Clone & Adapt Existing Setup. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack AI_Configuration_Assistant_Reference.pdf, page 4 §Allow"
   },
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack AI_Configuration_Assistant_Reference.pdf, page 4 §Show intelligent cards such as"
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
       "label": "Every home start",
       "columns": [
        "Museum",
        "Theme Park",
        "Water Park",
        "Zoo",
        "Aquarium",
        "Theatre",
        "Stadium",
        "Indoor Attraction",
        "Family Entertainment Center",
        "Festival",
        "Conference",
        "Temporary Event",
        "Start from Scratch",
        "Session Type Progress Last Activity Status",
        "Summer Festival Event 100% Yesterday Blueprint Ready"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 4 §Show intelligent cards such as"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected home start",
       "bindsTo": null,
       "columns": [
        "Museum",
        "Theme Park",
        "Water Park",
        "Zoo",
        "Aquarium",
        "Theatre",
        "Stadium",
        "Indoor Attraction",
        "Family Entertainment Center",
        "Festival",
        "Conference",
        "Temporary Event",
        "Start from Scratch",
        "Session Type Progress Last Activity Status",
        "Summer Festival Event 100% Yesterday Blueprint Ready"
       ],
       "notes": "The pack groups this record's detail under its own headings: “The screen should immediately answer”, “Subtitle”, “Large conversational input”.",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 4 §Show intelligent cards such as"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Create New Configuration",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 4 §Allow"
      },
      {
       "kind": "secondaryButton",
       "label": "Modify Existing Configuration",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 4 §Allow"
      },
      {
       "kind": "secondaryButton",
       "label": "Extend Existing Configuration",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 4 §Allow"
      },
      {
       "kind": "secondaryButton",
       "label": "Clone & Adapt Existing Setup",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 4 §Allow"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The home start list.",
   "error": "Could not load. Names which read failed and leaves the home start untouched.",
   "emptyFirstRun": "No home start yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the home start are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "startConfigurationSession",
    "contract": "ai",
    "purpose": "Start the configuration assistant",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "listConfigurationSessions",
    "contract": "ai",
    "purpose": "Configuration-assistant sessions",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "attachConfigurationSource",
    "contract": "ai",
    "purpose": "Attach an uploaded brief, brochure, price list, spreadsheet or brand asset to seed the session",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "Museum",
    "Theme Park",
    "Water Park",
    "Zoo",
    "Aquarium",
    "Theatre"
   ],
   "params": [
    {
     "name": "sessionId",
     "from": "session"
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-469",
   "workshopBoard": "wireframes/WS09 AI Configuration Assistant Board 1.dc.html#adm-469"
  },
  "apisNote": "Regenerated 9 September 2026 from AI_Configuration_Assistant_Reference.pdf page 4. 0 of 15 labels bound to a contract property; 19 of 34 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-470",
  "name": "Setup Type & Business Intent Discovery",
  "module": "Platform",
  "requiresModule": "ai",
  "wave": 3,
  "source": {
   "pack": "AI_Configuration_Assistant_Reference.pdf",
   "board": "1",
   "number": "2",
   "page": 5
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/setup-type-business-intent-discovery-adm-470",
   "component": "apps/ticvai-web/src/routes/platform/SetupTypeBusinessIntentDiscovery.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-469"
   ],
   "exitTo": [
    "ADM-469"
   ],
   "transitions": [
    {
     "to": "ADM-469",
     "trigger": "Back to AI Configuration Home & Start",
     "provenance": "structural — pack board 1 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Detected Setup; Likely Configuration Areas) and no display directory — it is settings, not a population",
  "purpose": "Understand what the administrator is actually trying to accomplish before asking detailed configuration questions. This is the first AI interview screen.",
  "gaps": [
   {
    "operation": null,
    "why": "**Setup Type & Business Intent Discovery declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write operations are missing or this screen is a view of something another screen builds.",
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
       "label": "Action: Create",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 5 §Detected Setup"
      },
      {
       "kind": "selectField",
       "label": "Object: Venue",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 5 §Detected Setup"
      },
      {
       "kind": "selectField",
       "label": "Venue Type: Museum",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 5 §Detected Setup"
      },
      {
       "kind": "selectField",
       "label": "Organization: Existing",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 5 §Detected Setup"
      },
      {
       "kind": "selectField",
       "label": "Location: Dubai",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 5 §Detected Setup"
      },
      {
       "kind": "selectField",
       "label": "Operation Type: Permanent",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 5 §Detected Setup"
      },
      {
       "kind": "selectField",
       "label": "Confidence: 96%",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 5 §Detected Setup"
      },
      {
       "kind": "selectField",
       "label": "✓ Venue",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 5 §Likely Configuration Areas"
      },
      {
       "kind": "selectField",
       "label": "✓ Products",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 5 §Likely Configuration Areas"
      },
      {
       "kind": "selectField",
       "label": "✓ Schedule",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 5 §Likely Configuration Areas"
      },
      {
       "kind": "selectField",
       "label": "✓ Capacity",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 5 §Likely Configuration Areas"
      },
      {
       "kind": "selectField",
       "label": "✓ Pricing",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 5 §Likely Configuration Areas"
      },
      {
       "kind": "selectField",
       "label": "✓ Sales Channels",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 5 §Likely Configuration Areas"
      },
      {
       "kind": "selectField",
       "label": "✓ Ticket Media",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 5 §Likely Configuration Areas"
      },
      {
       "kind": "selectField",
       "label": "✓ Access",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 5 §Likely Configuration Areas"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The type business intent configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the type business intent untouched.",
   "emptyFirstRun": "No type business intent configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "startConfigurationSession",
    "contract": "ai",
    "purpose": "Start the configuration assistant",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "answerConfigurationQuestion",
    "contract": "ai",
    "purpose": "Answer the current question",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "attachConfigurationSource",
    "contract": "ai",
    "purpose": "Attach an uploaded brief, brochure, price list, spreadsheet or brand asset to seed the session",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "listConfigurationSources",
    "contract": "ai",
    "purpose": "Attached documents with extraction status and what they could not read",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-470",
   "workshopBoard": "wireframes/WS09 AI Configuration Assistant Board 1.dc.html#adm-470"
  },
  "apisNote": "Regenerated 9 September 2026 from AI_Configuration_Assistant_Reference.pdf page 5. 0 of 0 labels bound to a contract property; 15 of 46 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "sessionId",
     "from": "session"
    }
   ]
  },
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
  "id": "ADM-471",
  "name": "Venue & Business Model Discovery",
  "module": "Platform",
  "requiresModule": "ai",
  "wave": 3,
  "source": {
   "pack": "AI_Configuration_Assistant_Reference.pdf",
   "board": "1",
   "number": "3",
   "page": 7
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/venue-business-model-discovery-adm-471",
   "component": "apps/ticvai-web/src/routes/platform/VenueBusinessModelDiscovery.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-469"
   ],
   "exitTo": [
    "ADM-469"
   ],
   "transitions": [
    {
     "to": "ADM-469",
     "trigger": "Back to AI Configuration Home & Start",
     "provenance": "structural — pack board 1 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Capture as relevant) and no display directory — it is settings, not a population",
  "purpose": "Understand how the business operates so TICVAI can determine which configuration branches are relevant.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 1 actions on this screen and the screen declares 0 operations.** Unserved: Confirm | Edit Understanding | Continue. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack AI_Configuration_Assistant_Reference.pdf, page 7 §Actions"
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
       "label": "Venue Name",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 7 §Capture as relevant"
      },
      {
       "kind": "selectField",
       "label": "Venue Type",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 7 §Capture as relevant"
      },
      {
       "kind": "selectField",
       "label": "Country",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 7 §Capture as relevant"
      },
      {
       "kind": "selectField",
       "label": "City",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 7 §Capture as relevant"
      },
      {
       "kind": "selectField",
       "label": "Time Zone",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 7 §Capture as relevant"
      },
      {
       "kind": "selectField",
       "label": "Currency",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 7 §Capture as relevant"
      },
      {
       "kind": "selectField",
       "label": "Operating Model",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 7 §Capture as relevant"
      },
      {
       "kind": "textField",
       "label": "Permanent / Seasonal / Temporary",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 7 §Capture as relevant"
      },
      {
       "kind": "textField",
       "label": "Indoor / Outdoor / Mixed",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 7 §Capture as relevant"
      },
      {
       "kind": "selectField",
       "label": "Number of Locations",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 7 §Capture as relevant"
      },
      {
       "kind": "textField",
       "label": "Number of Attractions / Experiences",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 7 §Capture as relevant"
      },
      {
       "kind": "selectField",
       "label": "Business Model Discovery",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 7 §Capture as relevant"
      },
      {
       "kind": "selectField",
       "label": "General Admission",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 7 §Capture as relevant"
      },
      {
       "kind": "selectField",
       "label": "Dated Admission",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 7 §Capture as relevant"
      },
      {
       "kind": "selectField",
       "label": "Open-Dated Admission",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 7 §Capture as relevant"
      },
      {
       "kind": "selectField",
       "label": "Timeslot Admission",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 7 §Capture as relevant"
      },
      {
       "kind": "selectField",
       "label": "Assigned Seating",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 7 §Capture as relevant"
      },
      {
       "kind": "selectField",
       "label": "Multi-Day Admission",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 7 §Capture as relevant"
      },
      {
       "kind": "selectField",
       "label": "Membership",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 7 §Capture as relevant"
      },
      {
       "kind": "selectField",
       "label": "Subscription",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 7 §Capture as relevant"
      },
      {
       "kind": "selectField",
       "label": "Pass",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 7 §Capture as relevant"
      },
      {
       "kind": "selectField",
       "label": "Attraction / Ride-Based",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 7 §Capture as relevant"
      },
      {
       "kind": "selectField",
       "label": "Mixed Model",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 7 §Capture as relevant"
      },
      {
       "kind": "selectField",
       "label": "Conditional Logic",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 7 §Capture as relevant"
      },
      {
       "kind": "selectField",
       "label": "Venue = Theatre",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 7 §Capture as relevant"
      },
      {
       "kind": "selectField",
       "label": "Performances",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 7 §Capture as relevant"
      },
      {
       "kind": "selectField",
       "label": "Seat Map",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 7 §Capture as relevant"
      },
      {
       "kind": "selectField",
       "label": "Sections",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 7 §Capture as relevant"
      },
      {
       "kind": "selectField",
       "label": "Price Categories",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 7 §Capture as relevant"
      },
      {
       "kind": "selectField",
       "label": "Show Schedule",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 7 §Capture as relevant"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Confirm | Edit Understanding | Continue",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 7 §Actions"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The venue business model configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the venue business model untouched.",
   "emptyFirstRun": "No venue business model configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "answerConfigurationQuestion",
    "contract": "ai",
    "purpose": "Answer the current question",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "getConfigurationBlueprint",
    "contract": "ai",
    "purpose": "The blueprint so far",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-471",
   "workshopBoard": "wireframes/WS09 AI Configuration Assistant Board 1.dc.html#adm-471"
  },
  "apisNote": "Regenerated 9 September 2026 from AI_Configuration_Assistant_Reference.pdf page 7. 0 of 0 labels bound to a contract property; 47 of 65 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "sessionId",
     "from": "session"
    }
   ]
  },
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
  "id": "ADM-472",
  "name": "Guided Question & Answer Workspace",
  "module": "Platform",
  "requiresModule": "ai",
  "wave": 3,
  "source": {
   "pack": "AI_Configuration_Assistant_Reference.pdf",
   "board": "1",
   "number": "4",
   "page": 9
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/guided-question-answer-workspace-adm-472",
   "component": "apps/ticvai-web/src/routes/platform/GuidedQuestionAnswerWorkspace.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-469"
   ],
   "exitTo": [
    "ADM-469"
   ],
   "transitions": [
    {
     "to": "ADM-469",
     "trigger": "Back to AI Configuration Home & Start",
     "provenance": "structural — pack board 1 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Provide the main adaptive AI interview workspace. This is the core screen of Board 1. It should feel conversational but remain structured and controlled.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack AI_Configuration_Assistant_Reference.pdf, page 9"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack AI_Configuration_Assistant_Reference.pdf, page 9"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "answerConfigurationQuestion",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "detailPanel",
       "derived": true,
       "impliedBy": "getConfigurationBlueprint",
       "notes": "One record, read-only."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "answerConfigurationQuestion"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The guided question answer list.",
   "error": "Could not load. Names which read failed and leaves the guided question answer untouched.",
   "emptyFirstRun": "No guided question answer yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the guided question answer are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "answerConfigurationQuestion",
    "contract": "ai",
    "purpose": "Answer the current question",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "getConfigurationBlueprint",
    "contract": "ai",
    "purpose": "The blueprint so far",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-472",
   "workshopBoard": "wireframes/WS09 AI Configuration Assistant Board 1.dc.html#adm-472"
  },
  "apisNote": "Regenerated 9 September 2026 from AI_Configuration_Assistant_Reference.pdf page 9. 0 of 0 labels bound to a contract property; 0 of 54 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "sessionId",
     "from": "session"
    }
   ]
  },
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
  "id": "ADM-473",
  "name": "Product & Admission Model Discovery",
  "module": "Platform",
  "requiresModule": "ai",
  "wave": 3,
  "source": {
   "pack": "AI_Configuration_Assistant_Reference.pdf",
   "board": "1",
   "number": "5",
   "page": 10
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/product-admission-model-discovery-adm-473",
   "component": "apps/ticvai-web/src/routes/platform/ProductAdmissionModelDiscovery.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-469"
   ],
   "exitTo": [
    "ADM-469"
   ],
   "transitions": [
    {
     "to": "ADM-469",
     "trigger": "Back to AI Configuration Home & Start",
     "provenance": "structural — pack board 1 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Determine what the venue sells and how each product provides admission or entitlement.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack AI_Configuration_Assistant_Reference.pdf, page 10"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack AI_Configuration_Assistant_Reference.pdf, page 10"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "answerConfigurationQuestion",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "detailPanel",
       "derived": true,
       "impliedBy": "getConfigurationBlueprint",
       "notes": "One record, read-only."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "answerConfigurationQuestion"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The product admission model list.",
   "error": "Could not load. Names which read failed and leaves the product admission model untouched.",
   "emptyFirstRun": "No product admission model yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the product admission model are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "answerConfigurationQuestion",
    "contract": "ai",
    "purpose": "Answer the current question",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "getConfigurationBlueprint",
    "contract": "ai",
    "purpose": "The blueprint so far",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-473",
   "workshopBoard": "wireframes/WS09 AI Configuration Assistant Board 1.dc.html#adm-473"
  },
  "apisNote": "Regenerated 9 September 2026 from AI_Configuration_Assistant_Reference.pdf page 10. 0 of 0 labels bound to a contract property; 0 of 51 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "sessionId",
     "from": "session"
    }
   ]
  },
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
  "id": "ADM-474",
  "name": "Operational Requirement Discovery",
  "module": "Platform",
  "requiresModule": "ai",
  "wave": 3,
  "source": {
   "pack": "AI_Configuration_Assistant_Reference.pdf",
   "board": "1",
   "number": "6",
   "page": 12
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/operational-requirement-discovery-adm-474",
   "component": "apps/ticvai-web/src/routes/platform/OperationalRequirementDiscovery.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-469"
   ],
   "exitTo": [
    "ADM-469"
   ],
   "transitions": [
    {
     "to": "ADM-469",
     "trigger": "Back to AI Configuration Home & Start",
     "provenance": "structural — pack board 1 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Understand the operational rules needed to deliver the configured products.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 1 actions on this screen and the screen declares 0 operations.** Unserved: Confirm Operations | Add Requirement | Continue. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack AI_Configuration_Assistant_Reference.pdf, page 12 §Actions"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack AI_Configuration_Assistant_Reference.pdf, page 12"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack AI_Configuration_Assistant_Reference.pdf, page 12"
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
       "label": "Confirm Operations | Add Requirement | Continue",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 12 §Actions"
      }
     ]
    },
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "detailPanel",
       "derived": true,
       "impliedBy": "getConfigurationBlueprint",
       "notes": "One record, read-only."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "answerConfigurationQuestion"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The operational requirement discovery list.",
   "error": "Could not load. Names which read failed and leaves the operational requirement discovery untouched.",
   "emptyFirstRun": "No operational requirement discovery yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the operational requirement discovery are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "answerConfigurationQuestion",
    "contract": "ai",
    "purpose": "Answer the current question",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "getConfigurationBlueprint",
    "contract": "ai",
    "purpose": "The blueprint so far",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-474",
   "workshopBoard": "wireframes/WS09 AI Configuration Assistant Board 1.dc.html#adm-474"
  },
  "apisNote": "Regenerated 9 September 2026 from AI_Configuration_Assistant_Reference.pdf page 12. 0 of 0 labels bound to a contract property; 1 of 47 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "sessionId",
     "from": "session"
    }
   ]
  },
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
  "id": "ADM-475",
  "name": "Commercial Requirement Discovery",
  "module": "Platform",
  "requiresModule": "ai",
  "wave": 3,
  "source": {
   "pack": "AI_Configuration_Assistant_Reference.pdf",
   "board": "1",
   "number": "7",
   "page": 13
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/commercial-requirement-discovery-adm-475",
   "component": "apps/ticvai-web/src/routes/platform/CommercialRequirementDiscovery.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-469"
   ],
   "exitTo": [
    "ADM-469"
   ],
   "transitions": [
    {
     "to": "ADM-469",
     "trigger": "Back to AI Configuration Home & Start",
     "provenance": "structural — pack board 1 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Understand how the venue intends to sell and commercially manage its products without actually configuring pricing yet.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack AI_Configuration_Assistant_Reference.pdf, page 13"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack AI_Configuration_Assistant_Reference.pdf, page 13"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "answerConfigurationQuestion",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "detailPanel",
       "derived": true,
       "impliedBy": "getConfigurationBlueprint",
       "notes": "One record, read-only."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "answerConfigurationQuestion"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The commercial requirement discovery list.",
   "error": "Could not load. Names which read failed and leaves the commercial requirement discovery untouched.",
   "emptyFirstRun": "No commercial requirement discovery yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the commercial requirement discovery are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "answerConfigurationQuestion",
    "contract": "ai",
    "purpose": "Answer the current question",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "getConfigurationBlueprint",
    "contract": "ai",
    "purpose": "The blueprint so far",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-475",
   "workshopBoard": "wireframes/WS09 AI Configuration Assistant Board 1.dc.html#adm-475"
  },
  "apisNote": "Regenerated 9 September 2026 from AI_Configuration_Assistant_Reference.pdf page 13. 0 of 0 labels bound to a contract property; 0 of 45 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "sessionId",
     "from": "session"
    }
   ]
  },
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
  "id": "ADM-476",
  "name": "Required, Recommended & Optional Decisions",
  "module": "Platform",
  "requiresModule": "ai",
  "wave": 3,
  "source": {
   "pack": "AI_Configuration_Assistant_Reference.pdf",
   "board": "1",
   "number": "8",
   "page": 14
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/required-recommended-optional-decisions-adm-476",
   "component": "apps/ticvai-web/src/routes/platform/RequiredRecommendedOptionalDecisions.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-469"
   ],
   "exitTo": [
    "ADM-469"
   ],
   "transitions": [
    {
     "to": "ADM-469",
     "trigger": "Back to AI Configuration Home & Start",
     "provenance": "structural — pack board 1 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Options) and no display directory — it is settings, not a population",
  "purpose": "Prevent the administrator from forgetting important configuration while also preventing unnecessary questions from blocking setup. This screen is fundamental to making the AI genuinely useful.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Configure Now",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 14 §Options"
      },
      {
       "kind": "selectField",
       "label": "Use Recommended Policy",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 14 §Options"
      },
      {
       "kind": "selectField",
       "label": "Decide Later",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 14 §Options"
      },
      {
       "kind": "selectField",
       "label": "Required Rule",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 14 §Options"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The required recommended optional configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the required recommended optional untouched.",
   "emptyFirstRun": "No required recommended optional configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "getConfigurationBlueprint",
    "contract": "ai",
    "purpose": "The blueprint so far",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "decideBlueprintRecommendation",
    "contract": "ai",
    "purpose": "Accept, modify, reject or defer a blueprint decision",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-476",
   "workshopBoard": "wireframes/WS09 AI Configuration Assistant Board 1.dc.html#adm-476"
  },
  "apisNote": "Regenerated 9 September 2026 from AI_Configuration_Assistant_Reference.pdf page 14. 0 of 0 labels bound to a contract property; 4 of 40 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "decisionKey",
     "from": "navigation"
    },
    {
     "name": "sessionId",
     "from": "session"
    }
   ]
  },
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
  "id": "ADM-477",
  "name": "Missing Information & Clarification Center",
  "module": "Platform",
  "requiresModule": "ai",
  "wave": 3,
  "source": {
   "pack": "AI_Configuration_Assistant_Reference.pdf",
   "board": "1",
   "number": "9",
   "page": 16
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/missing-information-clarification-center-adm-477",
   "component": "apps/ticvai-web/src/routes/platform/MissingInformationClarificationCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-469"
   ],
   "exitTo": [
    "ADM-469"
   ],
   "transitions": [
    {
     "to": "ADM-469",
     "trigger": "Back to AI Configuration Home & Start",
     "provenance": "structural — pack board 1 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen a metric directory (§Header KPIs) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's",
  "purpose": "Allow AI to identify incomplete, contradictory, ambiguous, or logically inconsistent requirements before producing the final blueprint.",
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Required Missing",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 16 §Header KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Clarifications Needed",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 16 §Header KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Conflicts",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 16 §Header KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Warnings",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 16 §Header KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Recommendations",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 16 §Header KPIs"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The missing information clarification list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the missing information clarification untouched.",
   "emptyFirstRun": "No missing information clarification yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the missing information clarification are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "answerConfigurationQuestion",
    "contract": "ai",
    "purpose": "Answer the current question",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "getConfigurationBlueprint",
    "contract": "ai",
    "purpose": "The blueprint so far",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "decideBlueprintRecommendation",
    "contract": "ai",
    "purpose": "Accept, modify, reject or defer a blueprint decision",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "attachConfigurationSource",
    "contract": "ai",
    "purpose": "Attach an uploaded brief, brochure, price list, spreadsheet or brand asset to seed the session",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "listConfigurationSources",
    "contract": "ai",
    "purpose": "Attached documents with extraction status and what they could not read",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-477",
   "workshopBoard": "wireframes/WS09 AI Configuration Assistant Board 1.dc.html#adm-477"
  },
  "apisNote": "Regenerated 9 September 2026 from AI_Configuration_Assistant_Reference.pdf page 16. 0 of 0 labels bound to a contract property; 5 of 26 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "decisionKey",
     "from": "navigation"
    },
    {
     "name": "sessionId",
     "from": "session"
    }
   ]
  },
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
  "id": "ADM-478",
  "name": "Configuration Blueprint & Dependency Map",
  "module": "Platform",
  "requiresModule": "ai",
  "wave": 3,
  "source": {
   "pack": "AI_Configuration_Assistant_Reference.pdf",
   "board": "1",
   "number": "10",
   "page": 17
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/configuration-blueprint-dependency-map-adm-478",
   "component": "apps/ticvai-web/src/routes/platform/ConfigurationBlueprintDependencyMap.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-469"
   ],
   "exitTo": [
    "ADM-469"
   ],
   "transitions": [
    {
     "to": "ADM-469",
     "trigger": "Back to AI Configuration Home & Start",
     "provenance": "structural — pack board 1 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Convert the entire AI conversation into a structured configuration blueprint that can be reviewed before moving to Board 2. This is the final output of Board 1. Nothing should yet be created in production.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack AI_Configuration_Assistant_Reference.pdf, page 17"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack AI_Configuration_Assistant_Reference.pdf, page 17"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "detailPanel",
       "derived": true,
       "impliedBy": "getConfigurationBlueprint",
       "notes": "One record, read-only."
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "buildConfigurationPlan",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "buildConfigurationPlan"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The blueprint dependency map list.",
   "error": "Could not load. Names which read failed and leaves the blueprint dependency map untouched.",
   "emptyFirstRun": "No blueprint dependency map yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the blueprint dependency map are still there. The pack's own statuses are Blueprint Ready — the state names which is selected.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getConfigurationBlueprint",
    "contract": "ai",
    "purpose": "The blueprint so far",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "buildConfigurationPlan",
    "contract": "ai",
    "purpose": "Compile the blueprint into a plan",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-478",
   "workshopBoard": "wireframes/WS09 AI Configuration Assistant Board 1.dc.html#adm-478"
  },
  "apisNote": "Regenerated 9 September 2026 from AI_Configuration_Assistant_Reference.pdf page 17. 0 of 0 labels bound to a contract property; 5 of 16 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "sessionId",
     "from": "session"
    }
   ]
  },
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
 "answerConfigurationQuestion": {
  "method": "POST",
  "path": "/configuration-sessions/{sessionId}/answers",
  "contract": "ai",
  "summary": "Answer the current question",
  "permission": "AI_USE",
  "offlineCapable": false,
  "conflictPolicy": "append",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "AiConfigurationTurn"
 },
 "attachConfigurationSource": {
  "method": "POST",
  "path": "/configuration-sessions/{sessionId}/sources",
  "contract": "ai",
  "summary": "Seed a configuration session from an uploaded document",
  "permission": "AI_USE",
  "offlineCapable": false,
  "conflictPolicy": "append",
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
 "buildConfigurationPlan": {
  "method": "POST",
  "path": "/configuration-sessions/{sessionId}/plan",
  "contract": "ai",
  "summary": "Compile the blueprint into a plan",
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
  "responds": "AiActionPlanDetail"
 },
 "decideBlueprintRecommendation": {
  "method": "POST",
  "path": "/configuration-sessions/{sessionId}/decisions/{decisionKey}",
  "contract": "ai",
  "summary": "Accept, modify, reject or defer a blueprint decision",
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
  "responds": "AiBlueprintDecision"
 },
 "getConfigurationBlueprint": {
  "method": "GET",
  "path": "/configuration-sessions/{sessionId}/blueprint",
  "contract": "ai",
  "summary": "The blueprint so far",
  "permission": "AI_USE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "module",
    "in": "query",
    "required": null
   },
   {
    "name": "decisionClass",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "AiBlueprintView"
 },
 "listConfigurationSessions": {
  "method": "GET",
  "path": "/configuration-sessions",
  "contract": "ai",
  "summary": "Configuration-assistant sessions",
  "permission": "AI_USE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "status",
    "in": "query",
    "required": null
   },
   {
    "name": "intent",
    "in": "query",
    "required": null
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
 "listConfigurationSources": {
  "method": "GET",
  "path": "/configuration-sessions/{sessionId}/sources",
  "contract": "ai",
  "summary": "Documents attached to a configuration session",
  "permission": "AI_USE",
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
 "startConfigurationSession": {
  "method": "POST",
  "path": "/configuration-sessions",
  "contract": "ai",
  "summary": "Start the configuration assistant",
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
  "responds": "AiConfigurationSession"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "AiActionPlan": {
  "type": "object",
  "x-ticvai-persistence": "ai.action_plan",
  "description": "**A plan: plan, validate, simulate, approve, execute, with rollback** (design 2.2 D, 3.8; AIC-086..107). Independent of any conversation (AIC-102). Its steps are `ai.action_step`; the change set is hashed so what was approved is what runs (AIC-181).",
  "required": [
   "origin",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "origin": {
    "type": "string",
    "enum": [
     "configurationSession",
     "generateConfiguration",
     "assistant",
     "riskCase",
     "operationalRequirement",
     "rollback"
    ]
   },
   "originRef": {
    "type": "string",
    "nullable": true
   },
   "summary": {
    "type": "string"
   },
   "status": {
    "type": "string",
    "enum": [
     "draft",
     "validated",
     "simulated",
     "awaitingApproval",
     "approved",
     "executing",
     "paused",
     "completed",
     "partiallyCompleted",
     "failed",
     "compensated",
     "cancelled",
     "rolledBack"
    ],
    "readOnly": true
   },
   "autonomyLevel": {
    "$ref": "#/components/schemas/AiAutonomyLevel"
   },
   "approvalTier": {
    "type": "integer",
    "minimum": 1,
    "maximum": 2,
    "description": "The approval tier (1 or 2), the floor the approvals matrix adds to (design 3.8). Not an autonomy level."
   },
   "approvalRequestId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "description": "The `approvals` request, where tier 2 or the matrix caught the plan."
   },
   "proposedActionId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "x-ticvai-references": "ai.proposed_action",
    "description": "The `ai.proposed_action` the plan is presented as for a decision."
   },
   "changeSetHash": {
    "type": "string",
    "readOnly": true
   },
   "governanceOutcome": {
    "allOf": [
     {
      "$ref": "#/components/schemas/AiGovernanceOutcome"
     }
    ],
    "readOnly": true
   },
   "policyVersionRef": {
    "type": "string",
    "readOnly": true,
    "description": "The governance policy version that decided it."
   },
   "simulation": {
    "type": "object",
    "additionalProperties": true,
    "nullable": true,
    "readOnly": true,
    "description": "Current versus proposed state, channels, future orders and issued tickets affected (flow D step 4)."
   },
   "partialCompletionAllowed": {
    "type": "boolean",
    "default": false,
    "description": "Where governance allows a partial completion; otherwise a failure compensates in reverse dependency order (AIC-098, AIC-134)."
   },
   "rollbackOfPlanId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "x-ticvai-references": "ai.action_plan"
   },
   "requestedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "x-ticvai-references": "identity.principal"
   },
   "createdAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   },
   "completedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."
   }
  }
 },
 "AiActionPlanDetail": {
  "type": "object",
  "x-ticvai-persistence": "none — ai.action_plan with its ai.action_step rows",
  "description": "A plan with its steps in DAG order.",
  "required": [
   "plan",
   "steps"
  ],
  "properties": {
   "plan": {
    "$ref": "#/components/schemas/AiActionPlan"
   },
   "steps": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/AiActionStep"
    }
   }
  }
 },
 "AiActionStep": {
  "type": "object",
  "x-ticvai-persistence": "ai.action_step",
  "description": "One step of a plan: a registered tool against `targetContract.targetOperation` at a contract version (AIC-095), with payload, provenance, compensation and the idempotency key `plan:{id}:step:{n}`. **Scoped through its plan** (`platform.apply_parent_rls`). Each step records its target object's version; drift pauses the plan (AIC-182).",
  "required": [
   "planId",
   "stepNumber",
   "toolKey",
   "targetContract",
   "targetOperation",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "planId": {
    "type": "string",
    "format": "uuid",
    "x-ticvai-references": "ai.action_plan"
   },
   "stepNumber": {
    "type": "integer",
    "minimum": 1
   },
   "dependsOn": {
    "type": "array",
    "items": {
     "type": "integer",
     "minimum": 1
    },
    "description": "Step numbers that must succeed first. The plan is a DAG."
   },
   "toolKey": {
    "type": "string"
   },
   "targetContract": {
    "type": "string"
   },
   "targetOperation": {
    "type": "string"
   },
   "contractVersion": {
    "type": "string"
   },
   "payload": {
    "type": "object",
    "additionalProperties": true,
    "description": "The request body of `targetOperation`, validated against it before the plan is approved."
   },
   "provenance": {
    "$ref": "#/components/schemas/AiProvenance"
   },
   "idempotencyKey": {
    "type": "string",
    "readOnly": true
   },
   "targetObjectRef": {
    "type": "string",
    "nullable": true
   },
   "targetObjectVersion": {
    "type": "string",
    "nullable": true,
    "description": "The version the step was planned against. A different version at execution is drift."
   },
   "reversible": {
    "type": "boolean"
   },
   "compensation": {
    "type": "object",
    "additionalProperties": true,
    "nullable": true
   },
   "status": {
    "type": "string",
    "enum": [
     "pending",
     "validated",
     "running",
     "succeeded",
     "failed",
     "compensated",
     "skipped",
     "paused"
    ],
    "readOnly": true
   },
   "attempts": {
    "type": "integer",
    "minimum": 0,
    "maximum": 3,
    "readOnly": true,
    "description": "Bounded at 3 (AIC-135)."
   },
   "lastError": {
    "type": "string",
    "nullable": true,
    "readOnly": true
   },
   "resultRef": {
    "type": "string",
    "nullable": true,
    "readOnly": true,
    "description": "The owning service's response: success is its answer, not a model's judgement (AIC-097)."
   },
   "startedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true
   },
   "completedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true
   }
  }
 },
 "AiBlueprintDecision": {
  "type": "object",
  "x-ticvai-persistence": "ai.blueprint_decision",
  "description": "One decision in a blueprint and what the administrator did with it. **Scoped through its blueprint** (`platform.apply_parent_rls`).",
  "required": [
   "blueprintId",
   "decisionKey",
   "decisionClass",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "blueprintId": {
    "type": "string",
    "format": "uuid",
    "x-ticvai-references": "ai.blueprint"
   },
   "decisionKey": {
    "type": "string"
   },
   "module": {
    "type": "string"
   },
   "decisionClass": {
    "type": "string",
    "enum": [
     "required",
     "recommended",
     "optional"
    ]
   },
   "question": {
    "type": "string",
    "nullable": true
   },
   "value": {
    "type": "object",
    "additionalProperties": true,
    "nullable": true
   },
   "provenance": {
    "$ref": "#/components/schemas/AiProvenance"
   },
   "sourceId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "x-ticvai-references": "ai.config_source",
    "description": "The attached document the value was extracted from (29 September, build; `attachConfigurationSource`)."
   },
   "sourceCitation": {
    "type": "string",
    "nullable": true,
    "maxLength": 200,
    "description": "Where in it, e.g. `page 4`, `sheet Prices!B7`, `logo region`."
   },
   "recommendation": {
    "type": "object",
    "additionalProperties": true,
    "nullable": true,
    "description": "What the assistant recommends and why (ADM-491): mandatory configuration and best practice kept apart."
   },
   "status": {
    "type": "string",
    "enum": [
     "open",
     "accepted",
     "modified",
     "rejected",
     "deferred"
    ]
   },
   "decidedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "x-ticvai-references": "identity.principal"
   },
   "decidedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true
   },
   "note": {
    "type": "string",
    "nullable": true
   }
  }
 },
 "AiBlueprintView": {
  "type": "object",
  "x-ticvai-persistence": "none — ai.blueprint with its ai.blueprint_decision rows",
  "description": "A blueprint with its decisions.",
  "required": [
   "blueprint",
   "decisions"
  ],
  "properties": {
   "blueprint": {
    "$ref": "#/components/schemas/AiConfigurationBlueprint"
   },
   "decisions": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/AiBlueprintDecision"
    }
   }
  }
 },
 "AiConfigurationBlueprint": {
  "type": "object",
  "x-ticvai-persistence": "ai.blueprint",
  "description": "**The blueprint** (design 2.2 D step 2, ADM-478): decisions, severity-graded issues and a dependency map. **Never `ready` while a required decision is deferred** (AIC-115).",
  "required": [
   "sessionId",
   "version",
   "readiness"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "sessionId": {
    "type": "string",
    "format": "uuid",
    "x-ticvai-references": "ai.config_session"
   },
   "version": {
    "type": "integer",
    "minimum": 1
   },
   "readiness": {
    "type": "string",
    "enum": [
     "notReady",
     "readyWithWarnings",
     "ready"
    ],
    "readOnly": true
   },
   "requiredOpen": {
    "type": "integer",
    "minimum": 0,
    "readOnly": true,
    "description": "Required decisions not yet accepted or modified."
   },
   "issues": {
    "$ref": "#/components/schemas/AiBlueprintIssueList"
   },
   "dependencyMap": {
    "type": "object",
    "additionalProperties": true,
    "readOnly": true,
    "description": "Configuration objects and the order they depend on each other, by module."
   },
   "summary": {
    "type": "string",
    "nullable": true
   },
   "createdAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."
   }
  }
 },
 "AiConfigurationQuestion": {
  "type": "object",
  "x-ticvai-persistence": "none — chosen per turn from the configuration knowledge model",
  "description": "**The next question, chosen by the configuration knowledge model, not by the language model** (design 2.2 D, AIC-111). The model only extracts a structured answer against `answerSchema`.",
  "required": [
   "questionKey",
   "text",
   "decisionClass"
  ],
  "properties": {
   "questionKey": {
    "type": "string"
   },
   "text": {
    "type": "string"
   },
   "module": {
    "type": "string",
    "nullable": true
   },
   "decisionClass": {
    "type": "string",
    "enum": [
     "required",
     "recommended",
     "optional"
    ]
   },
   "answerType": {
    "type": "string",
    "enum": [
     "freeText",
     "singleChoice",
     "multiChoice",
     "number",
     "date",
     "confirm"
    ]
   },
   "options": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "why": {
    "type": "string",
    "nullable": true,
    "description": "Why it is asked: which configuration branch it opens or closes."
   },
   "answerSchema": {
    "type": "object",
    "additionalProperties": true,
    "nullable": true,
    "description": "JSON Schema the extracted answer must satisfy."
   }
  }
 },
 "AiConfigurationSession": {
  "type": "object",
  "x-ticvai-persistence": "ai.config_session",
  "description": "**A configuration-assistant session** (design 2.2 D steps 1-2, C7; ADM-469..478). Discovery runs from the configuration knowledge model; every value carries provenance.",
  "required": [
   "intent",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "intent": {
    "type": "string",
    "enum": [
     "create",
     "modify",
     "extend",
     "clone"
    ]
   },
   "venueType": {
    "type": "string",
    "nullable": true,
    "description": "Museum, theme park, water park, zoo, aquarium, theatre, stadium, festival, conference..."
   },
   "sourceScopePath": {
    "type": "string",
    "nullable": true,
    "description": "The setup being cloned or extended."
   },
   "status": {
    "type": "string",
    "enum": [
     "discovering",
     "blueprintReady",
     "planned",
     "executing",
     "completed",
     "abandoned"
    ],
    "readOnly": true
   },
   "progressPercent": {
    "type": "integer",
    "minimum": 0,
    "maximum": 100,
    "readOnly": true
   },
   "nextQuestion": {
    "allOf": [
     {
      "$ref": "#/components/schemas/AiConfigurationQuestion"
     }
    ],
    "nullable": true,
    "readOnly": true
   },
   "conversationId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "x-ticvai-references": "ai.conversation"
   },
   "planId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "x-ticvai-references": "ai.action_plan"
   },
   "locale": {
    "type": "string",
    "nullable": true
   },
   "requestedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "x-ticvai-references": "identity.principal"
   },
   "startedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   },
   "lastActivityAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."
   }
  }
 },
 "AiConfigurationSource": {
  "type": "object",
  "x-ticvai-persistence": "ai.config_source",
  "description": "**A document attached to a configuration session** (1.3.31, 1.4.21, 2.6.50): the uploaded asset, what kind of source it is, and how its extraction went. The values it yields are blueprint decisions with provenance `inferred` and a citation back here. **Scoped through its session** (`platform.apply_parent_rls`).",
  "required": [
   "sessionId",
   "assetId",
   "sourceKind",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "sessionId": {
    "type": "string",
    "format": "uuid",
    "x-ticvai-references": "ai.config_session"
   },
   "assetId": {
    "type": "string",
    "format": "uuid",
    "x-ticvai-references": "assets.MediaAsset"
   },
   "sourceKind": {
    "type": "string",
    "enum": [
     "brief",
     "brochure",
     "catalogue",
     "priceList",
     "spreadsheet",
     "brandAsset"
    ]
   },
   "note": {
    "type": "string",
    "nullable": true
   },
   "status": {
    "type": "string",
    "enum": [
     "extracting",
     "extracted",
     "partial",
     "failed"
    ],
    "readOnly": true
   },
   "pageCount": {
    "type": "integer",
    "nullable": true,
    "readOnly": true
   },
   "valuesExtracted": {
    "type": "integer",
    "readOnly": true,
    "description": "Questions it pre-answered."
   },
   "unreadRegions": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "readOnly": true,
    "description": "Pages or regions it could not read, named so a person can answer by hand."
   },
   "attachedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "x-ticvai-references": "identity.principal"
   },
   "attachedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   },
   "completedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true
   }
  }
 },
 "AiConfigurationTurn": {
  "type": "object",
  "x-ticvai-persistence": "none — the answer is written to ai.blueprint_decision and the session",
  "description": "The result of one answer: what was extracted with its provenance, the next question and progress.",
  "required": [
   "session"
  ],
  "properties": {
   "session": {
    "$ref": "#/components/schemas/AiConfigurationSession"
   },
   "extracted": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "decisionKey": {
       "type": "string"
      },
      "value": {
       "type": "object",
       "additionalProperties": true,
       "nullable": true
      },
      "provenance": {
       "$ref": "#/components/schemas/AiProvenance"
      }
     }
    }
   },
   "nextQuestion": {
    "allOf": [
     {
      "$ref": "#/components/schemas/AiConfigurationQuestion"
     }
    ],
    "nullable": true
   },
   "clarificationsNeeded": {
    "type": "array",
    "items": {
     "type": "string"
    }
   }
  }
 },
 "AiProvenance": {
  "type": "string",
  "enum": [
   "confirmed",
   "aiRecommended",
   "inferred",
   "unknown"
  ],
  "description": "**Where a configuration value came from** (design 2.2 D, AIC-111): said by the administrator, recommended by the assistant, inferred from other answers, or not known yet. Shown beside every value; no confidence number is shown for configuration (design 5.6)."
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
 }
}
```
