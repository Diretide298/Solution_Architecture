# WS99 — Subscription Licensing AI Self Service board 2

**10 screens · 0 operations · 0 schemas · 0 permissions**

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

- **Every control that can be refused must be gated.** 0 permissions apply here:
  ``. A control nobody can use must say so,
  not sit enabled and fail.
- **0 of these operations work offline**
  
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `ADM-379` | Welcome & Start Your TICVAI Journey | configEditor | 0 | 0 | — |
| `ADM-380` | Customer & Organization Registration | listDetail | 0 | 0 | — |
| `ADM-381` | Venue Type & Business Profile | listDetail | 0 | 0 | — |
| `ADM-382` | Visitor, Capacity & Operational Scale | listDetail | 0 | 0 | — |
| `ADM-383` | Sales Channel Assessment | configEditor | 0 | 0 | — |
| `ADM-384` | Ticketing & Product Requirements | configEditor | 0 | 0 | — |
| `ADM-385` | Access, Queue & Visitor Experience Assessment | listDetail | 0 | 0 | — |
| `ADM-386` | Additional Business Module Assessment | listDetail | 0 | 0 | — |
| `ADM-387` | Integration, Payment & Technical Readiness | listDetail | 0 | 0 | — |
| `ADM-388` | AI Assessment Summary & Handoff | listDetail | 0 | 0 | — |

## Thin screens in this batch

