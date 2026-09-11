# WS105 — Subscription Licensing AI Self Service board 8

**10 screens · 0 operations · 0 schemas · 0 permissions**

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
| `BO-605` | Go-Live Readiness Command Center | listDetail | 0 | 0 | — |
| `BO-606` | Automated Validation Plan | listDetail | 0 | 0 | — |
| `BO-607` | Ticketing & Product Validation | listDetail | 0 | 0 | — |
| `BO-608` | End-to-End Sales Channel Testing | listDetail | 0 | 0 | — |
| `BO-609` | Payment & Financial Validation | listDetail | 0 | 0 | — |
| `BO-610` | Ticket, QR & Access Validation | listDetail | 0 | 0 | — |
| `BO-611` | User, Security & Integration Validation | listDetail | 0 | 0 | — |
| `BO-612` | Communication & Customer Journey Validation | listDetail | 0 | 0 | — |
| `BO-613` | Blocker, Warning & AI Resolution Center | configEditor | 0 | 0 | — |
| `BO-614` | Final Go-Live Approval & Production Launch | listDetail | 0 | 0 | — |

## Thin screens in this batch

**BO-605, BO-606, BO-607, BO-608, BO-609, BO-610, BO-611, BO-612, BO-614 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "BO-605",
  "name": "Go-Live Readiness Command Center",
  "module": "Setup & Go-Live",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Subscription_Licensing_AI_Self_Service.pdf",
   "board": "8",
   "number": "1",
   "page": 97
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/setup-go-live/go-live-readiness-command-center-bo-605",
   "component": "apps/venue-management-web/src/routes/setup-go-live/GoLiveReadinessCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-100",
    "BO-604",
    "BO-606",
    "BO-607",
    "BO-608",
    "BO-609",
    "BO-610",
    "BO-611",
    "BO-612",
    "BO-613",
    "BO-614"
   ],
   "exitTo": [
    "BO-100",
    "BO-606",
    "BO-607",
    "BO-608",
    "BO-609",
    "BO-610",
    "BO-611",
    "BO-612",
    "BO-613",
    "BO-614"
   ],
   "transitions": [
    {
     "to": "BO-100",
     "trigger": "Back to Venue Home",
     "provenance": "structural — Subscription board 8 on P08, 11 September 2026",
     "back": true
    },
    {
     "to": "BO-606",
     "trigger": "Automated Validation Plan",
     "provenance": "structural — Subscription board 8 on P08, 11 September 2026"
    },
    {
     "to": "BO-607",
     "trigger": "Ticketing & Product Validation",
     "provenance": "structural — Subscription board 8 on P08, 11 September 2026"
    },
    {
     "to": "BO-608",
     "trigger": "End-to-End Sales Channel Testing",
     "provenance": "structural — Subscription board 8 on P08, 11 September 2026"
    },
    {
     "to": "BO-609",
     "trigger": "Payment & Financial Validation",
     "provenance": "structural — Subscription board 8 on P08, 11 September 2026"
    },
    {
     "to": "BO-610",
     "trigger": "Ticket, QR & Access Validation",
     "provenance": "structural — Subscription board 8 on P08, 11 September 2026"
    },
    {
     "to": "BO-611",
     "trigger": "User, Security & Integration Validation",
     "provenance": "structural — Subscription board 8 on P08, 11 September 2026"
    },
    {
     "to": "BO-612",
     "trigger": "Communication & Customer Journey Validation",
     "provenance": "structural — Subscription board 8 on P08, 11 September 2026"
    },
    {
     "to": "BO-613",
     "trigger": "Blocker, Warning & AI Resolution Center",
     "provenance": "structural — Subscription board 8 on P08, 11 September 2026"
    },
    {
     "to": "BO-614",
     "trigger": "Final Go-Live Approval & Production Launch",
     "provenance": "structural — Subscription board 8 on P08, 11 September 2026"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Provide one central dashboard showing whether the customer is ready for production.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Subscription_Licensing_AI_Self_Service.pdf, page 97"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Subscription_Licensing_AI_Self_Service.pdf, page 97"
   }
  ],
  "layout": {
   "template": "split",
   "regions": []
  },
  "states": {
   "loading": "The go-live readiness list.",
   "error": "Could not load. Names which read failed and leaves the go-live readiness untouched.",
   "emptyFirstRun": "No go-live readiness yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the go-live readiness are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-605"
  },
  "apisNote": "Regenerated 9 September 2026 from Subscription_Licensing_AI_Self_Service.pdf page 97. 0 of 0 labels bound to a contract property; 0 of 13 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "notes": "**Moved from P09 `ADM-439` on 11 September 2026.** Board 8 is worked by the new customer's own administrator inside their tenant, not by TICVAI; `tools/applied/apply-subscription-placement.py` records why. `ADM-439` is retired and never reissued.",
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
  "id": "BO-606",
  "name": "Automated Validation Plan",
  "module": "Setup & Go-Live",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Subscription_Licensing_AI_Self_Service.pdf",
   "board": "8",
   "number": "2",
   "page": 98
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/setup-go-live/automated-validation-plan-bo-606",
   "component": "apps/venue-management-web/src/routes/setup-go-live/AutomatedValidationPlan.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-605"
   ],
   "exitTo": [
    "BO-605"
   ],
   "transitions": [
    {
     "to": "BO-605",
     "trigger": "Back to Go-Live Readiness Command Center",
     "provenance": "structural — Subscription board 8 on P08, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Automatically create the correct testing plan based on what the customer has actually purchased and configured. For example, if the customer purchased: Ticketing POS B2C B2B Access Control the system automatically creates the relevant validation plan.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Subscription_Licensing_AI_Self_Service.pdf, page 98"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Subscription_Licensing_AI_Self_Service.pdf, page 98"
   }
  ],
  "layout": {
   "template": "split",
   "regions": []
  },
  "states": {
   "loading": "The automated validation plan list.",
   "error": "Could not load. Names which read failed and leaves the automated validation plan untouched.",
   "emptyFirstRun": "No automated validation plan yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the automated validation plan are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-606"
  },
  "apisNote": "Regenerated 9 September 2026 from Subscription_Licensing_AI_Self_Service.pdf page 98. 0 of 0 labels bound to a contract property; 0 of 31 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "notes": "**Moved from P09 `ADM-440` on 11 September 2026.** Board 8 is worked by the new customer's own administrator inside their tenant, not by TICVAI; `tools/applied/apply-subscription-placement.py` records why. `ADM-440` is retired and never reissued.",
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
  "id": "BO-607",
  "name": "Ticketing & Product Validation",
  "module": "Setup & Go-Live",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Subscription_Licensing_AI_Self_Service.pdf",
   "board": "8",
   "number": "3",
   "page": 99
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/setup-go-live/ticketing-product-validation-bo-607",
   "component": "apps/venue-management-web/src/routes/setup-go-live/TicketingProductValidation.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-605"
   ],
   "exitTo": [
    "BO-605"
   ],
   "transitions": [
    {
     "to": "BO-605",
     "trigger": "Back to Go-Live Readiness Command Center",
     "provenance": "structural — Subscription board 8 on P08, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Validate that configured products can actually operate correctly.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Subscription_Licensing_AI_Self_Service.pdf, page 99"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Subscription_Licensing_AI_Self_Service.pdf, page 99"
   }
  ],
  "layout": {
   "template": "split",
   "regions": []
  },
  "states": {
   "loading": "The ticketing product validation list.",
   "error": "Could not load. Names which read failed and leaves the ticketing product validation untouched.",
   "emptyFirstRun": "No ticketing product validation yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the ticketing product validation are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-607"
  },
  "apisNote": "Regenerated 9 September 2026 from Subscription_Licensing_AI_Self_Service.pdf page 99. 0 of 0 labels bound to a contract property; 0 of 22 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "notes": "**Moved from P09 `ADM-441` on 11 September 2026.** Board 8 is worked by the new customer's own administrator inside their tenant, not by TICVAI; `tools/applied/apply-subscription-placement.py` records why. `ADM-441` is retired and never reissued.",
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
  "id": "BO-608",
  "name": "End-to-End Sales Channel Testing",
  "module": "Setup & Go-Live",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Subscription_Licensing_AI_Self_Service.pdf",
   "board": "8",
   "number": "4",
   "page": 100
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/setup-go-live/end-to-end-sales-channel-testing-bo-608",
   "component": "apps/venue-management-web/src/routes/setup-go-live/EndToEndSalesChannelTesting.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-605"
   ],
   "exitTo": [
    "BO-605"
   ],
   "transitions": [
    {
     "to": "BO-605",
     "trigger": "Back to Go-Live Readiness Command Center",
     "provenance": "structural — Subscription board 8 on P08, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Test the real customer transaction journey across each activated sales channel.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Subscription_Licensing_AI_Self_Service.pdf, page 100"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Subscription_Licensing_AI_Self_Service.pdf, page 100"
   }
  ],
  "layout": {
   "template": "split",
   "regions": []
  },
  "states": {
   "loading": "The end-to-end sales channel list.",
   "error": "Could not load. Names which read failed and leaves the end-to-end sales channel untouched.",
   "emptyFirstRun": "No end-to-end sales channel yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the end-to-end sales channel are still there. The pack's own statuses are ✓ Passed — the state names which is selected.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-608"
  },
  "apisNote": "Regenerated 9 September 2026 from Subscription_Licensing_AI_Self_Service.pdf page 100. 0 of 0 labels bound to a contract property; 2 of 17 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "notes": "**Moved from P09 `ADM-442` on 11 September 2026.** Board 8 is worked by the new customer's own administrator inside their tenant, not by TICVAI; `tools/applied/apply-subscription-placement.py` records why. `ADM-442` is retired and never reissued.",
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
  "id": "BO-609",
  "name": "Payment & Financial Validation",
  "module": "Setup & Go-Live",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Subscription_Licensing_AI_Self_Service.pdf",
   "board": "8",
   "number": "5",
   "page": 101
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/setup-go-live/payment-financial-validation-bo-609",
   "component": "apps/venue-management-web/src/routes/setup-go-live/PaymentFinancialValidation.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-605"
   ],
   "exitTo": [
    "BO-605"
   ],
   "transitions": [
    {
     "to": "BO-605",
     "trigger": "Back to Go-Live Readiness Command Center",
     "provenance": "structural — Subscription board 8 on P08, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Confirm that payment, taxation, refunds, and financial configuration work before accepting real customer money.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Subscription_Licensing_AI_Self_Service.pdf, page 101"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Subscription_Licensing_AI_Self_Service.pdf, page 101"
   }
  ],
  "layout": {
   "template": "split",
   "regions": []
  },
  "states": {
   "loading": "The payment financial validation list.",
   "error": "Could not load. Names which read failed and leaves the payment financial validation untouched.",
   "emptyFirstRun": "No payment financial validation yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the payment financial validation are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-609"
  },
  "apisNote": "Regenerated 9 September 2026 from Subscription_Licensing_AI_Self_Service.pdf page 101. 0 of 0 labels bound to a contract property; 0 of 17 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "notes": "**Moved from P09 `ADM-443` on 11 September 2026.** Board 8 is worked by the new customer's own administrator inside their tenant, not by TICVAI; `tools/applied/apply-subscription-placement.py` records why. `ADM-443` is retired and never reissued.",
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
  "id": "BO-610",
  "name": "Ticket, QR & Access Validation",
  "module": "Setup & Go-Live",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Subscription_Licensing_AI_Self_Service.pdf",
   "board": "8",
   "number": "6",
   "page": 102
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/setup-go-live/ticket-qr-access-validation-bo-610",
   "component": "apps/venue-management-web/src/routes/setup-go-live/TicketQrAccessValidation.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-605"
   ],
   "exitTo": [
    "BO-605"
   ],
   "transitions": [
    {
     "to": "BO-605",
     "trigger": "Back to Go-Live Readiness Command Center",
     "provenance": "structural — Subscription board 8 on P08, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Validate the complete journey from ticket creation to physical admission.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Subscription_Licensing_AI_Self_Service.pdf, page 102"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Subscription_Licensing_AI_Self_Service.pdf, page 102"
   }
  ],
  "layout": {
   "template": "split",
   "regions": []
  },
  "states": {
   "loading": "The ticket access validation list.",
   "error": "Could not load. Names which read failed and leaves the ticket access validation untouched.",
   "emptyFirstRun": "No ticket access validation yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the ticket access validation are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-610"
  },
  "apisNote": "Regenerated 9 September 2026 from Subscription_Licensing_AI_Self_Service.pdf page 102. 0 of 0 labels bound to a contract property; 0 of 22 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "notes": "**Moved from P09 `ADM-444` on 11 September 2026.** Board 8 is worked by the new customer's own administrator inside their tenant, not by TICVAI; `tools/applied/apply-subscription-placement.py` records why. `ADM-444` is retired and never reissued.",
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
  "id": "BO-611",
  "name": "User, Security & Integration Validation",
  "module": "Setup & Go-Live",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Subscription_Licensing_AI_Self_Service.pdf",
   "board": "8",
   "number": "7",
   "page": 103
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/setup-go-live/user-security-integration-validation-bo-611",
   "component": "apps/venue-management-web/src/routes/setup-go-live/UserSecurityIntegrationValidation.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-605"
   ],
   "exitTo": [
    "BO-605"
   ],
   "transitions": [
    {
     "to": "BO-605",
     "trigger": "Back to Go-Live Readiness Command Center",
     "provenance": "structural — Subscription board 8 on P08, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Verify that the environment is technically and operationally secure before launch.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Subscription_Licensing_AI_Self_Service.pdf, page 103"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Subscription_Licensing_AI_Self_Service.pdf, page 103"
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
       "kind": "banner",
       "label": "Permissions this screen separates",
       "notes": "**The pack separates these permissions and no action on the screen claims them yet:** Administrator login, Cashier login, Supervisor login, Restricted function test, Role permissions, Approval rights, MFA, Session controls. Each needs attaching to the control it gates, or the screen needs the control.",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 103 §User & Permission Tests"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The user security integration list.",
   "error": "Could not load. Names which read failed and leaves the user security integration untouched.",
   "emptyFirstRun": "No user security integration yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the user security integration are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-611"
  },
  "apisNote": "Regenerated 9 September 2026 from Subscription_Licensing_AI_Self_Service.pdf page 103. 0 of 0 labels bound to a contract property; 8 of 17 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "notes": "**Moved from P09 `ADM-445` on 11 September 2026.** Board 8 is worked by the new customer's own administrator inside their tenant, not by TICVAI; `tools/applied/apply-subscription-placement.py` records why. `ADM-445` is retired and never reissued.",
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
  "id": "BO-612",
  "name": "Communication & Customer Journey Validation",
  "module": "Setup & Go-Live",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Subscription_Licensing_AI_Self_Service.pdf",
   "board": "8",
   "number": "8",
   "page": 104
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/setup-go-live/communication-customer-journey-validation-bo-612",
   "component": "apps/venue-management-web/src/routes/setup-go-live/CommunicationCustomerJourneyValidation.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-605"
   ],
   "exitTo": [
    "BO-605"
   ],
   "transitions": [
    {
     "to": "BO-605",
     "trigger": "Back to Go-Live Readiness Command Center",
     "provenance": "structural — Subscription board 8 on P08, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Ensure that the customer receives the correct information throughout the booking journey.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Subscription_Licensing_AI_Self_Service.pdf, page 104"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Subscription_Licensing_AI_Self_Service.pdf, page 104"
   }
  ],
  "layout": {
   "template": "split",
   "regions": []
  },
  "states": {
   "loading": "The communication customer journey list.",
   "error": "Could not load. Names which read failed and leaves the communication customer journey untouched.",
   "emptyFirstRun": "No communication customer journey yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the communication customer journey are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-612"
  },
  "apisNote": "Regenerated 9 September 2026 from Subscription_Licensing_AI_Self_Service.pdf page 104. 0 of 0 labels bound to a contract property; 0 of 13 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "notes": "**Moved from P09 `ADM-446` on 11 September 2026.** Board 8 is worked by the new customer's own administrator inside their tenant, not by TICVAI; `tools/applied/apply-subscription-placement.py` records why. `ADM-446` is retired and never reissued.",
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
  "id": "BO-613",
  "name": "Blocker, Warning & AI Resolution Center",
  "module": "Setup & Go-Live",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Subscription_Licensing_AI_Self_Service.pdf",
   "board": "8",
   "number": "9",
   "page": 105
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/setup-go-live/blocker-warning-ai-resolution-center-bo-613",
   "component": "apps/venue-management-web/src/routes/setup-go-live/BlockerWarningAiResolutionCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-605"
   ],
   "exitTo": [
    "BO-605"
   ],
   "transitions": [
    {
     "to": "BO-605",
     "trigger": "Back to Go-Live Readiness Command Center",
     "provenance": "structural — Subscription board 8 on P08, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Where override is permitted, capture) and no display directory — it is settings, not a population",
  "purpose": "Bring all readiness problems into one actionable screen instead of forcing the customer to search through the system.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Reason",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 105 §Where override is permitted, capture"
      },
      {
       "kind": "selectField",
       "label": "User",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 105 §Where override is permitted, capture"
      },
      {
       "kind": "selectField",
       "label": "Role",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 105 §Where override is permitted, capture"
      },
      {
       "kind": "selectField",
       "label": "Approval",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 105 §Where override is permitted, capture"
      },
      {
       "kind": "selectField",
       "label": "Timestamp",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 105 §Where override is permitted, capture"
      },
      {
       "kind": "selectField",
       "label": "Expiry where applicable",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 105 §Where override is permitted, capture"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The blocker warning resolution configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the blocker warning resolution untouched.",
   "emptyFirstRun": "No blocker warning resolution configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-613"
  },
  "apisNote": "Regenerated 9 September 2026 from Subscription_Licensing_AI_Self_Service.pdf page 105. 0 of 0 labels bound to a contract property; 6 of 19 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "notes": "**Moved from P09 `ADM-447` on 11 September 2026.** Board 8 is worked by the new customer's own administrator inside their tenant, not by TICVAI; `tools/applied/apply-subscription-placement.py` records why. `ADM-447` is retired and never reissued.",
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
  "id": "BO-614",
  "name": "Final Go-Live Approval & Production Launch",
  "module": "Setup & Go-Live",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Subscription_Licensing_AI_Self_Service.pdf",
   "board": "8",
   "number": "10",
   "page": 106
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/setup-go-live/final-go-live-approval-production-launch-bo-614",
   "component": "apps/venue-management-web/src/routes/setup-go-live/FinalGoLiveApprovalProductionLaunch.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-605"
   ],
   "exitTo": [
    "BO-605"
   ],
   "transitions": [
    {
     "to": "BO-605",
     "trigger": "Back to Go-Live Readiness Command Center",
     "provenance": "structural — Subscription board 8 on P08, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Provide the final controlled decision to activate production operation.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Subscription_Licensing_AI_Self_Service.pdf, page 106"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Subscription_Licensing_AI_Self_Service.pdf, page 106"
   }
  ],
  "layout": {
   "template": "split",
   "regions": []
  },
  "states": {
   "loading": "The final go-live approval list.",
   "error": "Could not load. Names which read failed and leaves the final go-live approval untouched.",
   "emptyFirstRun": "No final go-live approval yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the final go-live approval are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-614"
  },
  "apisNote": "Regenerated 9 September 2026 from Subscription_Licensing_AI_Self_Service.pdf page 106. 0 of 0 labels bound to a contract property; 0 of 81 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "notes": "**Moved from P09 `ADM-448` on 11 September 2026.** Board 8 is worked by the new customer's own administrator inside their tenant, not by TICVAI; `tools/applied/apply-subscription-placement.py` records why. `ADM-448` is retired and never reissued.",
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
