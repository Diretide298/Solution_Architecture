# WS02 — Access Control board 2

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
| `BO-154` | Access Rule Command Center | commandCentre | 1 | 0 | — |
| `BO-155` | Visual Access Rule Builder | listDetail | 1 | 0 | — |
| `BO-156` | Entry, Exit & Re-entry Rules | listDetail | 1 | 0 | — |
| `BO-157` | Anti-Passback & Journey Sequence | configEditor | 1 | 0 | — |
| `BO-158` | Access Validity & Time Rules | configEditor | 1 | 3 | — |
| `BO-159` | Entitlement Consumption Engine | listDetail | 1 | 0 | — |
| `BO-160` | Multi-Park & Crossover Rules | listDetail | 1 | 0 | — |
| `BO-161` | Guest, Companion & Eligibility Rules | configEditor | 1 | 0 | — |
| `BO-162` | Group Admission & Quantity Validation | listDetail | 1 | 0 | — |
| `BO-163` | Rule Simulation, Conflict Check & Publication | listDetail | 1 | 0 | — |

## Thin screens in this batch

**BO-155, BO-156, BO-157, BO-159, BO-160, BO-162 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "BO-154",
  "name": "Access Rule Command Center",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Access Control Module_Reference.pdf",
   "board": "2",
   "number": "2.1",
   "page": 17
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/access-rule-command-center-bo-154",
   "component": "apps/venue-management-web/src/routes/access-venue/AccessRuleCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-100"
   ],
   "exitTo": [
    "BO-100",
    "BO-155",
    "BO-156",
    "BO-157",
    "BO-158",
    "BO-159",
    "BO-160",
    "BO-161",
    "BO-162",
    "BO-163"
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
     "to": "BO-155",
     "trigger": "Works in Visual Access Rule Builder",
     "provenance": "flow F112 step 1→2",
     "operation": "listAccessRule"
    },
    {
     "to": "BO-156",
     "trigger": "Works in Entry, Exit & Re-entry Rules",
     "provenance": "flow F112 step 3→4",
     "operation": "listAccessRule"
    },
    {
     "to": "BO-157",
     "trigger": "Works in Anti-Passback & Journey Sequence",
     "provenance": "flow F112 step 5→6",
     "operation": "listAccessRule"
    },
    {
     "to": "BO-158",
     "trigger": "Works in Access Validity & Time Rules",
     "provenance": "flow F112 step 7→8",
     "operation": "listAccessRule"
    },
    {
     "to": "BO-159",
     "trigger": "Works in Entitlement Consumption Engine",
     "provenance": "flow F112 step 9→10",
     "operation": "listAccessRule"
    },
    {
     "to": "BO-160",
     "trigger": "Works in Multi-Park & Crossover Rules",
     "provenance": "flow F112 step 11→12",
     "operation": "listAccessRule"
    },
    {
     "to": "BO-161",
     "trigger": "Works in Guest, Companion & Eligibility Rules",
     "provenance": "flow F112 step 13→14",
     "operation": "listAccessRule"
    },
    {
     "to": "BO-162",
     "trigger": "Works in Group Admission & Quantity Validation",
     "provenance": "flow F112 step 15→16",
     "operation": "listAccessRule"
    },
    {
     "to": "BO-163",
     "trigger": "Works in Rule Simulation, Conflict Check & Publication",
     "provenance": "flow F112 step 17→18",
     "operation": "listAccessRule"
    }
   ]
  },
  "density": "compact",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen both a metric directory (§Show) and a per-row directory (§Each rule displays) — counts over a population, then the population",
  "purpose": "Central configuration dashboard for all access and entitlement rules.",
  "purposeNote": "Administrator can centrally find, understand, create, clone, modify and govern all admission rules.",
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Active Access Rules",
       "provenance": "pack Access Control Module_Reference.pdf, page 17 §Show",
       "bindsTo": "AccessRuleCommandCenterView.activeAccessRules"
      },
      {
       "kind": "metricTile",
       "label": "Draft Rules",
       "provenance": "pack Access Control Module_Reference.pdf, page 17 §Show",
       "bindsTo": "AccessRuleCommandCenterView.draftRules"
      },
      {
       "kind": "metricTile",
       "label": "Scheduled Rules",
       "provenance": "pack Access Control Module_Reference.pdf, page 17 §Show",
       "bindsTo": "AccessRuleCommandCenterView.scheduledRules"
      },
      {
       "kind": "metricTile",
       "label": "Rules Pending Approval",
       "provenance": "pack Access Control Module_Reference.pdf, page 17 §Show",
       "bindsTo": "AccessRuleCommandCenterView.rulesPendingApproval"
      },
      {
       "kind": "metricTile",
       "label": "Venues Covered",
       "provenance": "pack Access Control Module_Reference.pdf, page 17 §Show",
       "bindsTo": "AccessRuleCommandCenterView.venuesCovered"
      },
      {
       "kind": "metricTile",
       "label": "Products/Tickets Covered",
       "provenance": "pack Access Control Module_Reference.pdf, page 17 §Show",
       "bindsTo": "AccessRuleCommandCenterView.productsTicketsCovered"
      },
      {
       "kind": "metricTile",
       "label": "Rules with Conflicts",
       "provenance": "pack Access Control Module_Reference.pdf, page 17 §Show",
       "bindsTo": "AccessRuleCommandCenterView.rulesWithConflicts"
      },
      {
       "kind": "metricTile",
       "label": "Rules Using Biometrics",
       "provenance": "pack Access Control Module_Reference.pdf, page 17 §Show",
       "bindsTo": "AccessRuleCommandCenterView.rulesUsingBiometrics"
      },
      {
       "kind": "metricTile",
       "label": "Rules Allowing Override",
       "provenance": "pack Access Control Module_Reference.pdf, page 17 §Show",
       "bindsTo": "AccessRuleCommandCenterView.rulesAllowingOverride"
      },
      {
       "kind": "metricTile",
       "label": "Offline-Compatible Rules",
       "provenance": "pack Access Control Module_Reference.pdf, page 17 §Show",
       "bindsTo": "AccessRuleCommandCenterView.offlineCompatibleRules"
      },
      {
       "kind": "metricTile",
       "label": "Recently Modified Rules",
       "provenance": "pack Access Control Module_Reference.pdf, page 17 §Show",
       "bindsTo": "AccessRuleCommandCenterView.recentlyModifiedRules"
      },
      {
       "kind": "metricTile",
       "label": "Upcoming Rule Changes",
       "provenance": "pack Access Control Module_Reference.pdf, page 17 §Show",
       "bindsTo": "AccessRuleCommandCenterView.upcomingRuleChanges"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "moduleTiles",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every access rule",
       "columns": [
        "Rule Applies To Location Validity Status"
       ],
       "bindsTo": "AccessRuleCommandCenterView",
       "operation": "listAccessRule",
       "provenance": "pack Access Control Module_Reference.pdf, page 17 §Each rule displays"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected access rule",
       "bindsTo": "AccessRuleCommandCenterView",
       "columns": [
        "Rule Applies To Location Validity Status"
       ],
       "notes": null,
       "provenance": "pack Access Control Module_Reference.pdf, page 17 §Each rule displays"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The access rule list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the access rule untouched.",
   "emptyFirstRun": "No access rule yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the access rule are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listAccessRule",
    "contract": "access",
    "purpose": "Access Rule Command Center",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-154"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 17. 12 of 13 labels bound to a contract property; 13 of 27 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-155",
  "name": "Visual Access Rule Builder",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Access Control Module_Reference.pdf",
   "board": "2",
   "number": "2.2",
   "page": 18
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/visual-access-rule-builder-bo-155",
   "component": "apps/venue-management-web/src/routes/access-venue/VisualAccessRuleBuilder.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-154"
   ],
   "exitTo": [
    "BO-154"
   ],
   "inferred": false,
   "notes": "**Reached from BO-154, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-154",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F112 step 2→3",
     "operation": "setVisualAccessRule"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Provide a no-code rule engine. This is where TICVAI should become significantly easier to configure than traditional access-control systems.",
  "purposeNote": "Complex admission rules can be configured without code or vendor development.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Access Control Module_Reference.pdf, page 18"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Access Control Module_Reference.pdf, page 18"
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
       "label": "Save changes",
       "provenance": "contract operation setVisualAccessRule"
      }
     ]
    },
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setVisualAccessRule"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The visual access rule list.",
   "error": "Could not load. Names which read failed and leaves the visual access rule untouched.",
   "emptyFirstRun": "No visual access rule yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the visual access rule are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setVisualAccessRule",
    "contract": "access",
    "purpose": "Visual Access Rule Builder",
    "trigger": "onAction",
    "invalidates": [
     "setVisualAccessRule"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-155"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 18. 0 of 0 labels bound to a contract property; 0 of 22 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-156",
  "name": "Entry, Exit & Re-entry Rules",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Access Control Module_Reference.pdf",
   "board": "2",
   "number": "2.3",
   "page": 19
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/entry-exit-re-entry-rules-bo-156",
   "component": "apps/venue-management-web/src/routes/access-venue/EntryExitReEntryRules.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-154"
   ],
   "exitTo": [
    "BO-154"
   ],
   "inferred": false,
   "notes": "**Reached from BO-154, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-154",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F112 step 4→5",
     "operation": "listEntryExitRule"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Configure admission quantity and journey sequencing. The source matrix explicitly requires configurable quantities for entry, exit and same-day re-entry, anti- passback intervals, required exit before re-entry, and required entry before exit.",
  "purposeNote": "The complete entry → exit → re-entry lifecycle can be configured independently by ticket/product/access policy.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Access Control Module_Reference.pdf, page 19"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Access Control Module_Reference.pdf, page 19"
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
       "impliedBy": "listEntryExitRule",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The entry exit re-entry list.",
   "error": "Could not load. Names which read failed and leaves the entry exit re-entry untouched.",
   "emptyFirstRun": "No entry exit re-entry yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the entry exit re-entry are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listEntryExitRule",
    "contract": "access",
    "purpose": "Entry, Exit & Re-entry Rules",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "EntryExitReEntryRulesView.unlimited",
    "EntryExitReEntryRulesView.once",
    "EntryExitReEntryRulesView.nTimes",
    "EntryExitReEntryRulesView.nPerDay",
    "EntryExitReEntryRulesView.nPerPeriod"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-156"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 19. 0 of 0 labels bound to a contract property; 0 of 24 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-157",
  "name": "Anti-Passback & Journey Sequence",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Access Control Module_Reference.pdf",
   "board": "2",
   "number": "2.4",
   "page": 20
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/anti-passback-journey-sequence-bo-157",
   "component": "apps/venue-management-web/src/routes/access-venue/AntiPassbackJourneySequence.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-154"
   ],
   "exitTo": [
    "BO-154"
   ],
   "inferred": false,
   "notes": "**Reached from BO-154, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-154",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F112 step 6→7",
     "operation": "listAntiPassbackJourney"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure required sequences such as) and no display directory — it is settings, not a population",
  "purpose": "Prevent credential sharing and impossible access sequences.",
  "purposeNote": "The system prevents credential sharing and invalid journey sequences while allowing configurable operational exceptions.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "textField",
       "label": "ENTRY → EXIT → RE-ENTRY",
       "provenance": "pack Access Control Module_Reference.pdf, page 20 §Configure required sequences such as"
      },
      {
       "kind": "textField",
       "label": "PARK A → CROSSOVER → PARK B",
       "provenance": "pack Access Control Module_Reference.pdf, page 20 §Configure required sequences such as"
      },
      {
       "kind": "textField",
       "label": "MAIN ENTRY → ATTRACTION ENTRY",
       "provenance": "pack Access Control Module_Reference.pdf, page 20 §Configure required sequences such as"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The anti-passback journey sequence configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the anti-passback journey sequence untouched.",
   "emptyFirstRun": "No anti-passback journey sequence configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listAntiPassbackJourney",
    "contract": "access",
    "purpose": "Anti-Passback & Journey Sequence",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-157"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 20. 0 of 0 labels bound to a contract property; 3 of 23 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-158",
  "name": "Access Validity & Time Rules",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Access Control Module_Reference.pdf",
   "board": "2",
   "number": "2.5",
   "page": 21
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/access-validity-time-rules-bo-158",
   "component": "apps/venue-management-web/src/routes/access-venue/AccessValidityTimeRules.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-154"
   ],
   "exitTo": [
    "BO-154"
   ],
   "inferred": false,
   "notes": "**Reached from BO-154, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-154",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F112 step 8→9",
     "operation": "listAccessValidityTime"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Determine when access is permitted.",
  "purposeNote": "Access validity can be controlled by dates, relative periods, calendars and precise time windows.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 3 actions on this screen and the screen declares 1 operation.** Unserved: End of Day, End of Week, End of Month. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Access Control Module_Reference.pdf, page 21 §Support"
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
       "label": "weekdays",
       "provenance": "pack Access Control Module_Reference.pdf, page 21 §Configure"
      },
      {
       "kind": "selectField",
       "label": "weekends",
       "provenance": "pack Access Control Module_Reference.pdf, page 21 §Configure"
      },
      {
       "kind": "selectField",
       "label": "peak dates",
       "provenance": "pack Access Control Module_Reference.pdf, page 21 §Configure"
      },
      {
       "kind": "selectField",
       "label": "off-peak dates",
       "provenance": "pack Access Control Module_Reference.pdf, page 21 §Configure"
      },
      {
       "kind": "selectField",
       "label": "holidays",
       "provenance": "pack Access Control Module_Reference.pdf, page 21 §Configure"
      },
      {
       "kind": "selectField",
       "label": "seasons",
       "provenance": "pack Access Control Module_Reference.pdf, page 21 §Configure"
      },
      {
       "kind": "selectField",
       "label": "event dates",
       "provenance": "pack Access Control Module_Reference.pdf, page 21 §Configure"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "destructiveButton",
       "label": "End of Day",
       "provenance": "pack Access Control Module_Reference.pdf, page 21 §Support"
      },
      {
       "kind": "destructiveButton",
       "label": "End of Week",
       "provenance": "pack Access Control Module_Reference.pdf, page 21 §Support"
      },
      {
       "kind": "destructiveButton",
       "label": "End of Month",
       "provenance": "pack Access Control Module_Reference.pdf, page 21 §Support"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmEndOfDay",
    "component": "confirmDialog",
    "trigger": "End of Day",
    "body": "**End of Day on a access validity time is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.",
    "provenance": "pack Access Control Module_Reference.pdf, page 21 §Support"
   },
   {
    "id": "confirmEndOfWeek",
    "component": "confirmDialog",
    "trigger": "End of Week",
    "body": "**End of Week on a access validity time is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.",
    "provenance": "pack Access Control Module_Reference.pdf, page 21 §Support"
   },
   {
    "id": "confirmEndOfMonth",
    "component": "confirmDialog",
    "trigger": "End of Month",
    "body": "**End of Month on a access validity time is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.",
    "provenance": "pack Access Control Module_Reference.pdf, page 21 §Support"
   }
  ],
  "states": {
   "loading": "The access validity time configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the access validity time untouched.",
   "emptyFirstRun": "No access validity time configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listAccessValidityTime",
    "contract": "access",
    "purpose": "Access Validity & Time Rules",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-158"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 21. 0 of 0 labels bound to a contract property; 10 of 25 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-159",
  "name": "Entitlement Consumption Engine",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Access Control Module_Reference.pdf",
   "board": "2",
   "number": "2.6",
   "page": 22
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/entitlement-consumption-engine-bo-159",
   "component": "apps/venue-management-web/src/routes/access-venue/EntitlementConsumptionEngine.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-154"
   ],
   "exitTo": [
    "BO-154"
   ],
   "inferred": false,
   "notes": "**Reached from BO-154, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-154",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F112 step 10→11",
     "operation": "listEntitlementConsumption"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Determine what gets consumed when access is granted. This is critical because one credential may represent several different entitlements. The matrix specifically describes a single QR capable of carrying park admission, ride entitlement, meal voucher, coupon, photo voucher and re-entry rights.",
  "purposeNote": "A validation event can consume the correct entitlement and immediately calculate the remaining balance.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 1 actions on this screen and the screen declares 1 operation.** Unserved: Membership benefit. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Access Control Module_Reference.pdf, page 22 §Support"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Access Control Module_Reference.pdf, page 22"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Access Control Module_Reference.pdf, page 22"
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
       "label": "Membership benefit",
       "provenance": "pack Access Control Module_Reference.pdf, page 22 §Support"
      }
     ]
    },
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listEntitlementConsumption",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The entitlement consumption list.",
   "error": "Could not load. Names which read failed and leaves the entitlement consumption untouched.",
   "emptyFirstRun": "No entitlement consumption yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the entitlement consumption are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listEntitlementConsumption",
    "contract": "access",
    "purpose": "Entitlement Consumption Engine",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "EntitlementConsumptionEngineView.parkAdmission",
    "EntitlementConsumptionEngineView.attractionAdmission",
    "EntitlementConsumptionEngineView.ride",
    "EntitlementConsumptionEngineView.fastPass",
    "EntitlementConsumptionEngineView.meal"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-159"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 22. 0 of 0 labels bound to a contract property; 1 of 27 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-160",
  "name": "Multi-Park & Crossover Rules",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Access Control Module_Reference.pdf",
   "board": "2",
   "number": "2.7",
   "page": 23
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/multi-park-crossover-rules-bo-160",
   "component": "apps/venue-management-web/src/routes/access-venue/MultiParkCrossoverRules.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-154"
   ],
   "exitTo": [
    "BO-154"
   ],
   "inferred": false,
   "notes": "**Reached from BO-154, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-154",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F112 step 12→13",
     "operation": "listMultiParkCrossover"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Configure complex access between multiple parks/venues. The matrix specifically requires multi-park access on different days, same-day crossover, park-specific entry quantities and conditional access based on previous park admission.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Access Control Module_Reference.pdf, page 23"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Access Control Module_Reference.pdf, page 23"
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
       "impliedBy": "listMultiParkCrossover",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The multi-park crossover rules list.",
   "error": "Could not load. Names which read failed and leaves the multi-park crossover rules untouched.",
   "emptyFirstRun": "No multi-park crossover rules yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the multi-park crossover rules are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listMultiParkCrossover",
    "contract": "access",
    "purpose": "Multi-Park & Crossover Rules",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-160"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 23. 0 of 0 labels bound to a contract property; 0 of 3 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-161",
  "name": "Guest, Companion & Eligibility Rules",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Access Control Module_Reference.pdf",
   "board": "2",
   "number": "2.8",
   "page": 24
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/guest-companion-eligibility-rules-bo-161",
   "component": "apps/venue-management-web/src/routes/access-venue/GuestCompanionEligibilityRules.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-154"
   ],
   "exitTo": [
    "BO-154"
   ],
   "inferred": false,
   "notes": "**Reached from BO-154, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-154",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F112 step 14→15",
     "operation": "listGuestCompanionEligibility"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Apply access conditions based on guest characteristics and relationships.",
  "purposeNote": "Access rules can consider guest category, linked persons and companion requirements.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 1 actions on this screen and the screen declares 1 operation.** Unserved: Child Ticket + Assigned Adult Ticket. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Access Control Module_Reference.pdf, page 24 §Support"
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
       "label": "Adult",
       "provenance": "pack Access Control Module_Reference.pdf, page 24 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Child",
       "provenance": "pack Access Control Module_Reference.pdf, page 24 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Junior",
       "provenance": "pack Access Control Module_Reference.pdf, page 24 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Senior",
       "provenance": "pack Access Control Module_Reference.pdf, page 24 §Configure"
      },
      {
       "kind": "selectField",
       "label": "POD",
       "provenance": "pack Access Control Module_Reference.pdf, page 24 §Configure"
      },
      {
       "kind": "selectField",
       "label": "POD Companion",
       "provenance": "pack Access Control Module_Reference.pdf, page 24 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Nanny",
       "provenance": "pack Access Control Module_Reference.pdf, page 24 §Configure"
      },
      {
       "kind": "selectField",
       "label": "VIP",
       "provenance": "pack Access Control Module_Reference.pdf, page 24 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Member",
       "provenance": "pack Access Control Module_Reference.pdf, page 24 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Staff",
       "provenance": "pack Access Control Module_Reference.pdf, page 24 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Accreditation",
       "provenance": "pack Access Control Module_Reference.pdf, page 24 §Configure"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Child Ticket + Assigned Adult Ticket",
       "provenance": "pack Access Control Module_Reference.pdf, page 24 §Support"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The guest companion eligibility configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the guest companion eligibility untouched.",
   "emptyFirstRun": "No guest companion eligibility configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listGuestCompanionEligibility",
    "contract": "access",
    "purpose": "Guest, Companion & Eligibility Rules",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-161"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 24. 0 of 0 labels bound to a contract property; 12 of 27 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-162",
  "name": "Group Admission & Quantity Validation",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Access Control Module_Reference.pdf",
   "board": "2",
   "number": "2.9",
   "page": 25
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/group-admission-quantity-validation-bo-162",
   "component": "apps/venue-management-web/src/routes/access-venue/GroupAdmissionQuantityValidation.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-154"
   ],
   "exitTo": [
    "BO-154"
   ],
   "inferred": false,
   "notes": "**Reached from BO-154, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-154",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F112 step 16→17",
     "operation": "listGroupAdmissionQuantity"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Handle B2B groups, school groups, tour groups and family/group tickets efficiently. The matrix specifically calls for faster admission for large B2B groups and the ability for one QR/group ticket to represent multiple admissions.",
  "purposeNote": "Large groups can be admitted quickly without scanning every guest individually when the configured product permits group admission.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Access Control Module_Reference.pdf, page 25"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Access Control Module_Reference.pdf, page 25"
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
       "impliedBy": "listGroupAdmissionQuantity",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The group admission quantity list.",
   "error": "Could not load. Names which read failed and leaves the group admission quantity untouched.",
   "emptyFirstRun": "No group admission quantity yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the group admission quantity are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listGroupAdmissionQuantity",
    "contract": "access",
    "purpose": "Group Admission & Quantity Validation",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "GroupAdmissionQuantityValidationView.authorizedQuantity50",
    "GroupAdmissionQuantityValidationView.authorizedGuests50",
    "GroupAdmissionQuantityValidationView.guestsEnteringNow42",
    "GroupAdmissionQuantityValidationView.entered42",
    "GroupAdmissionQuantityValidationView.remaining8"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-162"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 25. 0 of 0 labels bound to a contract property; 0 of 21 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-163",
  "name": "Rule Simulation, Conflict Check & Publication",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Access Control Module_Reference.pdf",
   "board": "2",
   "number": "2.10",
   "page": 26
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/rule-simulation-conflict-check-publication-bo-163",
   "component": "apps/venue-management-web/src/routes/access-venue/RuleSimulationConflictCheckPublication.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-154"
   ],
   "exitTo": [
    "BO-154"
   ],
   "inferred": false,
   "notes": "**Reached from BO-154, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation."
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "No access rule should reach a live gate without being tested.",
  "purposeNote": "Every access rule can be simulated, validated, approved, versioned, published and rolled back with a complete audit trail. Board 2 — Final Screen Structure # Backend Screen Core Responsibility 2.1 Access Rule Command Center Central access-rule management # Backend Screen Core Responsibility 2.2 Visual Access Rule Builder No-code admission logic 2.3 Entry, Exit & Re-entry Rules Admission quantities and lifecycle 2.4 Anti-Passback & Journey Sequence Sharing prevention and sequence control 2.5 Access Validity & Time Rules Dates, calendars, time and expiry 2.6 Entitlement Consumption Engine Consum",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Access Control Module_Reference.pdf, page 26"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Access Control Module_Reference.pdf, page 26"
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
       "label": "Rule V1.0",
       "provenance": "pack Access Control Module_Reference.pdf, page 26 §Support versioning"
      },
      {
       "kind": "secondaryButton",
       "label": "Rule V1.1",
       "provenance": "pack Access Control Module_Reference.pdf, page 26 §Support versioning"
      },
      {
       "kind": "secondaryButton",
       "label": "Rule V2.0",
       "provenance": "pack Access Control Module_Reference.pdf, page 26 §Support versioning"
      },
      {
       "kind": "publishGate",
       "label": "What publishing changes",
       "notes": "**Names what goes live, where, and from when.** A publish with no stated consequence is one somebody presses meaning to save.",
       "provenance": "authored — required by check-screens for publishRuleConflictCheck"
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
   "loading": "The rule simulation conflict list.",
   "error": "Could not load. Names which read failed and leaves the rule simulation conflict untouched.",
   "emptyFirstRun": "No rule simulation conflict yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the rule simulation conflict are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "publishRuleConflictCheck",
    "contract": "access",
    "purpose": "Rule Simulation, Conflict Check & Publication",
    "trigger": "onAction",
    "invalidates": [
     "publishRuleConflictCheck"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-163"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 26. 0 of 0 labels bound to a contract property; 3 of 59 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
 "listAccessRule": {
  "method": "GET",
  "path": "/access-rule",
  "contract": "access",
  "summary": "Access Rule Command Center",
  "permission": "SCOPE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "AccessRuleCommandCenterView"
 },
 "listAccessValidityTime": {
  "method": "GET",
  "path": "/access-validity-time",
  "contract": "access",
  "summary": "Access Validity & Time Rules",
  "permission": "SCOPE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "AccessValidityTimeRulesView"
 },
 "listAntiPassbackJourney": {
  "method": "GET",
  "path": "/anti-passback-journey",
  "contract": "access",
  "summary": "Anti-Passback & Journey Sequence",
  "permission": "SCOPE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "AntiPassbackJourneySequenceView"
 },
 "listEntitlementConsumption": {
  "method": "GET",
  "path": "/entitlement-consumption",
  "contract": "access",
  "summary": "Entitlement Consumption Engine",
  "permission": "SCOPE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "EntitlementConsumptionEngineView"
 },
 "listEntryExitRule": {
  "method": "GET",
  "path": "/entry-exit-rule",
  "contract": "access",
  "summary": "Entry, Exit & Re-entry Rules",
  "permission": "SCOPE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "EntryExitReEntryRulesView"
 },
 "listGroupAdmissionQuantity": {
  "method": "GET",
  "path": "/group-admission-quantity",
  "contract": "access",
  "summary": "Group Admission & Quantity Validation",
  "permission": "SCOPE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "GroupAdmissionQuantityValidationView"
 },
 "listGuestCompanionEligibility": {
  "method": "GET",
  "path": "/guest-companion-eligibility",
  "contract": "access",
  "summary": "Guest, Companion & Eligibility Rules",
  "permission": "SCOPE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "GuestCompanionEligibilityRulesView"
 },
 "listMultiParkCrossover": {
  "method": "GET",
  "path": "/multi-park-crossover",
  "contract": "access",
  "summary": "Multi-Park & Crossover Rules",
  "permission": "SCOPE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "MultiParkCrossoverRulesView"
 },
 "publishRuleConflictCheck": {
  "method": "PUT",
  "path": "/rule-conflict-check",
  "contract": "access",
  "summary": "Rule Simulation, Conflict Check & Publication",
  "permission": "ACCESS_POINT_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": "RuleSimulationConflictCheckPublicationInput",
  "responds": "RuleSimulationConflictCheckPublicationView"
 },
 "setVisualAccessRule": {
  "method": "PUT",
  "path": "/visual-access-rule",
  "contract": "access",
  "summary": "Visual Access Rule Builder",
  "permission": "ACCESS_POINT_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": "VisualAccessRuleBuilderInput",
  "responds": "VisualAccessRuleBuilderView"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "AccessRuleCommandCenterView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Access Rule Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "activeAccessRules": {
    "type": "integer",
    "description": "Active Access Rules"
   },
   "draftRules": {
    "type": "integer",
    "description": "Draft Rules"
   },
   "scheduledRules": {
    "type": "integer",
    "description": "Scheduled Rules"
   },
   "rulesPendingApproval": {
    "type": "string",
    "description": "Rules Pending Approval"
   },
   "venuesCovered": {
    "type": "string",
    "description": "Venues Covered"
   },
   "productsTicketsCovered": {
    "type": "string",
    "description": "Products/Tickets Covered"
   },
   "rulesWithConflicts": {
    "type": "integer",
    "description": "Rules with Conflicts"
   },
   "rulesUsingBiometrics": {
    "type": "integer",
    "description": "Rules Using Biometrics"
   },
   "rulesAllowingOverride": {
    "type": "string",
    "description": "Rules Allowing Override"
   },
   "offlineCompatibleRules": {
    "type": "integer",
    "description": "Offline-Compatible Rules"
   },
   "recentlyModifiedRules": {
    "type": "integer",
    "description": "Recently Modified Rules"
   },
   "upcomingRuleChanges": {
    "type": "integer",
    "description": "Upcoming Rule Changes"
   }
  }
 },
 "AccessValidityTimeRulesView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Access Validity & Time Rules displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "fromTo": {
    "type": "string",
    "description": "From / To"
   },
   "nDaysAfterSale": {
    "type": "string",
    "description": "N days after sale"
   },
   "nDaysAfterActivation": {
    "type": "string",
    "description": "N days after activation"
   },
   "nDaysAfterFirstUse": {
    "type": "string",
    "description": "N days after first use"
   },
   "endOfDay": {
    "type": "string",
    "description": "End of Day"
   },
   "endOfWeek": {
    "type": "string",
    "description": "End of Week"
   },
   "endOfMonth": {
    "type": "string",
    "description": "End of Month"
   },
   "endOfYear": {
    "type": "string",
    "description": "End of Year"
   },
   "weekdays": {
    "type": "string",
    "description": "weekdays"
   },
   "weekends": {
    "type": "string",
    "description": "weekends"
   },
   "peakDates": {
    "type": "string",
    "description": "peak dates"
   },
   "offPeakDates": {
    "type": "string",
    "description": "off-peak dates"
   },
   "holidays": {
    "type": "string",
    "description": "holidays"
   },
   "seasons": {
    "type": "string",
    "description": "seasons"
   },
   "eventDates": {
    "type": "string",
    "description": "event dates"
   },
   "blackoutDates": {
    "type": "string",
    "description": "blackout dates"
   },
   "toItsAdmissionPerformanceTime": {
    "type": "string",
    "format": "date-time",
    "description": "to its admission/performance time"
   }
  }
 },
 "AntiPassbackJourneySequenceView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Anti-Passback & Journey Sequence displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "credential": {
    "type": "string",
    "description": "Credential"
   },
   "guest": {
    "type": "string",
    "description": "Guest"
   },
   "gate": {
    "type": "string",
    "description": "Gate"
   },
   "attraction": {
    "type": "string",
    "description": "Attraction"
   },
   "park": {
    "type": "string",
    "description": "Park"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "entryExitReEntry": {
    "type": "string",
    "description": "ENTRY → EXIT → RE-ENTRY"
   },
   "mainEntryAttractionEntry": {
    "type": "string",
    "description": "MAIN ENTRY → ATTRACTION ENTRY"
   }
  }
 },
 "EntitlementConsumptionEngineView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Entitlement Consumption Engine displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "parkAdmission": {
    "type": "string",
    "description": "Park Admission"
   },
   "attractionAdmission": {
    "type": "string",
    "description": "Attraction Admission"
   },
   "ride": {
    "type": "string",
    "description": "Ride"
   },
   "fastPass": {
    "type": "string",
    "description": "Fast Pass"
   },
   "meal": {
    "type": "string",
    "description": "Meal"
   },
   "voucher": {
    "type": "string",
    "description": "Voucher"
   },
   "photo": {
    "type": "string",
    "description": "Photo"
   },
   "locker": {
    "type": "string",
    "description": "Locker"
   },
   "event": {
    "type": "string",
    "description": "Event"
   },
   "experience": {
    "type": "string",
    "description": "Experience"
   },
   "reEntry": {
    "type": "string",
    "description": "Re-entry"
   },
   "membershipBenefit": {
    "type": "string",
    "description": "Membership benefit"
   },
   "customEntitlement": {
    "type": "string",
    "description": "custom entitlement"
   },
   "quantity": {
    "type": "integer",
    "description": "Quantity (the pack shows 3)"
   },
   "consumptionPerValidation": {
    "type": "string",
    "description": "Consumption per validation (the pack shows 1)"
   },
   "exampleSilverFastPass": {
    "type": "string",
    "description": "Example — Silver Fast Pass"
   },
   "ride1Remaining2": {
    "type": "string",
    "description": "Ride 1 → Remaining 2"
   },
   "ride2Remaining1": {
    "type": "string",
    "description": "Ride 2 → Remaining 1"
   },
   "ride3Remaining0": {
    "type": "string",
    "description": "Ride 3 → Remaining 0"
   },
   "oneAccessPerRide": {
    "type": "string",
    "description": "one access per ride"
   }
  }
 },
 "EntryExitReEntryRulesView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Entry, Exit & Re-entry Rules displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "unlimited": {
    "type": "string",
    "description": "Unlimited"
   },
   "once": {
    "type": "string",
    "description": "Once"
   },
   "nTimes": {
    "type": "string",
    "description": "N times"
   },
   "nPerDay": {
    "type": "string",
    "description": "N per day"
   },
   "nPerPeriod": {
    "type": "string",
    "format": "date-time",
    "description": "N per period"
   },
   "exitScanRequired": {
    "type": "boolean",
    "description": "Exit scan required"
   },
   "exitScanOptional": {
    "type": "string",
    "description": "Exit scan optional"
   },
   "unlimitedExit": {
    "type": "string",
    "description": "Unlimited exit"
   },
   "nExits": {
    "type": "string",
    "description": "N exits"
   },
   "allowedNotAllowed": {
    "type": "boolean",
    "description": "Allowed / Not Allowed"
   },
   "maximumReEntries": {
    "type": "string",
    "description": "Maximum re-entries"
   },
   "sameDayOnly": {
    "type": "string",
    "description": "Same-day only"
   },
   "designatedGateRequired": {
    "type": "boolean",
    "description": "Designated gate required"
   },
   "exitRequiredFirst": {
    "type": "string",
    "description": "Exit required first"
   },
   "reEntryWindow": {
    "type": "string",
    "format": "date-time",
    "description": "Re-entry window"
   },
   "entry1": {
    "type": "string",
    "description": "Entry: 1"
   },
   "exitRequired": {
    "type": "boolean",
    "description": "Exit: Required"
   },
   "reEntry1": {
    "type": "string",
    "description": "Re-entry: 1"
   },
   "reEntryGateDesignatedGateOnly": {
    "type": "string",
    "description": "Re-entry Gate: Designated Gate Only"
   }
  }
 },
 "GroupAdmissionQuantityValidationView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Group Admission & Quantity Validation displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "authorizedQuantity50": {
    "type": "integer",
    "description": "Authorized Quantity: 50"
   },
   "authorizedGuests50": {
    "type": "string",
    "description": "Authorized Guests: 50"
   },
   "guestsEnteringNow42": {
    "type": "string",
    "description": "Guests Entering Now: 42"
   },
   "entered42": {
    "type": "string",
    "description": "Entered: 42"
   },
   "remaining8": {
    "type": "string",
    "description": "Remaining: 8"
   },
   "attendanceIncrement": {
    "type": "integer",
    "description": "Attendance increment (the pack shows +42)"
   },
   "entireGroup": {
    "type": "string",
    "description": "Entire Group"
   },
   "partialGroup": {
    "type": "string",
    "description": "Partial Group"
   },
   "multipleWaves": {
    "type": "string",
    "description": "Multiple Waves"
   },
   "leaderGuests": {
    "type": "string",
    "description": "Leader + Guests"
   },
   "singleQrMultiEntry": {
    "type": "string",
    "description": "Single QR Multi-Entry"
   },
   "individualChildTicketsUnderGroup": {
    "type": "string",
    "description": "Individual Child Tickets under Group"
   },
   "prevalidatedB2bManifest": {
    "type": "string",
    "description": "Prevalidated B2B Manifest"
   },
   "storedOnOneDevice": {
    "type": "string",
    "description": "stored on one device"
   }
  }
 },
 "GuestCompanionEligibilityRulesView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Guest, Companion & Eligibility Rules displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "adult": {
    "type": "string",
    "description": "Adult"
   },
   "child": {
    "type": "string",
    "description": "Child"
   },
   "junior": {
    "type": "string",
    "description": "Junior"
   },
   "senior": {
    "type": "string",
    "description": "Senior"
   },
   "pod": {
    "type": "string",
    "description": "POD"
   },
   "podCompanion": {
    "type": "string",
    "description": "POD Companion"
   },
   "nanny": {
    "type": "string",
    "description": "Nanny"
   },
   "vip": {
    "type": "string",
    "description": "VIP"
   },
   "member": {
    "type": "string",
    "description": "Member"
   },
   "staff": {
    "type": "string",
    "description": "Staff"
   },
   "accreditation": {
    "type": "string",
    "description": "Accreditation"
   },
   "customerSegment": {
    "type": "string",
    "description": "Customer Segment"
   },
   "beforeAdmission": {
    "type": "string",
    "description": "before admission"
   },
   "beforeExit": {
    "type": "string",
    "description": "before exit"
   },
   "journeys": {
    "type": "string",
    "description": "journeys"
   },
   "childA": {
    "type": "string",
    "description": "Child A"
   },
   "childB": {
    "type": "string",
    "description": "Child B"
   }
  }
 },
 "MultiParkCrossoverRulesView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Multi-Park & Crossover Rules displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "allowedParks": {
    "type": "string",
    "description": "allowed parks"
   },
   "parkOrder": {
    "type": "string",
    "description": "park order"
   },
   "sameDayCrossover": {
    "type": "string",
    "description": "same-day crossover"
   },
   "differentDayAccess": {
    "type": "string",
    "description": "different-day access"
   },
   "numberOfParkEntries": {
    "type": "integer",
    "description": "number of park entries"
   },
   "crossoverQuantity": {
    "type": "integer",
    "description": "crossover quantity"
   },
   "crossoverTime": {
    "type": "string",
    "format": "date-time",
    "description": "crossover time"
   },
   "prerequisitePark": {
    "type": "string",
    "description": "prerequisite park"
   },
   "reEntryAfterCrossover": {
    "type": "string",
    "description": "re-entry after crossover"
   }
  }
 },
 "RuleSimulationConflictCheckPublicationInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Rule Simulation, Conflict Check & Publication submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "adventureParkEnteredAt1400": {
    "type": "string",
    "description": "Adventure Park entered at 14:00"
   },
   "exitedAt1730": {
    "type": "string",
    "description": "Exited at 17:30"
   },
   "credentialValid": {
    "type": "string",
    "description": "✓ Credential Valid"
   },
   "visitDateValid": {
    "type": "string",
    "format": "date-time",
    "description": "✓ Visit Date Valid"
   },
   "waterParkEntitlement": {
    "type": "string",
    "description": "✓ Water Park Entitlement"
   },
   "crossoverAllowed": {
    "type": "boolean",
    "description": "✓ Crossover Allowed"
   },
   "previousParkRequirementMet": {
    "type": "string",
    "description": "✓ Previous Park Requirement Met"
   },
   "entryQuantityAvailable": {
    "type": "integer",
    "description": "✓ Entry Quantity Available"
   },
   "antiPassbackPassed": {
    "type": "string",
    "description": "✓ Anti-Passback Passed"
   },
   "verificationMethodValid": {
    "type": "string",
    "description": "✓ Verification Method Valid"
   },
   "denyRuleAc284": {
    "type": "string",
    "description": "DENY — RULE AC-284"
   },
   "ruleV10": {
    "type": "string",
    "description": "Rule V1.0"
   },
   "ruleV11": {
    "type": "string",
    "description": "Rule V1.1"
   },
   "ruleV20": {
    "type": "string",
    "description": "Rule V2.0"
   },
   "validatedOfflineAndInvalidated": {
    "type": "string",
    "description": "validated offline, and invalidated"
   },
   "entitlements": {
    "type": "string",
    "description": "entitlements"
   }
  }
 },
 "RuleSimulationConflictCheckPublicationView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Rule Simulation, Conflict Check & Publication displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "adventureParkEnteredAt1400": {
    "type": "string",
    "description": "Adventure Park entered at 14:00"
   },
   "exitedAt1730": {
    "type": "string",
    "description": "Exited at 17:30"
   },
   "credentialValid": {
    "type": "string",
    "description": "✓ Credential Valid"
   },
   "visitDateValid": {
    "type": "string",
    "format": "date-time",
    "description": "✓ Visit Date Valid"
   },
   "waterParkEntitlement": {
    "type": "string",
    "description": "✓ Water Park Entitlement"
   },
   "crossoverAllowed": {
    "type": "boolean",
    "description": "✓ Crossover Allowed"
   },
   "previousParkRequirementMet": {
    "type": "string",
    "description": "✓ Previous Park Requirement Met"
   },
   "entryQuantityAvailable": {
    "type": "integer",
    "description": "✓ Entry Quantity Available"
   },
   "antiPassbackPassed": {
    "type": "string",
    "description": "✓ Anti-Passback Passed"
   },
   "verificationMethodValid": {
    "type": "string",
    "description": "✓ Verification Method Valid"
   },
   "denyRuleAc284": {
    "type": "string",
    "description": "DENY — RULE AC-284"
   },
   "ruleV10": {
    "type": "string",
    "description": "Rule V1.0"
   },
   "ruleV11": {
    "type": "string",
    "description": "Rule V1.1"
   },
   "ruleV20": {
    "type": "string",
    "description": "Rule V2.0"
   },
   "validatedOfflineAndInvalidated": {
    "type": "string",
    "description": "validated offline, and invalidated"
   },
   "entitlements": {
    "type": "string",
    "description": "entitlements"
   }
  }
 },
 "VisualAccessRuleBuilderInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Visual Access Rule Builder submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "at": {
    "type": "string",
    "description": "AT"
   },
   "conditionsAreSatisfied": {
    "type": "string",
    "description": "conditions are satisfied"
   },
   "logic": {
    "type": "string",
    "description": "logic"
   },
   "ai": {
    "type": "string",
    "description": "AI"
   },
   "exited": {
    "type": "string",
    "description": "exited.\""
   }
  }
 },
 "VisualAccessRuleBuilderView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Visual Access Rule Builder displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "at": {
    "type": "string",
    "description": "AT"
   },
   "conditionsAreSatisfied": {
    "type": "string",
    "description": "conditions are satisfied"
   },
   "logic": {
    "type": "string",
    "description": "logic"
   },
   "ai": {
    "type": "string",
    "description": "AI"
   },
   "exited": {
    "type": "string",
    "description": "exited.\""
   }
  }
 }
}
```