**ADM-380, ADM-381, ADM-382, ADM-385, ADM-386, ADM-387, ADM-388 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "ADM-379",
  "name": "Welcome & Start Your TICVAI Journey",
  "module": "Tenants & Licensing",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Subscription_Licensing_AI_Self_Service.pdf",
   "board": "2",
   "number": "1",
   "page": 21
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/tenants-licensing/welcome-start-your-ticvai-journey-adm-379",
   "component": "apps/ticvai-web/src/routes/tenants-licensing/WelcomeStartYourTicvaiJourney.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-002"
   ],
   "exitTo": [
    "ADM-002",
    "ADM-380",
    "ADM-381",
    "ADM-382",
    "ADM-383",
    "ADM-384",
    "ADM-385",
    "ADM-386",
    "ADM-387",
    "ADM-388"
   ],
   "transitions": [
    {
     "to": "ADM-002",
     "trigger": "Back to Platform Dashboard",
     "provenance": "structural — pack board 2 wiring, 11 September 2026",
     "back": true
    },
    {
     "to": "ADM-380",
     "trigger": "Customer & Organization Registration",
     "provenance": "structural — pack board 2 wiring, 11 September 2026"
    },
    {
     "to": "ADM-381",
     "trigger": "Venue Type & Business Profile",
     "provenance": "structural — pack board 2 wiring, 11 September 2026"
    },
    {
     "to": "ADM-382",
     "trigger": "Visitor, Capacity & Operational Scale",
     "provenance": "structural — pack board 2 wiring, 11 September 2026"
    },
    {
     "to": "ADM-383",
     "trigger": "Sales Channel Assessment",
     "provenance": "structural — pack board 2 wiring, 11 September 2026"
    },
    {
     "to": "ADM-384",
     "trigger": "Ticketing & Product Requirements",
     "provenance": "structural — pack board 2 wiring, 11 September 2026"
    },
    {
     "to": "ADM-385",
     "trigger": "Access, Queue & Visitor Experience Assessment",
     "provenance": "structural — pack board 2 wiring, 11 September 2026"
    },
    {
     "to": "ADM-386",
     "trigger": "Additional Business Module Assessment",
     "provenance": "structural — pack board 2 wiring, 11 September 2026"
    },
    {
     "to": "ADM-387",
     "trigger": "Integration, Payment & Technical Readiness",
     "provenance": "structural — pack board 2 wiring, 11 September 2026"
    },
    {
     "to": "ADM-388",
     "trigger": "AI Assessment Summary & Handoff",
     "provenance": "structural — pack board 2 wiring, 11 September 2026"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Starting Options) and no display directory — it is settings, not a population",
  "purpose": "Provide the entry point for a new customer starting self-service onboarding.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Start New Setup",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 21 §Starting Options"
      },
      {
       "kind": "selectField",
       "label": "Continue Saved Setup",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 21 §Starting Options"
      },
      {
       "kind": "selectField",
       "label": "Sign In",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 21 §Starting Options"
      },
      {
       "kind": "selectField",
       "label": "Request Enterprise Consultation",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 21 §Starting Options"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The welcome start your configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the welcome start your untouched.",
   "emptyFirstRun": "No welcome start your configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-379"
  },
  "apisNote": "Regenerated 9 September 2026 from Subscription_Licensing_AI_Self_Service.pdf page 21. 0 of 0 labels bound to a contract property; 4 of 16 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-380",
  "name": "Customer & Organization Registration",
  "module": "Tenants & Licensing",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Subscription_Licensing_AI_Self_Service.pdf",
   "board": "2",
   "number": "2",
   "page": 22
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/tenants-licensing/customer-organization-registration-adm-380",
   "component": "apps/ticvai-web/src/routes/tenants-licensing/CustomerOrganizationRegistration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-379"
   ],
   "exitTo": [
    "ADM-379"
   ],
   "transitions": [
    {
     "to": "ADM-379",
     "trigger": "Back to Welcome & Start Your TICVAI Journey",
     "provenance": "structural — pack board 2 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Create the initial customer account and organization profile.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Subscription_Licensing_AI_Self_Service.pdf, page 22"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Subscription_Licensing_AI_Self_Service.pdf, page 22"
   }
  ],
  "layout": {
   "template": "split",
   "regions": []
  },
  "states": {
   "loading": "The customer organization registration list.",
   "error": "Could not load. Names which read failed and leaves the customer organization registration untouched.",
   "emptyFirstRun": "No customer organization registration yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the customer organization registration are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-380"
  },
  "apisNote": "Regenerated 9 September 2026 from Subscription_Licensing_AI_Self_Service.pdf page 22. 0 of 0 labels bound to a contract property; 0 of 22 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-381",
  "name": "Venue Type & Business Profile",
  "module": "Tenants & Licensing",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Subscription_Licensing_AI_Self_Service.pdf",
   "board": "2",
   "number": "3",
   "page": 23
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/tenants-licensing/venue-type-business-profile-adm-381",
   "component": "apps/ticvai-web/src/routes/tenants-licensing/VenueTypeBusinessProfile.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-379"
   ],
   "exitTo": [
    "ADM-379"
   ],
   "transitions": [
    {
     "to": "ADM-379",
     "trigger": "Back to Welcome & Start Your TICVAI Journey",
     "provenance": "structural — pack board 2 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Visual cards) and no metric row",
  "purpose": "Understand what type of operation the customer runs.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Subscription_Licensing_AI_Self_Service.pdf, page 23 §Visual cards"
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
       "label": "Every venue type business",
       "columns": [
        "Museum",
        "Attraction",
        "Theme Park",
        "Waterpark",
        "Stadium",
        "Theatre",
        "Exhibition / Event Venue",
        "Zoo / Aquarium",
        "Tour Operator",
        "Entertainment Center",
        "Multi-Venue Operator",
        "Other"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 23 §Visual cards"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected venue type business",
       "bindsTo": null,
       "columns": [
        "Museum",
        "Attraction",
        "Theme Park",
        "Waterpark",
        "Stadium",
        "Theatre",
        "Exhibition / Event Venue",
        "Zoo / Aquarium",
        "Tour Operator",
        "Entertainment Center",
        "Multi-Venue Operator",
        "Other"
       ],
       "notes": null,
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 23 §Visual cards"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The venue type business list.",
   "error": "Could not load. Names which read failed and leaves the venue type business untouched.",
   "emptyFirstRun": "No venue type business yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the venue type business are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "entryState": {
   "preloaded": [
    "Museum",
    "Attraction",
    "Theme Park",
    "Waterpark",
    "Stadium",
    "Theatre"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-381"
  },
  "apisNote": "Regenerated 9 September 2026 from Subscription_Licensing_AI_Self_Service.pdf page 23. 0 of 12 labels bound to a contract property; 19 of 22 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-382",
  "name": "Visitor, Capacity & Operational Scale",
  "module": "Tenants & Licensing",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Subscription_Licensing_AI_Self_Service.pdf",
   "board": "2",
   "number": "4",
   "page": 23
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/tenants-licensing/visitor-capacity-operational-scale-adm-382",
   "component": "apps/ticvai-web/src/routes/tenants-licensing/VisitorCapacityOperationalScale.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-379"
   ],
   "exitTo": [
    "ADM-379"
   ],
   "transitions": [
    {
     "to": "ADM-379",
     "trigger": "Back to Welcome & Start Your TICVAI Journey",
     "provenance": "structural — pack board 2 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Collect the information required to understand venue size and eventually calculate the VSI.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Subscription_Licensing_AI_Self_Service.pdf, page 23"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Subscription_Licensing_AI_Self_Service.pdf, page 23"
   }
  ],
  "layout": {
   "template": "split",
   "regions": []
  },
  "states": {
   "loading": "The visitor capacity operational list.",
   "error": "Could not load. Names which read failed and leaves the visitor capacity operational untouched.",
   "emptyFirstRun": "No visitor capacity operational yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the visitor capacity operational are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-382"
  },
  "apisNote": "Regenerated 9 September 2026 from Subscription_Licensing_AI_Self_Service.pdf page 23. 0 of 0 labels bound to a contract property; 0 of 24 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-383",
  "name": "Sales Channel Assessment",
  "module": "Tenants & Licensing",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Subscription_Licensing_AI_Self_Service.pdf",
   "board": "2",
   "number": "5",
   "page": 24
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/tenants-licensing/sales-channel-assessment-adm-383",
   "component": "apps/ticvai-web/src/routes/tenants-licensing/SalesChannelAssessment.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-379"
   ],
   "exitTo": [
    "ADM-379"
   ],
   "transitions": [
    {
     "to": "ADM-379",
     "trigger": "Back to Welcome & Start Your TICVAI Journey",
     "provenance": "structural — pack board 2 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Selectable options) and no display directory — it is settings, not a population",
  "purpose": "Understand how the customer intends to sell tickets and products.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "☐ On-site POS",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 24 §Selectable options"
      },
      {
       "kind": "textField",
       "label": "☐ Own Website / B2C",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 24 §Selectable options"
      },
      {
       "kind": "selectField",
       "label": "☐ Mobile App",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 24 §Selectable options"
      },
      {
       "kind": "selectField",
       "label": "☐ Tour Operators",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 24 §Selectable options"
      },
      {
       "kind": "selectField",
       "label": "☐ Hotels",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 24 §Selectable options"
      },
      {
       "kind": "selectField",
       "label": "☐ Resellers",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 24 §Selectable options"
      },
      {
       "kind": "selectField",
       "label": "☐ Corporate Customers",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 24 §Selectable options"
      },
      {
       "kind": "selectField",
       "label": "☐ Call Center",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 24 §Selectable options"
      },
      {
       "kind": "selectField",
       "label": "☐ Kiosk",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 24 §Selectable options"
      },
      {
       "kind": "textField",
       "label": "☐ Flying / Mobile POS",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 24 §Selectable options"
      },
      {
       "kind": "textField",
       "label": "☐ OTA / Third-Party Channels",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 24 §Selectable options"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The sales channel assessment configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the sales channel assessment untouched.",
   "emptyFirstRun": "No sales channel assessment configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-383"
  },
  "apisNote": "Regenerated 9 September 2026 from Subscription_Licensing_AI_Self_Service.pdf page 24. 0 of 0 labels bound to a contract property; 11 of 21 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-384",
  "name": "Ticketing & Product Requirements",
  "module": "Tenants & Licensing",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Subscription_Licensing_AI_Self_Service.pdf",
   "board": "2",
   "number": "6",
   "page": 25
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/tenants-licensing/ticketing-product-requirements-adm-384",
   "component": "apps/ticvai-web/src/routes/tenants-licensing/TicketingProductRequirements.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-379"
   ],
   "exitTo": [
    "ADM-379"
   ],
   "transitions": [
    {
     "to": "ADM-379",
     "trigger": "Back to Welcome & Start Your TICVAI Journey",
     "provenance": "structural — pack board 2 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Selectable options) and no display directory — it is settings, not a population",
  "purpose": "Understand what the venue intends to sell.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "General Admission",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 25 §Selectable options"
      },
      {
       "kind": "selectField",
       "label": "Dated Admission",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 25 §Selectable options"
      },
      {
       "kind": "selectField",
       "label": "Timeslot Admission",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 25 §Selectable options"
      },
      {
       "kind": "selectField",
       "label": "Open-Dated Ticket",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 25 §Selectable options"
      },
      {
       "kind": "selectField",
       "label": "Multi-Day Ticket",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 25 §Selectable options"
      },
      {
       "kind": "selectField",
       "label": "Family Ticket",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 25 §Selectable options"
      },
      {
       "kind": "selectField",
       "label": "Group Ticket",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 25 §Selectable options"
      },
      {
       "kind": "selectField",
       "label": "Membership",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 25 §Selectable options"
      },
      {
       "kind": "selectField",
       "label": "Annual Pass",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 25 §Selectable options"
      },
      {
       "kind": "selectField",
       "label": "Season Pass",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 25 §Selectable options"
      },
      {
       "kind": "selectField",
       "label": "Voucher",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 25 §Selectable options"
      },
      {
       "kind": "selectField",
       "label": "Bundle",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 25 §Selectable options"
      },
      {
       "kind": "selectField",
       "label": "Add-On",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 25 §Selectable options"
      },
      {
       "kind": "selectField",
       "label": "Camp / Course",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 25 §Selectable options"
      },
      {
       "kind": "selectField",
       "label": "Special Event",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 25 §Selectable options"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The ticketing product requirements configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the ticketing product requirements untouched.",
   "emptyFirstRun": "No ticketing product requirements configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-384"
  },
  "apisNote": "Regenerated 9 September 2026 from Subscription_Licensing_AI_Self_Service.pdf page 25. 0 of 0 labels bound to a contract property; 15 of 27 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-385",
  "name": "Access, Queue & Visitor Experience Assessment",
  "module": "Tenants & Licensing",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Subscription_Licensing_AI_Self_Service.pdf",
   "board": "2",
   "number": "7",
   "page": 26
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/tenants-licensing/access-queue-visitor-experience-assessment-adm-385",
   "component": "apps/ticvai-web/src/routes/tenants-licensing/AccessQueueVisitorExperienceAssessment.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-379"
   ],
   "exitTo": [
    "ADM-379"
   ],
   "transitions": [
    {
     "to": "ADM-379",
     "trigger": "Back to Welcome & Start Your TICVAI Journey",
     "provenance": "structural — pack board 2 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Determine admission and visitor-flow requirements.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Subscription_Licensing_AI_Self_Service.pdf, page 26"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Subscription_Licensing_AI_Self_Service.pdf, page 26"
   }
  ],
  "layout": {
   "template": "split",
   "regions": []
  },
  "states": {
   "loading": "The access queue visitor list.",
   "error": "Could not load. Names which read failed and leaves the access queue visitor untouched.",
   "emptyFirstRun": "No access queue visitor yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the access queue visitor are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-385"
  },
  "apisNote": "Regenerated 9 September 2026 from Subscription_Licensing_AI_Self_Service.pdf page 26. 0 of 0 labels bound to a contract property; 0 of 22 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-386",
  "name": "Additional Business Module Assessment",
  "module": "Tenants & Licensing",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Subscription_Licensing_AI_Self_Service.pdf",
   "board": "2",
   "number": "8",
   "page": 27
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/tenants-licensing/additional-business-module-assessment-adm-386",
   "component": "apps/ticvai-web/src/routes/tenants-licensing/AdditionalBusinessModuleAssessment.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-379"
   ],
   "exitTo": [
    "ADM-379"
   ],
   "transitions": [
    {
     "to": "ADM-379",
     "trigger": "Back to Welcome & Start Your TICVAI Journey",
     "provenance": "structural — pack board 2 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Identify additional TICVAI operational modules based on the customer's business.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Subscription_Licensing_AI_Self_Service.pdf, page 27"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Subscription_Licensing_AI_Self_Service.pdf, page 27"
   }
  ],
  "layout": {
   "template": "split",
   "regions": []
  },
  "states": {
   "loading": "The additional business module list.",
   "error": "Could not load. Names which read failed and leaves the additional business module untouched.",
   "emptyFirstRun": "No additional business module yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the additional business module are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-386"
  },
  "apisNote": "Regenerated 9 September 2026 from Subscription_Licensing_AI_Self_Service.pdf page 27. 0 of 0 labels bound to a contract property; 0 of 22 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-387",
  "name": "Integration, Payment & Technical Readiness",
  "module": "Tenants & Licensing",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Subscription_Licensing_AI_Self_Service.pdf",
   "board": "2",
   "number": "9",
   "page": 28
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/tenants-licensing/integration-payment-technical-readiness-adm-387",
   "component": "apps/ticvai-web/src/routes/tenants-licensing/IntegrationPaymentTechnicalReadiness.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-379"
   ],
   "exitTo": [
    "ADM-379"
   ],
   "transitions": [
    {
     "to": "ADM-379",
     "trigger": "Back to Welcome & Start Your TICVAI Journey",
     "provenance": "structural — pack board 2 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Understand external systems and technical requirements that could affect complexity, implementation approach and commercial scope.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Subscription_Licensing_AI_Self_Service.pdf, page 28"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Subscription_Licensing_AI_Self_Service.pdf, page 28"
   }
  ],
  "layout": {
   "template": "split",
   "regions": []
  },
  "states": {
   "loading": "The integration payment technical list.",
   "error": "Could not load. Names which read failed and leaves the integration payment technical untouched.",
   "emptyFirstRun": "No integration payment technical yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the integration payment technical are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-387"
  },
  "apisNote": "Regenerated 9 September 2026 from Subscription_Licensing_AI_Self_Service.pdf page 28. 0 of 0 labels bound to a contract property; 0 of 31 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-388",
  "name": "AI Assessment Summary & Handoff",
  "module": "Tenants & Licensing",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Subscription_Licensing_AI_Self_Service.pdf",
   "board": "2",
   "number": "10",
   "page": 29
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/tenants-licensing/ai-assessment-summary-handoff-adm-388",
   "component": "apps/ticvai-web/src/routes/tenants-licensing/AiAssessmentSummaryHandoff.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-379"
   ],
   "exitTo": [
    "ADM-379"
   ],
   "transitions": [
    {
     "to": "ADM-379",
     "trigger": "Back to Welcome & Start Your TICVAI Journey",
     "provenance": "structural — pack board 2 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Consolidate everything learned during onboarding and prepare the customer for Board 3/4 commercial recommendation.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Subscription_Licensing_AI_Self_Service.pdf, page 29"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Subscription_Licensing_AI_Self_Service.pdf, page 29"
   }
  ],
  "layout": {
   "template": "split",
   "regions": []
  },
  "states": {
   "loading": "The assessment summary handoff list.",
   "error": "Could not load. Names which read failed and leaves the assessment summary handoff untouched.",
   "emptyFirstRun": "No assessment summary handoff yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the assessment summary handoff are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-388"
  },
  "apisNote": "Regenerated 9 September 2026 from Subscription_Licensing_AI_Self_Service.pdf page 29. 0 of 0 labels bound to a contract property; 0 of 63 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
{}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{}
```
