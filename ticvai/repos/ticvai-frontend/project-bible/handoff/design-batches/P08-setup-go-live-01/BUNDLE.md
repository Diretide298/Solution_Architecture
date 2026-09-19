# P08-setup-go-live-01 — P08 · Setup & Go-Live

**1 screens · 0 operations · 0 schemas · 0 permissions**

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
| `BO-594` | Environment Ready & Handoff to AI Setup | configEditor | 0 | 0 | — |

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "BO-594",
  "name": "Environment Ready & Handoff to AI Setup",
  "module": "Setup & Go-Live",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Subscription_Licensing_AI_Self_Service.pdf",
   "board": "6",
   "number": "10",
   "page": 80
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/setup-go-live/environment-ready-handoff-to-ai-setup-bo-594",
   "component": "apps/venue-management-web/src/routes/setup-go-live/EnvironmentReadyHandoffToAiSetup.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-100"
   ],
   "exitTo": [
    "BO-100",
    "BO-595"
   ],
   "transitions": [
    {
     "to": "BO-100",
     "trigger": "Back to Venue Home",
     "provenance": "structural — Subscription board 6 on P08, 11 September 2026",
     "back": true
    },
    {
     "to": "BO-595",
     "trigger": "AI Setup Command Center",
     "provenance": "structural — the book's handoff, 6.10: \"This hands the customer directly to Board 7\", 11 September 2026"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configuration Status; AI Configuration prepares; Initial Configuration Prepared) and no display directory — it is settings, not a population",
  "purpose": "Confirm that provisioning is complete and move the customer into Board 7.",
  "gaps": [
   {
    "operation": null,
    "why": "**Environment Ready & Handoff to AI Setup declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write operations are missing or this screen is a view of something another screen builds.",
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
       "label": "Initial Configuration: 42%",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 80 §Configuration Status"
      },
      {
       "kind": "textField",
       "label": "Board 6 — Zero-Touch Requirement",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 80 §AI Configuration prepares"
      },
      {
       "kind": "selectField",
       "label": "↓",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 80 §Initial Configuration Prepared"
      },
      {
       "kind": "textField",
       "label": "Customer Receives “Environment Ready”",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 80 §Initial Configuration Prepared"
      },
      {
       "kind": "textField",
       "label": "Board 6 — Trial Handling",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 80 §Initial Configuration Prepared"
      },
      {
       "kind": "textField",
       "label": "Tenant Type = Trial",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 80 §Initial Configuration Prepared"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The environment ready handoff configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the environment ready handoff untouched.",
   "emptyFirstRun": "No environment ready handoff configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-594"
  },
  "apisNote": "Regenerated 9 September 2026 from Subscription_Licensing_AI_Self_Service.pdf page 80. 0 of 0 labels bound to a contract property; 6 of 83 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "notes": "**Moved from P09 `ADM-428` on 11 September 2026.** Board 6 is worked by the new customer's own administrator inside their tenant, not by TICVAI; `tools/applied/apply-subscription-placement.py` records why. `ADM-428` is retired and never reissued.",
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
{}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{}
```
