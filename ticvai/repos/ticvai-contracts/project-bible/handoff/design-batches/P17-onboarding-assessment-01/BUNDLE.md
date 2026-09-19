# P17-onboarding-assessment-01 — P17 · Onboarding & Assessment

**10 screens · 0 operations · 0 schemas · 0 permissions**

Platform P17 TICVAI Sign-up · ships as **ticvai-control** ·
public audience · web ·
online only

## Who this is for

**public on web.** Everything below is how you know what is
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
| `SGN-001` | Welcome & Start Your TICVAI Journey | configEditor | 0 | 0 | — |
| `SGN-002` | Customer & Organization Registration | listDetail | 0 | 0 | — |
| `SGN-003` | Venue Type & Business Profile | listDetail | 0 | 0 | — |
| `SGN-004` | Visitor, Capacity & Operational Scale | listDetail | 0 | 0 | — |
| `SGN-005` | Sales Channel Assessment | configEditor | 0 | 0 | — |
| `SGN-006` | Ticketing & Product Requirements | configEditor | 0 | 0 | — |
| `SGN-007` | Access, Queue & Visitor Experience Assessment | listDetail | 0 | 0 | — |
| `SGN-008` | Additional Business Module Assessment | listDetail | 0 | 0 | — |
| `SGN-009` | Integration, Payment & Technical Readiness | listDetail | 0 | 0 | — |
| `SGN-010` | AI Assessment Summary & Handoff | listDetail | 0 | 0 | — |

## Thin screens in this batch

