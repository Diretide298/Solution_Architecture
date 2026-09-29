# WS81 — Game and Ride board 4

**10 screens · 7 operations · 5 schemas · 3 permissions**

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
  `ACCESS_VALIDATE, PRODUCT_CONFIGURE, PRODUCT_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-424` | Gameplay Validation Command Center | commandCentre | 2 | 0 | — |
| `BO-425` | Gameplay Validation Rule Configuration | listDetail | 1 | 0 | — |
| `BO-426` | Deduction Priority & Funding Source Rules | listDetail | 1 | 0 | — |
| `BO-427` | All Games & Rides Pass Configuration | configEditor | 1 | 0 | — |
| `BO-428` | Specific Game/Ride Unlimited Entitlement | configEditor | 1 | 0 | — |
| `BO-429` | Specific Game/Ride Limited Entitlement | configEditor | 1 | 0 | — |
| `BO-430` | Game Package Builder | listDetail | 2 | 0 | — |
| `BO-431` | Entitlement Validity & Activation Rules | listDetail | 1 | 0 | — |
| `BO-432` | Real-Time Gameplay Authorization | listDetail | 1 | 0 | — |
| `BO-433` | Validation Simulator & Exception Analysis | listDetail | 1 | 0 | — |

## Thin screens in this batch

