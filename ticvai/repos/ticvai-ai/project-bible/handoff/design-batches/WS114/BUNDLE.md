# WS114 — ACCREDITATION board 7

**10 screens · 12 operations · 15 schemas · 8 permissions**

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

- **Every control that can be refused must be gated.** 8 permissions apply here:
  `ACCREDITATION_CONFIGURE, ACCREDITATION_MANAGE, ACCREDITATION_VIEW, GUEST_MANAGE, MARKETING_SEND, MARKETING_VIEW, REPORT_EXPORT, REPORT_VIEW_VENUE`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-674` | Accreditation Communications Command Center | listDetail | 1 | 0 | — |
| `BO-675` | Notification Rule Management | configEditor | 1 | 0 | — |
| `BO-676` | Expiry & Renewal Notification Scheduler | configEditor | 1 | 0 | — |
| `BO-677` | Communication Template Library | listDetail | 1 | 0 | — |
| `BO-678` | Channel, Language & Branding Configuration | configEditor | 1 | 0 | — |
| `BO-679` | Manual & Bulk Communication Center | listDetail | 1 | 0 | — |
| `BO-680` | Accreditation Bulk Import | listDetail | 1 | 0 | — |
| `BO-681` | Import Validation & Processing Monitor | listDetail | 1 | 0 | — |
| `BO-682` | Accreditation Export & Data Extract Center | configEditor | 6 | 0 | — |
| `BO-683` | Delivery, Batch & Operational History | listDetail | 1 | 0 | — |

## Thin screens in this batch

**BO-674, BO-677, BO-679, BO-680, BO-681, BO-683 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "BO-674",
  "name": "Accreditation Communications Command Center",
  "module": "Access & Venue",
  "requiresModule": "accreditation",
  "wave": 3,
  "source": {
   "pack": "ACCREDITATION.pdf",
   "board": "7",
   "number": "1",
   "page": 55
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/accreditation-communications-command-center-bo-674",
   "component": "apps/venue-management-web/src/routes/access-venue/AccreditationCommunicationsCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-100"
   ],
   "exitTo": [
    "BO-100",
    "BO-675",
    "BO-676",
    "BO-677",
    "BO-678",
    "BO-679",
    "BO-680",
    "BO-681",
    "BO-682",
    "BO-683"
   ],
   "transitions": [
    {
     "to": "BO-100",
     "trigger": "Back to Venue Home",
     "provenance": "structural — pack board 7 wiring, 19 September 2026",
     "back": true
    },
    {
     "to": "BO-675",
     "trigger": "Notification Rule Management",
     "provenance": "structural — pack board 7 wiring, 19 September 2026"
    },
    {
     "to": "BO-676",
     "trigger": "Expiry & Renewal Notification Scheduler",
     "provenance": "structural — pack board 7 wiring, 19 September 2026"
    },
    {
     "to": "BO-677",
     "trigger": "Communication Template Library",
     "provenance": "structural — pack board 7 wiring, 19 September 2026"
    },
    {
     "to": "BO-678",
     "trigger": "Channel, Language & Branding Configuration",
     "provenance": "structural — pack board 7 wiring, 19 September 2026"
    },
    {
     "to": "BO-679",
     "trigger": "Manual & Bulk Communication Center",
     "provenance": "structural — pack board 7 wiring, 19 September 2026"
    },
    {
     "to": "BO-680",
     "trigger": "Accreditation Bulk Import",
     "provenance": "structural — pack board 7 wiring, 19 September 2026"
    },
    {
     "to": "BO-681",
     "trigger": "Import Validation & Processing Monitor",
     "provenance": "structural — pack board 7 wiring, 19 September 2026"
    },
    {
     "to": "BO-682",
     "trigger": "Accreditation Export & Data Extract Center",
     "provenance": "structural — pack board 7 wiring, 19 September 2026"
    },
    {
     "to": "BO-683",
     "trigger": "Delivery, Batch & Operational History",
     "provenance": "structural — pack board 7 wiring, 19 September 2026"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Dashboard analytics shall show) and no metric row",
  "purpose": "Central dashboard for accreditation notifications and operational communications.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack ACCREDITATION.pdf, page 55 §Dashboard analytics shall show"
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
       "label": "Every accreditation communications",
       "columns": [
        "Delivery success rate",
        "Notifications by type",
        "Notifications by channel",
        "Failure trends",
        "Upcoming scheduled communications"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack ACCREDITATION.pdf, page 55 §Dashboard analytics shall show"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected accreditation communications",
       "bindsTo": null,
       "columns": [
        "Delivery success rate",
        "Notifications by type",
        "Notifications by channel",
        "Failure trends",
        "Upcoming scheduled communications"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Scope of Work”, “Key requirements”.",
       "provenance": "pack ACCREDITATION.pdf, page 55 §Dashboard analytics shall show"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The accreditation communications list.",
   "error": "Could not load. Names which read failed and leaves the accreditation communications untouched.",
   "emptyFirstRun": "No accreditation communications yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the accreditation communications are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setAccreditationNotificationRules",
    "contract": "accreditation",
    "purpose": "Notifications at a glance",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "Delivery success rate",
    "Notifications by type",
    "Notifications by channel",
    "Failure trends",
    "Upcoming scheduled communications"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-674",
   "workshopBoard": "wireframes/WS07 ACCREDITATION Board 7.dc.html#bo-674"
  },
  "apisNote": "Regenerated 9 September 2026 from ACCREDITATION.pdf page 55. 0 of 5 labels bound to a contract property; 5 of 29 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-675",
  "name": "Notification Rule Management",
  "module": "Access & Venue",
  "requiresModule": "accreditation",
  "wave": 3,
  "source": {
   "pack": "ACCREDITATION.pdf",
   "board": "7",
   "number": "2",
   "page": 56
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/notification-rule-management-bo-675",
   "component": "apps/venue-management-web/src/routes/access-venue/NotificationRuleManagement.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-674"
   ],
   "exitTo": [
    "BO-674"
   ],
   "transitions": [
    {
     "to": "BO-674",
     "trigger": "Back to Accreditation Communications Command Center",
     "provenance": "structural — pack board 7 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Each rule shall define) and no display directory — it is settings, not a population",
  "purpose": "Configure when accreditation notifications are automatically triggered.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Trigger",
       "provenance": "pack ACCREDITATION.pdf, page 56 §Each rule shall define"
      },
      {
       "kind": "selectField",
       "label": "Recipient",
       "provenance": "pack ACCREDITATION.pdf, page 56 §Each rule shall define"
      },
      {
       "kind": "selectField",
       "label": "Communication channel",
       "provenance": "pack ACCREDITATION.pdf, page 56 §Each rule shall define"
      },
      {
       "kind": "selectField",
       "label": "Template",
       "provenance": "pack ACCREDITATION.pdf, page 56 §Each rule shall define"
      },
      {
       "kind": "selectField",
       "label": "Timing",
       "provenance": "pack ACCREDITATION.pdf, page 56 §Each rule shall define"
      },
      {
       "kind": "selectField",
       "label": "Event/program scope",
       "provenance": "pack ACCREDITATION.pdf, page 56 §Each rule shall define"
      },
      {
       "kind": "selectField",
       "label": "Category",
       "provenance": "pack ACCREDITATION.pdf, page 56 §Each rule shall define"
      },
      {
       "kind": "selectField",
       "label": "Language",
       "provenance": "pack ACCREDITATION.pdf, page 56 §Each rule shall define"
      },
      {
       "kind": "selectField",
       "label": "Active/inactive status",
       "provenance": "pack ACCREDITATION.pdf, page 56 §Each rule shall define"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The notification rule configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the notification rule untouched.",
   "emptyFirstRun": "No notification rule configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "setAccreditationNotificationRules",
    "contract": "accreditation",
    "purpose": "Notification rules",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-675",
   "workshopBoard": "wireframes/WS07 ACCREDITATION Board 7.dc.html#bo-675"
  },
  "apisNote": "Regenerated 9 September 2026 from ACCREDITATION.pdf page 56. 0 of 0 labels bound to a contract property; 9 of 27 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-676",
  "name": "Expiry & Renewal Notification Scheduler",
  "module": "Access & Venue",
  "requiresModule": "accreditation",
  "wave": 3,
  "source": {
   "pack": "ACCREDITATION.pdf",
   "board": "7",
   "number": "3",
   "page": 57
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/expiry-renewal-notification-scheduler-bo-676",
   "component": "apps/venue-management-web/src/routes/access-venue/ExpiryRenewalNotificationScheduler.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-674"
   ],
   "exitTo": [
    "BO-674"
   ],
   "transitions": [
    {
     "to": "BO-674",
     "trigger": "Back to Accreditation Communications Command Center",
     "provenance": "structural — pack board 7 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Administrators shall define) and no display directory — it is settings, not a population",
  "purpose": "Configure proactive reminders before accreditation expiry or renewal.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Days before/after event",
       "provenance": "pack ACCREDITATION.pdf, page 57 §Administrators shall define"
      },
      {
       "kind": "selectField",
       "label": "Recipient",
       "provenance": "pack ACCREDITATION.pdf, page 57 §Administrators shall define"
      },
      {
       "kind": "selectField",
       "label": "Template",
       "provenance": "pack ACCREDITATION.pdf, page 57 §Administrators shall define"
      },
      {
       "kind": "selectField",
       "label": "Channel",
       "provenance": "pack ACCREDITATION.pdf, page 57 §Administrators shall define"
      },
      {
       "kind": "selectField",
       "label": "Escalation rule",
       "provenance": "pack ACCREDITATION.pdf, page 57 §Administrators shall define"
      },
      {
       "kind": "selectField",
       "label": "Retry policy",
       "provenance": "pack ACCREDITATION.pdf, page 57 §Administrators shall define"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The expiry renewal notification configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the expiry renewal notification untouched.",
   "emptyFirstRun": "No expiry renewal notification configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "setAccreditationNotificationRules",
    "contract": "accreditation",
    "purpose": "Expiry and renewal scheduling",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-676",
   "workshopBoard": "wireframes/WS07 ACCREDITATION Board 7.dc.html#bo-676"
  },
  "apisNote": "Regenerated 9 September 2026 from ACCREDITATION.pdf page 57. 0 of 0 labels bound to a contract property; 6 of 20 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-677",
  "name": "Communication Template Library",
  "module": "Access & Venue",
  "requiresModule": "accreditation",
  "wave": 3,
  "source": {
   "pack": "ACCREDITATION.pdf",
   "board": "7",
   "number": "4",
   "page": 58
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/communication-template-library-bo-677",
   "component": "apps/venue-management-web/src/routes/access-venue/CommunicationTemplateLibrary.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-674"
   ],
   "exitTo": [
    "BO-674"
   ],
   "transitions": [
    {
     "to": "BO-674",
     "trigger": "Back to Accreditation Communications Command Center",
     "provenance": "structural — pack board 7 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Manage reusable accreditation communication templates.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack ACCREDITATION.pdf, page 58"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack ACCREDITATION.pdf, page 58"
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
       "impliedBy": "listMessageTemplates",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The communication template list.",
   "error": "Could not load. Names which read failed and leaves the communication template untouched.",
   "emptyFirstRun": "No communication template yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the communication template are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listMessageTemplates",
    "contract": "marketing-crm",
    "purpose": "Template library",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-677",
   "workshopBoard": "wireframes/WS07 ACCREDITATION Board 7.dc.html#bo-677"
  },
  "apisNote": "Regenerated 9 September 2026 from ACCREDITATION.pdf page 58. 0 of 0 labels bound to a contract property; 0 of 28 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-678",
  "name": "Channel, Language & Branding Configuration",
  "module": "Access & Venue",
  "requiresModule": "accreditation",
  "wave": 3,
  "source": {
   "pack": "ACCREDITATION.pdf",
   "board": "7",
   "number": "5",
   "page": 59
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/channel-language-branding-configuration-bo-678",
   "component": "apps/venue-management-web/src/routes/access-venue/ChannelLanguageBrandingConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-674"
   ],
   "exitTo": [
    "BO-674"
   ],
   "transitions": [
    {
     "to": "BO-674",
     "trigger": "Back to Accreditation Communications Command Center",
     "provenance": "structural — pack board 7 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Administrators shall configure) and no display directory — it is settings, not a population",
  "purpose": "Control how communications are delivered and branded.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Sender identity",
       "provenance": "pack ACCREDITATION.pdf, page 59 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Reply information",
       "provenance": "pack ACCREDITATION.pdf, page 59 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Default language",
       "provenance": "pack ACCREDITATION.pdf, page 59 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Alternative languages",
       "provenance": "pack ACCREDITATION.pdf, page 59 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Tenant logo",
       "provenance": "pack ACCREDITATION.pdf, page 59 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Event branding",
       "provenance": "pack ACCREDITATION.pdf, page 59 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Venue branding",
       "provenance": "pack ACCREDITATION.pdf, page 59 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Header/footer",
       "provenance": "pack ACCREDITATION.pdf, page 59 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Contact information",
       "provenance": "pack ACCREDITATION.pdf, page 59 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Key requirement: 12.1.57",
       "provenance": "pack ACCREDITATION.pdf, page 59 §Administrators shall configure"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The channel language branding configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the channel language branding untouched.",
   "emptyFirstRun": "No channel language branding configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "setLocalizationBrandingCustomer",
    "contract": "marketing-crm",
    "purpose": "Channel, language and branding",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-678",
   "workshopBoard": "wireframes/WS07 ACCREDITATION Board 7.dc.html#bo-678"
  },
  "apisNote": "Regenerated 9 September 2026 from ACCREDITATION.pdf page 59. 0 of 0 labels bound to a contract property; 10 of 19 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-679",
  "name": "Manual & Bulk Communication Center",
  "module": "Access & Venue",
  "requiresModule": "accreditation",
  "wave": 3,
  "source": {
   "pack": "ACCREDITATION.pdf",
   "board": "7",
   "number": "6",
   "page": 59
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/manual-bulk-communication-center-bo-679",
   "component": "apps/venue-management-web/src/routes/access-venue/ManualBulkCommunicationCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-674"
   ],
   "exitTo": [
    "BO-674"
   ],
   "transitions": [
    {
     "to": "BO-674",
     "trigger": "Back to Accreditation Communications Command Center",
     "provenance": "structural — pack board 7 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Allow authorized operators to communicate with selected accreditation populations.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack ACCREDITATION.pdf, page 59"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack ACCREDITATION.pdf, page 59"
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
       "impliedBy": "sendTransactionalMessage",
       "label": "Send transactional message",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "sendTransactionalMessage"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The manual bulk communication list.",
   "error": "Could not load. Names which read failed and leaves the manual bulk communication untouched.",
   "emptyFirstRun": "No manual bulk communication yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the manual bulk communication are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "sendTransactionalMessage",
    "contract": "marketing-crm",
    "purpose": "Bulk communication",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-679",
   "workshopBoard": "wireframes/WS07 ACCREDITATION Board 7.dc.html#bo-679"
  },
  "apisNote": "Regenerated 9 September 2026 from ACCREDITATION.pdf page 59. 0 of 0 labels bound to a contract property; 0 of 21 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-680",
  "name": "Accreditation Bulk Import",
  "module": "Access & Venue",
  "requiresModule": "accreditation",
  "wave": 3,
  "source": {
   "pack": "ACCREDITATION.pdf",
   "board": "7",
   "number": "7",
   "page": 60
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/accreditation-bulk-import-bo-680",
   "component": "apps/venue-management-web/src/routes/access-venue/AccreditationBulkImport.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-674"
   ],
   "exitTo": [
    "BO-674"
   ],
   "transitions": [
    {
     "to": "BO-674",
     "trigger": "Back to Accreditation Communications Command Center",
     "provenance": "structural — pack board 7 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Import accreditation records at scale.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack ACCREDITATION.pdf, page 60"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack ACCREDITATION.pdf, page 60"
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
       "impliedBy": "importAccreditationHolders",
       "label": "Import accreditation holders",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "importAccreditationHolders"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The accreditation bulk import list.",
   "error": "Could not load. Names which read failed and leaves the accreditation bulk import untouched.",
   "emptyFirstRun": "No accreditation bulk import yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the accreditation bulk import are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "importAccreditationHolders",
    "contract": "accreditation",
    "purpose": "Bulk import a roster",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listAccreditationHolders"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-680",
   "workshopBoard": "wireframes/WS07 ACCREDITATION Board 7.dc.html#bo-680"
  },
  "apisNote": "Regenerated 9 September 2026 from ACCREDITATION.pdf page 60. 0 of 0 labels bound to a contract property; 0 of 21 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-681",
  "name": "Import Validation & Processing Monitor",
  "module": "Access & Venue",
  "requiresModule": "accreditation",
  "wave": 3,
  "source": {
   "pack": "ACCREDITATION.pdf",
   "board": "7",
   "number": "8",
   "page": 61
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/import-validation-processing-monitor-bo-681",
   "component": "apps/venue-management-web/src/routes/access-venue/ImportValidationProcessingMonitor.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-674"
   ],
   "exitTo": [
    "BO-674"
   ],
   "transitions": [
    {
     "to": "BO-674",
     "trigger": "Back to Accreditation Communications Command Center",
     "provenance": "structural — pack board 7 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§The screen shall display) and no metric row",
  "purpose": "Govern and monitor bulk accreditation imports.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack ACCREDITATION.pdf, page 61 §The screen shall display"
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
       "label": "Every import validation processing",
       "columns": [
        "Import batch ID",
        "File name",
        "Uploaded by",
        "Upload date/time",
        "Total records",
        "Valid records",
        "Warning records",
        "Failed records",
        "Duplicate records",
        "Processing status"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack ACCREDITATION.pdf, page 61 §The screen shall display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected import validation processing",
       "bindsTo": null,
       "columns": [
        "Import batch ID",
        "File name",
        "Uploaded by",
        "Upload date/time",
        "Total records",
        "Valid records",
        "Warning records",
        "Failed records",
        "Duplicate records",
        "Processing status"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Processing statuses shall include”.",
       "provenance": "pack ACCREDITATION.pdf, page 61 §The screen shall display"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The import validation processing list.",
   "error": "Could not load. Names which read failed and leaves the import validation processing untouched.",
   "emptyFirstRun": "No import validation processing yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the import validation processing are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "importAccreditationHolders",
    "contract": "accreditation",
    "purpose": "Validation and processing",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listAccreditationHolders"
    ]
   }
  ],
  "entryState": {
   "preloaded": [
    "Import batch ID",
    "File name",
    "Uploaded by",
    "Upload date/time",
    "Total records",
    "Valid records"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-681",
   "workshopBoard": "wireframes/WS07 ACCREDITATION Board 7.dc.html#bo-681"
  },
  "apisNote": "Regenerated 9 September 2026 from ACCREDITATION.pdf page 61. 0 of 10 labels bound to a contract property; 10 of 14 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-682",
  "name": "Accreditation Export & Data Extract Center",
  "module": "Access & Venue",
  "requiresModule": "accreditation",
  "wave": 3,
  "source": {
   "pack": "ACCREDITATION.pdf",
   "board": "7",
   "number": "9",
   "page": 61
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/accreditation-export-data-extract-center-bo-682",
   "component": "apps/venue-management-web/src/routes/access-venue/AccreditationExportDataExtractCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-674"
   ],
   "exitTo": [
    "BO-674"
   ],
   "transitions": [
    {
     "to": "BO-674",
     "trigger": "Back to Accreditation Communications Command Center",
     "provenance": "structural — pack board 7 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§The system shall capture) and no display directory — it is settings, not a population",
  "purpose": "Export authorized accreditation data for operational or reporting purposes.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Requested by",
       "provenance": "pack ACCREDITATION.pdf, page 61 §The system shall capture"
      },
      {
       "kind": "selectField",
       "label": "Export date/time",
       "provenance": "pack ACCREDITATION.pdf, page 61 §The system shall capture"
      },
      {
       "kind": "selectField",
       "label": "Filters",
       "provenance": "pack ACCREDITATION.pdf, page 61 §The system shall capture"
      },
      {
       "kind": "selectField",
       "label": "Fields exported",
       "provenance": "pack ACCREDITATION.pdf, page 61 §The system shall capture"
      },
      {
       "kind": "selectField",
       "label": "Number of records",
       "provenance": "pack ACCREDITATION.pdf, page 61 §The system shall capture"
      },
      {
       "kind": "selectField",
       "label": "Export status",
       "provenance": "pack ACCREDITATION.pdf, page 61 §The system shall capture"
      },
      {
       "kind": "selectField",
       "label": "Key requirement: 12.1.55",
       "provenance": "pack ACCREDITATION.pdf, page 61 §The system shall capture"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The accreditation export data configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the accreditation export data untouched.",
   "emptyFirstRun": "No accreditation export data configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "listAccreditationHolders",
    "contract": "accreditation",
    "purpose": "Export",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "listAccreditationExports",
    "contract": "accreditation",
    "purpose": "Export history: requested by, date, filters, fields, records, status",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "exportAccreditationData",
    "contract": "accreditation",
    "purpose": "Request an export",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "getAccreditationExport",
    "contract": "accreditation",
    "purpose": "Status and download link",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "runReport",
    "contract": "reporting",
    "purpose": "Report over the accreditation data sources",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "exportReportResult",
    "contract": "reporting",
    "purpose": "csv or xlsx extract",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-682",
   "workshopBoard": "wireframes/WS07 ACCREDITATION Board 7.dc.html#bo-682"
  },
  "apisNote": "Regenerated 9 September 2026 from ACCREDITATION.pdf page 61. 0 of 0 labels bound to a contract property; 7 of 24 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "executionId",
     "from": "navigation"
    },
    {
     "name": "exportId",
     "from": "navigation"
    },
    {
     "name": "reportId",
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
  "id": "BO-683",
  "name": "Delivery, Batch & Operational History",
  "module": "Access & Venue",
  "requiresModule": "accreditation",
  "wave": 3,
  "source": {
   "pack": "ACCREDITATION.pdf",
   "board": "7",
   "number": "10",
   "page": 62
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/delivery-batch-operational-history-bo-683",
   "component": "apps/venue-management-web/src/routes/access-venue/DeliveryBatchOperationalHistory.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-674"
   ],
   "exitTo": [
    "BO-674"
   ],
   "transitions": [
    {
     "to": "BO-674",
     "trigger": "Back to Accreditation Communications Command Center",
     "provenance": "structural — pack board 7 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Provide a consolidated history of notifications, communications, imports and exports.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack ACCREDITATION.pdf, page 62"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack ACCREDITATION.pdf, page 62"
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
       "impliedBy": "listAccreditationAudit",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The delivery batch operational list.",
   "error": "Could not load. Names which read failed and leaves the delivery batch operational untouched.",
   "emptyFirstRun": "No delivery batch operational yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the delivery batch operational are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listAccreditationAudit",
    "contract": "accreditation",
    "purpose": "Import and export audit",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-683",
   "workshopBoard": "wireframes/WS07 ACCREDITATION Board 7.dc.html#bo-683"
  },
  "apisNote": "Regenerated 9 September 2026 from ACCREDITATION.pdf page 62. 0 of 0 labels bound to a contract property; 0 of 23 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
 "exportAccreditationData": {
  "method": "POST",
  "path": "/accreditation-exports",
  "contract": "accreditation",
  "summary": "Export holders, applications, credentials or access assignments",
  "permission": "ACCREDITATION_MANAGE",
  "offlineCapable": null,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "AccreditationDataExport",
  "responds": null
 },
 "exportReportResult": {
  "method": "POST",
  "path": "/report-executions/{executionId}/export",
  "contract": "reporting",
  "summary": "Export a completed result",
  "permission": "REPORT_EXPORT",
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
 "getAccreditationExport": {
  "method": "GET",
  "path": "/accreditation-exports/{exportId}",
  "contract": "accreditation",
  "summary": "One export, and its download link once ready",
  "permission": "ACCREDITATION_MANAGE",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "AccreditationDataExport"
 },
 "importAccreditationHolders": {
  "method": "POST",
  "path": "/accreditation-imports",
  "contract": "accreditation",
  "summary": "Load a roster supplied by an organisation",
  "permission": "ACCREDITATION_MANAGE",
  "offlineCapable": null,
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
  "responds": "AccreditationImportResult"
 },
 "listAccreditationAudit": {
  "method": "GET",
  "path": "/accreditation-audit",
  "contract": "accreditation",
  "summary": "The immutable record of who granted what to whom",
  "permission": "ACCREDITATION_VIEW",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "holderId",
    "in": "query",
    "required": null
   },
   {
    "name": "from",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "AccreditationAuditRecord"
 },
 "listAccreditationExports": {
  "method": "GET",
  "path": "/accreditation-exports",
  "contract": "accreditation",
  "summary": "Exports taken, by whom, of what",
  "permission": "ACCREDITATION_MANAGE",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "status",
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
 "listAccreditationHolders": {
  "method": "GET",
  "path": "/accreditation-holders",
  "contract": "accreditation",
  "summary": "Everybody accredited, and what state they are in",
  "permission": "ACCREDITATION_VIEW",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "programmeId",
    "in": "query",
    "required": null
   },
   {
    "name": "organisationId",
    "in": "query",
    "required": null
   },
   {
    "name": "status",
    "in": "query",
    "required": null
   },
   {
    "name": "expiringWithinDays",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "AccreditationHolder"
 },
 "listMessageTemplates": {
  "method": "GET",
  "path": "/message-templates",
  "contract": "marketing-crm",
  "summary": "List message templates",
  "permission": "MARKETING_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "channel",
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
 "runReport": {
  "method": "POST",
  "path": "/reports/{reportId}/run",
  "contract": "reporting",
  "summary": "Run a report",
  "permission": "REPORT_VIEW_VENUE",
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
  "requestBody": "RunReportRequest",
  "responds": "ReportResult"
 },
 "sendTransactionalMessage": {
  "method": "POST",
  "path": "/messages",
  "contract": "marketing-crm",
  "summary": "Send a transactional message",
  "permission": "MARKETING_SEND",
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
 "setAccreditationNotificationRules": {
  "method": "PUT",
  "path": "/accreditation-notifications",
  "contract": "accreditation",
  "summary": "Who is told what, and when",
  "permission": "ACCREDITATION_CONFIGURE",
  "offlineCapable": null,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "AccreditationNotificationRules",
  "responds": "AccreditationNotificationRules"
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
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "AccreditationAuditRecord": {
  "type": "object",
  "x-ticvai-persistence": "accreditation.audit",
  "description": "Board 8.7. **Who gave this person access to that place, when, and on whose authority.**\n",
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "at": {
    "type": "string",
    "format": "date-time"
   },
   "holderId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "action": {
    "type": "string"
   },
   "actorPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "previousValue": {
    "nullable": true
   },
   "newValue": {
    "nullable": true
   },
   "reason": {
    "type": "string",
    "nullable": true
   },
   "approvalRequestId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "previousRecordHash": {
    "type": "string",
    "nullable": true
   },
   "recordHash": {
    "type": "string"
   },
   "integrity": {
    "type": "string",
    "readOnly": true,
    "enum": [
     "intact",
     "broken",
     "unverifiable"
    ]
   },
   "scopePath": {
    "type": "string"
   }
  }
 },
 "AccreditationDataExport": {
  "type": "object",
  "x-ticvai-persistence": "accreditation.data_export",
  "description": "12.1.55. **A spreadsheet of accredited people leaving the platform is an event someone should own.** Requested by `exportAccreditationData`, listed for BO-682, and fetched once `ready`.\n",
  "required": [
   "dataset",
   "format"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "dataset": {
    "type": "string",
    "enum": [
     "holders",
     "applications",
     "credentials",
     "accessAssignments",
     "documents"
    ]
   },
   "format": {
    "type": "string",
    "enum": [
     "csv",
     "xlsx"
    ]
   },
   "programmeId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "statusFilter": {
    "type": "string",
    "nullable": true
   },
   "organisationId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "categoryCode": {
    "type": "string",
    "nullable": true
   },
   "validOn": {
    "type": "string",
    "format": "date",
    "nullable": true,
    "description": "Only accreditations valid on this date — the register for one performance"
   },
   "fields": {
    "type": "array",
    "description": "The columns wanted. Omitted means the dataset's standard set",
    "items": {
     "type": "string"
    }
   },
   "includePersonalData": {
    "type": "boolean",
    "default": false,
    "description": "Contact details, date of birth, nationality and document references. Requires REPORT_EXPORT_PII and a purpose; recorded in the accreditation audit trail"
   },
   "purpose": {
    "type": "string",
    "maxLength": 500,
    "nullable": true
   },
   "requestedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "requestedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   },
   "recordCount": {
    "type": "integer",
    "nullable": true,
    "readOnly": true
   },
   "status": {
    "type": "string",
    "readOnly": true,
    "enum": [
     "queued",
     "running",
     "ready",
     "failed",
     "expired"
    ]
   },
   "downloadUrl": {
    "type": "string",
    "nullable": true,
    "readOnly": true,
    "description": "Signed and expiring"
   },
   "expiresAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true
   },
   "scopePath": {
    "type": "string"
   }
  }
 },
 "AccreditationHolder": {
  "type": "object",
  "x-ticvai-persistence": "accreditation.holder",
  "description": "**A subject who may never sign in to anything.** `identity` owns principals; this owns accredited people.\n",
  "required": [
   "id",
   "fullName"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "subjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "accreditationNumber": {
    "type": "string"
   },
   "fullName": {
    "type": "string"
   },
   "photoAssetId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "dateOfBirth": {
    "type": "string",
    "format": "date",
    "nullable": true
   },
   "nationality": {
    "type": "string",
    "nullable": true
   },
   "email": {
    "type": "string",
    "format": "email",
    "nullable": true,
    "description": "12.1.16. The holder's own address — where a mobile credential and renewal notices go"
   },
   "phone": {
    "type": "string",
    "nullable": true,
    "description": "12.1.16. E.164"
   },
   "identityDocumentVerified": {
    "type": "boolean",
    "default": false
   },
   "organisationId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "affiliationRole": {
    "type": "string",
    "nullable": true
   },
   "programmeId": {
    "type": "string",
    "format": "uuid"
   },
   "categoryCode": {
    "type": "string",
    "nullable": true
   },
   "status": {
    "type": "string",
    "enum": [
     "active",
     "suspended",
     "revoked",
     "expired",
     "archived"
    ]
   },
   "validFrom": {
    "type": "string",
    "format": "date",
    "nullable": true
   },
   "validTo": {
    "type": "string",
    "format": "date",
    "nullable": true
   },
   "completenessPercent": {
    "type": "integer",
    "readOnly": true
   },
   "scopePath": {
    "type": "string"
   }
  }
 },
 "AccreditationImportResult": {
  "type": "object",
  "description": "Board 7.8. **A bulk import is exactly where the same person gets accredited twice.**\n",
  "properties": {
   "rowsRead": {
    "type": "integer"
   },
   "created": {
    "type": "integer"
   },
   "updated": {
    "type": "integer"
   },
   "rejected": {
    "type": "integer"
   },
   "identityConflicts": {
    "type": "integer"
   },
   "rows": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "row": {
       "type": "integer"
      },
      "name": {
       "type": "string"
      },
      "outcome": {
       "type": "string"
      },
      "detail": {
       "type": "string",
       "nullable": true
      }
     }
    }
   },
   "committed": {
    "type": "boolean"
   }
  }
 },
 "AccreditationNotificationRules": {
  "type": "object",
  "x-ticvai-persistence": "accreditation.notification_rules",
  "description": "Board 7.2. **Notices go to the organisation as well as the holder.**",
  "properties": {
   "programmeId": {
    "type": "string",
    "format": "uuid"
   },
   "rules": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "event": {
       "type": "string",
       "enum": [
        "applicationReceived",
        "informationRequested",
        "approved",
        "rejected",
        "credentialReady",
        "expiringSoon",
        "renewalWindowOpen",
        "expired",
        "suspended",
        "revoked"
       ]
      },
      "daysBefore": {
       "type": "integer",
       "nullable": true
      },
      "recipients": {
       "type": "array",
       "items": {
        "type": "string",
        "enum": [
         "holder",
         "organisation",
         "sponsor",
         "accreditationTeam"
        ]
       }
      },
      "channels": {
       "type": "array",
       "items": {
        "type": "string"
       }
      },
      "templateId": {
       "type": "string",
       "format": "uuid",
       "nullable": true
      }
     }
    }
   },
   "scopePath": {
    "type": "string"
   }
  }
 },
 "ExportFormat": {
  "type": "string",
  "enum": [
   "csv",
   "xlsx",
   "pdf",
   "json"
  ]
 },
 "FieldType": {
  "type": "string",
  "enum": [
   "string",
   "integer",
   "decimal",
   "money",
   "boolean",
   "date",
   "dateTime",
   "uuid",
   "enum"
  ]
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
 "MessageTemplate": {
  "x-ticvai-persistence": "marketing.message_template",
  "type": "object",
  "required": [
   "id",
   "code",
   "name",
   "channel",
   "bodies"
  ],
  "properties": {
   "id": {
    "readOnly": true,
    "type": "string",
    "format": "uuid"
   },
   "code": {
    "type": "string",
    "maxLength": 64
   },
   "name": {
    "type": "string",
    "maxLength": 200
   },
   "channel": {
    "$ref": "#/components/schemas/MessageChannel"
   },
   "subjects": {
    "type": "object",
    "description": "Per language. Email only.",
    "additionalProperties": {
     "type": "string"
    }
   },
   "bodies": {
    "type": "object",
    "description": "Per language, keyed by ISO 639-1 code.",
    "additionalProperties": {
     "type": "string"
    }
   },
   "mergeFields": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "missingLanguages": {
    "type": "array",
    "readOnly": true,
    "description": "Enabled languages without a body. Flagged rather than silently falling back — a guest receiving English when they chose Arabic is a defect.\n",
    "items": {
     "type": "string"
    }
   },
   "providerTemplateId": {
    "type": "string",
    "nullable": true,
    "description": "Required for WhatsApp, where templates are pre-approved by the provider."
   },
   "brandId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The brand whose identity the template carries; null for the tenant default."
   },
   "ownership": {
    "type": "string",
    "enum": [
     "platform",
     "crm"
    ],
    "default": "crm",
    "description": "`platform` = a transactional template owned by the communication service; `crm` = a marketing template owned by CRM (`listSystemTransactionalTemplate`). Content by language and version is in `MessageTemplateVersion`. (decided 29 September, data model for the agreed operations)"
   }
  }
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
 "ReportResult": {
  "x-ticvai-persistence": "none — result set, cached in object storage",
  "type": "object",
  "required": [
   "executionId",
   "columns",
   "rows"
  ],
  "properties": {
   "executionId": {
    "type": "string"
   },
   "columns": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "key": {
       "type": "string"
      },
      "label": {
       "type": "string"
      },
      "type": {
       "$ref": "#/components/schemas/FieldType"
      }
     }
    }
   },
   "rows": {
    "type": "array",
    "description": "**Open on purpose; the shape is `columns`.** Each row is keyed by `columns[].key`, and each value is of that column's `type` — money as a `Money`, dates, date-times and uuids as strings. A report's columns are chosen at run time, so no fixed schema can name them.\n",
    "items": {
     "type": "object",
     "additionalProperties": true
    }
   },
   "totals": {
    "type": "object",
    "additionalProperties": true,
    "description": "Aggregated columns only, keyed and typed as a row is."
   },
   "rowCount": {
    "type": "integer"
   },
   "nextCursor": {
    "type": "string",
    "nullable": true
   },
   "generatedAt": {
    "type": "string",
    "format": "date-time"
   },
   "dataAsOf": {
    "type": "string",
    "format": "date-time",
    "description": "Replica position the result was read at. Reporting reads a lag-tolerant replica, so this may trail the primary by seconds — stating it prevents an argument about a figure that moved.\n"
   }
  }
 },
 "RunReportRequest": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "properties": {
   "parameters": {
    "type": "object",
    "additionalProperties": true,
    "description": "**Open on purpose; its shape is the report's.** Keyed by `ReportParameter.key` of the definition being run, each value of that parameter's `type`. An `isRequired` parameter with no value here and no `defaultValue` is the `400` `runReport` lists.\n"
   },
   "venueId": {
    "type": "string",
    "format": "uuid",
    "description": "Narrows to one venue. Omitting it returns everything the caller's scope permits — it cannot be used to reach beyond that.\n"
   },
   "dateFrom": {
    "type": "string",
    "format": "date",
    "description": "Defaults to today in the venue's time zone when not sent (decided 28 September, audit R158)."
   },
   "dateTo": {
    "type": "string",
    "format": "date",
    "description": "Defaults to today in the venue's time zone when not sent (audit R158)."
   },
   "forceAsync": {
    "type": "boolean",
    "default": false,
    "description": "Queue regardless of size, for a result to be collected later."
   }
  }
 }
}
```
