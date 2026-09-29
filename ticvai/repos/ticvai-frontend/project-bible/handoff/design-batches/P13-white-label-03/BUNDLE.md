# P13-white-label-03 — P13 · White Label (3 of 3)

**3 screens · 25 operations · 40 schemas · 6 permissions**

Platform P13 Venue CMS · ships as **venue-management** ·
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

- **Every control that can be refused must be gated.** 6 permissions apply here:
  `AI_USE, GUEST_VIEW, PRODUCT_CONFIGURE, PRODUCT_VIEW, TENANT_CONFIGURE, TENANT_PUBLISH`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `CMS-102` | Site Builder | multiStepForm | 7 | 1 | — |
| `CMS-103` | Booking Flows | listDetail | 14 | 3 | — |
| `CMS-104` | App Build & Store Publishing | listDetail | 7 | 2 | — |

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "CMS-102",
  "name": "Site Builder",
  "module": "White Label",
  "requiresModule": "core",
  "wave": 1,
  "capability": "C00",
  "implementation": {
   "app": "venue-management-web",
   "route": "/white-label/site-builder",
   "component": "apps/venue-management-web/src/routes/white-label/SiteBuilder.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "CMS-001"
   ],
   "exitTo": [
    "CMS-001",
    "CMS-103",
    "CMS-101",
    "CMS-007",
    "CMS-009",
    "CMS-002",
    "CMS-004",
    "CMS-008",
    "CMS-005",
    "CMS-003",
    "CMS-006",
    "CMS-012",
    "CMS-014",
    "CMS-015",
    "CMS-104"
   ],
   "inferred": false,
   "notes": "**The step-based CMS (decided 29 September, W12 and M24-05).** Each of the seven steps opens the full screen for its details and comes back here; progress is saved on every return, so the builder reopens where the operator left it.",
   "transitions": [
    {
     "to": "CMS-001",
     "trigger": "1 Venue and modules",
     "provenance": "authored 29 September, W12 (step 1 reuses CMS-001 for modules, feature toggles and guest checkout)",
     "back": true
    },
    {
     "to": "CMS-103",
     "trigger": "2 Ticketing flows",
     "provenance": "authored 29 September, W12 (steps 2 and 3 are CMS-103)",
     "back": true,
     "carries": [
      "bookingFlowId"
     ]
    },
    {
     "to": "CMS-103",
     "trigger": "3 Compose steps",
     "carries": [
      "bookingFlowId"
     ],
     "provenance": "authored 29 September, W12 (step order and step settings)",
     "back": true
    },
    {
     "to": "CMS-101",
     "trigger": "4 Help me choose",
     "provenance": "authored 29 September, W12 and W4",
     "back": true
    },
    {
     "to": "CMS-007",
     "trigger": "5 Look and feel — header, footer and home",
     "provenance": "authored 29 September, W12 (header and footer on CMS-007 and CMS-009)",
     "back": true
    },
    {
     "to": "CMS-009",
     "trigger": "5 Look and feel — navigation and menus",
     "provenance": "authored 29 September, W12",
     "back": true
    },
    {
     "to": "CMS-002",
     "trigger": "5 Look and feel — brand kit",
     "provenance": "authored 29 September, W12 (logos on CMS-002 and CMS-004)",
     "back": true
    },
    {
     "to": "CMS-004",
     "trigger": "5 Look and feel — logos",
     "provenance": "authored 29 September, W12",
     "back": true
    },
    {
     "to": "CMS-008",
     "trigger": "5 Look and feel — banners",
     "provenance": "authored 29 September, W12",
     "back": true
    },
    {
     "to": "CMS-005",
     "trigger": "5 Look and feel — theme",
     "provenance": "authored 29 September, W12 (theme and fonts on CMS-005 and CMS-003)",
     "back": true
    },
    {
     "to": "CMS-003",
     "trigger": "5 Look and feel — fonts",
     "provenance": "authored 29 September, W12",
     "back": true,
     "carries": [
      "version"
     ]
    },
    {
     "to": "CMS-009",
     "trigger": "6 Mobile app — tabs and the Buy tickets button",
     "provenance": "authored 29 September, MOB-1 and MOB-2",
     "back": true
    },
    {
     "to": "CMS-004",
     "trigger": "6 Mobile app — intro video",
     "provenance": "authored 29 September, MOB-5",
     "back": true
    },
    {
     "to": "CMS-007",
     "trigger": "6 Mobile app — home sections",
     "provenance": "authored 29 September, MOB-3",
     "back": true
    },
    {
     "to": "CMS-006",
     "trigger": "7 Preview",
     "provenance": "authored 29 September, W12 (step 7 is CMS-006, CMS-012 and CMS-014)",
     "back": true,
     "carries": [
      "version"
     ]
    },
    {
     "to": "CMS-012",
     "trigger": "7 Preview right to left",
     "provenance": "authored 29 September, W12",
     "back": true
    },
    {
     "to": "CMS-014",
     "trigger": "7 Publish",
     "provenance": "authored 29 September, W12",
     "back": true
    },
    {
     "to": "CMS-015",
     "trigger": "Roll back a version",
     "provenance": "authored 29 September, W12 (CMS-015 handles rollback)",
     "back": true,
     "carries": [
      "version"
     ]
    },
    {
     "to": "CMS-104",
     "trigger": "Build the mobile app",
     "precondition": "the tenant has published at least once",
     "provenance": "authored 29 September, M24-08",
     "back": true
    }
   ]
  },
  "notes": "**Added 29 September for W12 and M24-05: the CMS is a flow builder with a step-based shell.** The configuration side panel of the rev 3 prototype is a reference tool only (W12). The builder is the white-labelling builder M24-05 asks for, not a new set of editors: every step opens a screen that already exists and holds its details.",
  "density": "compact",
  "pattern": "multiStepForm",
  "patternReason": "`getSiteSetupProgress` holds the seven steps and their state, and `setSiteSetupProgress` saves each one — progress, fields per step, review, submit",
  "purpose": "Build a working site in about 30 minutes: pick a preset, then walk seven saved steps (venue and modules, ticketing flows, compose steps, Help me choose, look and feel, mobile app, preview and publish), each opening the full screen for its details. **The preset keeps the minimum path short (M24-05)**: it proposes the modules, the booking flows with their default step order, the home sections and the mobile tabs, so the only things an operator must supply are a logo, four colours and a Publish; everything else keeps the preset or the contract default and can be refined later.",
  "layout": {
   "template": "wizard",
   "regions": [
    {
     "name": "progress",
     "slot": "progress",
     "components": [
      {
       "kind": "progressIndicator",
       "label": "Seven steps",
       "bindsTo": "SiteSetupProgress",
       "columns": [
        "SiteSetupProgress.currentStep",
        "SiteSetupProgress.steps",
        "SiteSetupProgress.minimumPathDone"
       ],
       "operation": "getSiteSetupProgress",
       "notes": "1 Venue and modules · 2 Ticketing flows · 3 Compose steps · 4 Help me choose · 5 Look and feel · 6 Mobile app · 7 Preview and publish. Each step shows not started, in progress, done or skipped; steps 4 and 6 may be skipped. **Minimum path** (logo, colours, one valid flow, a publish) is marked, so an operator in a hurry sees what is left before the site works.",
       "provenance": "contract white-label.yaml GET /tenant-config/site-setup"
      }
     ]
    },
    {
     "name": "fields",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Start from",
       "bindsTo": "SiteSetupProgress.presetKey",
       "operation": "setSiteSetupProgress",
       "notes": "Theme park, water park, museum, theatre and arena, single attraction, play centre, several venues. **Proposes, never writes**: each step opens pre-filled from the preset, and nothing changes until the operator saves that step.",
       "provenance": "contract white-label.yaml PUT /tenant-config/site-setup"
      },
      {
       "kind": "cardList",
       "label": "Flow types the preset proposes",
       "bindsTo": "BookingFlowType",
       "columns": [
        "BookingFlowType.key",
        "BookingFlowType.name",
        "BookingFlowType.productKinds"
       ],
       "operation": "listBookingFlowTypes",
       "notes": "Step 2 in one tap: the preset's flow types, ticked; **Add these flows** creates each with the type's default steps and order (`createBookingFlowDefinition`). Composing the order is step 3, on CMS-103.",
       "provenance": "contract white-label.yaml GET /booking-flow-types"
      },
      {
       "kind": "dataTable",
       "label": "Flows this venue has",
       "bindsTo": "BookingFlow",
       "columns": [
        "BookingFlow.name",
        "BookingFlow.flowTypeKey",
        "BookingFlow.isDefaultForType",
        "BookingFlow.isValid"
       ],
       "operation": "listBookingFlows",
       "notes": "Steps 2 and 3 are done when every flow here is valid and each bookable product kind has one.",
       "provenance": "contract white-label.yaml GET /venues/{venueId}/booking-flows"
      }
     ]
    },
    {
     "name": "review",
     "slot": "review",
     "components": [
      {
       "kind": "detailPanel",
       "label": "What is live",
       "bindsTo": "TenantAppStatus",
       "columns": [
        "TenantAppStatus.isPublished",
        "TenantAppStatus.publishedVersion",
        "TenantAppStatus.hasUnpublishedChanges"
       ],
       "operation": "getTenantAppStatus",
       "provenance": "contract white-label.yaml GET /tenant-config/status"
      },
      {
       "kind": "banner",
       "label": "What still blocks a publish",
       "bindsTo": "ConfigValidationReport",
       "columns": [
        "ConfigValidationReport.passed",
        "ConfigValidationReport.findings"
       ],
       "operation": "validateTenantConfig",
       "notes": "Each finding links to the step and screen that fixes it (a missing logo to CMS-004, an invalid flow to CMS-103).",
       "provenance": "contract white-label.yaml POST /tenant-config/validate"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "submit",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Save and continue",
       "operation": "setSiteSetupProgress",
       "provenance": "contract white-label.yaml PUT /tenant-config/site-setup"
      },
      {
       "kind": "secondaryButton",
       "label": "Add these flows",
       "operation": "createBookingFlowDefinition",
       "provenance": "contract white-label.yaml POST /venues/{venueId}/booking-flows"
      },
      {
       "kind": "secondaryButton",
       "label": "Check what blocks a publish",
       "operation": "validateTenantConfig",
       "provenance": "contract white-label.yaml POST /tenant-config/validate"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The builder's progress, read by `getSiteSetupProgress`.",
   "error": "Could not load. Names which read failed and leaves the progress untouched.",
   "emptyFirstRun": "**Nothing set up yet.** Opens on Start from, with every step not started, and says the minimum path is a logo, four colours, the preset's flows and a publish.",
   "emptyNoResults": "The venue has no flow of a type the preset proposes yet; the flow list says so and offers Add these flows rather than showing an empty table.",
   "emptyNoAccess": "Shown when the caller lacks `TENANT_CONFIGURE`, which `getSiteSetupProgress` requires, and names that permission. **Never an empty form** — that reads as *there is nothing to set up*."
  },
  "apis": [
   {
    "operationId": "getSiteSetupProgress",
    "contract": "white-label",
    "purpose": "Where the operator is in the seven steps, and the preset picked",
    "trigger": "onLoad"
   },
   {
    "operationId": "setSiteSetupProgress",
    "contract": "white-label",
    "purpose": "Save the preset and each step's state on every return",
    "trigger": "onAction",
    "invalidates": [
     "getSiteSetupProgress"
    ]
   },
   {
    "operationId": "listBookingFlowTypes",
    "contract": "white-label",
    "purpose": "The flow types the preset proposes for step 2",
    "trigger": "onLoad"
   },
   {
    "operationId": "listBookingFlows",
    "contract": "white-label",
    "purpose": "The venue's flows, to mark steps 2 and 3 done",
    "trigger": "onLoad"
   },
   {
    "operationId": "createBookingFlowDefinition",
    "contract": "white-label",
    "purpose": "Add the preset's flows with their default steps in one go",
    "trigger": "onAction",
    "invalidates": [
     "listBookingFlows"
    ]
   },
   {
    "operationId": "getTenantAppStatus",
    "contract": "white-label",
    "purpose": "Whether the site is live, for step 7",
    "trigger": "onLoad"
   },
   {
    "operationId": "validateTenantConfig",
    "contract": "white-label",
    "purpose": "What still blocks a publish, each finding linked to its step",
    "trigger": "onAction"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "venueId",
     "from": "session"
    }
   ],
   "coldEntry": "Resolves the tenant and venue from the session and opens on the current step, or on Start from when nothing is saved."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-102"
  },
  "apisNote": "Authored 29 September 2026 (P29 pass, W12 and M24-05) from impact.md section b.",
  "overlays": [
   {
    "id": "formAddPresetFlows",
    "component": "modal",
    "trigger": "Add these flows",
    "body": "**Collects what `createBookingFlowDefinition` sends, once per ticked type.** Required: `flowTypeKey`, `name` (pre-filled from the type). `isDefaultForType` on. Steps are left out, so each flow gets the type's default steps and order. Dismissing sends nothing.",
    "bindsTo": "BookingFlow",
    "confirm": {
     "label": "Add flows",
     "operation": "createBookingFlowDefinition"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "flowTypeKey",
      "name"
     ]
    },
    "provenance": "contract white-label.yaml POST /venues/{venueId}/booking-flows"
   }
  ],
  "_platform": {
   "code": "P13",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue CMS",
   "name": "Venue CMS — White Label",
   "app": "venue-management-web",
   "offlineCapable": false,
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P08",
     "P12",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "CMS-103",
  "name": "Booking Flows",
  "module": "White Label",
  "requiresModule": "core",
  "wave": 1,
  "capability": "C00",
  "implementation": {
   "app": "venue-management-web",
   "route": "/white-label/booking-flows",
   "component": "apps/venue-management-web/src/routes/white-label/BookingFlows.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "CMS-102",
    "CMS-016",
    "CMS-014"
   ],
   "exitTo": [
    "CMS-102",
    "CMS-016",
    "CMS-101",
    "CMS-014"
   ],
   "inferred": false,
   "notes": "**Steps 2 and 3 of the Site Builder (decided 29 September, W12).** Also reached from Site Settings, which now holds only the venue-wide settings, and from Publishing when a flow blocks the publish.",
   "transitions": [
    {
     "to": "CMS-102",
     "trigger": "Back to the Site Builder",
     "provenance": "authored 29 September, W12",
     "back": true
    },
    {
     "to": "CMS-016",
     "trigger": "Venue-wide booking settings",
     "provenance": "authored 29 September, W12 (the settings every flow shares stay on CMS-016)"
    },
    {
     "to": "CMS-101",
     "trigger": "Help me choose",
     "provenance": "authored 29 September, W4 (an answer can point at a flow)"
    },
    {
     "to": "CMS-014",
     "trigger": "Publish with the site",
     "provenance": "authored 29 September, W12 (flows publish through publishTenantConfig)"
    }
   ]
  },
  "notes": "**Added 29 September for W12: operators pick their ticketing flows, see which steps are required, optional or conditional, and set their own order.** The catalogue (`listBookingFlowTypes`) is the same for every tenant: dated day pass, timed entry, open-dated, seated (fixed performance, or date and time then seat map), experience or workshop (product first, W8), surf or session (time then level), meeting room by the hour, cabana on a map or by size (W6), guided tour by language, transport, table reservation, membership, gift card and several locations. Flows reach guests with the rest of the site (`publishTenantConfig`); WEB-005..012, GST-007..009 and GST-041 order their steps from the published flow.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listBookingFlows` reads the venue's flows and `getBookingFlow` reads one of them to compose — list, select, act",
  "purpose": "Pick the venue's booking flows, turn optional steps on or off, set the step order within the allowed limits with a live preview, assign flows to products and categories, and validate them before they publish with the site.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "filters",
     "slot": "filters",
     "components": [
      {
       "kind": "selectField",
       "label": "Venue",
       "operation": "listBookingFlows",
       "notes": "The venue whose flows are shown (path `venueId`); defaults to the session venue.",
       "provenance": "contract white-label.yaml GET /venues/{venueId}/booking-flows"
      },
      {
       "kind": "selectField",
       "label": "Flow type",
       "operation": "listBookingFlows",
       "notes": "Sends `?flowTypeKey=`.",
       "provenance": "contract white-label.yaml GET /venues/{venueId}/booking-flows"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "The venue's flows",
       "bindsTo": "BookingFlow",
       "columns": [
        "BookingFlow.name",
        "BookingFlow.flowTypeKey",
        "BookingFlow.isDefaultForType",
        "BookingFlow.isEnabled",
        "BookingFlow.isValid",
        "BookingFlow.updatedAt"
       ],
       "operation": "listBookingFlows",
       "notes": "An invalid flow is marked and blocks the site's publish until it is fixed.",
       "provenance": "contract white-label.yaml GET /venues/{venueId}/booking-flows"
      },
      {
       "kind": "cardList",
       "label": "Flow types to pick from",
       "bindsTo": "BookingFlowType",
       "columns": [
        "BookingFlowType.key",
        "BookingFlowType.name",
        "BookingFlowType.description",
        "BookingFlowType.productKinds",
        "BookingFlowType.steps"
       ],
       "operation": "listBookingFlowTypes",
       "notes": "Each card lists the type's steps with their required, optional or conditional mark, so the choice is made knowing what the guest will go through.",
       "provenance": "contract white-label.yaml GET /booking-flow-types"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "Compose the steps",
       "bindsTo": "BookingFlow",
       "columns": [
        "BookingFlow.name",
        "BookingFlow.flowTypeKey",
        "BookingFlow.isDefaultForType",
        "BookingFlow.isEnabled",
        "BookingFlow.steps",
        "BookingFlow.isValid"
       ],
       "operation": "getBookingFlow",
       "notes": "**The step list, in the venue's order.** Each step carries its mark: *Required* (locked on), *Optional* (a switch) or *Conditional* (a switch, with the condition in words, e.g. \"only when the tenant has more than one venue\"). Steps are dragged to reorder; **a drop that breaks a constraint is refused before it lands** (`validateBookingFlow` with the proposed `steps`), and the constraint is named (\"payment is always last\", \"the seat map comes after date and time\"). Each step opens its settings: the step's own (`BookingFlowStep.settings`, e.g. the tour languages or the room's hours) and, read-only with a link to CMS-016, the venue-wide settings it uses.",
       "provenance": "contract white-label.yaml GET /booking-flows/{bookingFlowId}"
      },
      {
       "kind": "detailPanel",
       "label": "This flow's settings",
       "bindsTo": "BookingFlowLevelSettings",
       "columns": [
        "BookingFlowLevelSettings.performanceReveal",
        "BookingFlowLevelSettings.signInAt",
        "BookingFlowLevelSettings.seatEventDateMode",
        "BookingFlowLevelSettings.extrasStep",
        "BookingFlowLevelSettings.quickTour",
        "BookingFlowLevelSettings.consentQuestionIds"
       ],
       "operation": "getBookingFlow",
       "notes": "**Moved here from Site Settings on 29 September (W12)**, because they belong to one flow: date, time then tickets or all at once (REV3-2); sign in after add-ons or at payment (REV3-3); a seated event's date inline or over the seat map (REV3-4, seated flows only); the extras step auto, always or never; the quick tour (REV3-20); the flow's consent questions (REV3-26).",
       "provenance": "contract white-label.yaml GET /booking-flows/{bookingFlowId}"
      },
      {
       "kind": "multiSelect",
       "label": "Consent questions this flow asks",
       "bindsTo": "BookingFlowLevelSettings.consentQuestionIds",
       "operation": "listConsentQuestions",
       "notes": "**The questions every booking in this flow asks, whatever the product** (rev 3 REV3-26), e.g. a water park's \"Are you able to swim?\". Options are the active questions from `listConsentQuestions`, written on CMS-018. A Help me choose answer may pre-fill one; the guest still confirms it (W4).",
       "provenance": "contract marketing-crm.yaml GET /consent-questions"
      },
      {
       "kind": "livePreview",
       "label": "Preview",
       "notes": "**The flow as a guest meets it, step by step, on web and on mobile**, redrawn on every change and drawn from the record in hand. Calls nothing and publishes nothing; guests keep the published flow (`getPublishedBookingFlow`, shown beside it for comparison) until the site is published.",
       "provenance": "authored 29 September, W12"
      },
      {
       "kind": "dataTable",
       "label": "Products and categories using this flow",
       "bindsTo": "Product",
       "columns": [
        "Product.name",
        "Product.kind",
        "Product.categoryId",
        "Product.bookingFlowId"
       ],
       "operation": "listProducts",
       "notes": "Assign the flow to a product (`updateProduct` `bookingFlowId`) or a category (`setProductCategories`, the category's `bookingFlowId`). A product naming no flow uses its category's, then the venue's default for its kind. Set up also on BO-007/BO-008 and BO-115.",
       "provenance": "contract catalogue.yaml GET /products"
      },
      {
       "kind": "banner",
       "label": "Why this flow cannot publish",
       "bindsTo": "BookingFlowValidation",
       "columns": [
        "BookingFlowValidation.valid",
        "BookingFlowValidation.problems"
       ],
       "operation": "validateBookingFlow",
       "notes": "A required step turned off, a step out of its allowed order, a condition that can never hold, each naming the step and the fix.",
       "provenance": "contract white-label.yaml POST /booking-flows/{bookingFlowId}/validate"
      },
      {
       "kind": "publishGate",
       "label": "What publishing changes",
       "impliedBy": "publishTenantConfig",
       "notes": "**Flows publish with the whole site**, never alone: the gate names every venue flow that changed since the last version and the products whose steps will change for guests, and says the rest of the draft (theme, pages, navigation) goes live with it. Refused while any enabled flow is invalid (`409`, `bookingFlowInvalid`). Needs `TENANT_PUBLISH`.",
       "provenance": "contract white-label.yaml POST /tenant-config/publish"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Add a flow",
       "operation": "createBookingFlowDefinition",
       "provenance": "contract white-label.yaml POST /venues/{venueId}/booking-flows"
      },
      {
       "kind": "secondaryButton",
       "label": "Save flow",
       "operation": "updateBookingFlowDefinition",
       "provenance": "contract white-label.yaml PATCH /booking-flows/{bookingFlowId}"
      },
      {
       "kind": "secondaryButton",
       "label": "Validate",
       "operation": "validateBookingFlow",
       "provenance": "contract white-label.yaml POST /booking-flows/{bookingFlowId}/validate"
      },
      {
       "kind": "secondaryButton",
       "label": "Assign to product",
       "operation": "updateProduct",
       "provenance": "contract catalogue.yaml PATCH /products/{productId}"
      },
      {
       "kind": "secondaryButton",
       "label": "Assign to category",
       "operation": "setProductCategories",
       "provenance": "contract catalogue.yaml PUT /product-categories"
      },
      {
       "kind": "secondaryButton",
       "label": "Publish site",
       "operation": "publishTenantConfig",
       "permission": "TENANT_PUBLISH",
       "provenance": "contract white-label.yaml POST /tenant-config/publish"
      },
      {
       "kind": "destructiveButton",
       "label": "Remove flow",
       "operation": "deleteBookingFlow",
       "notes": "Refused `409` while a product or category names the flow or it is the default for products on sale; the refusal names them and offers to reassign.",
       "provenance": "contract white-label.yaml DELETE /booking-flows/{bookingFlowId}"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The venue's flows and the flow-type catalogue, read by `listBookingFlows` and `listBookingFlowTypes`.",
   "error": "Could not load. Names which read failed and leaves the flows untouched.",
   "emptyFirstRun": "**No flows at this venue yet.** Guests book through each type's default order until one is picked. Offers the flow-type cards and, from the Site Builder, the preset's flows in one step.",
   "emptyNoResults": "The flow-type filter matched nothing and the venue's other flows are still there. Names the filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `TENANT_CONFIGURE`, which `listBookingFlows` requires, and names that permission. **Never an empty table** — that reads as *there are no flows*."
  },
  "apis": [
   {
    "operationId": "listBookingFlows",
    "contract": "white-label",
    "purpose": "The venue's flows in the draft",
    "trigger": "onLoad"
   },
   {
    "operationId": "listBookingFlowTypes",
    "contract": "white-label",
    "purpose": "The flow types to pick from, with their steps and order constraints",
    "trigger": "onLoad"
   },
   {
    "operationId": "getBookingFlow",
    "contract": "white-label",
    "purpose": "One flow with every step, to compose",
    "trigger": "onAction"
   },
   {
    "operationId": "getPublishedBookingFlow",
    "contract": "white-label",
    "purpose": "What guests book through now, beside the draft in the preview",
    "trigger": "onAction"
   },
   {
    "operationId": "createBookingFlowDefinition",
    "contract": "white-label",
    "purpose": "Pick a flow type for the venue",
    "trigger": "onAction",
    "invalidates": [
     "listBookingFlows"
    ]
   },
   {
    "operationId": "updateBookingFlowDefinition",
    "contract": "white-label",
    "purpose": "Save the step order, the optional steps and the flow's settings",
    "trigger": "onAction",
    "invalidates": [
     "listBookingFlows",
     "getBookingFlow"
    ]
   },
   {
    "operationId": "validateBookingFlow",
    "contract": "white-label",
    "purpose": "Check a proposed order before it is dropped, or the saved flow",
    "trigger": "onAction"
   },
   {
    "operationId": "deleteBookingFlow",
    "contract": "white-label",
    "purpose": "Remove a flow nothing uses",
    "trigger": "onAction",
    "invalidates": [
     "listBookingFlows"
    ]
   },
   {
    "operationId": "publishTenantConfig",
    "contract": "white-label",
    "purpose": "Publish the site, flows included",
    "trigger": "onAction"
   },
   {
    "operationId": "listConsentQuestions",
    "contract": "marketing-crm",
    "purpose": "The consent questions a flow can ask (rev 3 REV3-26)",
    "trigger": "onLoad"
   },
   {
    "operationId": "listProducts",
    "contract": "catalogue",
    "purpose": "The products a flow is assigned to",
    "trigger": "onAction"
   },
   {
    "operationId": "updateProduct",
    "contract": "catalogue",
    "purpose": "Assign the flow to a product (`bookingFlowId`)",
    "trigger": "onAction",
    "invalidates": [
     "listProducts"
    ]
   },
   {
    "operationId": "listProductCategories",
    "contract": "catalogue",
    "purpose": "The categories a flow can be assigned to",
    "trigger": "onAction"
   },
   {
    "operationId": "setProductCategories",
    "contract": "catalogue",
    "purpose": "Assign the flow to a category (`bookingFlowId`)",
    "trigger": "onAction",
    "invalidates": [
     "listProductCategories"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "venueId",
     "from": "session"
    },
    {
     "name": "bookingFlowId",
     "from": "CMS-102",
     "optional": true
    },
    {
     "name": "productId",
     "from": "navigation"
    }
   ],
   "coldEntry": "Resolves the venue from the session and opens on the flow list, or on the flow named in the link."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-103"
  },
  "apisNote": "Authored 29 September 2026 (P29 pass, W12, W6, W8) from impact.md section b.",
  "overlays": [
   {
    "id": "formCreateBookingFlowDefinition",
    "component": "modal",
    "trigger": "Add a flow",
    "body": "**Collects what `createBookingFlowDefinition` sends.** Required: `flowTypeKey` (from the cards), `name`. Optional: `isDefaultForType`, `steps` (left out, the type's defaults), `settings`. Dismissing sends nothing.",
    "bindsTo": "BookingFlow",
    "confirm": {
     "label": "Add flow",
     "operation": "createBookingFlowDefinition"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "flowTypeKey",
      "name",
      "isDefaultForType",
      "steps",
      "settings"
     ]
    },
    "provenance": "contract white-label.yaml POST /venues/{venueId}/booking-flows"
   },
   {
    "id": "confirmDeleteBookingFlow",
    "component": "confirmDialog",
    "trigger": "Remove flow",
    "body": "Names the flow and says guests keep it until the next publish. Refused `409` while products or categories name it, and names them.",
    "confirm": {
     "label": "Remove",
     "operation": "deleteBookingFlow"
    },
    "dismiss": {
     "label": "Keep it"
    },
    "provenance": "contract white-label.yaml DELETE /booking-flows/{bookingFlowId}"
   },
   {
    "id": "confirmPublishSite",
    "component": "confirmDialog",
    "trigger": "Publish site",
    "body": "**Names what goes live**: the changed flows and the products whose booking steps change, with the rest of the draft. Asks for the publish note `publishTenantConfig` requires.",
    "confirm": {
     "label": "Publish",
     "operation": "publishTenantConfig"
    },
    "dismiss": {
     "label": "Cancel"
    },
    "provenance": "contract white-label.yaml POST /tenant-config/publish"
   }
  ],
  "_platform": {
   "code": "P13",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue CMS",
   "name": "Venue CMS — White Label",
   "app": "venue-management-web",
   "offlineCapable": false,
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P08",
     "P12",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "CMS-104",
  "name": "App Build & Store Publishing",
  "module": "White Label",
  "requiresModule": "core",
  "wave": 1,
  "capability": "C00",
  "implementation": {
   "app": "venue-management-web",
   "route": "/white-label/app-publishing",
   "component": "apps/venue-management-web/src/routes/white-label/AppPublishing.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "CMS-102",
    "CMS-014"
   ],
   "exitTo": [
    "CMS-102",
    "CMS-004",
    "CMS-014"
   ],
   "inferred": false,
   "notes": "Reached from the Site Builder after the first publish, and from Publishing when a change is build-time.",
   "transitions": [
    {
     "to": "CMS-102",
     "trigger": "Back to the Site Builder",
     "provenance": "authored 29 September, M24-08",
     "back": true
    },
    {
     "to": "CMS-004",
     "trigger": "App icons and splash",
     "provenance": "authored 29 September, M24-08 (build-time assets)"
    },
    {
     "to": "CMS-014",
     "trigger": "Publish the configuration first",
     "provenance": "authored 29 September, M24-08 (a build is made from a published version)"
    }
   ]
  },
  "notes": "**Added 29 September for M24-08.** TICVAI never publishes a client's app under its own developer account: each client opens and owns its Apple Developer account (with a D-U-N-S number) and its Google Play account, builds its app here from the published configuration, and uploads it, or lets us submit it with its own API credential. The accounts are make-or-break client inputs (`setStoreAccounts`).",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listAppBuilds` reads the builds and `getAppBuild` reads one — list, select, act; the checklist sits above the list",
  "purpose": "Get the tenant's own app into the App Store and Google Play under the client's own accounts — checklist, store listing, request a build, download or submit it, follow its review — with a guide for the steps only the client can take.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "filters",
     "slot": "filters",
     "components": [
      {
       "kind": "detailPanel",
       "label": "Before the first build",
       "bindsTo": "StorePublishingChecklist",
       "columns": [
        "StorePublishingChecklist.items",
        "StorePublishingChecklist.accounts"
       ],
       "operation": "getStoreAccounts",
       "notes": "Apple D-U-N-S number, Apple Developer account, Google Play developer account (**the client's to open; we cannot open them for them**), store listing, app icons, a published configuration. Each open item says what to do next.",
       "provenance": "contract white-label.yaml GET /tenant-config/store-accounts"
      },
      {
       "kind": "selectField",
       "label": "Platform",
       "operation": "listAppBuilds",
       "notes": "Sends `?platform=`, iOS or Android.",
       "provenance": "contract white-label.yaml GET /tenant-config/app-builds"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Builds",
       "bindsTo": "AppBuild",
       "columns": [
        "AppBuild.platform",
        "AppBuild.versionName",
        "AppBuild.buildNumber",
        "AppBuild.configVersion",
        "AppBuild.status",
        "AppBuild.requestedAt",
        "AppBuild.finishedAt"
       ],
       "operation": "listAppBuilds",
       "provenance": "contract white-label.yaml GET /tenant-config/app-builds"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected build",
       "bindsTo": "AppBuild",
       "columns": [
        "AppBuild.status",
        "AppBuild.failureReason",
        "AppBuild.packageAssetRef",
        "AppBuild.releaseNotes",
        "AppBuild.submitToStore"
       ],
       "operation": "getAppBuild",
       "notes": "Download the signed package to upload it in App Store Connect or the Play Console; with a credential recorded, the store review status follows here (submitted, in review, approved, rejected, released).",
       "provenance": "contract white-label.yaml GET /tenant-config/app-builds/{appBuildId}"
      },
      {
       "kind": "assistantPanel",
       "label": "App publishing guide",
       "operation": "sendAiMessage",
       "notes": "**The in-platform guide M24-08 asks for**: how to get a D-U-N-S number, open each account, fill the listing and answer store review. Grounded on a store-publishing knowledge source, no tenant data. `unavailable` until the ai \"app publishing guide\" assistant profile exists; the checklist guidance works without it.",
       "provenance": "authored 29 September, M24-08"
      },
      {
       "kind": "publishGate",
       "label": "What a build and a submission do",
       "impliedBy": "requestAppBuild",
       "notes": "Names the configuration version built, the build-time changes it carries (icons, splash, fonts, wallet and payment integrations) and the account it is signed for; with **Submit to the store**, says it goes to the client's store review under the client's account. Needs `TENANT_PUBLISH`.",
       "provenance": "contract white-label.yaml POST /tenant-config/app-builds"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Request a build",
       "operation": "requestAppBuild",
       "permission": "TENANT_PUBLISH",
       "provenance": "contract white-label.yaml POST /tenant-config/app-builds"
      },
      {
       "kind": "secondaryButton",
       "label": "Save store accounts and listing",
       "operation": "setStoreAccounts",
       "provenance": "contract white-label.yaml PUT /tenant-config/store-accounts"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The checklist and the builds, read by `getStoreAccounts` and `listAppBuilds`.",
   "error": "Could not load. Names which read failed.",
   "emptyFirstRun": "**No build yet.** Shows the checklist first: nothing can be built until the client's store account for the platform is recorded and a version is published.",
   "emptyNoResults": "No build for the platform picked. Names it and offers the other.",
   "emptyNoAccess": "Shown when the caller lacks `TENANT_CONFIGURE`, which `listAppBuilds` requires, and names that permission."
  },
  "apis": [
   {
    "operationId": "getStoreAccounts",
    "contract": "white-label",
    "purpose": "The client's store accounts and the checklist",
    "trigger": "onLoad"
   },
   {
    "operationId": "setStoreAccounts",
    "contract": "white-label",
    "purpose": "Record the client's own Apple and Google accounts and the store listing",
    "trigger": "onAction",
    "invalidates": [
     "getStoreAccounts"
    ]
   },
   {
    "operationId": "listAppBuilds",
    "contract": "white-label",
    "purpose": "The builds and their store status",
    "trigger": "onLoad"
   },
   {
    "operationId": "getAppBuild",
    "contract": "white-label",
    "purpose": "One build, its package and its review status",
    "trigger": "onAction"
   },
   {
    "operationId": "requestAppBuild",
    "contract": "white-label",
    "purpose": "Build the app from a published version, for the client's account",
    "trigger": "onAction",
    "invalidates": [
     "listAppBuilds"
    ]
   },
   {
    "operationId": "createAiConversation",
    "contract": "ai",
    "purpose": "Open a conversation with the app publishing guide",
    "trigger": "onAction"
   },
   {
    "operationId": "sendAiMessage",
    "contract": "ai",
    "purpose": "Ask the app publishing guide a question",
    "trigger": "onAction"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "appBuildId",
     "from": "navigation",
     "optional": true
    },
    {
     "name": "conversationId",
     "from": "navigation"
    }
   ],
   "coldEntry": "Resolves the tenant from the session and opens on the checklist and the newest build."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-104"
  },
  "apisNote": "Authored 29 September 2026 (P29 pass, M24-08) from impact.json.",
  "overlays": [
   {
    "id": "formSetStoreAccounts",
    "component": "modal",
    "trigger": "Save store accounts and listing",
    "body": "**Collects what `setStoreAccounts` sends**: per store, `accountHolderName`, `developerAccountId`, `appIdentifier`, `dunsNumber` (Apple, nine digits), optional `apiCredentialSecretRef` and the `listing` (name, subtitle, description and keywords in every tenant language, category, support and privacy links, screenshots). Refused `400` for an Apple account without a D-U-N-S number. Dismissing sends nothing.",
    "bindsTo": "StoreAccount",
    "confirm": {
     "label": "Save",
     "operation": "setStoreAccounts"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "accounts"
     ]
    },
    "provenance": "contract white-label.yaml PUT /tenant-config/store-accounts"
   },
   {
    "id": "confirmRequestAppBuild",
    "component": "confirmDialog",
    "trigger": "Request a build",
    "body": "**Names the platform, the version built and the account it is signed for.** Optional release notes and Submit to the store (needs a recorded credential). Refused `409` with the reason when the account is missing, nothing is published, or a build is already running.",
    "confirm": {
     "label": "Build",
     "operation": "requestAppBuild"
    },
    "dismiss": {
     "label": "Cancel"
    },
    "provenance": "contract white-label.yaml POST /tenant-config/app-builds"
   }
  ],
  "_platform": {
   "code": "P13",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue CMS",
   "name": "Venue CMS — White Label",
   "app": "venue-management-web",
   "offlineCapable": false,
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P08",
     "P12",
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
 "createAiConversation": {
  "method": "POST",
  "path": "/conversations",
  "contract": "ai",
  "summary": "Open a conversation",
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
  "responds": "AiConversation"
 },
 "createBookingFlowDefinition": {
  "method": "POST",
  "path": "/venues/{venueId}/booking-flows",
  "contract": "white-label",
  "summary": "Pick a booking flow for a venue",
  "permission": "TENANT_CONFIGURE",
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
  "requestBody": "BookingFlow",
  "responds": "BookingFlow"
 },
 "deleteBookingFlow": {
  "method": "DELETE",
  "path": "/booking-flows/{bookingFlowId}",
  "contract": "white-label",
  "summary": "Remove a booking flow from a venue",
  "permission": "TENANT_CONFIGURE",
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
 "getAppBuild": {
  "method": "GET",
  "path": "/tenant-config/app-builds/{appBuildId}",
  "contract": "white-label",
  "summary": "One app build, with its package and store status",
  "permission": "TENANT_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "AppBuild"
 },
 "getBookingFlow": {
  "method": "GET",
  "path": "/booking-flows/{bookingFlowId}",
  "contract": "white-label",
  "summary": "Read one of a venue's booking flows, every step included",
  "permission": "TENANT_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "BookingFlow"
 },
 "getPublishedBookingFlow": {
  "method": "GET",
  "path": "/venues/{venueId}/booking-flow",
  "contract": "white-label",
  "summary": "The published booking flow a product or category books through",
  "permission": null,
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "productId",
    "in": "query",
    "required": false
   },
   {
    "name": "productCategoryId",
    "in": "query",
    "required": false
   },
   {
    "name": "flowTypeKey",
    "in": "query",
    "required": false
   }
  ],
  "requestBody": null,
  "responds": "BookingFlow"
 },
 "getSiteSetupProgress": {
  "method": "GET",
  "path": "/tenant-config/site-setup",
  "contract": "white-label",
  "summary": "Where the tenant is in the Site Builder",
  "permission": "TENANT_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "SiteSetupProgress"
 },
 "getStoreAccounts": {
  "method": "GET",
  "path": "/tenant-config/store-accounts",
  "contract": "white-label",
  "summary": "The client's store accounts and the publishing checklist",
  "permission": "TENANT_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "StorePublishingChecklist"
 },
 "getTenantAppStatus": {
  "method": "GET",
  "path": "/tenant-config/status",
  "contract": "white-label",
  "summary": "App status and recent changes",
  "permission": null,
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "TenantAppStatus"
 },
 "listAppBuilds": {
  "method": "GET",
  "path": "/tenant-config/app-builds",
  "contract": "white-label",
  "summary": "The tenant's app builds, newest first",
  "permission": "TENANT_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "platform",
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
 "listBookingFlowTypes": {
  "method": "GET",
  "path": "/booking-flow-types",
  "contract": "white-label",
  "summary": "The booking flow types a venue can pick from, with their steps",
  "permission": "TENANT_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "productKind",
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
 "listBookingFlows": {
  "method": "GET",
  "path": "/venues/{venueId}/booking-flows",
  "contract": "white-label",
  "summary": "A venue's booking flows, in the working draft",
  "permission": "TENANT_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "flowTypeKey",
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
 "listConsentQuestions": {
  "method": "GET",
  "path": "/consent-questions",
  "contract": "marketing-crm",
  "summary": "The consent questions a venue asks at booking",
  "permission": "GUEST_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "kind",
    "in": "query",
    "required": null
   },
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
 "listProductCategories": {
  "method": "GET",
  "path": "/product-categories",
  "contract": "catalogue",
  "summary": "The merchandise hierarchy — categories, brands, collections",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "ProductCategoryNode"
 },
 "listProducts": {
  "method": "GET",
  "path": "/products",
  "contract": "catalogue",
  "summary": "List products",
  "permission": "PRODUCT_VIEW",
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
    "name": "kind",
    "in": "query",
    "required": null
   },
   {
    "name": "isSellable",
    "in": "query",
    "required": null
   },
   {
    "name": "categoryId",
    "in": "query",
    "required": null
   },
   {
    "name": "segmentTag",
    "in": "query",
    "required": null
   },
   {
    "name": "guidedAnswerIds",
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
 "publishTenantConfig": {
  "method": "POST",
  "path": "/tenant-config/publish",
  "contract": "white-label",
  "summary": "Publish the working draft",
  "permission": "TENANT_PUBLISH",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "ConfigVersion"
 },
 "requestAppBuild": {
  "method": "POST",
  "path": "/tenant-config/app-builds",
  "contract": "white-label",
  "summary": "Build the branded app for a store",
  "permission": "TENANT_PUBLISH",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
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
 "sendAiMessage": {
  "method": "POST",
  "path": "/conversations/{conversationId}/messages",
  "contract": "ai",
  "summary": "Ask",
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
  "responds": "AiMessage"
 },
 "setProductCategories": {
  "method": "PUT",
  "path": "/product-categories",
  "contract": "catalogue",
  "summary": "Define the hierarchy, in the order a guest sees it",
  "permission": "PRODUCT_CONFIGURE",
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
  "responds": "ProductCategory"
 },
 "setSiteSetupProgress": {
  "method": "PUT",
  "path": "/tenant-config/site-setup",
  "contract": "white-label",
  "summary": "Save the Site Builder's progress",
  "permission": "TENANT_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "SiteSetupProgress",
  "responds": "SiteSetupProgress"
 },
 "setStoreAccounts": {
  "method": "PUT",
  "path": "/tenant-config/store-accounts",
  "contract": "white-label",
  "summary": "Record the client's own Apple and Google store accounts and listings",
  "permission": "TENANT_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "StorePublishingChecklist"
 },
 "updateBookingFlowDefinition": {
  "method": "PATCH",
  "path": "/booking-flows/{bookingFlowId}",
  "contract": "white-label",
  "summary": "Reorder a flow's steps, switch optional steps, change its settings",
  "permission": "TENANT_CONFIGURE",
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
  "responds": "BookingFlow"
 },
 "updateProduct": {
  "method": "PATCH",
  "path": "/products/{productId}",
  "contract": "catalogue",
  "summary": "Update a product",
  "permission": "PRODUCT_CONFIGURE",
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
  "requestBody": "UpdateProductRequest",
  "responds": "Product"
 },
 "validateBookingFlow": {
  "method": "POST",
  "path": "/booking-flows/{bookingFlowId}/validate",
  "contract": "white-label",
  "summary": "Check a flow against its type",
  "permission": "TENANT_CONFIGURE",
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
  "responds": "BookingFlowValidation"
 },
 "validateTenantConfig": {
  "method": "POST",
  "path": "/tenant-config/validate",
  "contract": "white-label",
  "summary": "Validate the working draft",
  "permission": "TENANT_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "ConfigValidationReport"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "AiConversation": {
  "type": "object",
  "x-ticvai-persistence": "ai.conversation",
  "required": [
   "id",
   "principalId",
   "module",
   "startedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "principalId": {
    "type": "string",
    "format": "uuid"
   },
   "scopePath": {
    "type": "string"
   },
   "module": {
    "$ref": "../shared/common.yaml#/components/schemas/ModuleKey"
   },
   "locale": {
    "type": "string"
   },
   "messageCount": {
    "type": "integer"
   },
   "startedAt": {
    "type": "string",
    "format": "date-time"
   },
   "lastMessageAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "AiMessage": {
  "type": "object",
  "x-ticvai-persistence": "ai.message",
  "required": [
   "id",
   "conversationId",
   "role",
   "content",
   "createdAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "conversationId": {
    "type": "string",
    "format": "uuid"
   },
   "role": {
    "type": "string",
    "enum": [
     "user",
     "assistant",
     "system"
    ]
   },
   "content": {
    "type": "string"
   },
   "sources": {
    "$ref": "#/components/schemas/AiSourceList"
   },
   "confidence": {
    "type": "number",
    "nullable": true,
    "description": "8.1.5, 8.3.67. **Nullable on purpose** — a provider that does not report confidence must yield null rather than an invented number, and an interface showing 0.9 because the code defaulted it is worse than showing nothing.\n"
   },
   "rationale": {
    "type": "string",
    "nullable": true,
    "description": "8.3.68, 8.3.69."
   },
   "proposedAction": {
    "allOf": [
     {
      "$ref": "#/components/schemas/ProposedAction"
     }
    ],
    "nullable": true,
    "description": "Present where the answer suggests a change. **A draft, never applied here.**"
   },
   "traceId": {
    "type": "string"
   },
   "provider": {
    "$ref": "#/components/schemas/AiProviderKind"
   },
   "model": {
    "type": "string"
   },
   "promptTokens": {
    "type": "integer"
   },
   "completionTokens": {
    "type": "integer"
   },
   "latencyMs": {
    "type": "integer"
   },
   "createdAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "AiProviderKind": {
  "type": "string",
  "enum": [
   "openai",
   "gemini",
   "anthropic",
   "azureOpenai",
   "localLlm",
   "openaiCompatible"
  ],
  "description": "`openaiCompatible` (added 29 September, AI design 3.3): a customer endpoint that speaks the OpenAI API, taken with no custom development (AIC-009). Any other protocol needs an adapter.\n"
 },
 "AiSourceList": {
  "type": "array",
  "x-ticvai-persistence-kind": "valueObject",
  "x-ticvai-persistence-column": "jsonb",
  "description": "**The sources an answer was grounded in, stored with the answer** (8.3.70). One `jsonb` column on the row that carries it — `ai.message.sources` and `ai.activity.sources` — because the grounding audit reads the list as it was when the answer was given, and a source is never queried on its own.\n",
  "items": {
   "$ref": "#/components/schemas/AiSource"
  }
 },
 "AppAvailability": {
  "type": "string",
  "description": "**The sold-out or closed signal (decided 28 September, audit R073).** `open` is the normal state. `soldOut` shows WEB-029's sold-out state across the app while browsing still works; `closed` shows the closed state (a weather closure, a private event). Neither refuses a request on its own: it is what the guest is told, and a sale is still refused by availability where it applies. Set with `setMaintenanceMode`.\n",
  "enum": [
   "open",
   "soldOut",
   "closed"
  ],
  "default": "open"
 },
 "AppBuild": {
  "x-ticvai-persistence": "whitelabel.app_build",
  "type": "object",
  "description": "**One build of the tenant's branded app (decided 24 September, M24-08).** Made from a published `ConfigVersion`, signed for the client's own store account.\n",
  "required": [
   "id",
   "platform",
   "configVersion",
   "status",
   "requestedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "platform": {
    "type": "string",
    "enum": [
     "ios",
     "android"
    ]
   },
   "configVersion": {
    "type": "string",
    "description": "The `ConfigVersion.version` built."
   },
   "storeAccountId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "versionName": {
    "type": "string",
    "readOnly": true,
    "description": "The marketing version, e.g. 1.4.0."
   },
   "buildNumber": {
    "type": "integer",
    "readOnly": true
   },
   "status": {
    "type": "string",
    "readOnly": true,
    "enum": [
     "queued",
     "building",
     "built",
     "failed",
     "submitted",
     "inReview",
     "approved",
     "rejected",
     "released"
    ],
    "description": "`queued` to `built` or `failed` is the build service's; from `submitted` on it is read from the store with the client's credential, or stays `built` when the client uploads by hand."
   },
   "failureReason": {
    "type": "string",
    "nullable": true,
    "readOnly": true
   },
   "packageAssetRef": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "description": "The signed .ipa or .aab in the `assets` library, for the client to download and upload."
   },
   "releaseNotes": {
    "$ref": "#/components/schemas/LocalisedText"
   },
   "submitToStore": {
    "type": "boolean",
    "default": false
   },
   "requestedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   },
   "requestedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "finishedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "The partition key (ADR-0005). Written at `tenant` scope."
   }
  }
 },
 "BookingFlow": {
  "x-ticvai-persistence": "whitelabel.booking_flow",
  "type": "object",
  "description": "**A venue's booking flow (decided 29 September, W12: operators pick their flows, see which steps are required, set their own order).** Made from a `BookingFlowType`; lives in the working draft and reaches guests with `publishTenantConfig`, which copies the venue's flows into the version's snapshot. A product or category names its flow (catalogue `bookingFlowId`); otherwise the venue's default for the type serving its kind applies.\n",
  "required": [
   "flowTypeKey",
   "name"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "venueId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "From the path of `createBookingFlowDefinition`."
   },
   "flowTypeKey": {
    "$ref": "#/components/schemas/BookingFlowTypeKey"
   },
   "name": {
    "type": "string",
    "maxLength": 80,
    "description": "Staff-facing, e.g. \"Day pass, date first\". Not shown to guests."
   },
   "isDefaultForType": {
    "type": "boolean",
    "default": false,
    "description": "At most one per venue and type; setting it takes it from the previous default."
   },
   "isEnabled": {
    "type": "boolean",
    "default": true,
    "description": "A disabled flow is kept and not published; products naming it fall back to the default."
   },
   "steps": {
    "type": "array",
    "maxItems": 30,
    "description": "Every step of the type, in the venue's order. Filled from the type when left out on create.",
    "items": {
     "$ref": "#/components/schemas/BookingFlowStep"
    }
   },
   "settings": {
    "$ref": "#/components/schemas/BookingFlowLevelSettings"
   },
   "isValid": {
    "type": "boolean",
    "readOnly": true,
    "x-ticvai-derived": "onWrite",
    "description": "Whether the flow passes `validateBookingFlow`; worked out in the same transaction as each write. `publishTenantConfig` refuses a draft holding an invalid enabled flow."
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "The partition key (ADR-0005). Written at `venue` scope."
   },
   "updatedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   }
  }
 },
 "BookingFlowLevelSettings": {
  "x-ticvai-persistence": "none — jsonb column on whitelabel.booking_flow",
  "type": "object",
  "description": "**The settings that belong to one flow, not to the venue (decided 29 September, W12).** Moved here from `BookingFlowSettings`, which keeps the venue-wide ones. Each keeps its rev 3 meaning and default. A field left out takes its default.\n",
  "properties": {
   "performanceReveal": {
    "type": "string",
    "enum": [
     "dateTimeTicket",
     "allAtOnce"
    ],
    "default": "dateTimeTicket",
    "description": "**Performance reveal (rev 3 REV3-2).** `dateTimeTicket` shows the times only once a date is picked and the tickets only once a time is picked; `allAtOnce` shows them together. Product-first (W8) is the step order of `experienceWorkshop`, not a value here.\n"
   },
   "signInAt": {
    "type": "string",
    "enum": [
     "afterAddOns",
     "atPayment"
    ],
    "default": "afterAddOns",
    "description": "**Where the guest is asked to sign in, or for a guest-checkout code (rev 3 REV3-3).** `afterAddOns` asks as the guest leaves the extras step; `atPayment` asks at payment. The basket is kept either way.\n"
   },
   "seatEventDateMode": {
    "type": "string",
    "enum": [
     "inlineStep",
     "popupOnSeatMap"
    ],
    "default": "inlineStep",
    "description": "**Date and time on a seated event (rev 3 REV3-4).** `inlineStep` asks for them before the seat map; `popupOnSeatMap` opens the seat map with a date and time pop-up. Read only by the seated flow types.\n"
   },
   "extrasStep": {
    "type": "string",
    "enum": [
     "auto",
     "always",
     "never"
    ],
    "default": "auto",
    "description": "`auto` shows the extras step only when the cart's products have add-ons; `never` is the same as turning the optional `extras` step off."
   },
   "quickTour": {
    "type": "boolean",
    "default": false,
    "description": "**Quick tour (rev 3 REV3-20).** A first visit gets a coach-mark tour of this flow's steps, replayable from a Quick tour button. Seen-state kept on the device only.\n"
   },
   "consentQuestionIds": {
    "type": "array",
    "maxItems": 10,
    "uniqueItems": true,
    "default": [],
    "description": "**The flow's own consent questions (rev 3 REV3-26).** Asked on every booking through this flow, together with those of each product in the cart, each question once. Each id names an active `ConsentQuestion` of the tenant in marketing-crm, or 400. A Help me choose answer may pre-fill one (`GuidedChoice` `consentPrefill`); the guest still confirms it.\n",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   }
  }
 },
 "BookingFlowStep": {
  "x-ticvai-persistence": "whitelabel.booking_flow_step",
  "type": "object",
  "description": "One step of a venue's flow, in the venue's order (decided 29 September, W12).",
  "required": [
   "stepKey",
   "enabled",
   "sortOrder"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "bookingFlowId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "stepKey": {
    "$ref": "#/components/schemas/BookingFlowStepKey"
   },
   "enabled": {
    "type": "boolean",
    "description": "A `required` step cannot be off; the flow saves and `isValid` turns false."
   },
   "sortOrder": {
    "type": "integer",
    "minimum": 0
   },
   "requirement": {
    "type": "string",
    "enum": [
     "required",
     "optional",
     "conditional"
    ],
    "readOnly": true,
    "x-ticvai-derived": "onRead",
    "description": "From the flow type, so the CMS can mark the step without a second read."
   },
   "settings": {
    "type": "object",
    "additionalProperties": true,
    "default": {},
    "description": "The step's own settings, by the names the type's `stepSettings` gives for this step (e.g. `languages` on `language`, `minHours` on `duration`). A name the type does not give is refused with 400."
   }
  }
 },
 "BookingFlowStepKey": {
  "type": "string",
  "description": "Every step a guest booking flow can hold (decided 29 September, W12). What each step does on WEB and MOB, and which screen draws it, is in the screen definitions of P01 and P02; which types carry which steps is `x-ticvai-system-catalogue` on `BookingFlowType`. `payment` is always last. Sign-in is not a step: it is asked where the flow's `signInAt` says.\n",
  "enum": [
   "location",
   "helpMeChoose",
   "product",
   "date",
   "time",
   "performance",
   "level",
   "language",
   "duration",
   "route",
   "partySize",
   "resourceMap",
   "resourceSize",
   "seatMap",
   "tickets",
   "attendees",
   "membershipPlan",
   "giftCardValue",
   "recipient",
   "consent",
   "extras",
   "review",
   "payment"
  ]
 },
 "BookingFlowType": {
  "x-ticvai-persistence": "none — system catalogue, shipped with the service and the same for every tenant",
  "type": "object",
  "description": "**A flow type from the system catalogue (decided 29 September, W12).** Read-only: a venue picks one (`createBookingFlowDefinition`) and orders its steps within `orderConstraints`. `requirement` is `required` (cannot be turned off), `optional` (the venue chooses) or `conditional` (shown to a guest only when `condition` holds; the venue may still turn it off where it is not also required by law or by a product, as the condition says). `settingsOwned` names the settings, venue-wide (`BookingFlowSettings`) or flow-level (`BookingFlowLevelSettings`), that the CMS shows beside the step; `stepSettings` are the step's own settings, kept in `BookingFlowStep.settings`.\n",
  "x-ticvai-system-catalogue": {
   "commonConstraints": [
    {
     "kind": "last",
     "stepKey": "payment"
    },
    {
     "kind": "first",
     "stepKey": "location"
    },
    {
     "kind": "before",
     "stepKey": "helpMeChoose",
     "otherStepKey": "tickets"
    },
    {
     "kind": "before",
     "stepKey": "helpMeChoose",
     "otherStepKey": "product"
    },
    {
     "kind": "before",
     "stepKey": "tickets",
     "otherStepKey": "extras"
    },
    {
     "kind": "before",
     "stepKey": "tickets",
     "otherStepKey": "consent"
    },
    {
     "kind": "before",
     "stepKey": "review",
     "otherStepKey": "payment"
    }
   ],
   "commonConditions": {
    "location": "the tenant has more than one active venue and `locationSwitcher` is on",
    "helpMeChoose": "the venue has a published `GuidedChoice`",
    "consent": "the flow's `consentQuestionIds` or a product in the cart asks a consent question (REV3-26); cannot be turned off while either does",
    "attendees": "a product in the cart asks attendee details"
   },
   "types": [
    {
     "key": "datedDayPass",
     "productKinds": [
      "admission",
      "datedAdmission"
     ],
     "steps": [
      {
       "stepKey": "location",
       "requirement": "conditional"
      },
      {
       "stepKey": "helpMeChoose",
       "requirement": "conditional"
      },
      {
       "stepKey": "date",
       "requirement": "required",
       "settingsOwned": [
        "dateStripDays",
        "performanceReveal"
       ]
      },
      {
       "stepKey": "tickets",
       "requirement": "required",
       "settingsOwned": [
        "ticketCategories",
        "ticketTags",
        "cardInfo",
        "cardLayout",
        "cardSize",
        "showInfoOnly"
       ]
      },
      {
       "stepKey": "consent",
       "requirement": "conditional",
       "settingsOwned": [
        "consentQuestionIds"
       ]
      },
      {
       "stepKey": "extras",
       "requirement": "optional",
       "settingsOwned": [
        "extrasStep",
        "quantitiesOnAddOns"
       ]
      },
      {
       "stepKey": "review",
       "requirement": "optional"
      },
      {
       "stepKey": "payment",
       "requirement": "required",
       "settingsOwned": [
        "signInAt"
       ]
      }
     ]
    },
    {
     "key": "timedEntry",
     "productKinds": [
      "timedAdmission"
     ],
     "steps": [
      {
       "stepKey": "location",
       "requirement": "conditional"
      },
      {
       "stepKey": "helpMeChoose",
       "requirement": "conditional"
      },
      {
       "stepKey": "date",
       "requirement": "required",
       "settingsOwned": [
        "dateStripDays",
        "performanceReveal"
       ]
      },
      {
       "stepKey": "time",
       "requirement": "required",
       "settingsOwned": [
        "timesPerPage",
        "dayPartFilter",
        "dayPartBoundaries",
        "performanceReveal"
       ]
      },
      {
       "stepKey": "tickets",
       "requirement": "required",
       "settingsOwned": [
        "ticketCategories",
        "ticketTags",
        "cardInfo",
        "cardLayout",
        "cardSize",
        "showInfoOnly"
       ]
      },
      {
       "stepKey": "consent",
       "requirement": "conditional",
       "settingsOwned": [
        "consentQuestionIds"
       ]
      },
      {
       "stepKey": "extras",
       "requirement": "optional",
       "settingsOwned": [
        "extrasStep",
        "quantitiesOnAddOns"
       ]
      },
      {
       "stepKey": "review",
       "requirement": "optional"
      },
      {
       "stepKey": "payment",
       "requirement": "required",
       "settingsOwned": [
        "signInAt"
       ]
      }
     ],
     "orderConstraints": [
      {
       "kind": "before",
       "stepKey": "date",
       "otherStepKey": "time"
      }
     ]
    },
    {
     "key": "openDated",
     "productKinds": [
      "openDated",
      "admission"
     ],
     "steps": [
      {
       "stepKey": "location",
       "requirement": "conditional"
      },
      {
       "stepKey": "helpMeChoose",
       "requirement": "conditional"
      },
      {
       "stepKey": "tickets",
       "requirement": "required",
       "settingsOwned": [
        "ticketCategories",
        "ticketTags",
        "cardInfo",
        "cardLayout",
        "cardSize",
        "showInfoOnly"
       ]
      },
      {
       "stepKey": "consent",
       "requirement": "conditional",
       "settingsOwned": [
        "consentQuestionIds"
       ]
      },
      {
       "stepKey": "extras",
       "requirement": "optional",
       "settingsOwned": [
        "extrasStep",
        "quantitiesOnAddOns"
       ]
      },
      {
       "stepKey": "review",
       "requirement": "optional"
      },
      {
       "stepKey": "payment",
       "requirement": "required",
       "settingsOwned": [
        "signInAt"
       ]
      }
     ]
    },
    {
     "key": "seatedFixedPerformance",
     "productKinds": [
      "seated"
     ],
     "steps": [
      {
       "stepKey": "location",
       "requirement": "conditional"
      },
      {
       "stepKey": "performance",
       "requirement": "required",
       "condition": "skipped for the guest when the event has one on-sale performance"
      },
      {
       "stepKey": "seatMap",
       "requirement": "required",
       "settingsOwned": [
        "seatPicker",
        "seatViewPosition",
        "seatTimeBar",
        "mapView"
       ]
      },
      {
       "stepKey": "tickets",
       "requirement": "conditional",
       "condition": "the seat's price category has more than one ticket type (adult or child)"
      },
      {
       "stepKey": "consent",
       "requirement": "conditional",
       "settingsOwned": [
        "consentQuestionIds"
       ]
      },
      {
       "stepKey": "extras",
       "requirement": "optional",
       "settingsOwned": [
        "extrasStep",
        "quantitiesOnAddOns"
       ]
      },
      {
       "stepKey": "review",
       "requirement": "optional"
      },
      {
       "stepKey": "payment",
       "requirement": "required",
       "settingsOwned": [
        "signInAt"
       ]
      }
     ],
     "orderConstraints": [
      {
       "kind": "before",
       "stepKey": "performance",
       "otherStepKey": "seatMap"
      }
     ]
    },
    {
     "key": "seatedDateTimeSeatMap",
     "productKinds": [
      "seated"
     ],
     "steps": [
      {
       "stepKey": "location",
       "requirement": "conditional"
      },
      {
       "stepKey": "date",
       "requirement": "required",
       "settingsOwned": [
        "dateStripDays",
        "seatEventDateMode"
       ]
      },
      {
       "stepKey": "time",
       "requirement": "required",
       "settingsOwned": [
        "timesPerPage",
        "dayPartFilter",
        "dayPartBoundaries",
        "seatEventDateMode"
       ]
      },
      {
       "stepKey": "seatMap",
       "requirement": "required",
       "settingsOwned": [
        "seatPicker",
        "seatViewPosition",
        "seatTimeBar",
        "mapView",
        "seatEventDateMode"
       ]
      },
      {
       "stepKey": "tickets",
       "requirement": "conditional",
       "condition": "the seat's price category has more than one ticket type"
      },
      {
       "stepKey": "consent",
       "requirement": "conditional",
       "settingsOwned": [
        "consentQuestionIds"
       ]
      },
      {
       "stepKey": "extras",
       "requirement": "optional",
       "settingsOwned": [
        "extrasStep",
        "quantitiesOnAddOns"
       ]
      },
      {
       "stepKey": "review",
       "requirement": "optional"
      },
      {
       "stepKey": "payment",
       "requirement": "required",
       "settingsOwned": [
        "signInAt"
       ]
      }
     ],
     "orderConstraints": [
      {
       "kind": "before",
       "stepKey": "date",
       "otherStepKey": "time"
      },
      {
       "kind": "before",
       "stepKey": "time",
       "otherStepKey": "seatMap"
      }
     ]
    },
    {
     "key": "experienceWorkshop",
     "productKinds": [
      "timedAdmission",
      "admission"
     ],
     "steps": [
      {
       "stepKey": "location",
       "requirement": "conditional"
      },
      {
       "stepKey": "helpMeChoose",
       "requirement": "conditional"
      },
      {
       "stepKey": "product",
       "requirement": "required",
       "settingsOwned": [
        "cardLayout",
        "cardSize",
        "cardInfo",
        "showInfoOnly"
       ]
      },
      {
       "stepKey": "date",
       "requirement": "required",
       "settingsOwned": [
        "dateStripDays",
        "performanceReveal"
       ]
      },
      {
       "stepKey": "time",
       "requirement": "required",
       "settingsOwned": [
        "timesPerPage",
        "dayPartFilter",
        "dayPartBoundaries"
       ]
      },
      {
       "stepKey": "tickets",
       "requirement": "required",
       "settingsOwned": [
        "ticketCategories",
        "ticketTags"
       ]
      },
      {
       "stepKey": "attendees",
       "requirement": "conditional"
      },
      {
       "stepKey": "consent",
       "requirement": "conditional",
       "settingsOwned": [
        "consentQuestionIds"
       ]
      },
      {
       "stepKey": "extras",
       "requirement": "optional",
       "settingsOwned": [
        "extrasStep",
        "quantitiesOnAddOns"
       ]
      },
      {
       "stepKey": "review",
       "requirement": "optional"
      },
      {
       "stepKey": "payment",
       "requirement": "required",
       "settingsOwned": [
        "signInAt"
       ]
      }
     ],
     "orderConstraints": [
      {
       "kind": "before",
       "stepKey": "product",
       "otherStepKey": "date"
      },
      {
       "kind": "before",
       "stepKey": "date",
       "otherStepKey": "time"
      }
     ]
    },
    {
     "key": "surfSession",
     "productKinds": [
      "timedAdmission",
      "rental"
     ],
     "steps": [
      {
       "stepKey": "location",
       "requirement": "conditional"
      },
      {
       "stepKey": "date",
       "requirement": "required",
       "settingsOwned": [
        "dateStripDays"
       ]
      },
      {
       "stepKey": "time",
       "requirement": "required",
       "settingsOwned": [
        "timesPerPage",
        "dayPartFilter",
        "dayPartBoundaries"
       ]
      },
      {
       "stepKey": "level",
       "requirement": "required",
       "stepSettings": [
        {
         "name": "levels",
         "type": "string[]",
         "note": "level tags offered",
         "from the products' segmentTags": null
        }
       ]
      },
      {
       "stepKey": "tickets",
       "requirement": "required",
       "settingsOwned": [
        "ticketTags",
        "cardInfo"
       ]
      },
      {
       "stepKey": "consent",
       "requirement": "conditional",
       "settingsOwned": [
        "consentQuestionIds"
       ]
      },
      {
       "stepKey": "extras",
       "requirement": "optional",
       "settingsOwned": [
        "extrasStep",
        "quantitiesOnAddOns"
       ]
      },
      {
       "stepKey": "review",
       "requirement": "optional"
      },
      {
       "stepKey": "payment",
       "requirement": "required",
       "settingsOwned": [
        "signInAt"
       ]
      }
     ],
     "orderConstraints": [
      {
       "kind": "before",
       "stepKey": "date",
       "otherStepKey": "time"
      },
      {
       "kind": "before",
       "stepKey": "time",
       "otherStepKey": "level"
      }
     ]
    },
    {
     "key": "meetingRoomHourly",
     "productKinds": [
      "rental"
     ],
     "steps": [
      {
       "stepKey": "location",
       "requirement": "conditional"
      },
      {
       "stepKey": "date",
       "requirement": "required",
       "settingsOwned": [
        "dateStripDays"
       ]
      },
      {
       "stepKey": "time",
       "requirement": "required",
       "settingsOwned": [
        "timesPerPage",
        "dayPartFilter",
        "dayPartBoundaries"
       ]
      },
      {
       "stepKey": "duration",
       "requirement": "required",
       "stepSettings": [
        {
         "name": "minHours",
         "type": "integer",
         "default": 1
        },
        {
         "name": "maxHours",
         "type": "integer",
         "default": 8
        },
        {
         "name": "stepMinutes",
         "type": "integer",
         "default": 60
        }
       ]
      },
      {
       "stepKey": "partySize",
       "requirement": "optional",
       "stepSettings": [
        {
         "name": "minGuests",
         "type": "integer",
         "default": 1
        },
        {
         "name": "maxGuests",
         "type": "integer"
        }
       ]
      },
      {
       "stepKey": "extras",
       "requirement": "optional",
       "settingsOwned": [
        "extrasStep",
        "quantitiesOnAddOns"
       ]
      },
      {
       "stepKey": "review",
       "requirement": "optional"
      },
      {
       "stepKey": "payment",
       "requirement": "required",
       "settingsOwned": [
        "signInAt"
       ]
      }
     ],
     "orderConstraints": [
      {
       "kind": "before",
       "stepKey": "date",
       "otherStepKey": "time"
      },
      {
       "kind": "before",
       "stepKey": "time",
       "otherStepKey": "duration"
      }
     ]
    },
    {
     "key": "cabanaMap",
     "productKinds": [
      "rental"
     ],
     "steps": [
      {
       "stepKey": "location",
       "requirement": "conditional"
      },
      {
       "stepKey": "date",
       "requirement": "required",
       "settingsOwned": [
        "dateStripDays"
       ]
      },
      {
       "stepKey": "resourceMap",
       "requirement": "required",
       "condition": "the venue's resource selection policy lets the guest choose (resources setResourceSelectionPolicy guestMayChoose; REV3-15)",
       "settingsOwned": [
        "mapView"
       ]
      },
      {
       "stepKey": "consent",
       "requirement": "conditional",
       "settingsOwned": [
        "consentQuestionIds"
       ]
      },
      {
       "stepKey": "extras",
       "requirement": "optional",
       "settingsOwned": [
        "extrasStep",
        "quantitiesOnAddOns"
       ]
      },
      {
       "stepKey": "review",
       "requirement": "optional"
      },
      {
       "stepKey": "payment",
       "requirement": "required",
       "settingsOwned": [
        "signInAt"
       ]
      }
     ],
     "orderConstraints": [
      {
       "kind": "before",
       "stepKey": "date",
       "otherStepKey": "resourceMap"
      }
     ]
    },
    {
     "key": "cabanaBySize",
     "productKinds": [
      "rental"
     ],
     "steps": [
      {
       "stepKey": "location",
       "requirement": "conditional"
      },
      {
       "stepKey": "date",
       "requirement": "required",
       "settingsOwned": [
        "dateStripDays"
       ]
      },
      {
       "stepKey": "partySize",
       "requirement": "required",
       "stepSettings": [
        {
         "name": "minGuests",
         "type": "integer",
         "default": 1
        },
        {
         "name": "maxGuests",
         "type": "integer"
        }
       ]
      },
      {
       "stepKey": "resourceSize",
       "requirement": "required",
       "note": "the server assigns a unit of the chosen size"
      },
      {
       "stepKey": "consent",
       "requirement": "conditional",
       "settingsOwned": [
        "consentQuestionIds"
       ]
      },
      {
       "stepKey": "extras",
       "requirement": "optional",
       "settingsOwned": [
        "extrasStep",
        "quantitiesOnAddOns"
       ]
      },
      {
       "stepKey": "review",
       "requirement": "optional"
      },
      {
       "stepKey": "payment",
       "requirement": "required",
       "settingsOwned": [
        "signInAt"
       ]
      }
     ],
     "orderConstraints": [
      {
       "kind": "before",
       "stepKey": "date",
       "otherStepKey": "resourceSize"
      },
      {
       "kind": "before",
       "stepKey": "partySize",
       "otherStepKey": "resourceSize"
      }
     ]
    },
    {
     "key": "guidedTourByLanguage",
     "productKinds": [
      "timedAdmission"
     ],
     "steps": [
      {
       "stepKey": "location",
       "requirement": "conditional"
      },
      {
       "stepKey": "date",
       "requirement": "required",
       "settingsOwned": [
        "dateStripDays"
       ]
      },
      {
       "stepKey": "language",
       "requirement": "required",
       "stepSettings": [
        {
         "name": "languages",
         "type": "string[]",
         "note": "ISO 639-1 codes the tours run in"
        }
       ]
      },
      {
       "stepKey": "time",
       "requirement": "required",
       "settingsOwned": [
        "timesPerPage",
        "dayPartFilter",
        "dayPartBoundaries"
       ]
      },
      {
       "stepKey": "tickets",
       "requirement": "required",
       "settingsOwned": [
        "ticketCategories",
        "ticketTags"
       ]
      },
      {
       "stepKey": "extras",
       "requirement": "optional",
       "settingsOwned": [
        "extrasStep",
        "quantitiesOnAddOns"
       ]
      },
      {
       "stepKey": "review",
       "requirement": "optional"
      },
      {
       "stepKey": "payment",
       "requirement": "required",
       "settingsOwned": [
        "signInAt"
       ]
      }
     ],
     "orderConstraints": [
      {
       "kind": "before",
       "stepKey": "date",
       "otherStepKey": "time"
      },
      {
       "kind": "before",
       "stepKey": "language",
       "otherStepKey": "time"
      }
     ]
    },
    {
     "key": "transport",
     "productKinds": [
      "admission",
      "timedAdmission"
     ],
     "steps": [
      {
       "stepKey": "route",
       "requirement": "required"
      },
      {
       "stepKey": "date",
       "requirement": "required",
       "settingsOwned": [
        "dateStripDays"
       ]
      },
      {
       "stepKey": "time",
       "requirement": "required",
       "settingsOwned": [
        "timesPerPage",
        "dayPartFilter"
       ]
      },
      {
       "stepKey": "tickets",
       "requirement": "required",
       "settingsOwned": [
        "ticketCategories"
       ]
      },
      {
       "stepKey": "extras",
       "requirement": "optional",
       "settingsOwned": [
        "extrasStep"
       ]
      },
      {
       "stepKey": "review",
       "requirement": "optional"
      },
      {
       "stepKey": "payment",
       "requirement": "required",
       "settingsOwned": [
        "signInAt"
       ]
      }
     ],
     "orderConstraints": [
      {
       "kind": "before",
       "stepKey": "route",
       "otherStepKey": "time"
      },
      {
       "kind": "before",
       "stepKey": "date",
       "otherStepKey": "time"
      }
     ]
    },
    {
     "key": "tableReservation",
     "productKinds": [
      "fnb"
     ],
     "steps": [
      {
       "stepKey": "location",
       "requirement": "conditional"
      },
      {
       "stepKey": "date",
       "requirement": "required",
       "settingsOwned": [
        "dateStripDays"
       ]
      },
      {
       "stepKey": "partySize",
       "requirement": "required",
       "stepSettings": [
        {
         "name": "minGuests",
         "type": "integer",
         "default": 1
        },
        {
         "name": "maxGuests",
         "type": "integer",
         "default": 12
        }
       ]
      },
      {
       "stepKey": "time",
       "requirement": "required",
       "settingsOwned": [
        "timesPerPage",
        "dayPartFilter",
        "dayPartBoundaries"
       ]
      },
      {
       "stepKey": "extras",
       "requirement": "optional",
       "note": "pre-order",
       "settingsOwned": [
        "extrasStep"
       ]
      },
      {
       "stepKey": "review",
       "requirement": "optional"
      },
      {
       "stepKey": "payment",
       "requirement": "conditional",
       "condition": "the venue takes a deposit or pre-order for the table",
       "settingsOwned": [
        "signInAt"
       ]
      }
     ],
     "orderConstraints": [
      {
       "kind": "before",
       "stepKey": "date",
       "otherStepKey": "time"
      },
      {
       "kind": "before",
       "stepKey": "partySize",
       "otherStepKey": "time"
      }
     ]
    },
    {
     "key": "membership",
     "productKinds": [
      "membership"
     ],
     "steps": [
      {
       "stepKey": "membershipPlan",
       "requirement": "required"
      },
      {
       "stepKey": "attendees",
       "requirement": "required",
       "note": "each member's details"
      },
      {
       "stepKey": "consent",
       "requirement": "conditional",
       "settingsOwned": [
        "consentQuestionIds"
       ]
      },
      {
       "stepKey": "review",
       "requirement": "optional"
      },
      {
       "stepKey": "payment",
       "requirement": "required",
       "settingsOwned": [
        "signInAt"
       ]
      }
     ],
     "orderConstraints": [
      {
       "kind": "before",
       "stepKey": "membershipPlan",
       "otherStepKey": "attendees"
      }
     ]
    },
    {
     "key": "giftCard",
     "productKinds": [
      "giftCard"
     ],
     "steps": [
      {
       "stepKey": "giftCardValue",
       "requirement": "required"
      },
      {
       "stepKey": "recipient",
       "requirement": "required"
      },
      {
       "stepKey": "review",
       "requirement": "optional"
      },
      {
       "stepKey": "payment",
       "requirement": "required",
       "settingsOwned": [
        "signInAt"
       ]
      }
     ]
    },
    {
     "key": "multiLocation",
     "productKinds": [
      "admission",
      "timedAdmission",
      "datedAdmission"
     ],
     "steps": [
      {
       "stepKey": "location",
       "requirement": "required",
       "settingsOwned": [
        "locationSwitcher"
       ]
      },
      {
       "stepKey": "helpMeChoose",
       "requirement": "conditional"
      },
      {
       "stepKey": "product",
       "requirement": "required",
       "settingsOwned": [
        "cardLayout",
        "cardSize",
        "cardInfo"
       ]
      },
      {
       "stepKey": "date",
       "requirement": "conditional",
       "condition": "the product is dated or timed",
       "settingsOwned": [
        "dateStripDays",
        "performanceReveal"
       ]
      },
      {
       "stepKey": "time",
       "requirement": "conditional",
       "condition": "the product is timed",
       "settingsOwned": [
        "timesPerPage",
        "dayPartFilter",
        "dayPartBoundaries"
       ]
      },
      {
       "stepKey": "tickets",
       "requirement": "required",
       "settingsOwned": [
        "ticketCategories",
        "ticketTags"
       ]
      },
      {
       "stepKey": "consent",
       "requirement": "conditional",
       "settingsOwned": [
        "consentQuestionIds"
       ]
      },
      {
       "stepKey": "extras",
       "requirement": "optional",
       "settingsOwned": [
        "extrasStep",
        "quantitiesOnAddOns"
       ]
      },
      {
       "stepKey": "review",
       "requirement": "optional"
      },
      {
       "stepKey": "payment",
       "requirement": "required",
       "settingsOwned": [
        "signInAt"
       ]
      }
     ],
     "orderConstraints": [
      {
       "kind": "before",
       "stepKey": "location",
       "otherStepKey": "product"
      },
      {
       "kind": "before",
       "stepKey": "date",
       "otherStepKey": "time"
      }
     ]
    }
   ]
  },
  "required": [
   "key",
   "name",
   "productKinds",
   "steps",
   "orderConstraints"
  ],
  "properties": {
   "key": {
    "$ref": "#/components/schemas/BookingFlowTypeKey"
   },
   "name": {
    "$ref": "#/components/schemas/LocalisedText"
   },
   "description": {
    "$ref": "#/components/schemas/LocalisedText"
   },
   "productKinds": {
    "type": "array",
    "description": "The catalogue `ProductKind` values this type books. A venue's default flow for a type serves every product of these kinds that names no flow of its own.",
    "items": {
     "type": "string"
    }
   },
   "steps": {
    "type": "array",
    "description": "In the type's default order.",
    "items": {
     "type": "object",
     "required": [
      "stepKey",
      "requirement",
      "defaultSortOrder"
     ],
     "properties": {
      "stepKey": {
       "$ref": "#/components/schemas/BookingFlowStepKey"
      },
      "requirement": {
       "type": "string",
       "enum": [
        "required",
        "optional",
        "conditional"
       ]
      },
      "condition": {
       "allOf": [
        {
         "$ref": "#/components/schemas/LocalisedText"
        }
       ],
       "nullable": true,
       "description": "For `conditional`, when a guest meets the step."
      },
      "defaultEnabled": {
       "type": "boolean",
       "default": true
      },
      "defaultSortOrder": {
       "type": "integer",
       "minimum": 0
      },
      "settingsOwned": {
       "type": "array",
       "description": "Names of `BookingFlowSettings` (venue-wide) or `BookingFlowLevelSettings` (this flow) fields shown beside the step.",
       "items": {
        "type": "string"
       }
      },
      "stepSettings": {
       "type": "array",
       "description": "The step's own settings, kept in `BookingFlowStep.settings`.",
       "items": {
        "type": "object",
        "required": [
         "name",
         "type"
        ],
        "properties": {
         "name": {
          "type": "string"
         },
         "type": {
          "type": "string"
         },
         "default": {
          "description": "The value when the venue sets none."
         }
        }
       }
      }
     }
    }
   },
   "orderConstraints": {
    "type": "array",
    "description": "`first` and `last` pin a step; `before` puts `stepKey` somewhere ahead of `otherStepKey`. The common constraints (payment last, location first, Help me choose before the products) apply to every type as well as these.",
    "items": {
     "type": "object",
     "required": [
      "kind",
      "stepKey"
     ],
     "properties": {
      "kind": {
       "type": "string",
       "enum": [
        "first",
        "last",
        "before"
       ]
      },
      "stepKey": {
       "$ref": "#/components/schemas/BookingFlowStepKey"
      },
      "otherStepKey": {
       "allOf": [
        {
         "$ref": "#/components/schemas/BookingFlowStepKey"
        }
       ],
       "nullable": true,
       "description": "Required when `kind` is `before`."
      }
     }
    }
   }
  }
 },
 "BookingFlowTypeKey": {
  "type": "string",
  "description": "**The flow types the system catalogue offers (decided 29 September, W12; impact.md b).** `seatedFixedPerformance` and `seatedDateTimeSeatMap` are the two seated flows; `cabanaMap` and `cabanaBySize` are the two cabana flows (W6); `experienceWorkshop` puts the product before the date (W8); `multiLocation` opens on the location switcher.\n",
  "enum": [
   "datedDayPass",
   "timedEntry",
   "openDated",
   "seatedFixedPerformance",
   "seatedDateTimeSeatMap",
   "experienceWorkshop",
   "surfSession",
   "meetingRoomHourly",
   "cabanaMap",
   "cabanaBySize",
   "guidedTourByLanguage",
   "transport",
   "tableReservation",
   "membership",
   "giftCard",
   "multiLocation"
  ]
 },
 "BookingFlowValidation": {
  "x-ticvai-persistence": "none — computed",
  "type": "object",
  "required": [
   "valid",
   "problems"
  ],
  "properties": {
   "valid": {
    "type": "boolean"
   },
   "problems": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "kind",
      "stepKey",
      "message"
     ],
     "properties": {
      "kind": {
       "type": "string",
       "enum": [
        "requiredStepDisabled",
        "orderConstraintBroken",
        "conditionNeverHolds",
        "stepNotInType",
        "duplicateStep",
        "unknownStepSetting"
       ]
      },
      "stepKey": {
       "$ref": "#/components/schemas/BookingFlowStepKey"
      },
      "otherStepKey": {
       "allOf": [
        {
         "$ref": "#/components/schemas/BookingFlowStepKey"
        }
       ],
       "nullable": true,
       "description": "For `orderConstraintBroken`, the step it must come before or after."
      },
      "message": {
       "type": "string"
      }
     }
    }
   }
  }
 },
 "Channel": {
  "type": "string",
  "enum": [
   "pos",
   "kiosk",
   "web",
   "mobile",
   "b2b",
   "ota",
   "callCentre"
  ]
 },
 "ConfigFindingKind": {
  "type": "string",
  "enum": [
   "missingTranslation",
   "navigationTargetsDisabledModule",
   "homepageReferencesMissingContent",
   "contrastFailure",
   "missingRequiredAsset",
   "policyVersionMissing",
   "noVisibleNavigationItems",
   "unlicensedModuleEnabled",
   "arabicFontMissing",
   "bookingFlowInvalid",
   "bookingFlowMissing"
  ]
 },
 "ConfigValidationReport": {
  "x-ticvai-persistence": "none — computed",
  "type": "object",
  "required": [
   "passed",
   "errorCount",
   "warningCount",
   "findings"
  ],
  "properties": {
   "passed": {
    "type": "boolean"
   },
   "errorCount": {
    "type": "integer"
   },
   "warningCount": {
    "type": "integer"
   },
   "findings": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "kind",
      "severity",
      "message"
     ],
     "properties": {
      "kind": {
       "$ref": "#/components/schemas/ConfigFindingKind"
      },
      "severity": {
       "type": "string",
       "enum": [
        "error",
        "warning"
       ]
      },
      "message": {
       "type": "string"
      },
      "area": {
       "type": "string"
      },
      "reference": {
       "type": "string",
       "nullable": true
      }
     }
    }
   }
  }
 },
 "ConfigVersion": {
  "x-ticvai-persistence": "whitelabel.config_version",
  "type": "object",
  "required": [
   "version",
   "publishedAt",
   "publishedByPrincipalId",
   "note",
   "isCurrent"
  ],
  "properties": {
   "version": {
    "type": "string"
   },
   "publishedAt": {
    "type": "string",
    "format": "date-time"
   },
   "publishedByPrincipalId": {
    "type": "string",
    "format": "uuid"
   },
   "publishedByName": {
    "type": "string"
   },
   "note": {
    "type": "string"
   },
   "isCurrent": {
    "type": "boolean"
   },
   "scheduledFor": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "contentHash": {
    "type": "string"
   },
   "pendingBuildTimeChanges": {
    "type": "array",
    "description": "Changes in this version that will not reach guests until the next store release. Surfaced at publish so nobody expects a new icon tomorrow.\n",
    "items": {
     "type": "object",
     "properties": {
      "area": {
       "type": "string"
      },
      "description": {
       "type": "string"
      },
      "platforms": {
       "type": "array",
       "items": {
        "type": "string",
        "enum": [
         "ios",
         "android",
         "web"
        ]
       }
      }
     }
    }
   },
   "snapshot": {
    "type": "object",
    "additionalProperties": true,
    "readOnly": true,
    "description": "**What this version contained.** The working draft exactly as published, in the shape `getTenantConfig` returns (`TenantConfig`) — so `restoreConfigVersion` has something to copy back and `diffConfigVersion` something to compare. Deliberately an open object here: its shape is `TenantConfig`, and a `$ref` would make it a key to a `tenant_config` row rather than a copy. Written once by `publishTenantConfig` and never changed. Left out of `listConfigVersions` items; a version's content is read with `getTenantConfig?version=`.\n"
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `tenant` scope.**"
   }
  }
 },
 "ConsentQuestion": {
  "type": "object",
  "x-ticvai-persistence": "marketing.consent_question + marketing.consent_question_version",
  "description": "**A venue-defined consent question asked at booking** (decided 29 September, rev 3 REV3-26). Each version's text is kept in `consent_question_version`, so an answer always points at the exact words the guest saw. Attached to products by the catalogue and to booking flows by the white-label flow configuration; one or several per flow, as the venue chooses.\n",
  "required": [
   "id",
   "kind",
   "text",
   "version",
   "scope",
   "required",
   "blockingAnswer",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
    "readOnly": true
   },
   "kind": {
    "$ref": "#/components/schemas/ConsentQuestionKind"
   },
   "text": {
    "allOf": [
     {
      "$ref": "#/components/schemas/LocalisedText"
     }
    ],
    "description": "The question as the guest reads it, per locale."
   },
   "helpText": {
    "allOf": [
     {
      "$ref": "#/components/schemas/LocalisedText"
     }
    ],
    "nullable": true
   },
   "version": {
    "type": "integer",
    "minimum": 1,
    "readOnly": true,
    "description": "Raised by one each time the question changes (`updateConsentQuestion`)."
   },
   "scope": {
    "type": "string",
    "enum": [
     "perPerson",
     "perBooking"
    ],
    "default": "perPerson",
    "description": "Asked for each declared person, or once for the whole booking."
   },
   "required": {
    "type": "boolean",
    "default": true,
    "description": "Checkout waits until it is answered (`orders.checkoutCart` 422 `consentRequired`)."
   },
   "blockingAnswer": {
    "type": "string",
    "enum": [
     "yes",
     "no",
     "none"
    ],
    "default": "none",
    "description": "The answer that stops the booking, for the person or the booking it covers. `none` records the answer and blocks nothing."
   },
   "status": {
    "type": "string",
    "enum": [
     "active",
     "retired"
    ],
    "default": "active"
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005). Operations write it at `venue` scope."
   },
   "updatedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   }
  }
 },
 "ConsentQuestionKind": {
  "type": "string",
  "description": "What the question is about (decided 29 September, rev 3 REV3-26). `swim` feeds the derived `confidentSwimmer` on the order line; the others are recorded and checked as the venue set them.",
  "enum": [
   "swim",
   "scuba",
   "risk",
   "custom"
  ]
 },
 "GuestListing": {
  "type": "string",
  "enum": [
   "bookable",
   "infoOnly",
   "hidden"
  ],
  "default": "bookable",
  "description": "**How a product appears to a guest** (decided 29 September, rev 3 REV3-14). `bookable`: listed and searched while it is on sale, and added to the basket. `infoOnly`: listed and searched with its details, photo and `notBookableLabel` whether or not it is on sale, and **never added to a basket** (`addCartLine` refuses it with `409`); the screen opens its details instead. `hidden`: never listed or searched for a guest, and reachable only where a staff channel sells it. Independent of `isSellable`, which says whether a channel may sell it at all.\n"
 },
 "LocalisedText": {
  "x-ticvai-persistence": "none — jsonb column",
  "type": "object",
  "additionalProperties": {
   "type": "string"
  }
 },
 "MinimumAppVersion": {
  "x-ticvai-persistence": "none — embedded in tenant_config",
  "type": "object",
  "nullable": true,
  "description": "**The oldest guest app build still allowed to run (decided 28 September, audit R073).** A guest app whose own version is below the one for its platform shows the forced-upgrade screen (GST-047) and nothing else. Null, or a platform left null, forces nothing. Live at once through `setMaintenanceMode`, because an upgrade that must wait for a publish is not forced.\n",
  "properties": {
   "ios": {
    "type": "string",
    "nullable": true,
    "pattern": "^\\d+\\.\\d+\\.\\d+$"
   },
   "android": {
    "type": "string",
    "nullable": true,
    "pattern": "^\\d+\\.\\d+\\.\\d+$"
   }
  }
 },
 "ModuleKey": {
  "$ref": "../shared/common.yaml#/components/schemas/ModuleKey"
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
 "Product": {
  "x-ticvai-persistence": "catalogue.product",
  "type": "object",
  "required": [
   "id",
   "code",
   "name",
   "kind",
   "venueId",
   "scopePath",
   "isSellable",
   "hasVariants"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "code": {
    "type": "string",
    "maxLength": 64
   },
   "familyKey": {
    "type": "string",
    "maxLength": 64,
    "pattern": "^[A-Za-z0-9_-]+$",
    "nullable": true,
    "x-ticvai-unique": "venue",
    "description": "**The same product at another location** (decided 29 September, rev 3 REV3-18). Optional. A tenant that sells one attraction at several venues gives each venue's product the same key, e.g. `aquarium-entry`; the key names the family across the tenant and each venue has at most one product in it, so a second product at the same venue with the key is refused with `409 duplicate-code`. **What it is for:** when a guest changes location on the booking screen (the 'Booking at' switcher, `BookingFlowConfig.locationSwitcher`), lines whose product shares a `familyKey` with a product at the new venue are carried over to that product, with times and prices refreshed; every other line is cleared. Null means the product belongs to no family and its lines always clear on a switch. Compared case-insensitively, like `code`.\n"
   },
   "name": {
    "type": "string",
    "maxLength": 200
   },
   "description": {
    "type": "string"
   },
   "kind": {
    "$ref": "#/components/schemas/ProductKind"
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "scopePath": {
    "type": "string"
   },
   "createdByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "1.4.18. **The approval gate refuses an approver who is the author, and nothing recorded either.** `SeatBlock`, `DelegatedAccess` and `ManualDiscountRequest` all carry this and the product passing through approval did not.\n"
   },
   "approvedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true
   },
   "responsibleDepartmentId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Who owns this product commercially. A scope node at `department` level."
   },
   "onSaleFrom": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "1.4.8. **A seasonal product should not need somebody awake at midnight.** Archiving already runs on a timer in this contract, so the machinery exists; `effectiveFrom` appears on tax codes, FX rates and white-label policies and not here.\n"
   },
   "onSaleTo": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "Retires the product automatically. **Retirement is not deletion** — the product stops selling and every order that referenced it still resolves.\n"
   },
   "categoryId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "**Taken from their `fnb.product` and `retail.product`, 20 September.** `catalogue.product_category` has existed since 20 August with two operations and nothing could be filed under it — a merchandise hierarchy with a tree and no leaves. Their per-domain product tables both carried this column and ours did not.\n"
   },
   "lifecycleState": {
    "$ref": "#/components/schemas/ProductLifecycleState"
   },
   "isSellable": {
    "type": "boolean",
    "readOnly": true,
    "description": "True only when live **and** carried by a published bundle. Approval and publication are different acts.\n**Derived, never set.** It changes when `transitionProductLifecycle` moves the product and when `publishBundle` carries it, so `updateProduct` does not take it — `withdraw` is how a product stops selling.\n"
   },
   "isStockTracked": {
    "type": "boolean",
    "default": false,
    "description": "**Taken from their `fnb.product`, 20 September.** Whether a sale decrements stock, which is not what `isSellable` asks. A ticket is sellable and tracks no stock; a bottle of water is both. Without it, an F&B sale cannot tell inventory whether to move.\n"
   },
   "hasVariants": {
    "type": "boolean"
   },
   "variantCount": {
    "type": "integer"
   },
   "segmentTags": {
    "type": "array",
    "description": "7.3.5. **A channel and a segment tag are mandatory and nothing required either.** A catalogue that cannot be filtered by segment is a catalogue nobody can report on.\n**Hierarchical, not flat** — `family/with-toddlers` narrows `family` without duplicating it, which is how the promotions engine already treats scope.\n**A level is a tag under `level/`** (decided 29 September, rev 3 REV3-19): `level/beginner`, `level/intermediate`, `level/advanced`, `level/expert` (proposed codes, client to correct). A guest screen filters on it with `listProducts` `segmentTag`, and the words a guest reads beside each option come from `ProductCategory.description`, not from the tag.\n",
    "items": {
     "type": "string"
    }
   },
   "codeSchema": {
    "type": "string",
    "readOnly": true,
    "description": "7.3.4 specifies `[ParkCode]-[ProductType]-[Variant]`. **`Product.code` existed and nothing required a format**, so a venue with three thousand products had three thousand conventions.\nThe tenant sets the pattern and the platform generates against it. **Validation is the point, not the string** — a code typed by hand is a code that will not sort.\n"
   },
   "channels": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/Channel"
    }
   },
   "entitlementTemplateId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "What the buyer receives. Null for products that grant nothing — F&B and retail. Identity and entitlement are separate concerns.\n"
   },
   "blockedOffline": {
    "type": "boolean",
    "description": "True for seated and retail. Seated because a seat map is not a count; retail because stock depletes in real time.\n"
   },
   "dataMaskValues": {
    "type": "object",
    "additionalProperties": true,
    "description": "Custom fields. JSONB-backed, defined by the venue's data mask."
   },
   "guestListing": {
    "$ref": "#/components/schemas/GuestListing"
   },
   "notBookableLabel": {
    "allOf": [
     {
      "$ref": "#/components/schemas/LocalisedText"
     }
    ],
    "nullable": true,
    "description": "The label a guest reads on an `infoOnly` product, e.g. *Info only* or *Not bookable online; ask at the desk* (decided 29 September, rev 3 REV3-14). Each value at most 60 characters. Null means the guest screen shows its default wording. Ignored unless `guestListing` is `infoOnly`.\n"
   },
   "salesContact": {
    "allOf": [
     {
      "$ref": "#/components/schemas/ProductSalesContact"
     }
    ],
    "nullable": true,
    "description": "**Who a guest contacts to book a view-only product** (decided 29 September, W3), e.g. a training course listed with full details and no Book button. Shown as *Call sales* and *Email sales* on an `infoOnly` product. Null means the venue's own contact (white-label `getTenantAppStatus.contact`). Ignored unless `guestListing` is `infoOnly`.\n"
   },
   "bookingFlowId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "**The booking flow this product is sold through** (decided 29 September, W8 and W12): a white-label `BookingFlow` of the venue, which orders the guest's steps (for a workshop, the product first and then the date and time). Null means the category's flow (`ProductCategory.bookingFlowId`), and failing that the venue's flow for the product's `kind`. Written by `createProduct` and `updateProduct`, which refuse an id that is not a flow of the venue with `422`.\n"
   },
   "displayTags": {
    "type": "array",
    "maxItems": 6,
    "items": {
     "$ref": "#/components/schemas/ProductDisplayTag"
    },
    "description": "**Short facts a guest reads on the ticket card and under *Read more***: *2 Hours*, *Min 1.10 m*, *Free adult entry*, *Valid 90 days*, *Emirates ID* (decided 29 September, 23SEP-3). Not `segmentTags`, which are for reporting and segmentation and which a guest never reads.\n**Derived on read when none are set.** When the venue has written no tags, a read returns tags derived from the product's duration (`clock`), entitlement validity (`calendar`) and the eligibility rule's `minHeightCm` (`height`), each marked `derived: true`; they are never stored. Once the venue writes any tag, only what it wrote is returned. Whether the guest screen shows them is `BookingFlowConfig.ticketTags` (white-label).\n"
   },
   "media": {
    "type": "array",
    "maxItems": 20,
    "items": {
     "$ref": "#/components/schemas/ProductMedia"
    },
    "description": "**The product's own photos and video** (decided 29 September, 23SEP-4). *Read more* opens on the `isPrimary` item, and a listing shows each product's primary image, so two tickets in one category no longer share the category's picture (`ProductCategory.imageAssetId`).\nEvery `assetId` names an asset of the asset library (`assets.yaml` `MediaAsset`) in status `ready` whose kind matches `kind`; anything else is a `422`. **Exactly one item is `isPrimary`** when the list is not empty, and an `assetId` appears once; otherwise `400`. Setting the list records each reference as asset usage (`MediaUsage` with `surface: product`, `referenceId` the product id, `isLive` true while the product is listed to guests), which is what stops a used asset being archived from under the product.\n"
   },
   "consentQuestionIds": {
    "type": "array",
    "maxItems": 10,
    "uniqueItems": true,
    "items": {
     "type": "string",
     "format": "uuid"
    },
    "description": "**The consent questions a guest answers when booking this product**, in the order they are asked (decided 29 September, rev 3 REV3-26): *Are you able to swim?*, *Do you hold a scuba certification?*, *I accept the risk*. Each id names a consent question defined in marketing-crm (`ConsentQuestion`), which owns the text, its version and whether it is asked per person or once per booking; the answer is stored there as a consent record (question version, answer, who answered, when). **One question or several, as the venue chooses.** A flow can carry its own list too (`white-label.BookingFlow.settings.consentQuestionIds`, on the product's published booking flow as `getPublishedBookingFlow` resolves it: product, then category, then the venue's flow for the kind; moved from `BookingFlowConfig` 29 September, W12); a booking asks the union of the flow's questions and those of every product in the cart, each question once (`orders.Cart.consentQuestions`). An id that names no active consent question of the tenant is a `422`.\n"
   },
   "requiresTimeWindow": {
    "type": "boolean",
    "default": false,
    "description": "**True for a space sold by the hour**, e.g. a meeting room type (decided 29 September, rev 3 REV3-13). The product is the room type (*focus pod*, *majlis*, *boardroom*, *auditorium*), never a named room; its lengths are a `length` axis (`setProductAttributes`) whose values carry `durationMinutes`, and each length is a variant priced on its own in the price list, so price is the room rate for that length. The cart line carries the booked start and end (orders), the end being the start plus the chosen variant's `durationMinutes`; `resources.listProductStartTimes` supplies the start times for a variant and a date and `allocateResources` picks the room from the product's resource requirements (`setExperienceResourceRequirements`) at checkout. True requires every active variant to have a `durationMinutes`; otherwise `422`.\n"
   },
   "productOwnerPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The product owner (29 September, data model DM3), set with `setProductContextOwnership`. `responsibleDepartmentId` is the owning department."
   },
   "operationalContact": {
    "type": "string",
    "maxLength": 200,
    "nullable": true,
    "description": "A principal id or a name, as the context screen takes it."
   },
   "businessUnitId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "legalEntityId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "A `ledger.legal_entity`, read through finance."
   },
   "attractionId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "siteId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "locationId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "brandId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The brand, as the context screen names it (a catalogue brand category)."
   },
   "marketCode": {
    "type": "string",
    "maxLength": 40,
    "nullable": true
   },
   "salesTerritory": {
    "type": "string",
    "maxLength": 100,
    "nullable": true
   }
  }
 },
 "ProductCategory": {
  "type": "object",
  "x-ticvai-persistence": "catalogue.product_category",
  "description": "Retail Board 2 of the client's design set, 20 August. **`listSeatCategories` existed and a product category did not** — a seat category prices a seat, and a merchandise hierarchy groups a catalogue.\n**Brand sits here rather than as its own entity.** A venue with four brands and a hierarchy five levels deep can express that with a parent; a venue with one brand should not have to maintain a table containing one row.\n**`displayOrder` is not alphabetical and that is the point.** A retail category list runs in the order the merchandiser wants a guest to see it, and sorting by name puts *Accessories* above *Apparel* forever.\n",
  "required": [
   "id",
   "name",
   "kind"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "name": {
    "type": "string"
   },
   "code": {
    "type": "string",
    "maxLength": 64,
    "nullable": true,
    "x-ticvai-unique": "tenant",
    "description": "**Taken from their category tables, 20 September.** Ours had a uuid and a localised name, so an importer matching *Beverages* had to match on a display string that a venue is free to translate.\n**Unique per tenant where set** (decided 28 September, audit R108): two categories in one tenant never share a code, and `setProductCategories` refuses a body that would, with `409 duplicate-code`.\n"
   },
   "nameLocalised": {
    "type": "object",
    "additionalProperties": {
     "type": "string"
    }
   },
   "kind": {
    "type": "string",
    "enum": [
     "category",
     "brand",
     "collection",
     "season",
     "department"
    ]
   },
   "parentId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "**One tree, not four.** A brand under a department under a category is how a real merchandise hierarchy runs, and separate tables for each level cannot express a venue that nests them differently.\n"
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "Set by the server from the venue the caller acts at; not sent."
   },
   "displayOrder": {
    "type": "integer",
    "default": 100
   },
   "imageAssetId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "description": {
    "allOf": [
     {
      "$ref": "#/components/schemas/LocalisedText"
     }
    ],
    "nullable": true,
    "description": "The short line a guest reads under a category option, e.g. *Surf lessons: learn on the beginner wave with a coach* (decided 29 September, rev 3 REV3-19). Each language value at most 200 characters.\n"
   },
   "bookingFlowId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "**The booking flow for every product filed here** that names none of its own (decided 29 September, W12, BO-115). Null means the venue's flow for each product's `kind`. A white-label `BookingFlow` of the venue; `setProductCategories` refuses any other id with `422`.\n"
   },
   "isActive": {
    "type": "boolean",
    "default": true,
    "description": "**Deactivated rather than deleted.** A category with a season behind it still names the products sold under it, and removing it rewrites last year's report.\n"
   }
  }
 },
 "ProductCategoryNode": {
  "x-ticvai-persistence": "none — projection over catalogue.product_category",
  "description": "**One node of the tree `listProductCategories` returns.** A `ProductCategory` with its children nested under it, in `displayOrder`, so no caller reassembles the hierarchy from `parentId`. `setProductCategories` still takes the flat list, because a write names each parent by id.\n",
  "allOf": [
   {
    "$ref": "#/components/schemas/ProductCategory"
   },
   {
    "type": "object",
    "required": [
     "children"
    ],
    "properties": {
     "children": {
      "type": "array",
      "description": "Empty on a leaf.",
      "items": {
       "$ref": "#/components/schemas/ProductCategoryNode"
      }
     }
    }
   }
  ]
 },
 "ProductDisplayTag": {
  "x-ticvai-persistence": "none — jsonb column on catalogue.product",
  "type": "object",
  "required": [
   "kind",
   "label"
  ],
  "description": "One short fact on a ticket card (decided 29 September, 23SEP-3). `kind` picks the icon.",
  "properties": {
   "kind": {
    "type": "string",
    "enum": [
     "clock",
     "height",
     "free",
     "calendar",
     "id"
    ],
    "description": "`clock` a duration, `height` a height rule, `free` something included free, `calendar` a validity, `id` a document the guest must bring."
   },
   "label": {
    "allOf": [
     {
      "$ref": "#/components/schemas/LocalisedText"
     }
    ],
    "description": "What the guest reads, e.g. *2 Hours*. Each language value at most 40 characters."
   },
   "derived": {
    "type": "boolean",
    "readOnly": true,
    "default": false,
    "description": "True on a tag the server derived on read because the venue set none. Never sent."
   }
  }
 },
 "ProductKind": {
  "type": "string",
  "description": "**`openDated` added 24 August** from the client's *Create Ticket Flow* board, which names six main ticket types and this was the one with no kind: **valid on any date within an eligible range, rather than for a named performance or a fixed date.**\nThe mechanism already existed — `access.entitlement` carries `valid_from`, `valid_to`, `entries_allowed` and `frozen_days`, which is exactly an open-dated pass. **What was missing was the product saying it is one**, so a catalogue could not offer it and a report could not count it.\n**`datedAdmission` is a different thing and the two were being conflated**: dated is *this Tuesday*, open-dated is *any Tuesday between March and June*. A guest buying the second and being sold the first has bought the wrong ticket.\n**Transport uses two existing kinds, not a new one** (decided 29 September, rev 3 REV3-21). A one-way trip is `timedAdmission`: `transport.createTransportRoute` creates the route's product with one variant per passenger type, and each departure is a performance. A multi-trip or unlimited pass is `openDated`: `transport.createTransportPassType` creates it, with `EntitlementTemplate.entriesAllowed` = the pass's trips (null for unlimited), the validity = `validityDays`, and `EntitlementTemplate.transportRestriction` naming the station pair the pass was bought for, so `access` refuses it on another journey. The sale path is unchanged: both are cart lines, priced by `transport.quoteTransportFare` (orders `TransportLineAttributes`).\n",
  "enum": [
   "admission",
   "timedAdmission",
   "datedAdmission",
   "openDated",
   "seated",
   "membership",
   "bundle",
   "fnb",
   "retail",
   "rental",
   "addOn",
   "giftCard"
  ]
 },
 "ProductLifecycleState": {
  "type": "string",
  "enum": [
   "draft",
   "inReview",
   "approved",
   "live",
   "withdrawn",
   "archived"
  ]
 },
 "ProductMedia": {
  "x-ticvai-persistence": "catalogue.product_media",
  "type": "object",
  "required": [
   "assetId",
   "kind",
   "isPrimary"
  ],
  "description": "One photo or video of a product, referencing the asset library (decided 29 September, 23SEP-4). One row per product and asset, so the asset library can answer which products use an asset.\n",
  "properties": {
   "assetId": {
    "type": "string",
    "format": "uuid",
    "description": "A `MediaAsset` of `assets.yaml`, in status `ready`."
   },
   "kind": {
    "type": "string",
    "enum": [
     "image",
     "video"
    ]
   },
   "isPrimary": {
    "type": "boolean",
    "default": false,
    "description": "The item *Read more* opens on and a listing shows. Exactly one per product."
   },
   "displayOrder": {
    "type": "integer",
    "default": 100
   },
   "altText": {
    "allOf": [
     {
      "$ref": "#/components/schemas/LocalisedText"
     }
    ],
    "nullable": true
   }
  }
 },
 "ProductSalesContact": {
  "x-ticvai-persistence": "none — jsonb column on catalogue.product",
  "type": "object",
  "description": "Who to contact to book a view-only product (decided 29 September, W3). At least one of `phone` or `email`.\n",
  "minProperties": 1,
  "properties": {
   "phone": {
    "type": "string",
    "maxLength": 32,
    "nullable": true
   },
   "email": {
    "type": "string",
    "format": "email",
    "maxLength": 254,
    "nullable": true
   },
   "note": {
    "allOf": [
     {
      "$ref": "#/components/schemas/LocalisedText"
     }
    ],
    "nullable": true,
    "description": "A line shown under the contact, e.g. *Group courses are booked by phone*. At most 200 characters per language."
   }
  }
 },
 "ProposedAction": {
  "type": "object",
  "x-ticvai-persistence": "ai.proposed_action",
  "required": [
   "id",
   "kind",
   "targetContract",
   "targetOperation",
   "payload",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "interactionId": {
    "type": "string",
    "format": "uuid"
   },
   "kind": {
    "type": "string",
    "enum": [
     "pricing",
     "promotion",
     "operational",
     "financial",
     "configuration",
     "content",
     "audience"
    ],
    "description": "`content` (a marketing or storefront draft from `proposeMarketingContent`) and `audience` (a lookalike segment from `proposeLookalikeSegment`) added 29 September (build); both are applied by a person in the owning screen."
   },
   "targetContract": {
    "type": "string",
    "description": "Which contract would perform it. The assistant never performs it itself."
   },
   "targetOperation": {
    "type": "string"
   },
   "payload": {
    "type": "object",
    "additionalProperties": true,
    "description": "The request body a person would submit, ready to review. **Open on purpose: its shape is the request body of `targetOperation` in `targetContract`**, and it is validated against that operation, not restated here.\n"
   },
   "summary": {
    "type": "string"
   },
   "status": {
    "type": "string",
    "description": "**Expiry (decided 28 September, audit R213)**: a `proposed` action expires 7 days after `proposedAt`; an `approved` action not applied expires 24 hours after `decidedAt`. Both are proposed values, client to correct, and `expiresAt` carries the one that applies.\n",
    "enum": [
     "proposed",
     "approved",
     "rejected",
     "applied",
     "expired"
    ]
   },
   "expiresAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true,
    "x-ticvai-derived": "onWrite",
    "description": "When the expiry timer moves this action to `expired` — `proposedAt` plus 7 days while `proposed`, `decidedAt` plus 24 hours once `approved`, null once `rejected`, `applied` or `expired` (audit R213)."
   },
   "approvalLevel": {
    "type": "integer",
    "minimum": 1,
    "maximum": 2,
    "description": "8.3.65. Multi-level, because a discount and a pricing change differ in authority. **Two levels (decided 28 September, audit R213)**: `2` for anything touching prices or permissions (every `pricing` and `promotion` action, and any other whose payload sets a price, a discount, a role or a permission grant), which needs a manager other than the requester; `1` for everything else, which the requester approves themselves.\n"
   },
   "decidedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "decisionReason": {
    "type": "string",
    "nullable": true,
    "description": "Required on rejection. **The only signal the assistant is proposing badly**, and without it a poor model degrades silently.\n"
   },
   "proposedAt": {
    "type": "string",
    "format": "date-time"
   },
   "decidedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**Added 29 September (AI design 3.1):** `ai.proposed_action` had no policy — its only references were nullable. The scope it was proposed at, and the partition key row-level security reads.\n"
   },
   "planId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "x-ticvai-references": "ai.action_plan",
    "description": "The plan this action presents for a decision (AI design 2.2 D, 3.8)."
   },
   "approvalRequestId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "description": "The `approvals` request deciding a tier 2 or matrix-caught action (AI design 2.3)."
   },
   "changeSetHash": {
    "type": "string",
    "nullable": true,
    "readOnly": true,
    "description": "Hash of the change set approved; execution refuses a plan whose hash differs (AIC-181)."
   }
  }
 },
 "SiteSetupProgress": {
  "x-ticvai-persistence": "whitelabel.site_setup_progress",
  "type": "object",
  "description": "**The Site Builder's saved progress, one row per tenant (decided 29 September, W12 and M24-05).** Not configuration and not published. `presetKey` is the starting point the operator picked; the builder pre-fills each step from it, which is what keeps the minimum path to a working site at about 30 minutes.\n",
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "presetKey": {
    "type": "string",
    "nullable": true,
    "enum": [
     "themePark",
     "waterPark",
     "museum",
     "theatreAndArena",
     "singleAttraction",
     "playCentre",
     "multiVenue",
     null
    ],
    "description": "The starting point. Each preset proposes the modules, the booking flow types (with their default step order), the homepage sections, the mobile tabs and a booking-flow `preset`; nothing is written until the operator accepts a step."
   },
   "currentStep": {
    "allOf": [
     {
      "$ref": "#/components/schemas/SiteSetupStepKey"
     }
    ],
    "nullable": true
   },
   "steps": {
    "type": "object",
    "description": "One entry per `SiteSetupStepKey`.",
    "additionalProperties": {
     "type": "object",
     "required": [
      "status"
     ],
     "properties": {
      "status": {
       "type": "string",
       "enum": [
        "notStarted",
        "inProgress",
        "done",
        "skipped"
       ]
      },
      "completedAt": {
       "type": "string",
       "format": "date-time",
       "nullable": true
      },
      "completedByPrincipalId": {
       "type": "string",
       "format": "uuid",
       "nullable": true
      }
     }
    }
   },
   "minimumPathDone": {
    "type": "boolean",
    "readOnly": true,
    "x-ticvai-derived": "onRead",
    "description": "True once the minimum path is done: a logo, the four theme colours, at least one enabled valid booking flow and a published version. Everything else keeps its preset or schema default."
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "The partition key (ADR-0005). Written at `tenant` scope."
   },
   "updatedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   }
  }
 },
 "SiteSetupStepKey": {
  "type": "string",
  "description": "The seven Site Builder steps, in order (decided 29 September, W12): venue and modules (CMS-001), ticketing flows (CMS-103), compose steps (CMS-103), Help me choose (CMS-101), look and feel (CMS-007, CMS-009, CMS-002, CMS-004, CMS-008, CMS-005, CMS-003), mobile app (CMS-009, CMS-004, CMS-007), preview and publish (CMS-006, CMS-012, CMS-014).\n",
  "enum": [
   "venueAndModules",
   "ticketingFlows",
   "composeSteps",
   "helpMeChoose",
   "lookAndFeel",
   "mobileApp",
   "previewAndPublish"
  ]
 },
 "StoreAccount": {
  "x-ticvai-persistence": "whitelabel.store_account",
  "type": "object",
  "description": "**One of the client's own store accounts (decided 24 September, M24-08).** TICVAI never publishes under its own developer account.\n",
  "required": [
   "store",
   "accountHolderName",
   "developerAccountId",
   "appIdentifier"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "store": {
    "type": "string",
    "enum": [
     "appleAppStore",
     "googlePlay"
    ]
   },
   "accountHolderName": {
    "type": "string",
    "maxLength": 200,
    "description": "The client's legal entity as the store knows it."
   },
   "dunsNumber": {
    "type": "string",
    "nullable": true,
    "pattern": "^[0-9]{9}$",
    "description": "Required for `appleAppStore`; Apple enrols an organisation only with its D-U-N-S number."
   },
   "developerAccountId": {
    "type": "string",
    "maxLength": 64,
    "description": "Apple Team ID, or the Google Play developer account id."
   },
   "appIdentifier": {
    "type": "string",
    "maxLength": 155,
    "pattern": "^[A-Za-z][A-Za-z0-9_]*(\\.[A-Za-z0-9_]+)+$",
    "description": "The bundle id (Apple) or application id (Google) the app is signed with."
   },
   "apiCredentialSecretRef": {
    "type": "string",
    "nullable": true,
    "writeOnly": true,
    "description": "App Store Connect API key or Play service-account key, sent once and kept in the secret store; this is its reference. Needed only for `submitToStore`."
   },
   "hasApiCredential": {
    "type": "boolean",
    "readOnly": true,
    "x-ticvai-derived": "onRead"
   },
   "listing": {
    "type": "object",
    "description": "The store listing.",
    "properties": {
     "appName": {
      "$ref": "#/components/schemas/LocalisedText"
     },
     "subtitle": {
      "$ref": "#/components/schemas/LocalisedText"
     },
     "description": {
      "$ref": "#/components/schemas/LocalisedText"
     },
     "keywords": {
      "$ref": "#/components/schemas/LocalisedText"
     },
     "category": {
      "type": "string"
     },
     "supportUrl": {
      "type": "string",
      "format": "uri"
     },
     "privacyPolicyUrl": {
      "type": "string",
      "format": "uri"
     },
     "screenshotAssetRefs": {
      "type": "array",
      "items": {
       "type": "string",
       "format": "uuid"
      }
     }
    }
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "The partition key (ADR-0005). Written at `tenant` scope."
   },
   "updatedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   }
  }
 },
 "StorePublishingChecklist": {
  "x-ticvai-persistence": "none — computed",
  "type": "object",
  "required": [
   "accounts",
   "items"
  ],
  "properties": {
   "accounts": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/StoreAccount"
    }
   },
   "items": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "item",
      "done"
     ],
     "properties": {
      "item": {
       "type": "string",
       "enum": [
        "appleDunsNumber",
        "appleDeveloperAccount",
        "googlePlayDeveloperAccount",
        "storeListing",
        "appIcons",
        "publishedConfiguration"
       ]
      },
      "done": {
       "type": "boolean"
      },
      "clientOwned": {
       "type": "boolean",
       "description": "True for the three accounts, which only the client can open."
      },
      "guidance": {
       "type": "string",
       "description": "What to do next, in the operator's language."
      }
     }
    }
   }
  }
 },
 "TenantAppStatus": {
  "x-ticvai-persistence": "none — computed",
  "type": "object",
  "description": "Computed on read. The published fields come from the current `ConfigVersion`, the maintenance fields from the tenant's `tenant_config` row (`setMaintenanceMode`), and the draft fields from the working draft. **Fields marked staff only are left out of a response to a caller without a staff session** (`getTenantAppStatus`).\n",
  "required": [
   "tenantId",
   "isPublished",
   "isInMaintenance"
  ],
  "properties": {
   "tenantId": {
    "type": "string",
    "format": "uuid"
   },
   "isPublished": {
    "type": "boolean",
    "x-ticvai-derived": "onRead",
    "description": "True once any version has been published."
   },
   "publishedVersion": {
    "type": "string",
    "nullable": true
   },
   "publishedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "draftVersion": {
    "type": "string",
    "description": "Staff only."
   },
   "hasUnpublishedChanges": {
    "type": "boolean",
    "x-ticvai-derived": "onRead",
    "description": "Staff only. The working draft differs from the current version's `snapshot`."
   },
   "activeModuleCount": {
    "type": "integer",
    "x-ticvai-derived": "onRead",
    "description": "Staff only. `ModuleEnablement` rows with `isEnabled` true."
   },
   "licensedModuleCount": {
    "type": "integer",
    "x-ticvai-derived": "onRead",
    "description": "Staff only. `ModuleEnablement` rows with `isLicensed` true."
   },
   "activePageCount": {
    "type": "integer",
    "x-ticvai-derived": "onRead",
    "description": "Staff only. Content pages that are `published` and enabled."
   },
   "isInMaintenance": {
    "type": "boolean"
   },
   "maintenanceMessage": {
    "$ref": "#/components/schemas/LocalisedText"
   },
   "expectedBackAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "minimumAppVersion": {
    "$ref": "#/components/schemas/MinimumAppVersion"
   },
   "contact": {
    "$ref": "#/components/schemas/VenueContact"
   },
   "availability": {
    "$ref": "#/components/schemas/AppAvailability"
   },
   "availabilityMessage": {
    "allOf": [
     {
      "$ref": "#/components/schemas/LocalisedText"
     }
    ],
    "nullable": true,
    "description": "What the sold-out or closed screen says (WEB-029). Null shows the default wording."
   },
   "venues": {
    "type": "array",
    "maxItems": 200,
    "x-ticvai-derived": "onRead",
    "description": "**Public: the venues a guest can pick** (decided 28 September, audit R267; schema named 29 September, readiness close-out, our build plan). The source of the venue picker on WEB-001 and GST-001, returned with or without a session. **Published only**: a venue is listed when its scope node is active (`tenancy.OrgUnit.isActive`) and it is in the tenant's current published `ConfigVersion`; a venue added or reactivated since the last publish appears after the next publish, and a draft never reaches a guest. Ordered by `name`. Empty when nothing is published.\n",
    "items": {
     "type": "object",
     "required": [
      "venueId",
      "name"
     ],
     "properties": {
      "venueId": {
       "type": "string",
       "format": "uuid",
       "description": "**The venue's scope node** (`tenancy.OrgUnit.id`, level venue): what every guest screen that declares `venueId` `from: session` reads once the guest picks it."
      },
      "name": {
       "type": "string",
       "maxLength": 200,
       "description": "The venue's name (`tenancy.OrgUnit.name`)."
      },
      "city": {
       "type": "string",
       "maxLength": 120,
       "nullable": true,
       "description": "Shown under the name so two venues with similar names can be told apart."
      },
      "openingHoursToday": {
       "type": "object",
       "nullable": true,
       "description": "Today's opening hours in the venue's time zone, from `tenancy.VenueSettings` opening hours. Null when the venue is closed today or has none set.",
       "properties": {
        "opens": {
         "type": "string",
         "pattern": "^([01][0-9]|2[0-3]):[0-5][0-9]$"
        },
        "closes": {
         "type": "string",
         "pattern": "^([01][0-9]|2[0-3]):[0-5][0-9]$"
        }
       }
      }
     }
    }
   },
   "whatsNew": {
    "type": "array",
    "maxItems": 10,
    "x-ticvai-derived": "onRead",
    "description": "**Public: the guest \"what's new\"** (decided 29 September, rev 3 GAP-B2). Newest first, at most 10, from `platform-ops.Release.guestReleaseNotes` of the releases the tenant's cell has received; a release with no guest notes is skipped. Returned with or without a staff session.\n",
    "items": {
     "type": "object",
     "required": [
      "version",
      "publishedAt",
      "notes"
     ],
     "properties": {
      "version": {
       "type": "string",
       "description": "The release version."
      },
      "publishedAt": {
       "type": "string",
       "format": "date-time",
       "description": "When the release reached the tenant's cell."
      },
      "notes": {
       "$ref": "#/components/schemas/LocalisedText"
      }
     }
    }
   },
   "recentChanges": {
    "type": "array",
    "description": "Staff only. Names the principal behind each change, so it never reaches a public response.",
    "items": {
     "type": "object",
     "properties": {
      "area": {
       "type": "string"
      },
      "description": {
       "type": "string"
      },
      "principalId": {
       "type": "string",
       "format": "uuid"
      },
      "at": {
       "type": "string",
       "format": "date-time"
      }
     }
    }
   }
  }
 },
 "UpdateProductRequest": {
  "type": "object",
  "minProperties": 1,
  "properties": {
   "familyKey": {
    "type": "string",
    "maxLength": 64,
    "pattern": "^[A-Za-z0-9_-]+$",
    "nullable": true,
    "x-ticvai-unique": "venue",
    "description": "The product family across the tenant's venues (decided 29 September, rev 3 REV3-18); see `Product.familyKey`. At most one product per venue in a family, else `409 duplicate-code`."
   },
   "name": {
    "type": "string",
    "maxLength": 200
   },
   "description": {
    "type": "string"
   },
   "channels": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/Channel"
    }
   },
   "dataMaskValues": {
    "type": "object",
    "additionalProperties": true
   },
   "guestListing": {
    "$ref": "#/components/schemas/GuestListing"
   },
   "notBookableLabel": {
    "allOf": [
     {
      "$ref": "#/components/schemas/LocalisedText"
     }
    ],
    "nullable": true
   },
   "salesContact": {
    "allOf": [
     {
      "$ref": "#/components/schemas/ProductSalesContact"
     }
    ],
    "nullable": true,
    "description": "See `Product.salesContact` (W3, 29 September)."
   },
   "bookingFlowId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "See `Product.bookingFlowId` (W8, W12, 29 September)."
   },
   "displayTags": {
    "type": "array",
    "maxItems": 6,
    "items": {
     "$ref": "#/components/schemas/ProductDisplayTag"
    }
   },
   "media": {
    "type": "array",
    "maxItems": 20,
    "items": {
     "$ref": "#/components/schemas/ProductMedia"
    }
   },
   "consentQuestionIds": {
    "type": "array",
    "maxItems": 10,
    "uniqueItems": true,
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "requiresTimeWindow": {
    "type": "boolean"
   }
  }
 },
 "VenueContact": {
  "x-ticvai-persistence": "none — embedded in tenant_config",
  "type": "object",
  "nullable": true,
  "description": "How a guest reaches the venue: WEB-028 Contact & Venue Information, and the screen shown on an error or when the app cannot help (decided 28 September, audit R073). Public, because nothing here is personal.\n",
  "properties": {
   "phone": {
    "type": "string",
    "nullable": true
   },
   "email": {
    "type": "string",
    "format": "email",
    "nullable": true
   },
   "whatsapp": {
    "type": "string",
    "nullable": true
   },
   "address": {
    "allOf": [
     {
      "$ref": "#/components/schemas/LocalisedText"
     }
    ],
    "nullable": true
   },
   "openingHours": {
    "allOf": [
     {
      "$ref": "#/components/schemas/LocalisedText"
     }
    ],
    "nullable": true,
    "description": "Prose, as the guest reads it. The bookable hours are the catalogue's."
   }
  }
 }
}
```
