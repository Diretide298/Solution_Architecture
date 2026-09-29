# WS91 — Rental Management board 4

**10 screens · 11 operations · 9 schemas · 5 permissions**

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
  `PRICE_CONFIGURE, PRODUCT_VIEW, RENTAL_OVERRIDE, RENTAL_PRICE, RENTAL_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-524` | Rental Pricing Command Center | commandCentre | 2 | 0 | — |
| `BO-525` | Pricing Profile Builder | configEditor | 2 | 0 | — |
| `BO-526` | Duration & Tiered Pricing Configuration | configEditor | 1 | 0 | — |
| `BO-527` | Calendar, Peak & Seasonal Pricing | listDetail | 1 | 0 | — |
| `BO-528` | Dynamic Pricing & AI Recommendation | listDetail | 2 | 1 | — |
| `BO-529` | Deposit & Security Hold Policy | listDetail | 1 | 0 | — |
| `BO-530` | Deposit Lifecycle & Settlement Rules | configEditor | 1 | 0 | — |
| `BO-531` | Late Fee, Grace Period & Extension Pricing | configEditor | 1 | 0 | — |
| `BO-532` | Commercial Exceptions, Waivers & Overrides | listDetail | 1 | 0 | — |
| `BO-533` | Pricing Simulation, Validation & AI Commercial Intelligence | listDetail | 3 | 0 | — |

## Thin screens in this batch