**BO-425, BO-426, BO-429, BO-430, BO-431, BO-432, BO-433 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "BO-424",
  "name": "Gameplay Validation Command Center",
  "module": "Games & Rides",
  "requiresModule": "games",
  "wave": 3,
  "source": {
   "pack": "Game_and_Ride_Module.pdf",
   "board": "4",
   "number": "1",
   "page": 33
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/games-rides/gameplay-validation-command-center-bo-424",
   "component": "apps/venue-management-web/src/routes/games-rides/GameplayValidationCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-100"
   ],
   "exitTo": [
    "BO-100",
    "BO-425",
    "BO-426",
    "BO-427",
    "BO-428",
    "BO-429",
    "BO-430",
    "BO-431",
    "BO-432",
    "BO-433"
   ],
   "transitions": [
    {
     "to": "BO-100",
     "trigger": "Back to Venue Home",
     "provenance": "structural — pack board 4 wiring, 11 September 2026",
     "back": true
    },
    {
     "to": "BO-425",
     "trigger": "Gameplay Validation Rule Configuration",
     "provenance": "structural — pack board 4 wiring, 11 September 2026"
    },
    {
     "to": "BO-426",
     "trigger": "Deduction Priority & Funding Source Rules",
     "provenance": "structural — pack board 4 wiring, 11 September 2026"
    },
    {
     "to": "BO-427",
     "trigger": "All Games & Rides Pass Configuration",
     "provenance": "structural — pack board 4 wiring, 11 September 2026"
    },
    {
     "to": "BO-428",
     "trigger": "Specific Game/Ride Unlimited Entitlement",
     "provenance": "structural — pack board 4 wiring, 11 September 2026"
    },
    {
     "to": "BO-429",
     "trigger": "Specific Game/Ride Limited Entitlement",
     "provenance": "structural — pack board 4 wiring, 11 September 2026"
    },
    {
     "to": "BO-430",
     "trigger": "Game Package Builder",
     "provenance": "structural — pack board 4 wiring, 11 September 2026"
    },
    {
     "to": "BO-431",
     "trigger": "Entitlement Validity & Activation Rules",
     "provenance": "structural — pack board 4 wiring, 11 September 2026"
    },
    {
     "to": "BO-432",
     "trigger": "Real-Time Gameplay Authorization",
     "provenance": "structural — pack board 4 wiring, 11 September 2026"
    },
    {
     "to": "BO-433",
     "trigger": "Validation Simulator & Exception Analysis",
     "provenance": "structural — pack board 4 wiring, 11 September 2026"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Operators can monitor gameplay validation results and immediately identify abnormal rejection patterns.",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen a metric directory (§KPI Cards) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's",
  "purpose": "Provide an operational overview of gameplay authorization across all games and rides.",
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "filters",
     "components": [
      {
       "kind": "searchField",
       "label": "Search gameplay validation",
       "provenance": "pack Game_and_Ride_Module.pdf, page 33 §Filters"
      },
      {
       "kind": "multiSelect",
       "label": "Filter by",
       "columns": [
        "Venue",
        "Zone",
        "Attraction",
        "Validation Type",
        "Result",
        "Date/Time"
       ],
       "notes": "The pack filters this screen by venue, zone, attraction, validation type, result, date/time — which are present is a decision the pack already made.",
       "provenance": "pack Game_and_Ride_Module.pdf, page 33 §Filters"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Gameplay Requests Today",
       "provenance": "pack Game_and_Ride_Module.pdf, page 33 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Authorized Plays",
       "provenance": "pack Game_and_Ride_Module.pdf, page 33 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Rejected Plays",
       "provenance": "pack Game_and_Ride_Module.pdf, page 33 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Entitlement Plays",
       "provenance": "pack Game_and_Ride_Module.pdf, page 33 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Paid Plays",
       "provenance": "pack Game_and_Ride_Module.pdf, page 33 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Bonus Plays",
       "provenance": "pack Game_and_Ride_Module.pdf, page 33 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Free Plays",
       "provenance": "pack Game_and_Ride_Module.pdf, page 33 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Validation Errors",
       "provenance": "pack Game_and_Ride_Module.pdf, page 33 §KPI Cards"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The gameplay validation list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the gameplay validation untouched.",
   "emptyFirstRun": "No gameplay validation yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the gameplay validation are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getGameplayValidationRules",
    "contract": "games",
    "purpose": "Rules in force",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "listGameplayTransactions",
    "contract": "games",
    "purpose": "What they produced",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "Gameplay Requests Today",
    "Authorized Plays",
    "Rejected Plays",
    "Entitlement Plays",
    "Paid Plays",
    "Bonus Plays"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-424",
   "workshopBoard": "wireframes/WS61 Game and Ride Board 4.dc.html#bo-424"
  },
  "apisNote": "Regenerated 9 September 2026 from Game_and_Ride_Module.pdf page 33. 0 of 6 labels bound to a contract property; 14 of 28 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-425",
  "name": "Gameplay Validation Rule Configuration",
  "module": "Games & Rides",
  "requiresModule": "games",
  "wave": 3,
  "source": {
   "pack": "Game_and_Ride_Module.pdf",
   "board": "4",
   "number": "2",
   "page": 34
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/games-rides/gameplay-validation-rule-configuration-bo-425",
   "component": "apps/venue-management-web/src/routes/games-rides/GameplayValidationRuleConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-424"
   ],
   "exitTo": [
    "BO-424"
   ],
   "transitions": [
    {
     "to": "BO-424",
     "trigger": "Back to Gameplay Validation Command Center",
     "provenance": "structural — pack board 4 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Validation logic can be configured and executed consistently before gameplay authorization.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Configure the checks TICVAI performs before allowing a game or ride to start. The source requires validation before game start against balance, bonus and applicable entitlements.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Game_and_Ride_Module.pdf, page 34"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Game_and_Ride_Module.pdf, page 34"
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
       "impliedBy": "setGameplayValidationRules",
       "label": "Save",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setGameplayValidationRules"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The gameplay validation rule list.",
   "error": "Could not load. Names which read failed and leaves the gameplay validation rule untouched.",
   "emptyFirstRun": "No gameplay validation rule yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the gameplay validation rule are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setGameplayValidationRules",
    "contract": "games",
    "purpose": "What a tap is checked against",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getGameplayValidationRules"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-425",
   "workshopBoard": "wireframes/WS61 Game and Ride Board 4.dc.html#bo-425"
  },
  "apisNote": "Regenerated 9 September 2026 from Game_and_Ride_Module.pdf page 34. 0 of 0 labels bound to a contract property; 0 of 25 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-426",
  "name": "Deduction Priority & Funding Source Rules",
  "module": "Games & Rides",
  "requiresModule": "games",
  "wave": 3,
  "source": {
   "pack": "Game_and_Ride_Module.pdf",
   "board": "4",
   "number": "3",
   "page": 35
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/games-rides/deduction-priority-funding-source-rules-bo-426",
   "component": "apps/venue-management-web/src/routes/games-rides/DeductionPriorityFundingSourceRules.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-424"
   ],
   "exitTo": [
    "BO-424"
   ],
   "transitions": [
    {
     "to": "BO-424",
     "trigger": "Back to Gameplay Validation Command Center",
     "provenance": "structural — pack board 4 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "purposeNote": "The engine applies the configured funding priority and uses bonus first where the business rule requires it.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Determine which wallet/value source TICVAI consumes when more than one valid funding source is available. Requirement 10.2.7 explicitly states: “Bonus deduction should be done first.”",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Game_and_Ride_Module.pdf, page 35"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Game_and_Ride_Module.pdf, page 35"
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
       "impliedBy": "setGameplayValidationRules",
       "label": "Save",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setGameplayValidationRules"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The deduction priority funding list.",
   "error": "Could not load. Names which read failed and leaves the deduction priority funding untouched.",
   "emptyFirstRun": "No deduction priority funding yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the deduction priority funding are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setGameplayValidationRules",
    "contract": "games",
    "purpose": "Deduction priority",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getGameplayValidationRules"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-426",
   "workshopBoard": "wireframes/WS61 Game and Ride Board 4.dc.html#bo-426"
  },
  "apisNote": "Regenerated 9 September 2026 from Game_and_Ride_Module.pdf page 35. 0 of 0 labels bound to a contract property; 0 of 18 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-427",
  "name": "All Games & Rides Pass Configuration",
  "module": "Games & Rides",
  "requiresModule": "games",
  "wave": 3,
  "source": {
   "pack": "Game_and_Ride_Module.pdf",
   "board": "4",
   "number": "4",
   "page": 36
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/games-rides/all-games-rides-pass-configuration-bo-427",
   "component": "apps/venue-management-web/src/routes/games-rides/AllGamesRidesPassConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-424"
   ],
   "exitTo": [
    "BO-424"
   ],
   "transitions": [
    {
     "to": "BO-424",
     "trigger": "Back to Gameplay Validation Command Center",
     "provenance": "structural — pack board 4 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "purposeNote": "A valid all-games ticket allows access to all applicable attractions without requiring individual paid-wallet deductions.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Pass Setup; Options) and no display directory — it is settings, not a population",
  "purpose": "Configure a ticket/product that permits the guest to play all games/rides in the amusement park. This directly represents requirement 10.2.8.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Pass Name",
       "provenance": "pack Game_and_Ride_Module.pdf, page 36 §Pass Setup"
      },
      {
       "kind": "selectField",
       "label": "Product Code",
       "provenance": "pack Game_and_Ride_Module.pdf, page 36 §Pass Setup"
      },
      {
       "kind": "selectField",
       "label": "Venue",
       "provenance": "pack Game_and_Ride_Module.pdf, page 36 §Pass Setup"
      },
      {
       "kind": "selectField",
       "label": "Valid From",
       "provenance": "pack Game_and_Ride_Module.pdf, page 36 §Pass Setup"
      },
      {
       "kind": "selectField",
       "label": "Valid Until",
       "provenance": "pack Game_and_Ride_Module.pdf, page 36 §Pass Setup"
      },
      {
       "kind": "selectField",
       "label": "Activation Method",
       "provenance": "pack Game_and_Ride_Module.pdf, page 36 §Pass Setup"
      },
      {
       "kind": "selectField",
       "label": "Included Attraction Types",
       "provenance": "pack Game_and_Ride_Module.pdf, page 36 §Pass Setup"
      },
      {
       "kind": "selectField",
       "label": "Excluded Attractions",
       "provenance": "pack Game_and_Ride_Module.pdf, page 36 §Pass Setup"
      },
      {
       "kind": "selectField",
       "label": "Status",
       "provenance": "pack Game_and_Ride_Module.pdf, page 36 §Pass Setup"
      },
      {
       "kind": "selectField",
       "label": "Unlimited",
       "provenance": "pack Game_and_Ride_Module.pdf, page 36 §Options"
      },
      {
       "kind": "selectField",
       "label": "Limited Total Plays",
       "provenance": "pack Game_and_Ride_Module.pdf, page 36 §Options"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The all games rides configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the all games rides untouched.",
   "emptyFirstRun": "No all games rides configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "createGameEntitlement",
    "contract": "games",
    "purpose": "An all-games pass",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listGameEntitlements"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-427",
   "workshopBoard": "wireframes/WS61 Game and Ride Board 4.dc.html#bo-427"
  },
  "apisNote": "Regenerated 9 September 2026 from Game_and_Ride_Module.pdf page 36. 0 of 0 labels bound to a contract property; 11 of 20 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-428",
  "name": "Specific Game/Ride Unlimited Entitlement",
  "module": "Games & Rides",
  "requiresModule": "games",
  "wave": 3,
  "source": {
   "pack": "Game_and_Ride_Module.pdf",
   "board": "4",
   "number": "5",
   "page": 37
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/games-rides/specific-game-ride-unlimited-entitlement-bo-428",
   "component": "apps/venue-management-web/src/routes/games-rides/SpecificGameRideUnlimitedEntitlement.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-424"
   ],
   "exitTo": [
    "BO-424"
   ],
   "transitions": [
    {
     "to": "BO-424",
     "trigger": "Back to Gameplay Validation Command Center",
     "provenance": "structural — pack board 4 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "purposeNote": "The guest can repeatedly use selected games/rides while the entitlement remains valid.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Entitlement Configuration) and no display directory — it is settings, not a population",
  "purpose": "Configure products that provide unlimited free usage of selected games or rides. This directly implements requirement 10.2.11.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Entitlement Name",
       "provenance": "pack Game_and_Ride_Module.pdf, page 37 §Entitlement Configuration"
      },
      {
       "kind": "selectField",
       "label": "Product",
       "provenance": "pack Game_and_Ride_Module.pdf, page 37 §Entitlement Configuration"
      },
      {
       "kind": "selectField",
       "label": "Venue",
       "provenance": "pack Game_and_Ride_Module.pdf, page 37 §Entitlement Configuration"
      },
      {
       "kind": "selectField",
       "label": "Included Games",
       "provenance": "pack Game_and_Ride_Module.pdf, page 37 §Entitlement Configuration"
      },
      {
       "kind": "selectField",
       "label": "Included Rides",
       "provenance": "pack Game_and_Ride_Module.pdf, page 37 §Entitlement Configuration"
      },
      {
       "kind": "selectField",
       "label": "Validity",
       "provenance": "pack Game_and_Ride_Module.pdf, page 37 §Entitlement Configuration"
      },
      {
       "kind": "selectField",
       "label": "Activation",
       "provenance": "pack Game_and_Ride_Module.pdf, page 37 §Entitlement Configuration"
      },
      {
       "kind": "textField",
       "label": "Unlimited Usage = ON",
       "provenance": "pack Game_and_Ride_Module.pdf, page 37 §Entitlement Configuration"
      },
      {
       "kind": "selectField",
       "label": "Status",
       "provenance": "pack Game_and_Ride_Module.pdf, page 37 §Entitlement Configuration"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The specific game ride configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the specific game ride untouched.",
   "emptyFirstRun": "No specific game ride configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "createGameEntitlement",
    "contract": "games",
    "purpose": "Unlimited on one game",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listGameEntitlements"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-428",
   "workshopBoard": "wireframes/WS61 Game and Ride Board 4.dc.html#bo-428"
  },
  "apisNote": "Regenerated 9 September 2026 from Game_and_Ride_Module.pdf page 37. 0 of 0 labels bound to a contract property; 9 of 18 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-429",
  "name": "Specific Game/Ride Limited Entitlement",
  "module": "Games & Rides",
  "requiresModule": "games",
  "wave": 3,
  "source": {
   "pack": "Game_and_Ride_Module.pdf",
   "board": "4",
   "number": "6",
   "page": 37
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/games-rides/specific-game-ride-limited-entitlement-bo-429",
   "component": "apps/venue-management-web/src/routes/games-rides/SpecificGameRideLimitedEntitlement.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-424"
   ],
   "exitTo": [
    "BO-424"
   ],
   "transitions": [
    {
     "to": "BO-424",
     "trigger": "Back to Gameplay Validation Command Center",
     "provenance": "structural — pack board 4 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Each successful gameplay transaction reduces the applicable usage allowance and prevents additional plays once the limit reaches zero.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configuration) and no display directory — it is settings, not a population",
  "purpose": "Configure products providing a defined number of free plays on specific attractions. This directly implements requirement 10.2.12.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Entitlement Name",
       "provenance": "pack Game_and_Ride_Module.pdf, page 37 §Configuration"
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "createGameEntitlement",
       "label": "Create game entitlement",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "createGameEntitlement"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The specific game ride configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the specific game ride untouched.",
   "emptyFirstRun": "No specific game ride configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "createGameEntitlement",
    "contract": "games",
    "purpose": "A limited number of plays",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listGameEntitlements"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-429",
   "workshopBoard": "wireframes/WS61 Game and Ride Board 4.dc.html#bo-429"
  },
  "apisNote": "Regenerated 9 September 2026 from Game_and_Ride_Module.pdf page 37. 0 of 0 labels bound to a contract property; 1 of 21 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-430",
  "name": "Game Package Builder",
  "module": "Games & Rides",
  "requiresModule": "games",
  "wave": 3,
  "source": {
   "pack": "Game_and_Ride_Module.pdf",
   "board": "4",
   "number": "7",
   "page": 38
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/games-rides/game-package-builder-bo-430",
   "component": "apps/venue-management-web/src/routes/games-rides/GamePackageBuilder.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-424"
   ],
   "exitTo": [
    "BO-424"
   ],
   "transitions": [
    {
     "to": "BO-424",
     "trigger": "Back to Gameplay Validation Command Center",
     "provenance": "structural — pack board 4 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Administrators can create reusable packages containing selected games/rides with different usage allowances.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Create a package containing a specific collection of games/rides. Requirement 10.2.7 explicitly requires: Create a package with specific games. Define validity for the game entitlement.",
  "gaps": [
   {
    "operation": null,
    "why": "**Game Package Builder declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write operations are missing or this screen is a view of something another screen builds.",
    "source": "contract — the screen's declared operations"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Game_and_Ride_Module.pdf, page 38"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Game_and_Ride_Module.pdf, page 38"
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
       "impliedBy": "createGameEntitlement",
       "label": "Create game entitlement",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listGameEntitlements",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "createGameEntitlement"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The game package list.",
   "error": "Could not load. Names which read failed and leaves the game package untouched.",
   "emptyFirstRun": "No game package yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the game package are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "createGameEntitlement",
    "contract": "games",
    "purpose": "Build a package",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listGameEntitlements"
    ]
   },
   {
    "operationId": "listGameEntitlements",
    "contract": "games",
    "purpose": "Existing packages",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-430",
   "workshopBoard": "wireframes/WS61 Game and Ride Board 4.dc.html#bo-430"
  },
  "apisNote": "Regenerated 9 September 2026 from Game_and_Ride_Module.pdf page 38. 0 of 0 labels bound to a contract property; 0 of 17 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-431",
  "name": "Entitlement Validity & Activation Rules",
  "module": "Games & Rides",
  "requiresModule": "games",
  "wave": 3,
  "source": {
   "pack": "Game_and_Ride_Module.pdf",
   "board": "4",
   "number": "8",
   "page": 39
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/games-rides/entitlement-validity-activation-rules-bo-431",
   "component": "apps/venue-management-web/src/routes/games-rides/EntitlementValidityActivationRules.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-424"
   ],
   "exitTo": [
    "BO-424"
   ],
   "transitions": [
    {
     "to": "BO-424",
     "trigger": "Back to Gameplay Validation Command Center",
     "provenance": "structural — pack board 4 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "purposeNote": "The validation engine determines entitlement validity using its configured activation and expiration rules.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Control when a gameplay entitlement becomes valid and when it expires. The source specifically requires the ability to define validity for game entitlements.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Game_and_Ride_Module.pdf, page 39"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Game_and_Ride_Module.pdf, page 39"
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
       "impliedBy": "createGameEntitlement",
       "label": "Create game entitlement",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "createGameEntitlement"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The entitlement validity activation list.",
   "error": "Could not load. Names which read failed and leaves the entitlement validity activation untouched.",
   "emptyFirstRun": "No entitlement validity activation yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the entitlement validity activation are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "createGameEntitlement",
    "contract": "games",
    "purpose": "Validity and activation",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listGameEntitlements"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-431",
   "workshopBoard": "wireframes/WS61 Game and Ride Board 4.dc.html#bo-431"
  },
  "apisNote": "Regenerated 9 September 2026 from Game_and_Ride_Module.pdf page 39. 0 of 0 labels bound to a contract property; 0 of 19 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-432",
  "name": "Real-Time Gameplay Authorization",
  "module": "Games & Rides",
  "requiresModule": "games",
  "wave": 3,
  "source": {
   "pack": "Game_and_Ride_Module.pdf",
   "board": "4",
   "number": "9",
   "page": 40
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/games-rides/real-time-gameplay-authorization-bo-432",
   "component": "apps/venue-management-web/src/routes/games-rides/RealTimeGameplayAuthorization.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-424"
   ],
   "exitTo": [
    "BO-424"
   ],
   "transitions": [
    {
     "to": "BO-424",
     "trigger": "Back to Gameplay Validation Command Center",
     "provenance": "structural — pack board 4 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "purposeNote": "The authorization result identifies the validation checks, funding source, amount consumed, remaining value and final decision.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Provide the operational transaction view showing exactly how TICVAI evaluates a customer tap. Requirement 10.2.13 requires the system to validate the balance/card, bonus and entitlement in real time and deduct the applicable amount before gameplay.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Game_and_Ride_Module.pdf, page 40"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Game_and_Ride_Module.pdf, page 40"
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
       "impliedBy": "authoriseGameplay",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "authoriseGameplay"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The real-time gameplay authorization list.",
   "error": "Could not load. Names which read failed and leaves the real-time gameplay authorization untouched.",
   "emptyFirstRun": "No real-time gameplay authorization yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the real-time gameplay authorization are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "authoriseGameplay",
    "contract": "games",
    "purpose": "Authorise a tap",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listGameplayTransactions",
     "getGameCard"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-432",
   "workshopBoard": "wireframes/WS61 Game and Ride Board 4.dc.html#bo-432"
  },
  "apisNote": "Regenerated 9 September 2026 from Game_and_Ride_Module.pdf page 40. 0 of 0 labels bound to a contract property; 0 of 27 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-433",
  "name": "Validation Simulator & Exception Analysis",
  "module": "Games & Rides",
  "requiresModule": "games",
  "wave": 3,
  "source": {
   "pack": "Game_and_Ride_Module.pdf",
   "board": "4",
   "number": "10",
   "page": 41
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/games-rides/validation-simulator-exception-analysis-bo-433",
   "component": "apps/venue-management-web/src/routes/games-rides/ValidationSimulatorExceptionAnalysis.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-424"
   ],
   "exitTo": [
    "BO-424"
   ],
   "transitions": [
    {
     "to": "BO-424",
     "trigger": "Back to Gameplay Validation Command Center",
     "provenance": "structural — pack board 4 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Administrators can test configuration before activation and trace exactly why an actual gameplay transaction was authorized or rejected. recommending corrective actions. Board 4 — Exact Screen Mapping The Board 4 visual must contain exactly these ten screens and in this order: # Screen 1 Gameplay Validation Command Center 2 Gameplay Validation Rule Configuration 3 Deduction Priority & Funding Source Rules 4 All Games & Rides Pass Configuration 5 Specific Game/Ride Unlimited Entitlement 6 Specific Game/Ride Limited Entitlement 7 Game Package Builder 8 Entitlement Validity & Activation Rules 9 R",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Allow administrators to test entitlement and payment configurations before deployment and investigate rejected gameplay transactions.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Game_and_Ride_Module.pdf, page 41"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Game_and_Ride_Module.pdf, page 41"
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
       "impliedBy": "simulateGameplayAuthorisation",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "simulateGameplayAuthorisation"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The validation simulator exception list.",
   "error": "Could not load. Names which read failed and leaves the validation simulator exception untouched.",
   "emptyFirstRun": "No validation simulator exception yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the validation simulator exception are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "simulateGameplayAuthorisation",
    "contract": "games",
    "purpose": "Simulate and analyse exceptions",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-433",
   "workshopBoard": "wireframes/WS61 Game and Ride Board 4.dc.html#bo-433"
  },
  "apisNote": "Regenerated 9 September 2026 from Game_and_Ride_Module.pdf page 41. 0 of 0 labels bound to a contract property; 0 of 75 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
 "authoriseGameplay": {
  "method": "POST",
  "path": "/gameplay-authorisations",
  "contract": "games",
  "summary": "Decide a tap, now",
  "permission": "ACCESS_VALIDATE",
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
  "requestBody": "GameplayAuthorisationRequest",
  "responds": "GameplayAuthorisation"
 },
 "createGameEntitlement": {
  "method": "POST",
  "path": "/game-entitlements",
  "contract": "games",
  "summary": "Define a pass, package or per-game entitlement",
  "permission": "PRODUCT_CONFIGURE",
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
  "requestBody": "GameEntitlement",
  "responds": "GameEntitlement"
 },
 "getGameplayValidationRules": {
  "method": "GET",
  "path": "/gameplay-validation-rules",
  "contract": "games",
  "summary": "What a tap is checked against, and in what order",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "GameplayValidationRules"
 },
 "listGameEntitlements": {
  "method": "GET",
  "path": "/game-entitlements",
  "contract": "games",
  "summary": "Passes, packages and per-game entitlements",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "GameEntitlement"
 },
 "listGameplayTransactions": {
  "method": "GET",
  "path": "/gameplay-transactions",
  "contract": "games",
  "summary": "Taps, decisions and what they cost",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "from",
    "in": "query",
    "required": null
   },
   {
    "name": "readerId",
    "in": "query",
    "required": null
   },
   {
    "name": "outcome",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "GameplayTransaction"
 },
 "setGameplayValidationRules": {
  "method": "PUT",
  "path": "/gameplay-validation-rules",
  "contract": "games",
  "summary": "Deduction priority and the order of checks",
  "permission": "PRODUCT_CONFIGURE",
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
  "requestBody": "GameplayValidationRules",
  "responds": "GameplayValidationRules"
 },
 "simulateGameplayAuthorisation": {
  "method": "POST",
  "path": "/gameplay-authorisations/simulate",
  "contract": "games",
  "summary": "What would happen if this card tapped this reader",
  "permission": "PRODUCT_CONFIGURE",
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
  "requestBody": "GameplayAuthorisationRequest",
  "responds": "GameplayAuthorisation"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "GameEntitlement": {
  "type": "object",
  "x-ticvai-persistence": "games.entitlement",
  "description": "Board 4. **A right to play, not money** — consumed before money is.",
  "required": [
   "code",
   "kind"
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
   "kind": {
    "type": "string",
    "enum": [
     "allGamesPass",
     "unlimitedSingleGame",
     "limitedSingleGame",
     "package",
     "freePlay"
    ]
   },
   "gameIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "attractionTypeIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "playCount": {
    "type": "integer",
    "nullable": true,
    "description": "For `limitedSingleGame` and `package`. Null means unlimited."
   },
   "validityKind": {
    "type": "string",
    "enum": [
     "sameDay",
     "days",
     "untilDate",
     "untilUsed"
    ]
   },
   "validityDays": {
    "type": "integer",
    "nullable": true
   },
   "activationKind": {
    "type": "string",
    "enum": [
     "onPurchase",
     "onFirstUse",
     "onDate"
    ],
    "default": "onFirstUse",
    "description": "**On first use is what a guest expects from a day pass bought the night before.** On purchase is what a venue defaults to by accident, and it costs them a day.\n"
   },
   "dailyPlayCap": {
    "type": "integer",
    "nullable": true
   },
   "cooldownMinutes": {
    "type": "integer",
    "nullable": true,
    "description": "**Unlimited does not mean continuous.** A cooldown is how one child does not hold a popular ride all afternoon.\n"
   },
   "linkedProductId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "scopePath": {
    "type": "string"
   },
   "isActive": {
    "type": "boolean",
    "default": true
   }
  }
 },
 "GameplayAuthorisation": {
  "type": "object",
  "x-ticvai-persistence": "games.authorisation",
  "description": "Board 4.9. **The refusal reason is the product.**",
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "decision": {
    "type": "string",
    "enum": [
     "allow",
     "refuse"
    ]
   },
   "reason": {
    "type": "string",
    "nullable": true,
    "enum": [
     "ok",
     "cardNotFound",
     "cardExpired",
     "cardBlocked",
     "retapTooSoon",
     "heightRestriction",
     "ageRestriction",
     "insufficientFunds",
     "entitlementExhausted",
     "entitlementNotValidHere",
     "cooldownActive",
     "dailyCapReached",
     "readerNotConfigured",
     "gameUnavailable"
    ]
   },
   "guestMessage": {
    "type": "string",
    "nullable": true,
    "description": "***\"No plays left on your pass\"* rather than *\"Declined\"*.** One is a guest who understands; the other is a member of staff walking over.\n"
   },
   "chargedFrom": {
    "type": "string",
    "nullable": true
   },
   "amount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "entitlementId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "remainingBalance": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "remainingPlays": {
    "type": "integer",
    "nullable": true
   },
   "trace": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "check": {
       "type": "string"
      },
      "passed": {
       "type": "boolean"
      },
      "detail": {
       "type": "string",
       "nullable": true
      }
     }
    }
   },
   "decidedOffline": {
    "type": "boolean",
    "default": false
   },
   "scopePath": {
    "type": "string"
   }
  }
 },
 "GameplayAuthorisationRequest": {
  "type": "object",
  "required": [
   "readerId"
  ],
  "properties": {
   "readerId": {
    "type": "string",
    "format": "uuid"
   },
   "cardId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "credentialIdentifier": {
    "type": "string",
    "nullable": true
   },
   "gameId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "at": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "guestHeightCm": {
    "type": "integer",
    "nullable": true
   },
   "offline": {
    "type": "boolean",
    "default": false
   }
  }
 },
 "GameplayTransaction": {
  "type": "object",
  "x-ticvai-persistence": "games.gameplay_transaction",
  "description": "Boards 8.2 and 8.5. **The refused ones are the valuable half.**",
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "readerId": {
    "type": "string",
    "format": "uuid"
   },
   "gameId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "cardId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "at": {
    "type": "string",
    "format": "date-time"
   },
   "outcome": {
    "type": "string",
    "enum": [
     "allowed",
     "refused",
     "reversed"
    ]
   },
   "reason": {
    "type": "string",
    "nullable": true
   },
   "amount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "chargedFrom": {
    "type": "string",
    "nullable": true
   },
   "entitlementId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "ticketsEarned": {
    "type": "integer",
    "nullable": true
   },
   "decidedOffline": {
    "type": "boolean",
    "default": false
   },
   "syncedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "scopePath": {
    "type": "string"
   }
  }
 },
 "GameplayValidationRules": {
  "type": "object",
  "x-ticvai-persistence": "games.validation_rules",
  "description": "Boards 4.2 and 4.3. **Must be an answer, stated once**, rather than whatever the firmware happens to do.\n",
  "properties": {
   "deductionOrder": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "entitlement",
      "freePlay",
      "bonusCredit",
      "promotionalCredit",
      "gameCredit",
      "cashCredit",
      "directPay"
     ]
    }
   },
   "checkOrder": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "cardValid",
      "cardNotExpired",
      "cardNotBlocked",
      "restrictionsMet",
      "retapWindow",
      "entitlementAvailable",
      "fundsSufficient"
     ]
    }
   },
   "allowPartialEntitlement": {
    "type": "boolean",
    "default": false,
    "description": "**Whether an entitlement covering part of the price may be topped up with credit.** Usually no, because a guest who thinks they have a pass does not expect a charge.\n"
   },
   "refuseBelowBalance": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "offlineDecisionAllowed": {
    "type": "boolean",
    "default": true
   },
   "offlineMaximumValue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "scopePath": {
    "type": "string"
   }
  }
 }
}
```