**SGN-002, SGN-003, SGN-004, SGN-007, SGN-008, SGN-009, SGN-010 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "SGN-001",
  "name": "Welcome & Start Your TICVAI Journey",
  "module": "Onboarding & Assessment",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "sameAs": "ADM-379",
   "book": "Subscription_Licensing_AI_Self_Service.pdf",
   "board": "2",
   "number": "1",
   "page": 21
  },
  "implementation": {
   "app": "signup-web",
   "route": "/onboarding-assessment/welcome-start-your-ticvai-journey-sgn-001",
   "component": "apps/signup-web/src/routes/onboarding-assessment/WelcomeStartYourTicvaiJourney.tsx",
   "status": "notStarted"
  },
  "density": "compact",
  "notes": "The self-service form of `ADM-379`, for a prospect with no account. Decided 11 September 2026; P09 keeps its screen for the operator-led path (BL-165). `tools/applied/apply-subscription-placement.py` keeps the two in step.",
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P17 TICVAI Sign-up.dc.html#sgn-001"
  },
  "purpose": "Provide the entry point for a new customer starting self-service onboarding.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Starting Options) and no display directory — it is settings, not a population",
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
   "emptyNoAccess": "TODO — not decided. A prospect is signed out and holds no permission, so the operator wording on the P09 twin does not apply. The book offers *Continue Saved Setup* and *Sign In* on 2.1, which is where somebody without access to a saved setup would be sent; no minute has decided it.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [],
  "apisNote": "Regenerated 9 September 2026 from Subscription_Licensing_AI_Self_Service.pdf page 21. 0 of 0 labels bound to a contract property; 4 of 16 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "navigation": {
   "isEntryPoint": true,
   "exitTo": [
    "SGN-002"
   ],
   "transitions": [
    {
     "to": "SGN-002",
     "trigger": "Customer & Organization Registration",
     "provenance": "structural — the book's own journey, 2.1 \"Journey Preview\", 11 September 2026"
    }
   ],
   "entryFrom": [
    "SGN-002"
   ]
  },
  "_platform": {
   "code": "P17",
   "audience": "public",
   "formFactor": "web",
   "shortName": "TICVAI Sign-up",
   "name": "TICVAI Sign-up — Onboarding & Purchase",
   "offlineCapable": false,
   "app": "signup-web",
   "operator": "public",
   "targetApp": {
    "app": "ticvai-control",
    "name": "TICVAI Control",
    "shell": "web",
    "siblings": [
     "P09",
     "P10",
     "P11",
     "P14"
    ],
    "note": "**TICVAI operates all five**, whoever signs in. The partner portal, the accreditation intake, the developer portal and the sign-up are outward faces of the control plane, not separate products — but their users are not TICVAI staff, and the permission model has to hold that line. **P17 added 11 September 2026**: a prospect buying TICVAI has no tenant and no cell, so the control plane is the only thing that can serve them.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "SGN-002",
  "name": "Customer & Organization Registration",
  "module": "Onboarding & Assessment",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "sameAs": "ADM-380",
   "book": "Subscription_Licensing_AI_Self_Service.pdf",
   "board": "2",
   "number": "2",
   "page": 22
  },
  "implementation": {
   "app": "signup-web",
   "route": "/onboarding-assessment/customer-organization-registration-sgn-002",
   "component": "apps/signup-web/src/routes/onboarding-assessment/CustomerOrganizationRegistration.tsx",
   "status": "notStarted"
  },
  "density": "compact",
  "notes": "The self-service form of `ADM-380`, for a prospect with no account. Decided 11 September 2026; P09 keeps its screen for the operator-led path (BL-165). `tools/applied/apply-subscription-placement.py` keeps the two in step.",
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P17 TICVAI Sign-up.dc.html#sgn-002"
  },
  "purpose": "Create the initial customer account and organization profile.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "layout": {
   "template": "split",
   "regions": []
  },
  "states": {
   "loading": "The customer organization registration list.",
   "error": "Could not load. Names which read failed and leaves the customer organization registration untouched.",
   "emptyFirstRun": "No customer organization registration yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the customer organization registration are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "TODO — not decided. A prospect is signed out and holds no permission, so the operator wording on the P09 twin does not apply. The book offers *Continue Saved Setup* and *Sign In* on 2.1, which is where somebody without access to a saved setup would be sent; no minute has decided it."
  },
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
  "apis": [],
  "apisNote": "Regenerated 9 September 2026 from Subscription_Licensing_AI_Self_Service.pdf page 22. 0 of 0 labels bound to a contract property; 0 of 22 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "navigation": {
   "entryFrom": [
    "SGN-001",
    "SGN-003"
   ],
   "exitTo": [
    "SGN-001",
    "SGN-003"
   ],
   "transitions": [
    {
     "to": "SGN-001",
     "trigger": "Back to Welcome & Start Your TICVAI Journey",
     "provenance": "structural — the book's own journey, 2.1 \"Journey Preview\", 11 September 2026",
     "back": true
    },
    {
     "to": "SGN-003",
     "trigger": "Venue Type & Business Profile",
     "provenance": "structural — the book's own journey, 2.1 \"Journey Preview\", 11 September 2026"
    }
   ]
  },
  "_platform": {
   "code": "P17",
   "audience": "public",
   "formFactor": "web",
   "shortName": "TICVAI Sign-up",
   "name": "TICVAI Sign-up — Onboarding & Purchase",
   "offlineCapable": false,
   "app": "signup-web",
   "operator": "public",
   "targetApp": {
    "app": "ticvai-control",
    "name": "TICVAI Control",
    "shell": "web",
    "siblings": [
     "P09",
     "P10",
     "P11",
     "P14"
    ],
    "note": "**TICVAI operates all five**, whoever signs in. The partner portal, the accreditation intake, the developer portal and the sign-up are outward faces of the control plane, not separate products — but their users are not TICVAI staff, and the permission model has to hold that line. **P17 added 11 September 2026**: a prospect buying TICVAI has no tenant and no cell, so the control plane is the only thing that can serve them.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "SGN-003",
  "name": "Venue Type & Business Profile",
  "module": "Onboarding & Assessment",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "sameAs": "ADM-381",
   "book": "Subscription_Licensing_AI_Self_Service.pdf",
   "board": "2",
   "number": "3",
   "page": 23
  },
  "implementation": {
   "app": "signup-web",
   "route": "/onboarding-assessment/venue-type-business-profile-sgn-003",
   "component": "apps/signup-web/src/routes/onboarding-assessment/VenueTypeBusinessProfile.tsx",
   "status": "notStarted"
  },
  "density": "compact",
  "notes": "The self-service form of `ADM-381`, for a prospect with no account. Decided 11 September 2026; P09 keeps its screen for the operator-led path (BL-165). `tools/applied/apply-subscription-placement.py` keeps the two in step.",
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P17 TICVAI Sign-up.dc.html#sgn-003"
  },
  "purpose": "Understand what type of operation the customer runs.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Visual cards) and no metric row",
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
   "emptyNoAccess": "TODO — not decided. A prospect is signed out and holds no permission, so the operator wording on the P09 twin does not apply. The book offers *Continue Saved Setup* and *Sign In* on 2.1, which is where somebody without access to a saved setup would be sent; no minute has decided it."
  },
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Subscription_Licensing_AI_Self_Service.pdf, page 23 §Visual cards"
   }
  ],
  "apis": [],
  "apisNote": "Regenerated 9 September 2026 from Subscription_Licensing_AI_Self_Service.pdf page 23. 0 of 12 labels bound to a contract property; 19 of 22 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "navigation": {
   "entryFrom": [
    "SGN-002",
    "SGN-004"
   ],
   "exitTo": [
    "SGN-002",
    "SGN-004"
   ],
   "transitions": [
    {
     "to": "SGN-002",
     "trigger": "Back to Customer & Organization Registration",
     "provenance": "structural — the book's own journey, 2.1 \"Journey Preview\", 11 September 2026",
     "back": true
    },
    {
     "to": "SGN-004",
     "trigger": "Visitor, Capacity & Operational Scale",
     "provenance": "structural — the book's own journey, 2.1 \"Journey Preview\", 11 September 2026"
    }
   ]
  },
  "_platform": {
   "code": "P17",
   "audience": "public",
   "formFactor": "web",
   "shortName": "TICVAI Sign-up",
   "name": "TICVAI Sign-up — Onboarding & Purchase",
   "offlineCapable": false,
   "app": "signup-web",
   "operator": "public",
   "targetApp": {
    "app": "ticvai-control",
    "name": "TICVAI Control",
    "shell": "web",
    "siblings": [
     "P09",
     "P10",
     "P11",
     "P14"
    ],
    "note": "**TICVAI operates all five**, whoever signs in. The partner portal, the accreditation intake, the developer portal and the sign-up are outward faces of the control plane, not separate products — but their users are not TICVAI staff, and the permission model has to hold that line. **P17 added 11 September 2026**: a prospect buying TICVAI has no tenant and no cell, so the control plane is the only thing that can serve them.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "SGN-004",
  "name": "Visitor, Capacity & Operational Scale",
  "module": "Onboarding & Assessment",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "sameAs": "ADM-382",
   "book": "Subscription_Licensing_AI_Self_Service.pdf",
   "board": "2",
   "number": "4",
   "page": 23
  },
  "implementation": {
   "app": "signup-web",
   "route": "/onboarding-assessment/visitor-capacity-operational-scale-sgn-004",
   "component": "apps/signup-web/src/routes/onboarding-assessment/VisitorCapacityOperationalScale.tsx",
   "status": "notStarted"
  },
  "density": "compact",
  "notes": "The self-service form of `ADM-382`, for a prospect with no account. Decided 11 September 2026; P09 keeps its screen for the operator-led path (BL-165). `tools/applied/apply-subscription-placement.py` keeps the two in step.",
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P17 TICVAI Sign-up.dc.html#sgn-004"
  },
  "purpose": "Collect the information required to understand venue size and eventually calculate the VSI.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "layout": {
   "template": "split",
   "regions": []
  },
  "states": {
   "loading": "The visitor capacity operational list.",
   "error": "Could not load. Names which read failed and leaves the visitor capacity operational untouched.",
   "emptyFirstRun": "No visitor capacity operational yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the visitor capacity operational are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "TODO — not decided. A prospect is signed out and holds no permission, so the operator wording on the P09 twin does not apply. The book offers *Continue Saved Setup* and *Sign In* on 2.1, which is where somebody without access to a saved setup would be sent; no minute has decided it."
  },
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
  "apis": [],
  "apisNote": "Regenerated 9 September 2026 from Subscription_Licensing_AI_Self_Service.pdf page 23. 0 of 0 labels bound to a contract property; 0 of 24 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "navigation": {
   "entryFrom": [
    "SGN-003",
    "SGN-005"
   ],
   "exitTo": [
    "SGN-003",
    "SGN-005"
   ],
   "transitions": [
    {
     "to": "SGN-003",
     "trigger": "Back to Venue Type & Business Profile",
     "provenance": "structural — the book's own journey, 2.1 \"Journey Preview\", 11 September 2026",
     "back": true
    },
    {
     "to": "SGN-005",
     "trigger": "Sales Channel Assessment",
     "provenance": "structural — the book's own journey, 2.1 \"Journey Preview\", 11 September 2026"
    }
   ]
  },
  "_platform": {
   "code": "P17",
   "audience": "public",
   "formFactor": "web",
   "shortName": "TICVAI Sign-up",
   "name": "TICVAI Sign-up — Onboarding & Purchase",
   "offlineCapable": false,
   "app": "signup-web",
   "operator": "public",
   "targetApp": {
    "app": "ticvai-control",
    "name": "TICVAI Control",
    "shell": "web",
    "siblings": [
     "P09",
     "P10",
     "P11",
     "P14"
    ],
    "note": "**TICVAI operates all five**, whoever signs in. The partner portal, the accreditation intake, the developer portal and the sign-up are outward faces of the control plane, not separate products — but their users are not TICVAI staff, and the permission model has to hold that line. **P17 added 11 September 2026**: a prospect buying TICVAI has no tenant and no cell, so the control plane is the only thing that can serve them.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "SGN-005",
  "name": "Sales Channel Assessment",
  "module": "Onboarding & Assessment",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "sameAs": "ADM-383",
   "book": "Subscription_Licensing_AI_Self_Service.pdf",
   "board": "2",
   "number": "5",
   "page": 24
  },
  "implementation": {
   "app": "signup-web",
   "route": "/onboarding-assessment/sales-channel-assessment-sgn-005",
   "component": "apps/signup-web/src/routes/onboarding-assessment/SalesChannelAssessment.tsx",
   "status": "notStarted"
  },
  "density": "compact",
  "notes": "The self-service form of `ADM-383`, for a prospect with no account. Decided 11 September 2026; P09 keeps its screen for the operator-led path (BL-165). `tools/applied/apply-subscription-placement.py` keeps the two in step.",
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P17 TICVAI Sign-up.dc.html#sgn-005"
  },
  "purpose": "Understand how the customer intends to sell tickets and products.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Selectable options) and no display directory — it is settings, not a population",
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
   "emptyNoAccess": "TODO — not decided. A prospect is signed out and holds no permission, so the operator wording on the P09 twin does not apply. The book offers *Continue Saved Setup* and *Sign In* on 2.1, which is where somebody without access to a saved setup would be sent; no minute has decided it.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [],
  "apisNote": "Regenerated 9 September 2026 from Subscription_Licensing_AI_Self_Service.pdf page 24. 0 of 0 labels bound to a contract property; 11 of 21 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "navigation": {
   "entryFrom": [
    "SGN-004",
    "SGN-006"
   ],
   "exitTo": [
    "SGN-004",
    "SGN-006"
   ],
   "transitions": [
    {
     "to": "SGN-004",
     "trigger": "Back to Visitor, Capacity & Operational Scale",
     "provenance": "structural — the book's own journey, 2.1 \"Journey Preview\", 11 September 2026",
     "back": true
    },
    {
     "to": "SGN-006",
     "trigger": "Ticketing & Product Requirements",
     "provenance": "structural — the book's own journey, 2.1 \"Journey Preview\", 11 September 2026"
    }
   ]
  },
  "_platform": {
   "code": "P17",
   "audience": "public",
   "formFactor": "web",
   "shortName": "TICVAI Sign-up",
   "name": "TICVAI Sign-up — Onboarding & Purchase",
   "offlineCapable": false,
   "app": "signup-web",
   "operator": "public",
   "targetApp": {
    "app": "ticvai-control",
    "name": "TICVAI Control",
    "shell": "web",
    "siblings": [
     "P09",
     "P10",
     "P11",
     "P14"
    ],
    "note": "**TICVAI operates all five**, whoever signs in. The partner portal, the accreditation intake, the developer portal and the sign-up are outward faces of the control plane, not separate products — but their users are not TICVAI staff, and the permission model has to hold that line. **P17 added 11 September 2026**: a prospect buying TICVAI has no tenant and no cell, so the control plane is the only thing that can serve them.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "SGN-006",
  "name": "Ticketing & Product Requirements",
  "module": "Onboarding & Assessment",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "sameAs": "ADM-384",
   "book": "Subscription_Licensing_AI_Self_Service.pdf",
   "board": "2",
   "number": "6",
   "page": 25
  },
  "implementation": {
   "app": "signup-web",
   "route": "/onboarding-assessment/ticketing-product-requirements-sgn-006",
   "component": "apps/signup-web/src/routes/onboarding-assessment/TicketingProductRequirements.tsx",
   "status": "notStarted"
  },
  "density": "compact",
  "notes": "The self-service form of `ADM-384`, for a prospect with no account. Decided 11 September 2026; P09 keeps its screen for the operator-led path (BL-165). `tools/applied/apply-subscription-placement.py` keeps the two in step.",
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P17 TICVAI Sign-up.dc.html#sgn-006"
  },
  "purpose": "Understand what the venue intends to sell.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Selectable options) and no display directory — it is settings, not a population",
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
   "emptyNoAccess": "TODO — not decided. A prospect is signed out and holds no permission, so the operator wording on the P09 twin does not apply. The book offers *Continue Saved Setup* and *Sign In* on 2.1, which is where somebody without access to a saved setup would be sent; no minute has decided it.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [],
  "apisNote": "Regenerated 9 September 2026 from Subscription_Licensing_AI_Self_Service.pdf page 25. 0 of 0 labels bound to a contract property; 15 of 27 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "navigation": {
   "entryFrom": [
    "SGN-005",
    "SGN-007"
   ],
   "exitTo": [
    "SGN-005",
    "SGN-007"
   ],
   "transitions": [
    {
     "to": "SGN-005",
     "trigger": "Back to Sales Channel Assessment",
     "provenance": "structural — the book's own journey, 2.1 \"Journey Preview\", 11 September 2026",
     "back": true
    },
    {
     "to": "SGN-007",
     "trigger": "Access, Queue & Visitor Experience Assessment",
     "provenance": "structural — the book's own journey, 2.1 \"Journey Preview\", 11 September 2026"
    }
   ]
  },
  "_platform": {
   "code": "P17",
   "audience": "public",
   "formFactor": "web",
   "shortName": "TICVAI Sign-up",
   "name": "TICVAI Sign-up — Onboarding & Purchase",
   "offlineCapable": false,
   "app": "signup-web",
   "operator": "public",
   "targetApp": {
    "app": "ticvai-control",
    "name": "TICVAI Control",
    "shell": "web",
    "siblings": [
     "P09",
     "P10",
     "P11",
     "P14"
    ],
    "note": "**TICVAI operates all five**, whoever signs in. The partner portal, the accreditation intake, the developer portal and the sign-up are outward faces of the control plane, not separate products — but their users are not TICVAI staff, and the permission model has to hold that line. **P17 added 11 September 2026**: a prospect buying TICVAI has no tenant and no cell, so the control plane is the only thing that can serve them.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "SGN-007",
  "name": "Access, Queue & Visitor Experience Assessment",
  "module": "Onboarding & Assessment",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "sameAs": "ADM-385",
   "book": "Subscription_Licensing_AI_Self_Service.pdf",
   "board": "2",
   "number": "7",
   "page": 26
  },
  "implementation": {
   "app": "signup-web",
   "route": "/onboarding-assessment/access-queue-visitor-experience-assessment-sgn-007",
   "component": "apps/signup-web/src/routes/onboarding-assessment/AccessQueueVisitorExperienceAssessment.tsx",
   "status": "notStarted"
  },
  "density": "compact",
  "notes": "The self-service form of `ADM-385`, for a prospect with no account. Decided 11 September 2026; P09 keeps its screen for the operator-led path (BL-165). `tools/applied/apply-subscription-placement.py` keeps the two in step.",
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P17 TICVAI Sign-up.dc.html#sgn-007"
  },
  "purpose": "Determine admission and visitor-flow requirements.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "layout": {
   "template": "split",
   "regions": []
  },
  "states": {
   "loading": "The access queue visitor list.",
   "error": "Could not load. Names which read failed and leaves the access queue visitor untouched.",
   "emptyFirstRun": "No access queue visitor yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the access queue visitor are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "TODO — not decided. A prospect is signed out and holds no permission, so the operator wording on the P09 twin does not apply. The book offers *Continue Saved Setup* and *Sign In* on 2.1, which is where somebody without access to a saved setup would be sent; no minute has decided it."
  },
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
  "apis": [],
  "apisNote": "Regenerated 9 September 2026 from Subscription_Licensing_AI_Self_Service.pdf page 26. 0 of 0 labels bound to a contract property; 0 of 22 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "navigation": {
   "entryFrom": [
    "SGN-006",
    "SGN-008"
   ],
   "exitTo": [
    "SGN-006",
    "SGN-008"
   ],
   "transitions": [
    {
     "to": "SGN-006",
     "trigger": "Back to Ticketing & Product Requirements",
     "provenance": "structural — the book's own journey, 2.1 \"Journey Preview\", 11 September 2026",
     "back": true
    },
    {
     "to": "SGN-008",
     "trigger": "Additional Business Module Assessment",
     "provenance": "structural — the book's own journey, 2.1 \"Journey Preview\", 11 September 2026"
    }
   ]
  },
  "_platform": {
   "code": "P17",
   "audience": "public",
   "formFactor": "web",
   "shortName": "TICVAI Sign-up",
   "name": "TICVAI Sign-up — Onboarding & Purchase",
   "offlineCapable": false,
   "app": "signup-web",
   "operator": "public",
   "targetApp": {
    "app": "ticvai-control",
    "name": "TICVAI Control",
    "shell": "web",
    "siblings": [
     "P09",
     "P10",
     "P11",
     "P14"
    ],
    "note": "**TICVAI operates all five**, whoever signs in. The partner portal, the accreditation intake, the developer portal and the sign-up are outward faces of the control plane, not separate products — but their users are not TICVAI staff, and the permission model has to hold that line. **P17 added 11 September 2026**: a prospect buying TICVAI has no tenant and no cell, so the control plane is the only thing that can serve them.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "SGN-008",
  "name": "Additional Business Module Assessment",
  "module": "Onboarding & Assessment",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "sameAs": "ADM-386",
   "book": "Subscription_Licensing_AI_Self_Service.pdf",
   "board": "2",
   "number": "8",
   "page": 27
  },
  "implementation": {
   "app": "signup-web",
   "route": "/onboarding-assessment/additional-business-module-assessment-sgn-008",
   "component": "apps/signup-web/src/routes/onboarding-assessment/AdditionalBusinessModuleAssessment.tsx",
   "status": "notStarted"
  },
  "density": "compact",
  "notes": "The self-service form of `ADM-386`, for a prospect with no account. Decided 11 September 2026; P09 keeps its screen for the operator-led path (BL-165). `tools/applied/apply-subscription-placement.py` keeps the two in step.",
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P17 TICVAI Sign-up.dc.html#sgn-008"
  },
  "purpose": "Identify additional TICVAI operational modules based on the customer's business.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "layout": {
   "template": "split",
   "regions": []
  },
  "states": {
   "loading": "The additional business module list.",
   "error": "Could not load. Names which read failed and leaves the additional business module untouched.",
   "emptyFirstRun": "No additional business module yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the additional business module are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "TODO — not decided. A prospect is signed out and holds no permission, so the operator wording on the P09 twin does not apply. The book offers *Continue Saved Setup* and *Sign In* on 2.1, which is where somebody without access to a saved setup would be sent; no minute has decided it."
  },
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
  "apis": [],
  "apisNote": "Regenerated 9 September 2026 from Subscription_Licensing_AI_Self_Service.pdf page 27. 0 of 0 labels bound to a contract property; 0 of 22 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "navigation": {
   "entryFrom": [
    "SGN-007",
    "SGN-009"
   ],
   "exitTo": [
    "SGN-007",
    "SGN-009"
   ],
   "transitions": [
    {
     "to": "SGN-007",
     "trigger": "Back to Access, Queue & Visitor Experience Assessment",
     "provenance": "structural — the book's own journey, 2.1 \"Journey Preview\", 11 September 2026",
     "back": true
    },
    {
     "to": "SGN-009",
     "trigger": "Integration, Payment & Technical Readiness",
     "provenance": "structural — the book's own journey, 2.1 \"Journey Preview\", 11 September 2026"
    }
   ]
  },
  "_platform": {
   "code": "P17",
   "audience": "public",
   "formFactor": "web",
   "shortName": "TICVAI Sign-up",
   "name": "TICVAI Sign-up — Onboarding & Purchase",
   "offlineCapable": false,
   "app": "signup-web",
   "operator": "public",
   "targetApp": {
    "app": "ticvai-control",
    "name": "TICVAI Control",
    "shell": "web",
    "siblings": [
     "P09",
     "P10",
     "P11",
     "P14"
    ],
    "note": "**TICVAI operates all five**, whoever signs in. The partner portal, the accreditation intake, the developer portal and the sign-up are outward faces of the control plane, not separate products — but their users are not TICVAI staff, and the permission model has to hold that line. **P17 added 11 September 2026**: a prospect buying TICVAI has no tenant and no cell, so the control plane is the only thing that can serve them.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "SGN-009",
  "name": "Integration, Payment & Technical Readiness",
  "module": "Onboarding & Assessment",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "sameAs": "ADM-387",
   "book": "Subscription_Licensing_AI_Self_Service.pdf",
   "board": "2",
   "number": "9",
   "page": 28
  },
  "implementation": {
   "app": "signup-web",
   "route": "/onboarding-assessment/integration-payment-technical-readiness-sgn-009",
   "component": "apps/signup-web/src/routes/onboarding-assessment/IntegrationPaymentTechnicalReadiness.tsx",
   "status": "notStarted"
  },
  "density": "compact",
  "notes": "The self-service form of `ADM-387`, for a prospect with no account. Decided 11 September 2026; P09 keeps its screen for the operator-led path (BL-165). `tools/applied/apply-subscription-placement.py` keeps the two in step.",
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P17 TICVAI Sign-up.dc.html#sgn-009"
  },
  "purpose": "Understand external systems and technical requirements that could affect complexity, implementation approach and commercial scope.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "layout": {
   "template": "split",
   "regions": []
  },
  "states": {
   "loading": "The integration payment technical list.",
   "error": "Could not load. Names which read failed and leaves the integration payment technical untouched.",
   "emptyFirstRun": "No integration payment technical yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the integration payment technical are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "TODO — not decided. A prospect is signed out and holds no permission, so the operator wording on the P09 twin does not apply. The book offers *Continue Saved Setup* and *Sign In* on 2.1, which is where somebody without access to a saved setup would be sent; no minute has decided it."
  },
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
  "apis": [],
  "apisNote": "Regenerated 9 September 2026 from Subscription_Licensing_AI_Self_Service.pdf page 28. 0 of 0 labels bound to a contract property; 0 of 31 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "navigation": {
   "entryFrom": [
    "SGN-008",
    "SGN-010"
   ],
   "exitTo": [
    "SGN-008",
    "SGN-010"
   ],
   "transitions": [
    {
     "to": "SGN-008",
     "trigger": "Back to Additional Business Module Assessment",
     "provenance": "structural — the book's own journey, 2.1 \"Journey Preview\", 11 September 2026",
     "back": true
    },
    {
     "to": "SGN-010",
     "trigger": "AI Assessment Summary & Handoff",
     "provenance": "structural — the book's own journey, 2.1 \"Journey Preview\", 11 September 2026"
    }
   ]
  },
  "_platform": {
   "code": "P17",
   "audience": "public",
   "formFactor": "web",
   "shortName": "TICVAI Sign-up",
   "name": "TICVAI Sign-up — Onboarding & Purchase",
   "offlineCapable": false,
   "app": "signup-web",
   "operator": "public",
   "targetApp": {
    "app": "ticvai-control",
    "name": "TICVAI Control",
    "shell": "web",
    "siblings": [
     "P09",
     "P10",
     "P11",
     "P14"
    ],
    "note": "**TICVAI operates all five**, whoever signs in. The partner portal, the accreditation intake, the developer portal and the sign-up are outward faces of the control plane, not separate products — but their users are not TICVAI staff, and the permission model has to hold that line. **P17 added 11 September 2026**: a prospect buying TICVAI has no tenant and no cell, so the control plane is the only thing that can serve them.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "SGN-010",
  "name": "AI Assessment Summary & Handoff",
  "module": "Onboarding & Assessment",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "sameAs": "ADM-388",
   "book": "Subscription_Licensing_AI_Self_Service.pdf",
   "board": "2",
   "number": "10",
   "page": 29
  },
  "implementation": {
   "app": "signup-web",
   "route": "/onboarding-assessment/ai-assessment-summary-handoff-sgn-010",
   "component": "apps/signup-web/src/routes/onboarding-assessment/AiAssessmentSummaryHandoff.tsx",
   "status": "notStarted"
  },
  "density": "compact",
  "notes": "The self-service form of `ADM-388`, for a prospect with no account. Decided 11 September 2026; P09 keeps its screen for the operator-led path (BL-165). `tools/applied/apply-subscription-placement.py` keeps the two in step.",
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P17 TICVAI Sign-up.dc.html#sgn-010"
  },
  "purpose": "Consolidate everything learned during onboarding and prepare the customer for Board 3/4 commercial recommendation.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "layout": {
   "template": "split",
   "regions": []
  },
  "states": {
   "loading": "The assessment summary handoff list.",
   "error": "Could not load. Names which read failed and leaves the assessment summary handoff untouched.",
   "emptyFirstRun": "No assessment summary handoff yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the assessment summary handoff are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "TODO — not decided. A prospect is signed out and holds no permission, so the operator wording on the P09 twin does not apply. The book offers *Continue Saved Setup* and *Sign In* on 2.1, which is where somebody without access to a saved setup would be sent; no minute has decided it."
  },
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
  "apis": [],
  "apisNote": "Regenerated 9 September 2026 from Subscription_Licensing_AI_Self_Service.pdf page 29. 0 of 0 labels bound to a contract property; 0 of 63 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "navigation": {
   "entryFrom": [
    "SGN-009",
    "SGN-011"
   ],
   "exitTo": [
    "SGN-009",
    "SGN-011"
   ],
   "transitions": [
    {
     "to": "SGN-009",
     "trigger": "Back to Integration, Payment & Technical Readiness",
     "provenance": "structural — the book's own journey, 2.1 \"Journey Preview\", 11 September 2026",
     "back": true
    },
    {
     "to": "SGN-011",
     "trigger": "Recommended Package Overview",
     "provenance": "structural — the book's own journey, 2.1 \"Journey Preview\", 11 September 2026"
    }
   ]
  },
  "_platform": {
   "code": "P17",
   "audience": "public",
   "formFactor": "web",
   "shortName": "TICVAI Sign-up",
   "name": "TICVAI Sign-up — Onboarding & Purchase",
   "offlineCapable": false,
   "app": "signup-web",
   "operator": "public",
   "targetApp": {
    "app": "ticvai-control",
    "name": "TICVAI Control",
    "shell": "web",
    "siblings": [
     "P09",
     "P10",
     "P11",
     "P14"
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