**BO-527, BO-528, BO-529, BO-532, BO-533 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "BO-524",
  "name": "Rental Pricing Command Center",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Rental_Management.pdf",
   "board": "4",
   "number": "1",
   "page": 38
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/rental-pricing-command-center-bo-524",
   "component": "apps/venue-management-web/src/routes/rentals/RentalPricingCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-100"
   ],
   "exitTo": [
    "BO-100",
    "BO-525",
    "BO-526",
    "BO-527",
    "BO-528",
    "BO-529",
    "BO-530",
    "BO-531",
    "BO-532",
    "BO-533"
   ],
   "transitions": [
    {
     "to": "BO-100",
     "trigger": "Back to Venue Home",
     "provenance": "structural — pack board 4 wiring, 11 September 2026",
     "back": true
    },
    {
     "to": "BO-525",
     "trigger": "Pricing Profile Builder",
     "provenance": "structural — pack board 4 wiring, 11 September 2026"
    },
    {
     "to": "BO-526",
     "trigger": "Duration & Tiered Pricing Configuration",
     "provenance": "structural — pack board 4 wiring, 11 September 2026"
    },
    {
     "to": "BO-527",
     "trigger": "Calendar, Peak & Seasonal Pricing",
     "provenance": "structural — pack board 4 wiring, 11 September 2026"
    },
    {
     "to": "BO-528",
     "trigger": "Dynamic Pricing & AI Recommendation",
     "provenance": "structural — pack board 4 wiring, 11 September 2026"
    },
    {
     "to": "BO-529",
     "trigger": "Deposit & Security Hold Policy",
     "provenance": "structural — pack board 4 wiring, 11 September 2026"
    },
    {
     "to": "BO-530",
     "trigger": "Deposit Lifecycle & Settlement Rules",
     "provenance": "structural — pack board 4 wiring, 11 September 2026"
    },
    {
     "to": "BO-531",
     "trigger": "Late Fee, Grace Period & Extension Pricing",
     "provenance": "structural — pack board 4 wiring, 11 September 2026"
    },
    {
     "to": "BO-532",
     "trigger": "Commercial Exceptions, Waivers & Overrides",
     "provenance": "structural — pack board 4 wiring, 11 September 2026"
    },
    {
     "to": "BO-533",
     "trigger": "Pricing Simulation, Validation & AI Commercial Intelligence",
     "provenance": "structural — pack board 4 wiring, 11 September 2026"
    }
   ]
  },
  "density": "compact",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen a metric directory (§KPI Cards) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's",
  "purpose": "Central management screen for all rental pricing and commercial policies.",
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "filters",
     "components": [
      {
       "kind": "searchField",
       "label": "Search rental pricing",
       "provenance": "pack Rental_Management.pdf, page 38 §Filters"
      },
      {
       "kind": "multiSelect",
       "label": "Filter by",
       "columns": [
        "Venue",
        "Location",
        "Product",
        "Category",
        "Pricing Model",
        "Deposit Type",
        "Effective Date",
        "Status"
       ],
       "notes": "The pack filters this screen by venue, location, product, category, pricing model, deposit type and 2 more — which are present is a decision the pack already made.",
       "provenance": "pack Rental_Management.pdf, page 38 §Filters"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Active Pricing Profiles",
       "provenance": "pack Rental_Management.pdf, page 38 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Products Without Pricing",
       "provenance": "pack Rental_Management.pdf, page 38 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Deposit Policies",
       "provenance": "pack Rental_Management.pdf, page 38 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Dynamic Pricing Enabled",
       "provenance": "pack Rental_Management.pdf, page 38 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Upcoming Price Changes",
       "provenance": "pack Rental_Management.pdf, page 38 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Pricing Exceptions",
       "provenance": "pack Rental_Management.pdf, page 38 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Approval Pending",
       "provenance": "pack Rental_Management.pdf, page 38 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "AI Recommendations",
       "provenance": "pack Rental_Management.pdf, page 38 §KPI Cards"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "+ Create Pricing Profile",
       "provenance": "pack Rental_Management.pdf, page 38 §Actions"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The rental pricing list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the rental pricing untouched.",
   "emptyFirstRun": "No rental pricing yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the rental pricing are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listRentalPricingProfiles",
    "contract": "rental",
    "purpose": "Profiles, and products without one",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "createRentalPricingProfile",
    "contract": "rental",
    "purpose": "Create a new rental pricing profile",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration): serves the pack action(s) + Create Pricing Profile",
    "invalidates": [
     "listRentalPricingProfiles"
    ]
   }
  ],
  "entryState": {
   "preloaded": [
    "Active Pricing Profiles",
    "Products Without Pricing",
    "Deposit Policies",
    "Dynamic Pricing Enabled",
    "Upcoming Price Changes",
    "Pricing Exceptions"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-524",
   "workshopBoard": "wireframes/WS119 Rental Management Board 4.dc.html#bo-524"
  },
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 38. 0 of 8 labels bound to a contract property; 17 of 24 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Pack actions reconciled 29 September (VM close-out):** + Create Pricing Profile: `createRentalPricingProfile`.",
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
  "id": "BO-525",
  "name": "Pricing Profile Builder",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Rental_Management.pdf",
   "board": "4",
   "number": "2",
   "page": 39
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/pricing-profile-builder-bo-525",
   "component": "apps/venue-management-web/src/routes/rentals/PricingProfileBuilder.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-524"
   ],
   "exitTo": [
    "BO-524"
   ],
   "transitions": [
    {
     "to": "BO-524",
     "trigger": "Back to Rental Pricing Command Center",
     "provenance": "structural — pack board 4 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Select) and no display directory — it is settings, not a population",
  "purpose": "Create the master commercial pricing profile associated with a rental product.",
  "gaps": [
   {
    "operation": null,
    "why": "**Pricing Profile Builder declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write operations are missing or this screen is a view of something another screen builds.",
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
       "label": "Flat Rate",
       "provenance": "pack Rental_Management.pdf, page 39 §Select"
      },
      {
       "kind": "selectField",
       "label": "Duration Based",
       "provenance": "pack Rental_Management.pdf, page 39 §Select"
      },
      {
       "kind": "selectField",
       "label": "Tiered",
       "provenance": "pack Rental_Management.pdf, page 39 §Select"
      },
      {
       "kind": "selectField",
       "label": "Peak / Off-Peak",
       "provenance": "pack Rental_Management.pdf, page 39 §Select"
      },
      {
       "kind": "selectField",
       "label": "Weekend",
       "provenance": "pack Rental_Management.pdf, page 39 §Select"
      },
      {
       "kind": "selectField",
       "label": "Seasonal",
       "provenance": "pack Rental_Management.pdf, page 39 §Select"
      },
      {
       "kind": "selectField",
       "label": "Dynamic / AI-Assisted",
       "provenance": "pack Rental_Management.pdf, page 39 §Select"
      },
      {
       "kind": "selectField",
       "label": "Hybrid",
       "provenance": "pack Rental_Management.pdf, page 39 §Select"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The pricing profile configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the pricing profile untouched.",
   "emptyFirstRun": "No pricing profile configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "createRentalPricingProfile",
    "contract": "rental",
    "purpose": "Build a profile",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listRentalPricingProfiles"
    ]
   },
   {
    "operationId": "updateRentalPricingProfile",
    "contract": "rental",
    "purpose": "Change it",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listRentalPricingProfiles"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-525",
   "workshopBoard": "wireframes/WS119 Rental Management Board 4.dc.html#bo-525"
  },
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 39. 0 of 0 labels bound to a contract property; 8 of 25 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "profileId",
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
  "id": "BO-526",
  "name": "Duration & Tiered Pricing Configuration",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Rental_Management.pdf",
   "board": "4",
   "number": "3",
   "page": 40
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/duration-tiered-pricing-configuration-bo-526",
   "component": "apps/venue-management-web/src/routes/rentals/DurationTieredPricingConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-524"
   ],
   "exitTo": [
    "BO-524"
   ],
   "transitions": [
    {
     "to": "BO-524",
     "trigger": "Back to Rental Pricing Command Center",
     "provenance": "structural — pack board 4 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§For customer-defined durations; Configure) and no display directory — it is settings, not a population",
  "purpose": "Configure pricing according to rental duration. This directly implements the fixed and dynamic-duration requirements.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "textField",
       "label": "Minimum Charge: AED 40",
       "provenance": "pack Rental_Management.pdf, page 40 §For customer-defined durations"
      },
      {
       "kind": "textField",
       "label": "Billing Increment: 15 minutes",
       "provenance": "pack Rental_Management.pdf, page 40 §For customer-defined durations"
      },
      {
       "kind": "textField",
       "label": "Additional Increment: AED 10",
       "provenance": "pack Rental_Management.pdf, page 40 §For customer-defined durations"
      },
      {
       "kind": "selectField",
       "label": "Exact usage",
       "provenance": "pack Rental_Management.pdf, page 40 §Configure"
      },
      {
       "kind": "textField",
       "label": "Round up to 15 minutes",
       "provenance": "pack Rental_Management.pdf, page 40 §Configure"
      },
      {
       "kind": "textField",
       "label": "Round up to 30 minutes",
       "provenance": "pack Rental_Management.pdf, page 40 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Full next hour",
       "provenance": "pack Rental_Management.pdf, page 40 §Configure"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The duration tiered pricing configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the duration tiered pricing untouched.",
   "emptyFirstRun": "No duration tiered pricing configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "updateRentalPricingProfile",
    "contract": "rental",
    "purpose": "Duration and tiered rates",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listRentalPricingProfiles"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-526",
   "workshopBoard": "wireframes/WS119 Rental Management Board 4.dc.html#bo-526"
  },
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 40. 0 of 0 labels bound to a contract property; 7 of 18 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "profileId",
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
  "id": "BO-527",
  "name": "Calendar, Peak & Seasonal Pricing",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Rental_Management.pdf",
   "board": "4",
   "number": "4",
   "page": 41
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/calendar-peak-seasonal-pricing-bo-527",
   "component": "apps/venue-management-web/src/routes/rentals/CalendarPeakSeasonalPricing.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-524"
   ],
   "exitTo": [
    "BO-524"
   ],
   "transitions": [
    {
     "to": "BO-524",
     "trigger": "Back to Rental Pricing Command Center",
     "provenance": "structural — pack board 4 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Allow price differentiation according to date and time.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Rental_Management.pdf, page 41"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Rental_Management.pdf, page 41"
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
       "impliedBy": "updateRentalPricingProfile",
       "label": "Save",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "updateRentalPricingProfile"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The calendar peak seasonal list.",
   "error": "Could not load. Names which read failed and leaves the calendar peak seasonal untouched.",
   "emptyFirstRun": "No calendar peak seasonal yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the calendar peak seasonal are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "updateRentalPricingProfile",
    "contract": "rental",
    "purpose": "Peak, weekend and seasonal rules",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listRentalPricingProfiles"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-527",
   "workshopBoard": "wireframes/WS119 Rental Management Board 4.dc.html#bo-527"
  },
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 41. 0 of 0 labels bound to a contract property; 0 of 8 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "profileId",
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
  "id": "BO-528",
  "name": "Dynamic Pricing & AI Recommendation",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Rental_Management.pdf",
   "board": "4",
   "number": "5",
   "page": 42
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/dynamic-pricing-ai-recommendation-bo-528",
   "component": "apps/venue-management-web/src/routes/rentals/DynamicPricingAiRecommendation.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-524"
   ],
   "exitTo": [
    "BO-524"
   ],
   "transitions": [
    {
     "to": "BO-524",
     "trigger": "Back to Rental Pricing Command Center",
     "provenance": "structural — pack board 4 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Connect Rental Management to TICVAI's broader Dynamic Pricing capability without duplicating the core Dynamic Pricing module. The original rental requirements explicitly support dynamic pricing.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Rental_Management.pdf, page 42"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Rental_Management.pdf, page 42"
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
       "label": "Accept | Modify | Reject | Schedule",
       "provenance": "pack Rental_Management.pdf, page 42 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Transition dynamic pricing strategy",
       "operation": "transitionDynamicPricingStrategy",
       "permission": "PRICE_CONFIGURE",
       "notes": "**The strategy's status moves, as calls** (29 September, writers pass).",
       "provenance": "contract catalogue.yaml POST /dynamic-pricing-strategies/{strategyId}/lifecycle"
      }
     ]
    },
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listDynamicPricingStrategy",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The dynamic pricing recommendation list.",
   "error": "Could not load. Names which read failed and leaves the dynamic pricing recommendation untouched.",
   "emptyFirstRun": "No dynamic pricing recommendation yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the dynamic pricing recommendation are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listDynamicPricingStrategy",
    "contract": "catalogue",
    "purpose": "Dynamic pricing",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "transitionDynamicPricingStrategy",
    "contract": "catalogue",
    "purpose": "Activate, pause, resume or retire a dynamic pricing strategy",
    "trigger": "onAction",
    "invalidates": [
     "listDynamicPricingStrategy"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-528",
   "workshopBoard": "wireframes/WS119 Rental Management Board 4.dc.html#bo-528"
  },
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 42. 0 of 0 labels bound to a contract property; 1 of 22 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Pack actions reconciled 29 September (VM close-out):** Accept | Modify | Reject | Schedule dropped (AI design pending review (accept/modify/reject/schedule acts on AI pricing recommendations; would bind ai decideProposedAction)).",
  "overlays": [
   {
    "id": "formTransitionDynamicPricingStrategy",
    "component": "modal",
    "trigger": "Transition dynamic pricing strategy",
    "body": "**Collects what `transitionDynamicPricingStrategy` sends before it is called.** Required: `action`. Optional: `reason`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Transition dynamic pricing strategy",
     "operation": "transitionDynamicPricingStrategy"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "action",
      "reason"
     ]
    },
    "provenance": "contract catalogue.yaml POST /dynamic-pricing-strategies/{strategyId}/lifecycle"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "strategyId",
     "from": "navigation",
     "optional": true
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
  "id": "BO-529",
  "name": "Deposit & Security Hold Policy",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Rental_Management.pdf",
   "board": "4",
   "number": "6",
   "page": 43
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/deposit-security-hold-policy-bo-529",
   "component": "apps/venue-management-web/src/routes/rentals/DepositSecurityHoldPolicy.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-524"
   ],
   "exitTo": [
    "BO-524"
   ],
   "transitions": [
    {
     "to": "BO-524",
     "trigger": "Back to Rental Pricing Command Center",
     "provenance": "structural — pack board 4 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Configure financial security required before equipment is released. The original scope supports fixed and percentage deposits and multiple deposit methods.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Rental_Management.pdf, page 43"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Rental_Management.pdf, page 43"
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
       "label": "Credit Card Pre-Authorization",
       "provenance": "pack Rental_Management.pdf, page 43 §Enable"
      },
      {
       "kind": "secondaryButton",
       "label": "Card Charge",
       "provenance": "pack Rental_Management.pdf, page 43 §Enable"
      },
      {
       "kind": "secondaryButton",
       "label": "Wallet",
       "provenance": "pack Rental_Management.pdf, page 43 §Enable"
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
   "loading": "The deposit security hold list.",
   "error": "Could not load. Names which read failed and leaves the deposit security hold untouched.",
   "emptyFirstRun": "No deposit security hold yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the deposit security hold are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setRentalDepositPolicy",
    "contract": "rental",
    "purpose": "Deposit basis, limits and instruments",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listRentalPricingProfiles"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-529",
   "workshopBoard": "wireframes/WS119 Rental Management Board 4.dc.html#bo-529"
  },
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 43. 0 of 0 labels bound to a contract property; 3 of 18 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Pack actions reconciled 29 September (VM close-out):** Credit Card Pre-Authorization, Card Charge, Wallet are choices sent by `setRentalDepositPolicy` (instruments cardPreAuthorisation|cardCharge|wallet).",
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
  "id": "BO-530",
  "name": "Deposit Lifecycle & Settlement Rules",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Rental_Management.pdf",
   "board": "4",
   "number": "7",
   "page": 44
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/deposit-lifecycle-settlement-rules-bo-530",
   "component": "apps/venue-management-web/src/routes/rentals/DepositLifecycleSettlementRules.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-524"
   ],
   "exitTo": [
    "BO-524"
   ],
   "transitions": [
    {
     "to": "BO-524",
     "trigger": "Back to Rental Pricing Command Center",
     "provenance": "structural — pack board 4 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Control what happens to the deposit throughout the rental lifecycle.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Automatic release",
       "provenance": "pack Rental_Management.pdf, page 44 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Manual inspection required",
       "provenance": "pack Rental_Management.pdf, page 44 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Supervisor approval threshold",
       "provenance": "pack Rental_Management.pdf, page 44 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Partial capture permitted",
       "provenance": "pack Rental_Management.pdf, page 44 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Full capture permitted",
       "provenance": "pack Rental_Management.pdf, page 44 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Auto-release delay",
       "provenance": "pack Rental_Management.pdf, page 44 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Refund method",
       "provenance": "pack Rental_Management.pdf, page 44 §Configure"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The deposit lifecycle settlement configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the deposit lifecycle settlement untouched.",
   "emptyFirstRun": "No deposit lifecycle settlement configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "setRentalDepositPolicy",
    "contract": "rental",
    "purpose": "Release, capture and approval thresholds",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listRentalPricingProfiles"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-530",
   "workshopBoard": "wireframes/WS119 Rental Management Board 4.dc.html#bo-530"
  },
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 44. 0 of 0 labels bound to a contract property; 7 of 16 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-531",
  "name": "Late Fee, Grace Period & Extension Pricing",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Rental_Management.pdf",
   "board": "4",
   "number": "8",
   "page": 44
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/late-fee-grace-period-extension-pricing-bo-531",
   "component": "apps/venue-management-web/src/routes/rentals/LateFeeGracePeriodExtensionPricing.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-524"
   ],
   "exitTo": [
    "BO-524"
   ],
   "transitions": [
    {
     "to": "BO-524",
     "trigger": "Back to Rental Pricing Command Center",
     "provenance": "structural — pack board 4 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Select) and no display directory — it is settings, not a population",
  "purpose": "Configure the commercial treatment of rentals that extend beyond the original return time. The source explicitly requires automatic late-fee calculation and grace-period configuration.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Fixed Fee",
       "provenance": "pack Rental_Management.pdf, page 44 §Select"
      },
      {
       "kind": "selectField",
       "label": "Per Minute",
       "provenance": "pack Rental_Management.pdf, page 44 §Select"
      },
      {
       "kind": "selectField",
       "label": "Per 15 Minutes",
       "provenance": "pack Rental_Management.pdf, page 44 §Select"
      },
      {
       "kind": "selectField",
       "label": "Per 30 Minutes",
       "provenance": "pack Rental_Management.pdf, page 44 §Select"
      },
      {
       "kind": "selectField",
       "label": "Per Hour",
       "provenance": "pack Rental_Management.pdf, page 44 §Select"
      },
      {
       "kind": "selectField",
       "label": "Tiered",
       "provenance": "pack Rental_Management.pdf, page 44 §Select"
      },
      {
       "kind": "selectField",
       "label": "Maximum Daily Charge",
       "provenance": "pack Rental_Management.pdf, page 44 §Select"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The late fee grace configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the late fee grace untouched.",
   "emptyFirstRun": "No late fee grace configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "setRentalFeePolicy",
    "contract": "rental",
    "purpose": "Grace, late fee and extension pricing",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listRentalPricingProfiles"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-531",
   "workshopBoard": "wireframes/WS119 Rental Management Board 4.dc.html#bo-531"
  },
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 44. 0 of 0 labels bound to a contract property; 7 of 17 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-532",
  "name": "Commercial Exceptions, Waivers & Overrides",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Rental_Management.pdf",
   "board": "4",
   "number": "9",
   "page": 45
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/commercial-exceptions-waivers-overrides-bo-532",
   "component": "apps/venue-management-web/src/routes/rentals/CommercialExceptionsWaiversOverrides.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-524"
   ],
   "exitTo": [
    "BO-524"
   ],
   "transitions": [
    {
     "to": "BO-524",
     "trigger": "Back to Rental Pricing Command Center",
     "provenance": "structural — pack board 4 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Control authorized deviations from normal commercial policies.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Rental_Management.pdf, page 45"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Rental_Management.pdf, page 45"
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
       "impliedBy": "requestRentalCommercialOverride",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "requestRentalCommercialOverride"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The commercial exceptions waivers list.",
   "error": "Could not load. Names which read failed and leaves the commercial exceptions waivers untouched.",
   "emptyFirstRun": "No commercial exceptions waivers yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the commercial exceptions waivers are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "requestRentalCommercialOverride",
    "contract": "rental",
    "purpose": "Waive or adjust, with approval",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-532",
   "workshopBoard": "wireframes/WS119 Rental Management Board 4.dc.html#bo-532"
  },
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 45. 0 of 0 labels bound to a contract property; 0 of 23 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-533",
  "name": "Pricing Simulation, Validation & AI Commercial Intelligence",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Rental_Management.pdf",
   "board": "4",
   "number": "10",
   "page": 46
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/pricing-simulation-validation-ai-commercial-intelligence-bo-533",
   "component": "apps/venue-management-web/src/routes/rentals/PricingSimulationValidationAiCommercialIntellige.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-524"
   ],
   "exitTo": [
    "BO-524"
   ],
   "transitions": [
    {
     "to": "BO-524",
     "trigger": "Back to Rental Pricing Command Center",
     "provenance": "structural — pack board 4 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Allow administrators to test commercial configuration before publishing it. This is particularly important because rental pricing can involve duration, calendar, location, deposit and dynamic pricing simultaneously.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Rental_Management.pdf, page 46"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Rental_Management.pdf, page 46"
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
       "impliedBy": "listCommercialPricing",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "simulateRentalPricing",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "simulateRentalPricing"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The pricing simulation validation list.",
   "error": "Could not load. Names which read failed and leaves the pricing simulation validation untouched.",
   "emptyFirstRun": "No pricing simulation validation yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the pricing simulation validation are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listCommercialPricing",
    "contract": "catalogue",
    "purpose": "Commercial Pricing Command Center",
    "trigger": "onLoad"
   },
   {
    "operationId": "simulateRentalPricing",
    "contract": "rental",
    "purpose": "Test the configuration",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "explainRentalPrice",
    "contract": "rental",
    "purpose": "Why the price is what it is",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-533",
   "workshopBoard": "wireframes/WS119 Rental Management Board 4.dc.html#bo-533"
  },
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 46. 0 of 0 labels bound to a contract property; 0 of 51 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
 "createRentalPricingProfile": {
  "method": "POST",
  "path": "/rental-pricing-profiles",
  "contract": "rental",
  "summary": "Define how a rental is priced",
  "permission": "RENTAL_PRICE",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "RentalPricingProfile",
  "responds": "RentalPricingProfile"
 },
 "explainRentalPrice": {
  "method": "POST",
  "path": "/rental-price/explain",
  "contract": "rental",
  "summary": "Why the price is what it is, rule by rule",
  "permission": "RENTAL_VIEW",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "RentalQuoteRequest",
  "responds": "RentalPriceExplanation"
 },
 "listCommercialPricing": {
  "method": "GET",
  "path": "/commercial-pricing",
  "contract": "catalogue",
  "summary": "Commercial Pricing Command Center",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "country",
    "in": "query",
    "required": false
   },
   {
    "name": "productType",
    "in": "query",
    "required": false
   },
   {
    "name": "priceListType",
    "in": "query",
    "required": false
   },
   {
    "name": "venue",
    "in": "query",
    "required": false
   },
   {
    "name": "brand",
    "in": "query",
    "required": false
   },
   {
    "name": "market",
    "in": "query",
    "required": false
   },
   {
    "name": "currency",
    "in": "query",
    "required": false
   },
   {
    "name": "owner",
    "in": "query",
    "required": false
   },
   {
    "name": "status",
    "in": "query",
    "required": false
   },
   {
    "name": "search",
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
 "listDynamicPricingStrategy": {
  "method": "GET",
  "path": "/dynamic-pricing-strategy",
  "contract": "catalogue",
  "summary": "Dynamic Pricing Strategy Command Center",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "strategyType",
    "in": "query",
    "required": false
   },
   {
    "name": "status",
    "in": "query",
    "required": false
   },
   {
    "name": "automationMode",
    "in": "query",
    "required": false
   },
   {
    "name": "venue",
    "in": "query",
    "required": false
   },
   {
    "name": "search",
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
 "listRentalPricingProfiles": {
  "method": "GET",
  "path": "/rental-pricing-profiles",
  "contract": "rental",
  "summary": "Pricing profiles, and the products with none",
  "permission": "RENTAL_VIEW",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "productId",
    "in": "query",
    "required": null
   },
   {
    "name": "unpricedOnly",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "RentalPricingProfile"
 },
 "requestRentalCommercialOverride": {
  "method": "POST",
  "path": "/rental-overrides",
  "contract": "rental",
  "summary": "Deviate from policy, with a reason and an approver",
  "permission": "RENTAL_OVERRIDE",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "RentalOverride",
  "responds": "RentalOverride"
 },
 "setRentalDepositPolicy": {
  "method": "PUT",
  "path": "/rental-deposit-policies",
  "contract": "rental",
  "summary": "How much is held, how, and what happens to it",
  "permission": "RENTAL_PRICE",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "RentalDepositPolicy",
  "responds": "RentalDepositPolicy"
 },
 "setRentalFeePolicy": {
  "method": "PUT",
  "path": "/rental-fee-policies",
  "contract": "rental",
  "summary": "Grace period, late fees and extension pricing",
  "permission": "RENTAL_PRICE",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "RentalFeePolicy",
  "responds": "RentalFeePolicy"
 },
 "simulateRentalPricing": {
  "method": "POST",
  "path": "/rental-price/simulate",
  "contract": "rental",
  "summary": "Test a commercial configuration before publishing it",
  "permission": "RENTAL_PRICE",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "RentalQuoteRequest",
  "responds": null
 },
 "transitionDynamicPricingStrategy": {
  "method": "POST",
  "path": "/dynamic-pricing-strategies/{strategyId}/lifecycle",
  "contract": "catalogue",
  "summary": "Activate, pause, resume or retire a dynamic pricing strategy",
  "permission": "PRICE_CONFIGURE",
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
  "responds": "DynamicPricingStrategy"
 },
 "updateRentalPricingProfile": {
  "method": "PUT",
  "path": "/rental-pricing-profiles/{profileId}",
  "contract": "rental",
  "summary": "Change a pricing profile",
  "permission": "RENTAL_PRICE",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "RentalPricingProfile",
  "responds": "RentalPricingProfile"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "DynamicPricingStrategy": {
  "type": "object",
  "x-ticvai-persistence": "catalogue.dynamic_pricing_strategy",
  "description": "**A dynamic pricing strategy: what it prices, from which base and how often** (29 September, data model DM3). ADM-088 and ADM-089. Its rules are `pricing.dynamic_price_rule` rows naming it; its ladder `catalogue.price_ladder`; its limits and automation `catalogue.dynamic_pricing_control`. **Rules-based now; AI factors inform, never replace, the rules** (MoM 19 Aug 2026).",
  "required": [
   "id",
   "scopePath",
   "code",
   "name",
   "strategyType",
   "scopeType",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005). Operations write it at `venue` scope."
   },
   "code": {
    "type": "string",
    "maxLength": 40
   },
   "name": {
    "type": "string",
    "maxLength": 200
   },
   "description": {
    "type": "string",
    "nullable": true
   },
   "strategyType": {
    "type": "string",
    "enum": [
     "demandBased",
     "occupancyBased",
     "availabilityBased",
     "inventoryBased",
     "bookingVelocity",
     "timeToEvent",
     "seasonal",
     "dayOfWeek",
     "timeslot",
     "channel",
     "segment",
     "location",
     "hybrid"
    ]
   },
   "scopeType": {
    "type": "string",
    "enum": [
     "singleProduct",
     "productFamily",
     "event",
     "multiplePerformances",
     "venue",
     "selectedTimeslots",
     "selectedPriceCategories"
    ]
   },
   "venueId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "productId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "productFamily": {
    "type": "string",
    "maxLength": 100,
    "nullable": true
   },
   "eventId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "performanceIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "timeslotIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "priceCategoryIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "businessUnit": {
    "type": "string",
    "maxLength": 100,
    "nullable": true
   },
   "marketCode": {
    "type": "string",
    "maxLength": 40,
    "nullable": true
   },
   "basePriceSource": {
    "type": "string",
    "maxLength": 100,
    "description": "The price list or rate the adjustments start from."
   },
   "evaluationFrequency": {
    "type": "string",
    "enum": [
     "every15Minutes",
     "every30Minutes",
     "hourly",
     "daily",
     "onInventoryChange",
     "onThresholdTrigger"
    ],
    "default": "hourly"
   },
   "combinationMode": {
    "type": "string",
    "enum": [
     "independent",
     "combinable",
     "exclusive",
     "fallback"
    ],
    "default": "independent"
   },
   "effectiveFrom": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "effectiveTo": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "clonedFromStrategyId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "ownerPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "status": {
    "type": "string",
    "enum": [
     "draft",
     "active",
     "paused",
     "frozen",
     "expired",
     "retired"
    ],
    "default": "draft"
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
 "RentalDepositPolicy": {
  "type": "object",
  "x-ticvai-persistence": "rental.deposit_policy",
  "description": "Boards 4.6 and 4.7. **Held, not taken**, and settled against an inspection.",
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "productId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "categoryId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "required": {
    "type": "boolean",
    "default": true
   },
   "basis": {
    "type": "string",
    "enum": [
     "fixed",
     "percentage",
     "riskBased"
    ]
   },
   "fixedAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "percentage": {
    "type": "number",
    "nullable": true
   },
   "minimumAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "maximumAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "instruments": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "cardPreAuthorisation",
      "cardCharge",
      "cash",
      "wallet"
     ]
    }
   },
   "autoRelease": {
    "type": "boolean",
    "default": true
   },
   "inspectionRequiredBeforeRelease": {
    "type": "boolean",
    "default": false
   },
   "autoReleaseDelayHours": {
    "type": "integer",
    "default": 0
   },
   "partialCapturePermitted": {
    "type": "boolean",
    "default": true
   },
   "supervisorApprovalThreshold": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "waiverEligible": {
    "type": "boolean",
    "default": false
   },
   "scopePath": {
    "type": "string"
   }
  }
 },
 "RentalFeePolicy": {
  "type": "object",
  "x-ticvai-persistence": "rental.fee_policy",
  "description": "Board 4.8. **Extension is priced below late return on purpose** — *\"this encourages customers to extend properly rather than returning late.\"*\n",
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "productId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "gracePeriodMinutes": {
    "type": "integer",
    "default": 0
   },
   "lateFeeBasis": {
    "type": "string",
    "enum": [
     "fixed",
     "perMinute",
     "per15Minutes",
     "per30Minutes",
     "perHour",
     "tiered"
    ]
   },
   "lateFeeAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "lateFeeTiers": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "afterMinutes": {
       "type": "integer"
      },
      "amount": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      }
     }
    }
   },
   "maximumDailyCharge": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "extensionPricePerIncrement": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "extensionIncrementMinutes": {
    "type": "integer",
    "default": 30
   },
   "notReturnedAfterHours": {
    "type": "integer",
    "nullable": true,
    "description": "**When a late rental becomes a lost one.** The deposit is captured in full and the asset retired; without a threshold the fee accrues forever and nobody decides.\n"
   },
   "damageFeeMaximum": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "**A ceiling, not a rate.** Added 22 September: `rental.settlement.damage_fee` was stored with nothing bounding it. **A dent is assessed, not tabulated** — the amount is entered per incident against the actual damage, so the control is how high an operator may go, the same shape `maximumDailyCharge` already gives the late fee.\n"
   },
   "damageFeeApprovalAbove": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "**Above this, a second person signs it off.** A damage fee is the one charge on a settlement that a single operator decides alone, and the one a guest is most likely to dispute. The shape is `orders.RefundPolicy.requiresApprovalAbove`, applied to the other direction of money.\n"
   },
   "missingItemFeeBasis": {
    "type": "string",
    "enum": [
     "replacementCost",
     "fixedAmount"
    ],
    "description": "**What an unreturned item costs.** `replacementCost` reads the item's own replacement value, which is what the fee usually is; `fixedAmount` uses `missingItemFeeAmount`. Added 22 September — `rental.settlement.missing_item_fee` was stored with no source.\n"
   },
   "missingItemFeeAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Used when `missingItemFeeBasis` is `fixedAmount`."
   },
   "scopePath": {
    "type": "string"
   }
  }
 },
 "RentalOverride": {
  "type": "object",
  "x-ticvai-persistence": "rental.override",
  "description": "Board 4.9. **The original amount is recorded as well as the adjusted one.**",
  "required": [
   "kind",
   "reason"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "bookingId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "kind": {
    "type": "string",
    "enum": [
     "priceOverride",
     "complimentary",
     "depositWaiver",
     "depositReduction",
     "lateFeeWaiver",
     "damageFeeWaiver",
     "extensionFeeWaiver",
     "manualRefund",
     "goodwill"
    ]
   },
   "originalAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "adjustedAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "reason": {
    "type": "string"
   },
   "requestedBy": {
    "type": "string",
    "format": "uuid"
   },
   "approvedBy": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "approvalRequestId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "at": {
    "type": "string",
    "format": "date-time"
   },
   "scopePath": {
    "type": "string"
   }
  }
 },
 "RentalPriceExplanation": {
  "type": "object",
  "description": "Board 4.10 — *\"show why the price was calculated.\"* **The ordered trace, including the rules that did not apply**, because *\"why is it not the peak price\"* is asked as often as *\"why is it\"*.\n",
  "properties": {
   "quote": {
    "$ref": "#/components/schemas/RentalQuote"
   },
   "steps": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "order": {
       "type": "integer"
      },
      "stage": {
       "type": "string",
       "enum": [
        "basePrice",
        "locationRule",
        "calendarRule",
        "dynamicPricing",
        "channelEligibility",
        "promotion",
        "manualOverride",
        "tax"
       ]
      },
      "ruleId": {
       "type": "string",
       "format": "uuid",
       "nullable": true
      },
      "ruleName": {
       "type": "string",
       "nullable": true
      },
      "applied": {
       "type": "boolean"
      },
      "skippedBecause": {
       "type": "string",
       "nullable": true
      },
      "amountBefore": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      },
      "amountAfter": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      }
     }
    }
   }
  }
 },
 "RentalPricingProfile": {
  "type": "object",
  "x-ticvai-persistence": "rental.pricing_profile",
  "description": "Board 4.2. **Several will apply at once**, and the precedence is configurable and auditable (board 4.10).\n",
  "required": [
   "code",
   "name",
   "model"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "code": {
    "type": "string"
   },
   "name": {
    "type": "string"
   },
   "productId": {
    "type": "string",
    "format": "uuid"
   },
   "venueId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "locationIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "currency": {
    "type": "string",
    "pattern": "^[A-Z]{3}$",
    "x-ticvai-persisted": false,
    "description": "**Resolved from the region, not stored** (ADR-0018). Region-scoped and not overridable below it, so a row in a UAE region is AED and cannot be anything else. Kept on the wire, removed from the table.\n"
   },
   "salesChannel": {
    "type": "string",
    "nullable": true
   },
   "customerSegmentId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "model": {
    "type": "string",
    "enum": [
     "flat",
     "durationBased",
     "tiered",
     "peakOffPeak",
     "weekend",
     "seasonal",
     "dynamic",
     "hybrid"
    ]
   },
   "basePrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "durationTiers": {
    "type": "array",
    "description": "Board 4.3. *30 min AED 40, 60 min AED 60, 90 min AED 80, 120 min AED 95.*",
    "items": {
     "type": "object",
     "properties": {
      "minutes": {
       "type": "integer"
      },
      "price": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      }
     }
    }
   },
   "minimumCharge": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "billingIncrementMinutes": {
    "type": "integer",
    "nullable": true
   },
   "additionalIncrementPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "rounding": {
    "type": "string",
    "enum": [
     "exactUsage",
     "roundUp15",
     "roundUp30",
     "roundUpHour"
    ],
    "default": "exactUsage"
   },
   "calendarRules": {
    "type": "array",
    "description": "Board 4.4. *Peak 16:00–20:00 AED 90/hr; off-peak 09:00–12:00 AED 50/hr; peak season 1 Nov – 31 Mar.*\n",
    "items": {
     "type": "object",
     "properties": {
      "kind": {
       "type": "string",
       "enum": [
        "peak",
        "offPeak",
        "weekend",
        "seasonal",
        "special"
       ]
      },
      "from": {
       "type": "string",
       "nullable": true
      },
      "to": {
       "type": "string",
       "nullable": true
      },
      "dateFrom": {
       "type": "string",
       "format": "date",
       "nullable": true
      },
      "dateTo": {
       "type": "string",
       "format": "date",
       "nullable": true
      },
      "adjustmentPercent": {
       "type": "number",
       "nullable": true
      },
      "price": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      }
     }
    }
   },
   "dynamicEnabled": {
    "type": "boolean",
    "default": false
   },
   "dynamicMaxIncreasePercent": {
    "type": "number",
    "default": 25
   },
   "dynamicMaxDecreasePercent": {
    "type": "number",
    "default": 15
   },
   "priority": {
    "type": "integer",
    "default": 0
   },
   "effectiveFrom": {
    "type": "string",
    "format": "date",
    "nullable": true
   },
   "effectiveTo": {
    "type": "string",
    "format": "date",
    "nullable": true
   },
   "status": {
    "type": "string",
    "enum": [
     "draft",
     "pendingApproval",
     "active",
     "scheduled",
     "expired"
    ]
   },
   "scopePath": {
    "type": "string"
   }
  }
 },
 "RentalQuote": {
  "type": "object",
  "x-ticvai-persistence": "rental.quote",
  "description": "Board 4.10. **Rental amount and deposit are returned apart, because the deposit is not revenue.**\n**A quote `quoteRentalPrice` issues is stored until `expiresAt`**, with what was asked, so the figures it gave can be held to and checked later. `explainRentalPrice` and `simulateRentalPricing` return the same shape and store nothing (decided 29 September, data model DM4).\n**Consumed by `acceptedQuoteId`** on `createRentalBooking` and the extension. A quote is not deleted when it is used or expires: a nightly job removes quotes 30 days past `expiresAt` that no booking references, so a booking can always show the quote it was priced at (decided 29 September, writers pass; DM4).\n",
  "required": [
   "quoteId",
   "productId",
   "from",
   "to",
   "rentalAmount",
   "depositAmount"
  ],
  "properties": {
   "quoteId": {
    "type": "string",
    "format": "uuid"
   },
   "productId": {
    "type": "string",
    "format": "uuid",
    "description": "The request's product; with `locationId`, `from`, `to` and `quantity`, what was quoted."
   },
   "locationId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "from": {
    "type": "string",
    "format": "date-time"
   },
   "to": {
    "type": "string",
    "format": "date-time"
   },
   "quantity": {
    "type": "integer",
    "default": 1
   },
   "customerId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "rentalAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "taxAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "addOnAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "discountAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "totalPayable": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "depositAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "depositInstrument": {
    "type": "string",
    "nullable": true
   },
   "expiresAt": {
    "type": "string",
    "format": "date-time",
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
    "description": "The partition key (ADR-0005), written at `venue` scope."
   }
  }
 },
 "RentalQuoteRequest": {
  "type": "object",
  "required": [
   "productId",
   "from",
   "to"
  ],
  "properties": {
   "productId": {
    "type": "string",
    "format": "uuid"
   },
   "locationId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "from": {
    "type": "string",
    "format": "date-time"
   },
   "to": {
    "type": "string",
    "format": "date-time"
   },
   "quantity": {
    "type": "integer",
    "default": 1
   },
   "salesChannel": {
    "type": "string",
    "nullable": true
   },
   "customerId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "promotionCode": {
    "type": "string",
    "nullable": true
   }
  }
 }
}
```
