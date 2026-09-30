# P08-access-venue-03 — P08 · Access & Venue (3 of 3)

**5 screens · 14 operations · 23 schemas · 7 permissions**

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

- **Every control that can be refused must be gated.** 7 permissions apply here:
  `ORDER_CREATE, REPORT_VIEW_VENUE, RESOURCE_BOOK, RESOURCE_MANAGE, RESOURCE_VIEW, SCOPE_VIEW, TENANT_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-096` | Resource Calendar | statusTracker | 2 | 1 | — |
| `BO-097` | Check Out & Check In | configEditor | 5 | 3 | — |
| `BO-098` | Qualifications | configEditor | 1 | 0 | — |
| `BO-099` | Performance Manifest | statusTracker | 2 | 1 | — |
| `BO-103` | Access & Venue | listDetail | 4 | 0 | — |

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "BO-096",
  "name": "Resource Calendar",
  "module": "Access & Venue",
  "requiresModule": "resources",
  "wave": 2,
  "implementation": {
   "app": "venue-management-web",
   "route": "/resources/calendar",
   "component": "apps/venue-management-web/src/routes/resources/ResourceCalendar.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-095"
   ],
   "exitTo": [
    "BO-097",
    "BO-099"
   ],
   "transitions": [
    {
     "to": "BO-097",
     "trigger": "The guest arrives;",
     "provenance": "flow F25 step 3→4",
     "operation": "bookResource"
    },
    {
     "to": "BO-099",
     "trigger": "Performance Manifest",
     "provenance": "derived — BO-099 declares entryState.params performanceId and BO-096 holds none of them, so the edge carries nothing and BO-099 opens cold"
    }
   ]
  },
  "notes": "CF-125. **Conflict detection before assignment is the whole point** — two bookings on one cabana is a guest arriving to find somebody in their chair, and it must be impossible rather than unlikely.",
  "density": "compact",
  "pattern": "statusTracker",
  "patternReason": "`getResourceAvailability` reads one record and nothing reads a population — the screen is about that one thing",
  "purpose": "See what is free, and book it without double-booking.",
  "layout": {
   "template": "detail",
   "regions": [
    {
     "name": "contentBody",
     "slot": "record",
     "components": [
      {
       "kind": "calendarView",
       "label": "Calendar",
       "operation": "getResourceAvailability",
       "notes": "Each resource's bookings, blocks and cleanings placed by hour. Day, week, month and agenda views; the day starts at the venue's `calendarDayStartHour`. Filters the category on what it read.",
       "provenance": "decided 29 September 2026, 17 September minutes M17-03 (applied 30 September)"
      },
      {
       "kind": "detailPanel",
       "label": "The resource availability",
       "bindsTo": "ResourceAvailability",
       "columns": [
        "ResourceAvailability.resourceId",
        "ResourceAvailability.freeWindows",
        "ResourceAvailability.blockedWindows"
       ],
       "operation": "getResourceAvailability",
       "provenance": "contract resources.yaml GET /resources/{resourceId}/availability"
      },
      {
       "kind": "timeline",
       "bindsTo": "ResourceAvailability",
       "notes": "Setup and teardown render as their own bands, not as part of the booking — **a 30-minute turnaround is invisible if it is drawn inside the booking**",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "primaryButton",
       "label": "Book",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "banner",
       "notes": "Conflicts, named with times. *Not available* on something a guest can see is not an answer",
       "provenance": "carried from the previous definition"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Book resource",
       "operation": "bookResource",
       "provenance": "contract resources.yaml POST /resource-bookings"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "Calendar grid; today renders first",
   "error": "Could not load availability. **Do not book blind** — a booking made against a stale calendar is the double-booking this screen exists to prevent.",
   "emptyFirstRun": "Nothing booked in this window. **Free is the default state and it is worth showing plainly** — an empty calendar at a venue that takes bookings is either a quiet week or a resource nobody knows exists.",
   "emptyNoResults": "No availability in this window. The response says why — booked, setup, teardown, maintenance or closed — because **wait and look elsewhere are different answers**.",
   "emptyNoAccess": "You do not have RESOURCE_VIEW."
  },
  "apis": [
   {
    "operationId": "getResourceAvailability",
    "contract": "resources",
    "purpose": "Free windows",
    "trigger": "onLoad"
   },
   {
    "operationId": "bookResource",
    "contract": "resources",
    "purpose": "Reserve",
    "trigger": "onAction"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "resourceId",
     "from": "BO-095"
    }
   ],
   "coldEntry": "Resolves from the session; a cold arrival is the ordinary case."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-096"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 2 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formBookResource",
    "component": "modal",
    "trigger": "Book resource",
    "body": "**Collects what `bookResource` sends before it is called.** Required: `from`, `to`. Optional: `resourceId`, `resourceKind`, `subjectId`, `orderId`, `recurrence`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Book resource",
     "operation": "bookResource"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "from",
      "to",
      "resourceId",
      "resourceKind",
      "subjectId",
      "orderId",
      "recurrence"
     ]
    },
    "provenance": "contract resources.yaml POST /resource-bookings"
   }
  ],
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
  "id": "BO-097",
  "name": "Check Out & Check In",
  "module": "Access & Venue",
  "requiresModule": "resources",
  "wave": 2,
  "implementation": {
   "app": "venue-management-web",
   "route": "/resources/check-out",
   "component": "apps/venue-management-web/src/routes/resources/ResourceCheckOutForm.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-095",
    "BO-096"
   ],
   "exitTo": [
    "BO-095",
    "BO-096"
   ],
   "inferred": false,
   "notes": "**Returns to BO-095, BO-096.** Stated on 4 September: this screen declared where it is reached from and no way to leave, so whoever landed on it was stuck. The return path is the same edge travelled the other way, not a guess about the product.",
   "transitions": [
    {
     "to": "BO-096",
     "trigger": "Resource Calendar",
     "carries": [
      "resourceId"
     ],
     "provenance": "derived — BO-096 declares entryState.params resourceId and BO-097 holds resourceId, so an edge into it carries them"
    }
   ]
  },
  "notes": "CF-125, CF-126. **The deposit is held, not taken** — a deposit taken and refunded is two transactions and a fee. **Damage routes the resource to maintenance directly**, because routing through available leaves a window where the next guest books a broken item. **The deposit operations are declared here because this screen calls them** — F25 named them at steps 4 and 5 and the screen did not, which the flow checker refused. **A step calling an operation its screen does not declare is one of the two out of step**, and in this case it was the screen.",
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the screen declares only writes (`checkOutResource`, `checkInResource`, `authoriseStoredValue`) and no read of a population — it is settings, not a list",
  "purpose": "Hand it over with a deposit, take it back, settle.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "textField",
       "label": "amount",
       "bindsTo": "Money.amount",
       "provenance": "contract resources.yaml POST /resource-bookings/{bookingId}/check-out"
      },
      {
       "kind": "textField",
       "label": "currency",
       "bindsTo": "Money.currency",
       "provenance": "contract resources.yaml POST /resource-bookings/{bookingId}/check-out"
      },
      {
       "kind": "textField",
       "label": "scale",
       "bindsTo": "Money.scale",
       "provenance": "contract resources.yaml POST /resource-bookings/{bookingId}/check-out"
      },
      {
       "kind": "textField",
       "label": "Condition note",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "fileUpload",
       "label": "Condition photos",
       "notes": "Taken on the way out, not only on the way back",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "primaryButton",
       "label": "Check out",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "secondaryButton",
       "label": "Check in",
       "provenance": "carried from the previous definition"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Check out resource",
       "operation": "checkOutResource",
       "provenance": "contract resources.yaml POST /resource-bookings/{bookingId}/check-out"
      },
      {
       "kind": "secondaryButton",
       "label": "Check in resource",
       "operation": "checkInResource",
       "provenance": "contract resources.yaml POST /resource-bookings/{bookingId}/check-in"
      },
      {
       "kind": "secondaryButton",
       "label": "Authorise stored value",
       "operation": "authoriseStoredValue",
       "provenance": "contract orders.yaml POST /stored-value/authorisations"
      },
      {
       "kind": "secondaryButton",
       "label": "Release stored value",
       "operation": "relinquishStoredValue",
       "provenance": "contract orders.yaml POST /stored-value/authorisations/{authorisationId}/release"
      },
      {
       "kind": "secondaryButton",
       "label": "Capture stored value",
       "operation": "captureStoredValue",
       "provenance": "contract orders.yaml POST /stored-value/authorisations/{authorisationId}/capture"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The booking and its condition history",
   "error": "Could not load. **Check-out and check-in work offline** — the deposit hold reconciles on sync.",
   "emptyFirstRun": "Nothing is out. **The list a poolside attendant checks at close** — anything still here at the end of the day is a conversation.",
   "emptyNoAccess": "You do not have RESOURCE_BOOK.",
   "offline": "Queued locally. The deposit is authorised on sync, and **the condition note taken now is the only defence against a dispute later**."
  },
  "apis": [
   {
    "operationId": "checkOutResource",
    "contract": "resources",
    "purpose": "Hand over",
    "trigger": "onAction"
   },
   {
    "operationId": "checkInResource",
    "contract": "resources",
    "purpose": "Take back",
    "trigger": "onAction"
   },
   {
    "operationId": "authoriseStoredValue",
    "contract": "orders",
    "purpose": "Hold the deposit",
    "trigger": "onAction"
   },
   {
    "operationId": "relinquishStoredValue",
    "contract": "orders",
    "purpose": "Release it",
    "trigger": "onAction"
   },
   {
    "operationId": "captureStoredValue",
    "contract": "orders",
    "purpose": "Take some or all of the held balance",
    "trigger": "onAction",
    "provenance": "wiring gap, 19 September 2026 — the screen showed the noun and could not act on it",
    "invalidates": [
     "getStoredValueAuthorisation"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "authorisationId",
     "from": "deepLink"
    },
    {
     "name": "bookingId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know whether the record moved, closed or never existed, because those are three different next actions. **The scope is resolved from the session, never from the link**: a link cannot move somebody to a venue they do not hold. Arrives with `authorisationId`, `bookingId`."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-097"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 4 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formCaptureStoredValue",
    "component": "modal",
    "trigger": "Capture stored value",
    "body": "**Collects what `captureStoredValue` sends before it is called.** Required: `amount`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Capture stored value",
     "operation": "captureStoredValue"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "amount"
     ]
    },
    "provenance": "contract orders.yaml POST /stored-value/authorisations/{authorisationId}/capture"
   },
   {
    "id": "formCheckInResource",
    "component": "modal",
    "trigger": "Check in resource",
    "body": "**Collects what `checkInResource` sends before it is called.** Required: `condition`, `recordedAt`. Optional: `captureAmount`, `note`, `blockFurtherBookings`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Check in resource",
     "operation": "checkInResource"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "condition",
      "recordedAt",
      "captureAmount",
      "note",
      "blockFurtherBookings"
     ]
    },
    "provenance": "contract resources.yaml POST /resource-bookings/{bookingId}/check-in"
   },
   {
    "id": "formAuthoriseStoredValue",
    "component": "modal",
    "trigger": "Authorise stored value",
    "body": "**Collects what `authoriseStoredValue` sends before it is called.** Required: `kind`, `instrumentId`, `amount`. Optional: `reference`, `holdSeconds`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Authorise stored value",
     "operation": "authoriseStoredValue"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "kind",
      "instrumentId",
      "amount",
      "reference",
      "holdSeconds"
     ]
    },
    "provenance": "contract orders.yaml POST /stored-value/authorisations"
   }
  ],
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
  "id": "BO-098",
  "name": "Qualifications",
  "module": "Access & Venue",
  "requiresModule": "resources",
  "wave": 2,
  "implementation": {
   "app": "venue-management-web",
   "route": "/resources/qualifications",
   "component": "apps/venue-management-web/src/routes/resources/QualificationList.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-095"
   ],
   "exitTo": [
    "BO-095"
   ],
   "inferred": false,
   "notes": "**Returns to BO-095.** Stated on 4 September: this screen declared where it is reached from and no way to leave, so whoever landed on it was stuck. The return path is the same edge travelled the other way, not a guess about the product."
  },
  "notes": "CF-125. **Expiry is the field that makes this worth having** — a certification with no expiry is one nobody renews.",
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the screen declares only writes (`setResourceQualifications`) and no read of a population — it is settings, not a list",
  "purpose": "What a person is certified to do, and until when.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "textField",
       "label": "code",
       "bindsTo": "Qualification.code",
       "provenance": "contract resources.yaml PUT /resources/{resourceId}/qualifications"
      },
      {
       "kind": "textField",
       "label": "name",
       "bindsTo": "Qualification.name",
       "provenance": "contract resources.yaml PUT /resources/{resourceId}/qualifications"
      },
      {
       "kind": "textField",
       "label": "issuedAt",
       "bindsTo": "Qualification.issuedAt",
       "provenance": "contract resources.yaml PUT /resources/{resourceId}/qualifications"
      },
      {
       "kind": "textField",
       "label": "expiresAt",
       "bindsTo": "Qualification.expiresAt",
       "provenance": "contract resources.yaml PUT /resources/{resourceId}/qualifications"
      },
      {
       "kind": "textField",
       "label": "issuer",
       "bindsTo": "Qualification.issuer",
       "provenance": "contract resources.yaml PUT /resources/{resourceId}/qualifications"
      },
      {
       "kind": "textField",
       "label": "documentAssetId",
       "bindsTo": "Qualification.documentAssetId",
       "provenance": "contract resources.yaml PUT /resources/{resourceId}/qualifications"
      },
      {
       "kind": "textField",
       "label": "scopePath",
       "bindsTo": "Qualification.scopePath",
       "provenance": "contract resources.yaml PUT /resources/{resourceId}/qualifications"
      },
      {
       "kind": "dataTable",
       "bindsTo": "Qualification[]",
       "notes": "Sorted by expiry, not by name — **a lifeguard certificate that lapsed last month is a safety failure, not a data-quality one**",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "banner",
       "notes": "Expired qualifications held by staff on today rota",
       "provenance": "carried from the previous definition"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Save resource qualifications",
       "operation": "setResourceQualifications",
       "provenance": "contract resources.yaml PUT /resources/{resourceId}/qualifications"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "Qualifications with their expiry",
   "error": "Could not load.",
   "emptyFirstRun": "No qualifications recorded. **A role is not a skill** — 1.2.36 requires the check before assignment, not after.",
   "emptyNoAccess": "You do not have RESOURCE_MANAGE."
  },
  "apis": [
   {
    "operationId": "setResourceQualifications",
    "contract": "resources",
    "purpose": "Set qualifications",
    "trigger": "onAction"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "resourceId",
     "from": "BO-095"
    }
   ],
   "coldEntry": "Resolves from the session; a cold arrival is the ordinary case."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-098"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 1 operation this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
  "id": "BO-099",
  "name": "Performance Manifest",
  "module": "Access & Venue",
  "requiresModule": "resources",
  "wave": 2,
  "implementation": {
   "app": "venue-management-web",
   "route": "/resources/session-manifest",
   "component": "apps/venue-management-web/src/routes/resources/SessionManifest.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-096",
    "BO-015"
   ],
   "exitTo": [
    "BO-096",
    "BO-015"
   ],
   "inferred": false,
   "notes": "**Returns to BO-096.** Stated on 4 September: this screen declared where it is reached from and no way to leave, so whoever landed on it was stuck. The return path is the same edge travelled the other way, not a guess about the product.",
   "transitions": [
    {
     "to": "BO-096",
     "trigger": "Resource Calendar",
     "provenance": "derived — BO-096 declares entryState.params resourceId and BO-099 holds none of them, so the edge carries nothing and BO-096 opens cold"
    },
    {
     "to": "BO-015",
     "trigger": "Back to Performance Calendar",
     "carries": [
      "performanceId"
     ],
     "back": true,
     "provenance": "stated 28 September — the manifest is opened from a Performance (audit R165), so the return goes to the calendar holding that performance"
    }
   ]
  },
  "notes": "CF-125, CF-129. Distinct from duration, which variants already handle.",
  "density": "compact",
  "pattern": "statusTracker",
  "patternReason": "`getPerformanceManifest` reads one record and nothing reads a population — the screen is about that one thing",
  "purpose": "Who is in a performance, in what order. Opened from a Performance (renamed from session, decided 28 September, audit R165).",
  "layout": {
   "template": "detail",
   "regions": [
    {
     "name": "contentBody",
     "slot": "record",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The performance participant",
       "bindsTo": "PerformanceParticipant",
       "columns": [
        "PerformanceParticipant.id",
        "PerformanceParticipant.performanceId",
        "PerformanceParticipant.subjectId",
        "PerformanceParticipant.position",
        "PerformanceParticipant.experienceLevel",
        "PerformanceParticipant.packageName",
        "PerformanceParticipant.notes",
        "PerformanceParticipant.hasSignedWaiver"
       ],
       "operation": "getPerformanceManifest",
       "provenance": "contract resources.yaml GET /performances/{performanceId}/manifest"
      },
      {
       "kind": "dataTable",
       "bindsTo": "PerformanceParticipant[]",
       "notes": "Drag to reorder. **The running order is operational** — an instructor takes beginners first, and booking order puts one between two advanced riders",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "banner",
       "notes": "Unsigned waivers, named. **An instructor about to start does not want to discover one at the water edge**",
       "provenance": "carried from the previous definition"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Reorder performance manifest",
       "operation": "reorderPerformanceManifest",
       "provenance": "contract resources.yaml PUT /performances/{performanceId}/manifest"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "Participants in running order",
   "error": "Could not load the manifest.",
   "emptyFirstRun": "Nobody booked into this performance yet.",
   "emptyNoResults": "No participants match.",
   "emptyNoAccess": "You do not have RESOURCE_VIEW.",
   "offline": "The cached manifest. **An instructor at the water edge needs this more than anyone**, and that is where the signal is worst."
  },
  "apis": [
   {
    "operationId": "getPerformanceManifest",
    "contract": "resources",
    "purpose": "The manifest",
    "trigger": "onLoad"
   },
   {
    "operationId": "reorderPerformanceManifest",
    "contract": "resources",
    "purpose": "Change the order",
    "trigger": "onAction"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "performanceId",
     "from": "BO-015"
    }
   ],
   "coldEntry": "**Opened from a Performance** (decided 28 September, audit R165) — BO-015 Performance Calendar supplies `performanceId`, the path parameter of `getPerformanceManifest` and `reorderPerformanceManifest`. Without one the screen says which performance is missing and returns to the calendar."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-099"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 2 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formReorderPerformanceManifest",
    "component": "modal",
    "trigger": "Reorder performance manifest",
    "body": "**Collects what `reorderPerformanceManifest` sends before it is called.** Required: `order`, `recordedAt`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Reorder performance manifest",
     "operation": "reorderPerformanceManifest"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "order",
      "recordedAt"
     ]
    },
    "provenance": "contract resources.yaml PUT /performances/{performanceId}/manifest"
   }
  ],
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
  "id": "BO-103",
  "name": "Access & Venue",
  "module": "Access & Venue",
  "requiresModule": "core",
  "wave": 1,
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue",
   "component": "apps/venue-management-web/src/routes/home/AccessVenueList.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-100"
   ],
   "exitTo": [
    "BO-001",
    "BO-002",
    "BO-003",
    "BO-004",
    "BO-005",
    "BO-006",
    "BO-030",
    "BO-031",
    "BO-032",
    "BO-033",
    "BO-034",
    "BO-035",
    "BO-038",
    "BO-069",
    "BO-071",
    "BO-072",
    "BO-092",
    "BO-093",
    "BO-094",
    "BO-095",
    "BO-096",
    "BO-097",
    "BO-098",
    "BO-099"
   ],
   "transitions": [
    {
     "to": "BO-001",
     "trigger": "Queue Directory",
     "provenance": "derived — BO-001 declares entryState.params eventId, feedId, queueId and BO-103 holds none of them, so the edge carries nothing and BO-001 opens cold"
    },
    {
     "to": "BO-002",
     "trigger": "Queue Configuration",
     "provenance": "derived — BO-002 declares entryState.params performanceId, queueId and BO-103 holds none of them, so the edge carries nothing and BO-002 opens cold"
    },
    {
     "to": "BO-003",
     "trigger": "Queue Integration Setup",
     "provenance": "derived — BO-003 declares entryState.params feedId, orderId and BO-103 holds none of them, so the edge carries nothing and BO-003 opens cold"
    },
    {
     "to": "BO-004",
     "trigger": "Manual Wait Time Entry",
     "provenance": "derived — BO-004 declares entryState.params queueId, refundId and BO-103 holds none of them, so the edge carries nothing and BO-004 opens cold"
    },
    {
     "to": "BO-005",
     "trigger": "Queue Monitor",
     "provenance": "derived — BO-005 declares entryState.params campaignId, queueId and BO-103 holds none of them, so the edge carries nothing and BO-005 opens cold"
    },
    {
     "to": "BO-006",
     "trigger": "Parking Configuration",
     "carries": [
      "accessPointId"
     ],
     "provenance": "derived — BO-006 declares entryState.params accessPointId and BO-103 holds accessPointId, so an edge into it carries them"
    },
    {
     "to": "BO-030",
     "trigger": "Work Order Verification",
     "provenance": "derived — BO-030 declares entryState.params workOrderId and BO-103 holds none of them, so the edge carries nothing and BO-030 opens cold"
    },
    {
     "to": "BO-031",
     "trigger": "Asset Register",
     "provenance": "derived — BO-031 declares entryState.params assetId and BO-103 holds none of them, so the edge carries nothing and BO-031 opens cold"
    },
    {
     "to": "BO-032",
     "trigger": "Admission Profiles",
     "provenance": "derived — BO-032 declares entryState.params profileId, ruleId and BO-103 holds none of them, so the edge carries nothing and BO-032 opens cold"
    },
    {
     "to": "BO-033",
     "trigger": "Blacklist Management",
     "carries": [
      "mediaCode"
     ],
     "provenance": "derived — BO-033 declares entryState.params mediaCode and BO-103 holds mediaCode, so an edge into it carries them"
    },
    {
     "to": "BO-038",
     "trigger": "Reconciliation Queue",
     "provenance": "derived — BO-038 declares entryState.params queueId and BO-103 holds none of them, so the edge carries nothing and BO-038 opens cold"
    },
    {
     "to": "BO-069",
     "trigger": "Asset Register",
     "provenance": "derived — BO-069 declares entryState.params assetId, gameId and BO-103 holds none of them, so the edge carries nothing and BO-069 opens cold"
    },
    {
     "to": "BO-071",
     "trigger": "Planned Maintenance",
     "provenance": "derived — BO-071 declares entryState.params roleId and BO-103 holds none of them, so the edge carries nothing and BO-071 opens cold"
    },
    {
     "to": "BO-072",
     "trigger": "Incident Log",
     "provenance": "derived — BO-072 declares entryState.params incidentId and BO-103 holds none of them, so the edge carries nothing and BO-072 opens cold"
    },
    {
     "to": "BO-093",
     "trigger": "Map Import & Labelling",
     "provenance": "derived — BO-093 declares entryState.params jobId, mapId and BO-103 holds none of them, so the edge carries nothing and BO-093 opens cold"
    },
    {
     "to": "BO-094",
     "trigger": "Map Editor & Publish",
     "provenance": "derived — BO-094 declares entryState.params mapId, pathId and BO-103 holds none of them, so the edge carries nothing and BO-094 opens cold"
    },
    {
     "to": "BO-096",
     "trigger": "Resource Calendar",
     "provenance": "derived — BO-096 declares entryState.params resourceId and BO-103 holds none of them, so the edge carries nothing and BO-096 opens cold"
    },
    {
     "to": "BO-097",
     "trigger": "Check Out & Check In",
     "provenance": "derived — BO-097 declares entryState.params authorisationId, bookingId and BO-103 holds none of them, so the edge carries nothing and BO-097 opens cold"
    },
    {
     "to": "BO-098",
     "trigger": "Qualifications",
     "provenance": "derived — BO-098 declares entryState.params resourceId and BO-103 holds none of them, so the edge carries nothing and BO-098 opens cold"
    },
    {
     "to": "BO-099",
     "trigger": "Performance Manifest",
     "provenance": "derived — BO-099 declares entryState.params performanceId and BO-103 holds none of them, so the edge carries nothing and BO-099 opens cold"
    }
   ]
  },
  "notes": "Section landing. **24 screens reach the entry point through here** — before 20 August they reached it through nothing. **Given its section's own operations on 4 September.** It sat on `getVenueSettings` alone, which made it identical to every other section landing page — a hub that shows nothing of its section is a menu item, not a screen.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listAccessPoints` reads the population and `getVenueSettings` reads one of them — list, select, act",
  "purpose": "Everything in access & venue.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "textField",
       "label": "Venue id",
       "operation": "listAccessPoints",
       "notes": "Sends `?venueId=` to `listAccessPoints`.",
       "provenance": "contract access.yaml GET /access-points"
      },
      {
       "kind": "dataTable",
       "label": "Every access point",
       "bindsTo": "AccessPoint",
       "columns": [
        "AccessPoint.id",
        "AccessPoint.code",
        "AccessPoint.name",
        "AccessPoint.venueId",
        "AccessPoint.scopePath",
        "AccessPoint.externalCredentialSources",
        "AccessPoint.scanAnomalyRules",
        "AccessPoint.operatingMode",
        "AccessPoint.vehicleLocationCapture",
        "AccessPoint.mode",
        "AccessPoint.direction",
        "AccessPoint.antiPassbackEnabled"
       ],
       "operation": "listAccessPoints",
       "provenance": "contract access.yaml GET /access-points"
      },
      {
       "kind": "dataTable",
       "label": "Every scan event",
       "bindsTo": "ScanEvent",
       "columns": [
        "ScanEvent.id",
        "ScanEvent.accessPointId",
        "ScanEvent.venueId",
        "ScanEvent.scopePath",
        "ScanEvent.ticketId",
        "ScanEvent.mediaCode",
        "ScanEvent.outcome",
        "ScanEvent.denyReason",
        "ScanEvent.direction",
        "ScanEvent.operatorPrincipalId",
        "ScanEvent.deviceId",
        "ScanEvent.overridesScanId"
       ],
       "operation": "listScans",
       "provenance": "contract access.yaml GET /access/scans"
      },
      {
       "kind": "metricTile",
       "label": "Takings and admissions today",
       "bindsTo": "KpiValue",
       "columns": [
        "KpiValue.code",
        "KpiValue.name",
        "KpiValue.value",
        "KpiValue.period",
        "KpiValue.comparison",
        "KpiValue.direction"
       ],
       "operation": "getKpiValues",
       "notes": "**Takings and admissions**, from `getKpiValues?kpiCodes=takings,admissions`; with no `period` the period is today in the venue's time zone (decided 28 September, audit R283).",
       "provenance": "contract reporting.yaml GET /kpi-values"
      },
      {
       "kind": "cardList",
       "bindsTo": "screens",
       "notes": "24 screens. **No attention counts** until a summary operation exists to supply them (decided 28 September, audit R283).",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "searchField",
       "label": "Search access & venue",
       "provenance": "carried from the previous definition"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected access point",
       "bindsTo": "AccessPoint",
       "columns": [
        "AccessPoint.id",
        "AccessPoint.code",
        "AccessPoint.name",
        "AccessPoint.venueId",
        "AccessPoint.scopePath",
        "AccessPoint.externalCredentialSources",
        "AccessPoint.scanAnomalyRules",
        "AccessPoint.operatingMode",
        "AccessPoint.vehicleLocationCapture",
        "AccessPoint.mode",
        "AccessPoint.direction",
        "AccessPoint.antiPassbackEnabled",
        "AccessPoint.requiresExitBeforeReentry",
        "AccessPoint.driver",
        "AccessPoint.geofence",
        "AccessPoint.isActive"
       ],
       "operation": "listAccessPoints",
       "provenance": "contract access.yaml GET /access-points"
      },
      {
       "kind": "detailPanel",
       "label": "The venue settings",
       "bindsTo": "VenueSettings",
       "columns": [
        "VenueSettings.id",
        "VenueSettings.venueId",
        "VenueSettings.currencyCode",
        "VenueSettings.currencyScale",
        "VenueSettings.supportHours",
        "VenueSettings.quietHours",
        "VenueSettings.biometrics",
        "VenueSettings.segregatedAccess",
        "VenueSettings.alerting"
       ],
       "operation": "getVenueSettings",
       "provenance": "contract tenancy.yaml GET /venues/{venueId}/settings"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The list, with counts.",
   "error": "Could not load. Venue Home is still reachable.",
   "emptyFirstRun": "**Nothing configured in access & venue yet.** The action is the first thing to set up, not a blank list.",
   "emptyNoResults": "Nothing matches the filter.",
   "emptyNoAccess": "You do not have permission for access & venue. **Said plainly** — an empty section reads as broken."
  },
  "apis": [
   {
    "operationId": "getKpiValues",
    "contract": "reporting",
    "purpose": "Today's takings and admissions tiles — `kpiCodes=takings,admissions`, period defaulting to today (decided 28 September, audit R283)",
    "trigger": "onLoad"
   },
   {
    "operationId": "getVenueSettings",
    "contract": "tenancy",
    "purpose": "What is enabled here",
    "trigger": "onLoad"
   },
   {
    "operationId": "listAccessPoints",
    "contract": "access",
    "purpose": "Gates and lanes in this venue",
    "trigger": "onLoad"
   },
   {
    "operationId": "listScans",
    "contract": "access",
    "purpose": "Admissions as they happen",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "venueId",
     "from": "session"
    }
   ],
   "coldEntry": "**Resolves from the session, so a cold arrival is the ordinary case** — a manager bookmarks the back office and opens it every morning. A principal with more than one venue is asked which before the page renders, rather than shown the first one.",
   "preloaded": [
    "VenueSettings.id",
    "VenueSettings.venueId",
    "VenueSettings.supportHours",
    "VenueSettings.quietHours",
    "VenueSettings.segregatedAccess"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-103"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 3 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
 "authoriseStoredValue": {
  "method": "POST",
  "path": "/stored-value/authorisations",
  "contract": "orders",
  "summary": "Hold a balance on any stored-value instrument",
  "permission": "ORDER_CREATE",
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
  "responds": "StoredValueAuthorisation"
 },
 "bookResource": {
  "method": "POST",
  "path": "/resource-bookings",
  "contract": "resources",
  "summary": "Reserve a specific resource for a window — staff only",
  "permission": "RESOURCE_BOOK",
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
  "responds": "ResourceBooking"
 },
 "captureStoredValue": {
  "method": "POST",
  "path": "/stored-value/authorisations/{authorisationId}/capture",
  "contract": "orders",
  "summary": "Take some or all of a held balance",
  "permission": "ORDER_CREATE",
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
  "responds": "StoredValueAuthorisation"
 },
 "checkInResource": {
  "method": "POST",
  "path": "/resource-bookings/{bookingId}/check-in",
  "contract": "resources",
  "summary": "Take it back, and settle the deposit",
  "permission": "RESOURCE_BOOK",
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
  "responds": "ResourceBooking"
 },
 "checkOutResource": {
  "method": "POST",
  "path": "/resource-bookings/{bookingId}/check-out",
  "contract": "resources",
  "summary": "Hand it over, with a deposit against it",
  "permission": "RESOURCE_BOOK",
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
  "responds": "ResourceBooking"
 },
 "getKpiValues": {
  "method": "GET",
  "path": "/kpi-values",
  "contract": "reporting",
  "summary": "Current values, against target, with movement",
  "permission": "REPORT_VIEW_VENUE",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "kpiIds",
    "in": "query",
    "required": null
   },
   {
    "name": "kpiCodes",
    "in": "query",
    "required": null
   },
   {
    "name": "scopePath",
    "in": "query",
    "required": null
   },
   {
    "name": "period",
    "in": "query",
    "required": null
   },
   {
    "name": "compareTo",
    "in": "query",
    "required": null
   },
   {
    "name": "interval",
    "in": "query",
    "required": null
   },
   {
    "name": "groupBy",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "KpiValue"
 },
 "getPerformanceManifest": {
  "method": "GET",
  "path": "/performances/{performanceId}/manifest",
  "contract": "resources",
  "summary": "Who is in a performance, in what order",
  "permission": "RESOURCE_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "PerformanceParticipant"
 },
 "getResourceAvailability": {
  "method": "GET",
  "path": "/resources/{resourceId}/availability",
  "contract": "resources",
  "summary": "When it is free, with conflicts already resolved",
  "permission": "RESOURCE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "from",
    "in": "query",
    "required": true
   },
   {
    "name": "to",
    "in": "query",
    "required": true
   }
  ],
  "requestBody": null,
  "responds": "ResourceAvailability"
 },
 "getVenueSettings": {
  "method": "GET",
  "path": "/venues/{venueId}/settings",
  "contract": "tenancy",
  "summary": "Operational settings for this venue",
  "permission": "TENANT_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "VenueSettings"
 },
 "listAccessPoints": {
  "method": "GET",
  "path": "/access-points",
  "contract": "access",
  "summary": "List access points",
  "permission": "SCOPE_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "venueId",
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
 "listScans": {
  "method": "GET",
  "path": "/access/scans",
  "contract": "access",
  "summary": "List scan events",
  "permission": "REPORT_VIEW_VENUE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "accessPointId",
    "in": "query",
    "required": null
   },
   {
    "name": "ticketId",
    "in": "query",
    "required": null
   },
   {
    "name": "outcome",
    "in": "query",
    "required": null
   },
   {
    "name": "recordedFrom",
    "in": "query",
    "required": null
   },
   {
    "name": "recordedTo",
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
 "relinquishStoredValue": {
  "method": "POST",
  "path": "/stored-value/authorisations/{authorisationId}/release",
  "contract": "orders",
  "summary": "Give a hold back",
  "permission": "ORDER_CREATE",
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
  "responds": "StoredValueAuthorisation"
 },
 "reorderPerformanceManifest": {
  "method": "PUT",
  "path": "/performances/{performanceId}/manifest",
  "contract": "resources",
  "summary": "Change the running order",
  "permission": "RESOURCE_BOOK",
  "offlineCapable": true,
  "conflictPolicy": "lastWriterWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "PerformanceParticipant"
 },
 "setResourceQualifications": {
  "method": "PUT",
  "path": "/resources/{resourceId}/qualifications",
  "contract": "resources",
  "summary": "What a person resource is certified to do, and until when",
  "permission": "RESOURCE_MANAGE",
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
  "responds": "Qualification"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "AccessPoint": {
  "x-ticvai-persistence": "access.access_point",
  "type": "object",
  "required": [
   "id",
   "code",
   "name",
   "venueId",
   "operatingMode",
   "isActive"
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
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "scopePath": {
    "type": "string"
   },
   "externalCredentialSources": {
    "allOf": [
     {
      "$ref": "#/components/schemas/ExternalCredentialSourceList"
     }
    ],
    "description": "BL-108. **A hotel room card admitting a guest to a water park** — externally issued, and the platform validates it without having sold it.\n**The entitlement is created on first use, not on check-in.** A hotel with 400 rooms does not want 400 entitlements a night for guests who never visit.\n"
   },
   "scanAnomalyRules": {
    "allOf": [
     {
      "$ref": "#/components/schemas/ScanAnomalyRuleList"
     }
    ],
    "description": "BL-104. **Rule-based scan anomalies, separated from the parked model-based engine** — device sharing, simultaneous entries at two gates, an impossible walking time between them.\n**These are deterministic and need no model**, which is why they are here and not in `ai`: two entries eight seconds apart at gates four hundred metres apart is arithmetic.\n"
   },
   "operatingMode": {
    "allOf": [
     {
      "$ref": "#/components/schemas/AccessPointOperatingMode"
     }
    ],
    "default": "normal",
    "description": "**Set by the podium with `setTurnstileMode`, and it wins** (audit R221). BL-107 and BL-109. **A closed turnstile and one in emergency drop-arm mode look the same in the model and are opposite in meaning.** Closed refuses everybody; drop-arm lets everybody through, and it is the state that exists for an evacuation.\n**`podium` is a supervised validation position** — a member of staff directing a group through a lane, validating by eye against a list. It scans nothing and it is how school parties actually enter.\n**`freeFlow` counts without validating.** Useful at a free event, and a mode that must be visibly distinct from a broken reader.\n"
   },
   "vehicleLocationCapture": {
    "type": "boolean",
    "default": false,
    "description": "BL-023. **Nothing helped a guest find their vehicle.** Where the access point is a car park entry, the level and zone are captured against the visit so the app can answer it — **the guest who cannot find their car at 11pm is the last impression of the day.**\n"
   },
   "mode": {
    "allOf": [
     {
      "$ref": "#/components/schemas/TurnstileMode"
     }
    ],
    "nullable": true,
    "description": "Narrows `operatingMode` only: `freeRotation` or `closed` within `normal` or `podium`, null otherwise and whenever the turnstile validates in its fixed `direction` (audit R221).\n"
   },
   "direction": {
    "allOf": [
     {
      "$ref": "#/components/schemas/Direction"
     }
    ],
    "description": "**Fixed per access point** (audit R221): set in the back office by `createAccessPoint` and `updateAccessPoint`, never by the podium.\n"
   },
   "antiPassbackEnabled": {
    "type": "boolean"
   },
   "requiresExitBeforeReentry": {
    "type": "boolean",
    "default": false,
    "description": "Written by `createAccessPoint` and `updateAccessPoint`, and returned so the edit form reads back what it wrote."
   },
   "driver": {
    "type": "string",
    "nullable": true,
    "description": "Driver identifier for the controller behind this access point, as written by `createAccessPoint` and `updateAccessPoint`. Where the reader speaks OSDP the driver is standards-based; the controller layer above it is vendor-specific.\n"
   },
   "geofence": {
    "allOf": [
     {
      "$ref": "#/components/schemas/AccessPointGeofence"
     }
    ],
    "nullable": true,
    "description": "Written by `setAccessPointGeofence`; null until one is set. **One `jsonb` column on the access point row** (`access.access_point.geofence`), read with the point when a handheld validates against it.\n"
   },
   "isActive": {
    "type": "boolean"
   },
   "lastHeartbeatAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   }
  }
 },
 "AccessPointGeofence": {
  "type": "object",
  "x-ticvai-persistence-kind": "valueObject",
  "x-ticvai-persistence-column": "jsonb",
  "description": "Where a handheld may validate for one access point, and what happens outside it. The body of `setAccessPointGeofence` and the value of `AccessPoint.geofence`.\n",
  "required": [
   "enforcement"
  ],
  "properties": {
   "latitude": {
    "type": "number"
   },
   "longitude": {
    "type": "number"
   },
   "radiusMetres": {
    "type": "integer",
    "minimum": 5,
    "maximum": 5000
   },
   "enforcement": {
    "type": "string",
    "enum": [
     "off",
     "warn",
     "deny"
    ],
    "description": "`off` keeps the fence on record and checks nothing; `warn` lets a validation from outside the fence through with a warning; `deny` refuses it.\n"
   },
   "allowProximityBeacon": {
    "type": "boolean",
    "description": "Accept a BLE proximity assertion in place of GPS. Better indoors."
   }
  }
 },
 "AccessPointOperatingMode": {
  "type": "string",
  "description": "BL-107 and BL-109. **What the gate does, and what the podium sets** (`setTurnstileMode`, decided 28 September, audit R221). `closed` refuses everybody; `dropArm` lets everybody through and exists for an evacuation; `podium` is supervised validation by eye; `freeFlow` counts without validating; `maintenance` takes the lane out of use.\n",
  "enum": [
   "normal",
   "freeFlow",
   "dropArm",
   "closed",
   "podium",
   "maintenance"
  ]
 },
 "DenyReason": {
  "type": "string",
  "description": "Enumerated so the client can render an appropriate operator prompt. A gate operator facing a queue needs a reason and a next action, not a boolean.\n",
  "enum": [
   "notFound",
   "notYetValid",
   "expired",
   "alreadyUsed",
   "reentryLimitReached",
   "exitRequiredBeforeReentry",
   "wrongAccessPoint",
   "wrongPerformance",
   "outsideAdmissionWindow",
   "entitlementSuspended",
   "blacklisted",
   "capacityReached",
   "waiverRequired",
   "accompanimentRequired",
   "mediaDeactivated",
   "unpaid",
   "delegatedRightExhausted",
   "delegatedRightRevoked",
   "journeyNotCovered"
  ]
 },
 "Direction": {
  "type": "string",
  "enum": [
   "entry",
   "exit",
   "reentry",
   "crossover"
  ]
 },
 "ExternalCredentialSourceList": {
  "type": "array",
  "x-ticvai-persistence-kind": "valueObject",
  "x-ticvai-persistence-column": "jsonb",
  "description": "**One `jsonb` column on the access point row** (`access.access_point.external_credential_sources`). Read with the access point when a credential is presented; a source is never queried on its own.\n",
  "items": {
   "type": "object",
   "properties": {
    "kind": {
     "type": "string",
     "enum": [
      "hotelRoomCard",
      "corporateBadge",
      "cityPass",
      "transitCard",
      "partnerToken"
     ]
    },
    "providerName": {
     "type": "string"
    },
    "endpoint": {
     "type": "string"
    },
    "credentialRef": {
     "type": "string"
    },
    "grantsProductId": {
     "type": "string",
     "format": "uuid"
    }
   }
  }
 },
 "KpiValue": {
  "type": "object",
  "description": "BI board 10.3. **Value, target, variance, direction and freshness in one read.**",
  "properties": {
   "kpiId": {
    "type": "string",
    "format": "uuid"
   },
   "code": {
    "type": "string"
   },
   "bucketStart": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "The start of the bucket this value covers, when `getKpiValues` was asked for an `interval`; null otherwise."
   },
   "groupKey": {
    "type": "string",
    "nullable": true,
    "description": "The value of the `groupBy` dimension this row is for (a status, a category code, a tier); null when no `groupBy` was asked."
   },
   "name": {
    "type": "string"
   },
   "scopePath": {
    "type": "string"
   },
   "period": {
    "type": "string"
   },
   "value": {
    "$ref": "#/components/schemas/MetricValue"
   },
   "target": {
    "allOf": [
     {
      "$ref": "#/components/schemas/MetricValue"
     }
    ],
    "nullable": true
   },
   "comparison": {
    "allOf": [
     {
      "$ref": "#/components/schemas/MetricValue"
     }
    ],
    "nullable": true
   },
   "variancePercent": {
    "type": "number",
    "nullable": true
   },
   "direction": {
    "type": "string",
    "enum": [
     "up",
     "down",
     "flat"
    ]
   },
   "status": {
    "type": "string",
    "enum": [
     "green",
     "amber",
     "red",
     "noTarget"
    ]
   },
   "asOf": {
    "type": "string",
    "format": "date-time"
   },
   "stale": {
    "type": "boolean",
    "description": "**True when the pipeline behind it has not refreshed.** A number nobody flagged as stale is a number somebody will act on.\n"
   }
  }
 },
 "MetricValue": {
  "x-ticvai-persistence-column": "numeric(18,4)",
  "description": "**A reading of a metric or KPI, or a threshold on one.** A `Money` where the metric is money-valued — `MetricSource` lists those in `x-ticvai-money-valued`, and a KPI is when its `unit` is `currency` — and a plain number otherwise. naming-and-style 5.1: money is never a float, at any layer.\nStored as `numeric(18,4)` either way: a money value stores its amount, and currency and scale resolve from the scope as they do for every `Money`.\n",
  "oneOf": [
   {
    "type": "number"
   },
   {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   }
  ]
 },
 "Money": {
  "type": "object",
  "x-ticvai-persistence-kind": "valueObject",
  "x-ticvai-persistence-column": "numeric(18,4)",
  "description": "**On the wire this is three fields; in the database it is one column.**\n24 August. Every column typed `Money` was landing as `jsonb` — 129 of them, including `orders.shift.opening_float`, `inventory.purchase_order.total` and `promotions.voucher.balance`. **`orders.cash_movement.amount` was `numeric(18,4)` because somebody hand-typed that one**, and the inconsistency is what made it visible.\n**A jsonb price cannot be summed in SQL.** Every total, variance and reconciliation moves into application code — and a shift variance computed in .NET against a ledger computed in Postgres is two answers to one question. That is F13 month-end and F98 takings-to-ledger, both walked, both assuming the arithmetic is in the database.\n**`currency` and `scale` are not stored per row.** ADR-0018 makes them region-scoped and not overridable below, so they resolve from the scope walk — storing AED against nine million rows in a UAE region is nine million copies of a fact that cannot differ. A row that needed its own currency would be a row in the wrong region.\n**They stay on the wire** because a client reading a figure should not have to walk a hierarchy to know what it means.\n",
  "required": [
   "amount",
   "currency",
   "scale"
  ],
  "properties": {
   "amount": {
    "type": "string",
    "description": "Decimal string, never a float. Up to 4 decimal places. **Persisted as `numeric(18,4)`** — the string is a transport choice, so a JavaScript client cannot round a fare in transit.\n",
    "pattern": "^-?\\d+(\\.\\d{1,4})?$"
   },
   "currency": {
    "type": "string",
    "description": "**Resolved from the region, not stored on the row** (ADR-0018). OMR uses 3 decimal places and AED uses 2 — a venue on a different scale from its region is a ledger that cannot consolidate.\n",
    "pattern": "^[A-Z]{3}$"
   },
   "scale": {
    "type": "integer",
    "description": "Resolved from the region alongside `currency`.",
    "minimum": 0,
    "maximum": 4
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
 "PerformanceParticipant": {
  "type": "object",
  "x-ticvai-persistence": "resources.performance_participant",
  "description": "1.3.44. **The running order is operational.** An instructor takes beginners first, and a manifest sorted by booking time puts one between two advanced riders.\nFormerly `SessionParticipant` on `resources.session_participant`: a session is a Performance and the manifest hangs off one (decided 28 September, audit R165).\n",
  "required": [
   "id",
   "performanceId",
   "subjectId",
   "position"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "performanceId": {
    "type": "string",
    "format": "uuid",
    "description": "The `catalogue.performance` this participant is on (audit R165)."
   },
   "subjectId": {
    "type": "string",
    "format": "uuid"
   },
   "position": {
    "type": "integer"
   },
   "experienceLevel": {
    "type": "string",
    "enum": [
     "firstTime",
     "beginner",
     "intermediate",
     "advanced"
    ],
    "nullable": true
   },
   "packageName": {
    "type": "string",
    "nullable": true
   },
   "notes": {
    "type": "string",
    "nullable": true
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true,
    "description": "When the device made the running-order change that set `position` — the `recordedAt` of the last `reorderPerformanceManifest`. Null until the order is first changed.\n"
   },
   "syncedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true,
    "description": "When that change reached the server (naming-and-style 5.2)."
   },
   "hasSignedWaiver": {
    "type": "boolean",
    "readOnly": true,
    "description": "2.15.9. **Shown on the manifest because that is where it is acted on** — an instructor about to start does not want to discover an unsigned waiver at the water's edge.\n"
   }
  }
 },
 "Qualification": {
  "type": "object",
  "x-ticvai-persistence": "resources.qualification",
  "description": "1.2.36. **A role is not a skill**, and the check happens before assignment rather than after.\n",
  "required": [
   "code",
   "name"
  ],
  "properties": {
   "resourceId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "**The resource that holds this qualification.** Set from the path of `setResourceQualifications`; without it a stored qualification belongs to nobody and the check before assignment has nothing to check against. One row per resource and `code`.\n"
   },
   "code": {
    "type": "string"
   },
   "name": {
    "type": "string"
   },
   "issuedAt": {
    "type": "string",
    "format": "date",
    "nullable": true
   },
   "expiresAt": {
    "type": "string",
    "format": "date",
    "nullable": true,
    "description": "**The field that makes this worth having.** A certification with no expiry is one nobody renews, and a lifeguard certificate that lapsed last month is a safety failure rather than a data-quality one.\n"
   },
   "issuer": {
    "type": "string",
    "nullable": true
   },
   "documentAssetId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "scopePath": {
    "type": "string",
    "description": "**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**"
   }
  }
 },
 "ResourceAvailability": {
  "type": "object",
  "description": "**Free windows, with setup and teardown already subtracted.** A client computing this from bookings will forget the turnaround.\n",
  "properties": {
   "resourceId": {
    "type": "string",
    "format": "uuid"
   },
   "freeWindows": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "from": {
       "type": "string",
       "format": "date-time"
      },
      "to": {
       "type": "string",
       "format": "date-time"
      }
     }
    }
   },
   "blockedWindows": {
    "type": "array",
    "description": "**With a reason, because they are not the same.** Booked and under repair need different responses from an operator looking for something free — wait, or look elsewhere.\n",
    "items": {
     "type": "object",
     "properties": {
      "from": {
       "type": "string",
       "format": "date-time"
      },
      "to": {
       "type": "string",
       "format": "date-time"
      },
      "reason": {
       "type": "string",
       "enum": [
        "booked",
        "held",
        "setup",
        "teardown",
        "maintenance",
        "blackout",
        "closed",
        "cleaning"
       ],
       "description": "`held` is a live `ResourceHold` (rev 3 REV3-15): taken now, free again if it expires. `cleaning` is a cleaning the resource's `cleaningPolicy` places (W10, 29 September).\n"
      }
     }
    }
   }
  }
 },
 "ResourceBooking": {
  "type": "object",
  "x-ticvai-persistence": "resources.booking",
  "required": [
   "id",
   "resourceId",
   "from",
   "to",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "resourceId": {
    "type": "string",
    "format": "uuid"
   },
   "subjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "orderId": {
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
   "status": {
    "$ref": "#/components/schemas/ResourceBookingStatus"
   },
   "holdId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The `ResourceHold` this booking was converted from, where a guest picked the resource on a venue map (rev 3 REV3-15). Null for a staff booking or an allocation.\n"
   },
   "recurrenceGroupId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Ties the occurrences of a recurring booking. **Cancelling one week does not cancel the series**, and cancelling the series is a separate act with a separate confirmation.\n"
   },
   "depositAuthorisationId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The hold, through `orders.authoriseStoredValue` (CF-126). **A deposit taken and refunded is two transactions and a fee; held and released is neither.**\n"
   },
   "checkedOutAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "dueBackAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "returnedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "conditionOut": {
    "type": "string",
    "nullable": true
   },
   "conditionIn": {
    "type": "string",
    "nullable": true
   },
   "syncedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true,
    "description": "When the latest offline check-out or check-in write reached the server. **The device times are `checkedOutAt` and `returnedAt`**, taken from each write's `recordedAt`; this is the server's half of the pair naming-and-style 5.2 requires. Null while pending.\n"
   }
  }
 },
 "ResourceBookingStatus": {
  "type": "string",
  "enum": [
   "reserved",
   "checkedOut",
   "returned",
   "overdue",
   "cancelled",
   "noShow"
  ]
 },
 "ResourceKind": {
  "type": "string",
  "description": "BL-135. **`locker` was an entitlement kind in `orders` and nothing issued, assigned or released one.** A locker is a specific object checked out to a named guest and returned — which is this context exactly, and modelling it as an entitlement would have needed a second check-out mechanism.\nA seed for `ResourceType` rather than the law (board 1.02): a customer adding a class does it with `createResourceType`, not by waiting for this list to grow.\n**`table` is a non-dining spot** (decided 29 September, rev 3 GAP-C2, confirmed by Chinmay): a beach or event table placed on a venue map, picked and sold like a cabana (`createResourceHold`, then the order). **A dining table is not this**: restaurant tables stay `fnb` tables, booked with `fnb.createTableReservation` and the waitlist (audit R073 (d)).\n",
  "enum": [
   "cabana",
   "lounger",
   "locker",
   "wheelchair",
   "stroller",
   "equipment",
   "room",
   "auditorium",
   "vehicle",
   "instructor",
   "staff",
   "table",
   "pitch",
   "studio",
   "other"
  ],
  "x-ticvai-refuses": {
   "mealPlan": "**Listed by 5.5.8b and deliberately not a kind.** 5.5.8b groups meal plans with lockers and parking, but a meal plan is a balance rather than an object. It resolves to `retail.Wallet` with a `mealPlan` credit kind (CF-126), not to a resource — so it is not offered here, and a form built from this enum cannot offer it either."
  }
 },
 "ScanAnomalyRuleList": {
  "type": "array",
  "x-ticvai-persistence-kind": "valueObject",
  "x-ticvai-persistence-column": "jsonb",
  "description": "**One `jsonb` column on the access point row** (`access.access_point.scan_anomaly_rules`). Read with the access point at validation, and a rule is never queried on its own.\n",
  "items": {
   "type": "object",
   "properties": {
    "rule": {
     "type": "string",
     "enum": [
      "simultaneousEntry",
      "impossibleTravelTime",
      "rapidReentry",
      "sharedDevice",
      "velocityBreach"
     ]
    },
    "action": {
     "type": "string",
     "enum": [
      "log",
      "flag",
      "requireSupervisor",
      "deny"
     ]
    },
    "thresholdSeconds": {
     "type": "integer",
     "nullable": true
    }
   }
  }
 },
 "ScanEvent": {
  "x-ticvai-append-only": "recordedAt",
  "x-ticvai-persistence": "access.scan_event",
  "type": "object",
  "required": [
   "id",
   "accessPointId",
   "venueId",
   "outcome",
   "direction",
   "recordedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "description": "The scan's client-generated UUIDv7, the key offline replay deduplicates on."
   },
   "accessPointId": {
    "type": "string",
    "format": "uuid"
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "scopePath": {
    "type": "string"
   },
   "ticketId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The `Entitlement.id` scanned; null where the media resolved to nothing."
   },
   "mediaCode": {
    "type": "string",
    "nullable": true
   },
   "outcome": {
    "$ref": "#/components/schemas/ScanOutcome"
   },
   "denyReason": {
    "$ref": "#/components/schemas/DenyReason"
   },
   "direction": {
    "$ref": "#/components/schemas/Direction"
   },
   "operatorPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "deviceId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "overridesScanId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "**Set only on an override row**, naming the denied scan it admits against (decided 28 September, audit R228). The denied scan itself is never updated: the denial and the override are two rows, and at most one override row names any scan. Null on every other scan.\n"
   },
   "overrideReason": {
    "type": "string",
    "nullable": true,
    "description": "The supervisor's justification, on the override row only. The overriding principal is that row's `operatorPrincipalId`."
   },
   "dynamicPolicyId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The dynamic access policy (`access.dynamic_policy`) whose result decided this scan; null when no dynamic policy matched and the entitlement alone decided (added 29 September, build pass, 3.3.48). `listDynamicPolicyEffectiveness` counts from it."
   },
   "dynamicPolicyVersion": {
    "type": "integer",
    "minimum": 1,
    "nullable": true,
    "description": "The version of that policy in force at the scan, so a report spanning a change counts each version apart."
   },
   "dynamicPolicyResult": {
    "type": "string",
    "enum": [
     "allow",
     "deny",
     "review",
     "requireId",
     "requireBiometric",
     "requireCompanion",
     "requireSupervisor"
    ],
    "nullable": true,
    "description": "What the policy decided, which for a step-up is not the same as the scan's outcome."
   },
   "quantity": {
    "type": "integer",
    "minimum": 1,
    "default": 1,
    "description": "Admissions this scan counted. More than one only for a group wave (`validateGroupAccess`) or a quantity entitlement consumed in one pass (added 29 September, data-model close-out DM1)."
   },
   "localSequence": {
    "type": "integer",
    "nullable": true,
    "description": "The device-local sequence number of a scan recorded offline; null for an online scan (added 29 September, data-model close-out DM1)."
   },
   "packageVersion": {
    "type": "string",
    "nullable": true,
    "description": "The offline package (`access.edge_package`) the device validated against; null for an online scan (added 29 September, data-model close-out DM1)."
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time"
   },
   "syncedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "Null while pending. Differs from recordedAt for offline scans."
   }
  }
 },
 "ScanOutcome": {
  "type": "string",
  "enum": [
   "admitted",
   "denied",
   "overridden"
  ]
 },
 "StoredValueAuthorisation": {
  "type": "object",
  "x-ticvai-persistence": "orders.stored_value_authorisation",
  "description": "A hold against any stored-value instrument. **Two-phase by necessity, not by preference** — an arcade machine, a kitchen and a gate all take time between committing to a spend and knowing it succeeded, and a balance that cannot be held is a balance that gets double-spent or refunded by hand.\n",
  "required": [
   "id",
   "kind",
   "instrumentId",
   "amount",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "kind": {
    "$ref": "#/components/schemas/StoredValueKind"
   },
   "instrumentId": {
    "type": "string",
    "format": "uuid",
    "description": "The wallet, card, voucher or position being held against."
   },
   "amount": {
    "$ref": "#/components/schemas/Money"
   },
   "status": {
    "type": "string",
    "enum": [
     "held",
     "partiallyCaptured",
     "captured",
     "released",
     "expired"
    ],
    "description": "**Mirrors `cross-region.WalletAuthorisation` exactly**, which is the point — one lifecycle rather than six.\n"
   },
   "capturedAmount": {
    "$ref": "#/components/schemas/Money"
   },
   "expiresAt": {
    "type": "string",
    "format": "date-time",
    "description": "**Released automatically.** A hold nobody releases is a guest whose balance is short with no explanation, and the arcade is where that happens most.\n"
   },
   "reference": {
    "type": "string",
    "description": "What the hold is for — an order, a play, a table visit."
   },
   "scopePath": {
    "type": "string",
    "description": "**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**"
   }
  }
 },
 "StoredValueKind": {
  "type": "string",
  "description": "**Six things in this package hold a balance and behave the same way** — a wallet, a gift card, a game card, a voucher, a loyalty position and a prepaid entitlement. They were built separately across three sessions and each grew its own balance, bonus balance, status, blocked reason and expiry (CF-126).\n**The concern is not tidiness. Only one of the six could hold an authorisation.** `authoriseWalletSpend` / `captureWalletAuthorisation` / `relinquishWalletAuthorisation` gave two-phase spend to the retail wallet alone, so **a guest with 200 game credits starting a play the machine then failed had no held balance** — the credits were either taken or not, with no third state.\nThe entities stay distinct because their lifecycles genuinely differ — a gift card activates at a till, a loyalty position never expires the same way. **What is shared is the spend mechanism**, and this enum is what lets it be shared.\n",
  "enum": [
   "wallet",
   "giftCard",
   "gameCard",
   "voucher",
   "loyalty",
   "prepaidEntitlement"
  ]
 },
 "TurnstileMode": {
  "type": "string",
  "description": "**Reduced to two values — decided 28 September, audit R221.** Entry, exit, re-entry and crossover were the access point's `Direction` under another name, and two fields that could disagree left the gate to guess. Direction is fixed per access point; within `normal` or `podium` operation the turnstile may only be let spin free or held closed.\n",
  "enum": [
   "freeRotation",
   "closed"
  ]
 },
 "VenueSettings": {
  "type": "object",
  "x-ticvai-persistence": "platform.venue_settings",
  "description": "**Venue-level operational configuration that no other level can answer.**\nRegion owns currency, tax regime and fiscal year (ADR-0011). Venue owns the things that vary between two venues in one region — **opening hours, support hours, and what the local law requires of the gate.**\n**And the configured limits** (decided 28 September, audit R094): every limit the contracts call *configured* is a field here, from `displayCurrencies` and `cartLeaseSeconds` down to the grouped `catalogue`, `inventory`, `seating`, `promotions`, `fnb`, `queue`, `reporting`, `marketing` and `identity` settings. **Each has a tenant-level default**: the tenant sets it once with `setVenueSettingsDefaults`, a venue overrides it within the field's bounds, and a null field here inherits it. Each field's `default` is the proposed tenant default, marked proposed, client to correct (audit R094); `docs/active/configured-limits-proposal.md` is the sheet the client corrects, and where the two differ this contract is what runs.\n",
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"
   },
   "venueId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "From the path of `setVenueSettings`."
   },
   "calendarDayStartHour": {
    "type": "integer",
    "minimum": 0,
    "maximum": 23,
    "nullable": true,
    "default": 6,
    "description": "**Where the venue's calendar day starts** (17 September minutes M17-03, added 30 September): the first hour row of every day and week calendar view (`calendarView` in `screens/_components.yaml`), so a venue open 06:00 to 02:00 sees its night on the day it belongs to. Display only: it moves no booking, slot or business date. Null inherits the tenant default (proposed 6, client to correct).\n"
   },
   "currencyCode": {
    "type": "string",
    "pattern": "^[A-Z]{3}$",
    "nullable": true,
    "readOnly": true,
    "description": "**`readOnly` is the freeze.** `setVenueSettings` takes this whole schema as its request body, so without it any settings save could rewrite the currency of a venue that had already traded — which is the one thing ADR-0018's amendment forbids. It is set when the venue is provisioned, defaulted from the region, and changed only by an operation whose precondition is that the venue has not yet traded.\n**The venue's trading currency, defaulted from its region and frozen once the venue has traded** (ADR-0018, amended 20 September). Currency was a region-only fact, grouped with tax rates on the reasoning that *\"a venue cannot choose its VAT\"* -- true of tax and over-applied to currency, because a free-zone unit, a duty-free shop and a cruise terminal genuinely trade in a currency their region does not.\n**This column exists because the freeze needs somewhere to live.** A venue that resolved purely from its region would silently follow a region currency change after it had already traded, and every dated artefact beneath it -- a price list is a `validFrom`/`validTo` range -- would render retrospectively wrong. Null means \"resolve from the region\", which is the answer for every venue that has not overridden.\n"
   },
   "currencyScale": {
    "type": "integer",
    "minimum": 0,
    "maximum": 4,
    "nullable": true,
    "readOnly": true,
    "description": "**Scale travels with currency** (ADR-0008), and so does the freeze. OMR is three decimal places because Oman says so; overriding the currency without the scale gets rounding wrong. Set together or not at all.\n"
   },
   "supportHours": {
    "type": "object",
    "description": "CF-100. **A venue decides whether its support desk is 24/7 or bounded, and the platform does not.** This was recorded as an open question for eleven days and was never one — the code is identical either way, and what was missing was somewhere to put the answer.\n",
    "properties": {
     "mode": {
      "type": "string",
      "enum": [
       "alwaysOn",
       "businessHours",
       "custom",
       "none"
      ]
     },
     "timezone": {
      "type": "string",
      "description": "IANA zone the `windows` are read in. Absent, they are read in the region's `timeZone`, like every other wall-clock time in this contract.\n"
     },
     "windows": {
      "type": "array",
      "items": {
       "type": "object",
       "properties": {
        "day": {
         "type": "string",
         "enum": [
          "mon",
          "tue",
          "wed",
          "thu",
          "fri",
          "sat",
          "sun"
         ]
        },
        "from": {
         "type": "string",
         "description": "Wall-clock time the desk opens."
        },
        "to": {
         "type": "string",
         "description": "Wall-clock time the desk closes."
        }
       }
      }
     },
     "outOfHoursMessage": {
      "type": "string",
      "nullable": true
     }
    }
   },
   "quietHours": {
    "type": "object",
    "nullable": true,
    "description": "**When the platform does not send.** A wallet low-balance alert at 3am is a complaint, and journeys and message triggers both respect this.\n**Operational messages ignore it** — a queue-turn alert is why a guest is holding the phone.\n",
    "properties": {
     "from": {
      "type": "string",
      "description": "Wall-clock time sending stops",
      "in the region's time zone.": null
     },
     "to": {
      "type": "string",
      "description": "Wall-clock time sending resumes",
      "in the region's time zone.": null
     }
    }
   },
   "biometrics": {
    "type": "object",
    "nullable": true,
    "description": "CF-35, BL-096, BL-105, BL-106. **The venue-level master switch, and the one place a person is asked whether the paperwork exists.** Biometric data is sensitive under PDPL (Federal Decree-Law 45/2021) — heightened protection, explicit consent, and an Article 21 assessment before the processing rather than after it.\n**Nothing below this switch operates while it is off.** `AdmissionRules` may carry a `biometricPolicy` per ticket type and those rules are inert until a venue enables biometrics here, which means a profile copied between venues cannot start capturing faces at the destination.\n**Venue level because that is where the assessment is filed.** Region owns tax and currency; the DPIA, the consent notice and the hardware are a venue's.\n",
    "properties": {
     "isEnabled": {
      "type": "boolean",
      "default": false,
      "description": "**Off by default, and turning it on is refused without the two fields below.** `setVenueSettings` answers 422 rather than accepting an enable it cannot evidence — **a DPIA nobody can name is a DPIA nobody did**, and the point of the refusal is that the person switching this on is asked at the moment they switch it on rather than by an auditor a year later.\n"
     },
     "dpiaReference": {
      "type": "string",
      "nullable": true,
      "maxLength": 200,
      "description": "**The venue's own reference for its Article 21 assessment.** The platform does not hold the document and does not judge it; it records that one was named, by whom, and when — which is what an audit asks for and what the venue can produce.\n"
     },
     "consentNoticeAcknowledgedAt": {
      "type": "string",
      "format": "date-time",
      "nullable": true,
      "description": "**When somebody confirmed the consent forms are in place at the point of capture.** A guest consenting in an app is a record; a guest consenting at a ticket counter is a notice somebody has to have printed and a question somebody has to have asked.\n"
     },
     "acknowledgedByPrincipalId": {
      "type": "string",
      "format": "uuid",
      "nullable": true,
      "readOnly": true,
      "description": "**Who confirmed it.** An acknowledgement with no name behind it cannot be followed up, and this is the field that makes the switch an act rather than a setting. Recorded by the server as the caller whose save carried the acknowledgement, so it cannot name somebody else.\n"
     },
     "faceTagPurgeMinutesAfterClose": {
      "type": "integer",
      "nullable": true,
      "default": 0,
      "description": "BL-106. **How long a same-visit Face Tag survives past the close of the operating day**, and zero is the default because that is what 3.2.44 describes. A non-zero value is an operational allowance for a late reconciliation, not a retention period — **`facePass` ignores this entirely** and is bounded by its entitlement.\n"
     }
    }
   },
   "segregatedAccess": {
    "type": "object",
    "nullable": true,
    "description": "CF-130. **Configured at venue level because it changes by region and the venue is where it is known** — a Ladies Night, a family session, a prayer-time closure.\n**The platform does not infer gender.** 3.2.45 asks for automatic gender recognition and 3.2.46 for rule-based facial recognition validation, and neither is built. Two reasons, and the second is the one that decided it:\n**A Ladies Night ticket is already gendered at the point of sale**, so the gate checks the entitlement the platform issued rather than the face in front of it — deterministic, auditable, and already contracted through `admissionRules`.\n**And these events are staffed.** A steward at the entrance is making the judgment anyway, and a classifier that overrules a person who can see more than it can is a machine and a human disagreeing while a guest waits.\n**`genderVerification` is a switch, not an implementation.** Where a venue's access hardware offers the capability and the venue chooses to use it, this turns it on — following ADR-0015's standards-first driver model, where the device does what the device does. **Not everything needs to be built.**\n",
    "properties": {
     "isEnabled": {
      "type": "boolean",
      "default": false
     },
     "appliesToAccessPointIds": {
      "type": "array",
      "items": {
       "type": "string",
       "format": "uuid"
      }
     },
     "schedule": {
      "type": "array",
      "items": {
       "type": "object",
       "properties": {
        "day": {
         "type": "string",
         "enum": [
          "mon",
          "tue",
          "wed",
          "thu",
          "fri",
          "sat",
          "sun"
         ]
        },
        "from": {
         "type": "string",
         "description": "Wall-clock time",
         "in the region's time zone.": null
        },
        "to": {
         "type": "string",
         "description": "Wall-clock time",
         "in the region's time zone.": null
        },
        "admits": {
         "type": "string",
         "enum": [
          "all",
          "women",
          "womenAndChildren",
          "families",
          "members"
         ]
        }
       }
      }
     },
     "entitlementGated": {
      "type": "boolean",
      "default": true,
      "readOnly": true,
      "description": "**Always true, and stated rather than assumed.** The gate admits on the entitlement. Everything below is advisory on top of that, and nothing replaces it.\n"
     },
     "genderVerification": {
      "type": "string",
      "enum": [
       "off",
       "staffAssisted",
       "deviceAssisted"
      ],
      "default": "off",
      "description": "`off` — the entitlement decides and a steward handles exceptions. **The default, and what is contracted.**\n`staffAssisted` — the steward's screen shows the ticket type so they can ask. No inference anywhere.\n`deviceAssisted` — **the venue's access hardware performs the check, not the platform.** Available only where the driver reports the capability, and the result is **advisory to the steward rather than decisive at the turnstile** (3.2.45 asks for rejection; this deviates deliberately).\n"
     },
     "overrideRateAlertThreshold": {
      "type": "number",
      "nullable": true,
      "description": "Where `deviceAssisted` is on. **An override rate near zero means the steward has stopped deciding**, and that is the number that says whether the human safeguard is working or decorative.\n"
     }
    }
   },
   "alerting": {
    "type": "object",
    "description": "CF-134. **On-platform notification, marked as read.** Six contracts detect their own trouble and none told a person.\n**The panel is the default and email or WhatsApp only where the matrix names them** — an operational alert that arrives by email is an alert nobody sees in time.\n",
    "properties": {
     "channel": {
      "type": "string",
      "enum": [
       "dashboardPanel",
       "dashboardAndEmail",
       "dashboardAndWhatsapp"
      ],
      "default": "dashboardPanel"
     },
     "acknowledgementRequired": {
      "type": "boolean",
      "default": true
     },
     "escalateAfterMinutes": {
      "type": "integer",
      "nullable": true
     }
    }
   },
   "displayCurrencies": {
    "type": "array",
    "nullable": true,
    "description": "**Which currencies this venue shows guests** (decided 28 September, audit R120 (a)). ISO 4217 codes, each one its region holds an `FxRate` for; the rate itself stays per region and is never set here. `finance.listFxRates` with `venueId` narrows the region's rates to these. Null or empty shows the trading currency only. A code the region has no rate for is refused `400`.\n",
    "items": {
     "type": "string",
     "pattern": "^[A-Z]{3}$"
    }
   },
   "cartLeaseSeconds": {
    "type": "integer",
    "nullable": true,
    "minimum": 30,
    "maximum": 3600,
    "default": 900,
    "description": "**How long a cart holds capacity** (decided 28 September, audit R169): 15 minutes, the default `catalogue.acquireInventoryHold` takes for `ttlSeconds`. Proposed, client to correct (audit R094).\n"
   },
   "cartHoldExtensionMinutes": {
    "type": "integer",
    "nullable": true,
    "minimum": 1,
    "maximum": 30,
    "default": 5,
    "description": "How long one `orders.extendCart` extension adds. Proposed, client to correct (audit R094)."
   },
   "cartMaxExtensions": {
    "type": "integer",
    "nullable": true,
    "minimum": 0,
    "maximum": 5,
    "default": 1,
    "description": "How many extensions a cart may take before `extensionCapReached` (`Cart.maxExtensions`). Proposed, client to correct (audit R094)."
   },
   "resaleCutoffHours": {
    "type": "integer",
    "nullable": true,
    "minimum": 0,
    "maximum": 168,
    "default": 24,
    "description": "Hours before the performance after which a ticket can no longer be listed for resale (`orders.createResaleListing`). Proposed, client to correct (audit R094)."
   },
   "exchangeCutoffHours": {
    "type": "integer",
    "nullable": true,
    "minimum": 0,
    "maximum": 720,
    "default": 24,
    "description": "Hours before the original performance after which lines can no longer be exchanged (`orders.exchangeOrderLines`, `outsideExchangeWindow`). Proposed, client to correct (audit R094)."
   },
   "rescheduleCutoffHours": {
    "type": "integer",
    "nullable": true,
    "minimum": 0,
    "maximum": 720,
    "default": 24,
    "description": "Hours before the original performance after which an order can no longer be rescheduled (`orders.rescheduleOrder`, `outsideRescheduleWindow`). Proposed, client to correct (audit R094)."
   },
   "reservationMaxExtensions": {
    "type": "integer",
    "nullable": true,
    "minimum": 0,
    "maximum": 5,
    "default": 1,
    "description": "How many times `orders.extendReservation` may extend one reservation. Proposed, client to correct (audit R094)."
   },
   "shiftVarianceThreshold": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "nullable": true,
    "description": "Over or short at shift close beyond which the shift waits in `pendingVariance` for `shift.acceptShiftVariance`. **Proposed tenant default AED 20.00, bounds 0 to 1,000 in the venue currency; client finance to correct (audit R094).**\n"
   },
   "catalogue": {
    "type": "object",
    "nullable": true,
    "properties": {
     "maxVariantsPerProduct": {
      "type": "integer",
      "nullable": true,
      "minimum": 1,
      "maximum": 2000,
      "default": 200,
      "description": "Variants one product may generate from its attributes (`setProductAttributes` refuses above it). Proposed, client to correct (audit R094)."
     },
     "waitlistOfferHoldMinutes": {
      "type": "integer",
      "nullable": true,
      "minimum": 1,
      "maximum": 1440,
      "default": 30,
      "description": "How long a waitlist offer holds the released capacity for the guest it was offered to. Proposed, client to correct (audit R094)."
     },
     "bulkPriceChangeEscalationPercent": {
      "type": "number",
      "nullable": true,
      "minimum": 0,
      "maximum": 100,
      "default": 10,
      "description": "A `bulkChangePrices` run changing any price by more than this percentage needs `PRICE_CONFIGURE` (audit R197). Proposed, client to correct (audit R094)."
     },
     "bulkPriceChangeEscalationCount": {
      "type": "integer",
      "nullable": true,
      "minimum": 1,
      "default": 50,
      "description": "A `bulkChangePrices` run touching more prices than this needs `PRICE_CONFIGURE` (audit R197). Proposed, client to correct (audit R094)."
     }
    }
   },
   "inventory": {
    "type": "object",
    "nullable": true,
    "properties": {
     "overReceiptTolerancePercent": {
      "type": "number",
      "nullable": true,
      "minimum": 0,
      "maximum": 25,
      "default": 5,
      "description": "Percent above the outstanding ordered quantity a goods receipt line may record (`createGoodsReceipt`). Proposed, client to correct (audit R094)."
     },
     "countVarianceTolerancePercent": {
      "type": "number",
      "nullable": true,
      "minimum": 0,
      "maximum": 25,
      "default": 2,
      "description": "Percent difference between counted and expected quantity before a count line is an exception (`getCountVariance`). Proposed, client to correct (audit R094)."
     },
     "countVarianceApprovalAmount": {
      "allOf": [
       {
        "$ref": "../shared/common.yaml#/components/schemas/Money"
       }
      ],
      "nullable": true,
      "description": "Total variance value of a count above which posting it needs approval (`postStockCount`). **Proposed tenant default 1,000.00 in the venue currency, client finance to correct (audit R094).**\n"
     }
    }
   },
   "seating": {
    "type": "object",
    "nullable": true,
    "properties": {
     "seatHoldExtensionSeconds": {
      "type": "integer",
      "nullable": true,
      "minimum": 60,
      "maximum": 1800,
      "default": 300,
      "description": "What one `extendSeatHold` adds. No hold outlives 30 minutes in all (audit R169). Proposed, client to correct (audit R094)."
     },
     "seatHoldMaxExtensions": {
      "type": "integer",
      "nullable": true,
      "minimum": 0,
      "maximum": 5,
      "default": 2,
      "description": "How many times a seat hold may be extended. Proposed, client to correct (audit R094). A resource hold on a venue map (`resources.extendResourceHold`) uses the same two bounds (decided 29 September, rev 3 REV3-15)."
     },
     "maxSeatsPerGuestOrder": {
      "type": "integer",
      "nullable": true,
      "minimum": 1,
      "maximum": 50,
      "default": 10,
      "description": "**Seats one guest may take in one booking on a guest channel** (Guest Web, Guest App), decided 29 September, rev 3 REV3-7. `seating.createSeatHold` counts the seats in the request plus the seats the same guest already holds on the same performance, and refuses above this with `422` `seat-limit-exceeded`, naming the limit. Default 10, bounds 1 to 50; a venue sets its own in Venue Management. Staff and POS sales keep 10 per sale (audit R080 (c)) and do not read this field.\n"
     }
    }
   },
   "promotions": {
    "type": "object",
    "nullable": true,
    "properties": {
     "maxDiscountPercent": {
      "type": "number",
      "nullable": true,
      "minimum": 0,
      "maximum": 100,
      "default": 30,
      "description": "The largest discount one promotion may give (`createPromotion` refuses above it). Proposed, client to correct (audit R094)."
     },
     "nearZeroLinePrice": {
      "allOf": [
       {
        "$ref": "../shared/common.yaml#/components/schemas/Money"
       }
      ],
      "nullable": true,
      "description": "Net line price below which a stacked combination is flagged near-zero in `analysePromotionConflicts` (audit R096 (5)); a warning, not a refusal. **Proposed tenant default AED 1.00, client to correct (audit R094).**\n"
     }
    }
   },
   "fnb": {
    "type": "object",
    "nullable": true,
    "properties": {
     "recallWindowMinutes": {
      "type": "integer",
      "nullable": true,
      "minimum": 0,
      "maximum": 60,
      "default": 10,
      "description": "Minutes after a bump during which `recallKitchenTicket` still recalls; after it the act is a refire. Proposed, client to correct (audit R094)."
     },
     "compEscalationAmount": {
      "allOf": [
       {
        "$ref": "../shared/common.yaml#/components/schemas/Money"
       }
      ],
      "nullable": true,
      "description": "Line value above which `compItem` needs `ORDER_DISCOUNT` (audit R197). **Proposed tenant default AED 100.00, client to correct (audit R094).**\n"
     },
     "foodSafetyLeadPrincipalId": {
      "type": "string",
      "format": "uuid",
      "nullable": true,
      "description": "**The venue's food-safety lead**, to whom `escalateCorrectiveAction` sends every escalation (decided 28 September, audit R096 (9)). A venue fact, so it has no tenant default; while it is null an escalation is refused `409 no-food-safety-lead`.\n"
     }
    }
   },
   "queue": {
    "type": "object",
    "nullable": true,
    "properties": {
     "crossQueueLimit": {
      "type": "integer",
      "nullable": true,
      "minimum": 1,
      "maximum": 10,
      "default": 2,
      "description": "Virtual queues one guest party may wait in at once (`joinQueue`, `crossQueueLimitReached`). Proposed, client to correct (audit R094)."
     }
    }
   },
   "reporting": {
    "type": "object",
    "nullable": true,
    "properties": {
     "inlineRunRowLimit": {
      "type": "integer",
      "nullable": true,
      "minimum": 1000,
      "maximum": 100000,
      "default": 5000,
      "description": "Estimated rows above which `runReport` answers `202` and runs in the background. Proposed, client to correct (audit R094)."
     },
     "dashboardRefreshBudgetPerMinute": {
      "type": "integer",
      "nullable": true,
      "minimum": 1,
      "default": 24,
      "description": "Tile refreshes per minute, summed over a dashboard's tiles, that `createDashboard` allows. Proposed, client to correct (audit R094)."
     }
    }
   },
   "marketing": {
    "type": "object",
    "nullable": true,
    "properties": {
     "attributionWindowDays": {
      "type": "integer",
      "nullable": true,
      "minimum": 1,
      "maximum": 30,
      "default": 7,
      "description": "Days after a campaign touch within which a booking is attributed to it (`getCampaignPerformance`). Proposed, client to correct (audit R094)."
     }
    }
   },
   "identity": {
    "type": "object",
    "nullable": true,
    "properties": {
     "guestOtpMaxAttempts": {
      "type": "integer",
      "nullable": true,
      "minimum": 3,
      "maximum": 10,
      "default": 5,
      "description": "Wrong entries allowed per guest one-time code before `verifyGuestOtp` invalidates it. A guest code is tenant-scoped, so the tenant default is the value used. Proposed, client to correct (audit R094).\n"
     },
     "guestTwoStep": {
      "type": "object",
      "nullable": true,
      "description": "**Guest two-step verification: a venue option, off unless the venue enables it in Venue Management** (decided 29 September, rev 3 GAP-B1, per venue, superseding the second part of audit R167, \"no guest MFA\"; an earlier draft of the same day put it on the tenant's `PasswordPolicy`, which no longer carries it). **The guest's enrolment stays tenant-wide**: one guest account across the tenant's venues, so a method enrolled once is used in every venue that has this on, and is never asked in a venue that has it off. Identity learns the venue from `venueId` on the guest sign-in (`verifyGuestOtp`, `guestPasswordLogin`, `guestSocialLogin`, `guestUaePassLogin`) and on `createMfaChallenge`: the venue the guest app or booking is in; with no venue given, an enrolled guest is asked when any venue of the tenant has it on. Guests may enrol `totp` with `emailOtp` as the fallback, as staff do (audit R126 (5)); it is never forced. Guests still never use enterprise SSO (R167, first part). A null inherits the tenant default set with `setVenueSettingsDefaults`.\n",
      "properties": {
       "enabled": {
        "type": "boolean",
        "default": false,
        "description": "Off unless the venue enables it. While no venue of the tenant has it on, guests cannot enrol (`enrolMfaMethod` answers 403 `guest-two-step-disabled`)."
       },
       "stepUpActions": {
        "type": "array",
        "uniqueItems": true,
        "description": "The guest actions in this venue that ask an enrolled guest for the factor again, whatever the age of the session. The service performing the action passes this venue to `createMfaChallenge`. Proposed, client to correct (rev 3 GAP-B1).\n",
        "items": {
         "type": "string",
         "enum": [
          "changeContactDetails",
          "changePassword",
          "managePaymentMethods",
          "transferTickets",
          "deleteAccount"
         ]
        },
        "default": [
         "changeContactDetails",
         "changePassword",
         "managePaymentMethods",
         "deleteAccount"
        ]
       }
      }
     }
    }
   }
  }
 }
}
```
