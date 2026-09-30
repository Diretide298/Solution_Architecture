# P01-booking-selection-01 — P01 · Booking & Selection

**7 screens · 32 operations · 65 schemas · 7 permissions**

Platform P01 Guest Web · ships as **guest** ·
guest audience · web ·
online only

## Who this is for

**guest on web.** Everything below is how you know what is
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
  `AI_USE, ORDER_CREATE, ORDER_VIEW, PRICE_VIEW, PRODUCT_VIEW, RESOURCE_VIEW, VENUE_MAP_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store. Offline, a screen shows what was already loaded, under the banner below.
- **Offline, every screen shows one banner, the same on web and app:** *"You're offline. Connect to the internet to book, pay, order or join a queue."* The moment the connection drops, on every screen, above the screen's own content. By itself as soon as the connection is back, with a short "Back online" confirmation. **It never** Covers what is already on screen, or appears for a server error — that is the screen's own error state, and a guest told they are offline when the venue is down reconnects for nothing. Each screen's `states.offline` says what stays on screen and what waits.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `WEB-005` | Ticket Type Selection | listDetail | 6 | 3 | — |
| `WEB-006` | Date & Performance Selection | statusTracker | 8 | 3 | — |
| `WEB-007` | Interactive Seat Selection | statusTracker | 6 | 3 | — |
| `WEB-008` | Add-ons & Upsell | statusTracker | 6 | 1 | — |
| `WEB-009` | Wishlist | statusTracker | 3 | 2 | — |
| `WEB-047` | Map Booking — Cabanas & Spots | listDetail | 8 | 1 | — |
| `WEB-048` | Book a Space by the Hour | multiStepForm | 4 | 0 | — |

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "WEB-005",
  "name": "Ticket Type Selection",
  "module": "Booking & Selection",
  "requiresModule": "ticketing",
  "wave": 1,
  "capability": "C80",
  "implementation": {
   "app": "guest-web",
   "route": "/booking-and-selection/ticket-type-selection",
   "component": "apps/guest-web/src/routes/booking-and-selection/TicketTypeSelectionForm.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "WEB-004",
    "WEB-006",
    "WEB-002"
   ],
   "exitTo": [
    "WEB-001",
    "WEB-006",
    "WEB-007",
    "WEB-008",
    "WEB-010",
    "WEB-016"
   ],
   "transitions": [
    {
     "to": "WEB-006",
     "trigger": "Change date or time (the dated flow picks them first)",
     "provenance": "decided 29 September, rev 3 REV3-2: date → time → ticket; WEB-006 now comes before this screen (flow F01 step 3→4)",
     "carries": [
      "eventId"
     ]
    },
    {
     "to": "WEB-007",
     "trigger": "Interactive Seat Selection",
     "carries": [
      "eventId"
     ],
     "provenance": "derived — WEB-007 declares entryState.params eventId, holdId, performanceId and WEB-005 holds eventId, so an edge into it carries them"
    },
    {
     "to": "WEB-008",
     "trigger": "Add-ons & Upsell",
     "provenance": "derived — WEB-008 declares entryState.params bundleId and WEB-005 holds none of them, so the edge carries nothing and WEB-008 opens cold"
    },
    {
     "to": "WEB-010",
     "trigger": "Shopping Cart",
     "carries": [
      "code",
      "lineId"
     ],
     "provenance": "derived — WEB-010 declares entryState.params cartId, code, holdId, lineId, performanceId and WEB-005 holds code, lineId, so an edge into it carries them"
    },
    {
     "to": "WEB-016",
     "trigger": "Continue, when sign-in is asked after add-ons and this booking has no add-ons step",
     "carries": [
      "cartId"
     ],
     "provenance": "decided 29 September, rev 3 REV3-3: `BookingFlowConfig.signInAt` `afterAddOns`; the basket is kept"
    },
    {
     "to": "WEB-006",
     "trigger": "Workshop chosen, then date and time (product-first flow)",
     "carries": [
      "productId"
     ],
     "provenance": "decided 29 September 2026, W8"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listProductVariants` reads a population and nothing reads one of them; the detail is the row until a `get` exists",
  "purpose": "Choose which ticket and how many.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "banner",
       "label": "Booking at",
       "notes": "The venue this booking is for, with **Change location**. Reuses the venue choice of WEB-001 (audit R267). On a switch the selection is cleared, except lines whose product shares a `familyKey` with a product at the new venue, which move to it; times and prices refresh. Shown only when `BookingFlowConfig.locationSwitcher` is on.",
       "provenance": "decided 29 September, rev 3 REV3-18"
      },
      {
       "kind": "cardList",
       "label": "Ticket categories",
       "bindsTo": "ProductCategory",
       "notes": "`ticketCategories` `categoryThenSubcategory` (default): category tiles, then that category's tickets (`listProducts?categoryId=`); `flatList`: every ticket at once.",
       "operation": "listProductCategories",
       "provenance": "decided 29 September, rev 3 REV3-16"
      },
      {
       "kind": "selectField",
       "label": "Choose your experience",
       "bindsTo": "ProductCategory",
       "notes": "Each option carries its one-line `ProductCategory.description`. Narrows `listProducts?categoryId=`.",
       "operation": "listProductCategories",
       "provenance": "decided 29 September, rev 3 REV3-19"
      },
      {
       "kind": "selectField",
       "label": "Select level",
       "notes": "Beginner to expert, from the products' `segmentTags` `level/<code>` (`listProducts?segmentTag=`). **Reset** clears both filters.",
       "operation": "listProducts",
       "provenance": "decided 29 September, rev 3 REV3-19"
      },
      {
       "kind": "banner",
       "label": "Help me choose",
       "bindsTo": "GuidedChoice",
       "notes": "The venue's published Help me choose, if any (404 = none, and nothing shows). `mode` `button`: a button on this step; `popupOnArrival`: the pop-up also opens once on the first arrival (a seen flag on the device only); `showBanner`: a dark banner under the products (*Choose from the experiences above or let us help you decide*). Opens the Help me choose pop-up. **29 September (W4): the answers filter the list** (`guidedAnswerIds` on `listProducts`); *Show everything* clears it. Not a consent step: a swimmer answer pre-fills the REV3-26 swim consent, which the guest still confirms.",
       "operation": "getPublishedGuidedChoice",
       "provenance": "decided 29 September, rev 3 REV3-11"
      },
      {
       "kind": "iconButton",
       "label": "Quick tour",
       "notes": "Replays the four-step coach-mark tour. Shown only when `BookingFlowConfig.quickTour` is on (default off).",
       "provenance": "decided 29 September, rev 3 REV3-20"
      },
      {
       "kind": "dataTable",
       "label": "Every product variant",
       "bindsTo": "ProductVariant",
       "columns": [
        "ProductVariant.id",
        "ProductVariant.productId",
        "ProductVariant.sku",
        "ProductVariant.axisValues",
        "ProductVariant.isActive"
       ],
       "operation": "listProductVariants",
       "provenance": "contract catalogue.yaml GET /products/{productId}/variants"
      },
      {
       "kind": "cardList",
       "bindsTo": "ProductVariant[]",
       "notes": "Each row is a variant with a stepper. Price updates live. Each row shows `ProductVariant.description` (who it is for, what it includes) behind the (i) when `BookingFlowConfig.cardInfo` is on (23SEP-6), its display tags when `ticketTags` is on (23SEP-3) and its own photo (23SEP-4). In the dated flow the rows stay hidden until a time is picked (`performanceReveal` `dateTimeTicket`, REV3-2)",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "banner",
       "bindsTo": "PromotionEvaluation.rejected",
       "notes": "Shows near-miss offers — \"add one more for the family rate\". Uses the rejected list, which exists precisely so this can be said",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "progressIndicator",
       "label": "Booking steps",
       "bindsTo": "BookingFlow",
       "columns": [
        "BookingFlow.steps"
       ],
       "operation": "getPublishedBookingFlow",
       "notes": "The steps of the published flow in their `sortOrder`, this one (tickets) highlighted. A step the flow has turned off is not shown and is skipped by Continue and Back.",
       "provenance": "decided 29 September 2026, W12; CMS-103 Booking Flows"
      },
      {
       "kind": "secondaryButton",
       "label": "Show everything",
       "operation": "listProducts",
       "notes": "Clears the Help me choose filter (W4).",
       "provenance": "decided 29 September 2026, W4"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected product variant",
       "bindsTo": "ProductVariant",
       "columns": [
        "ProductVariant.id",
        "ProductVariant.productId",
        "ProductVariant.sku",
        "ProductVariant.axisValues",
        "ProductVariant.isActive"
       ],
       "operation": "listProductVariants",
       "provenance": "contract catalogue.yaml GET /products/{productId}/variants"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Evaluate promotions",
       "operation": "evaluatePromotions",
       "provenance": "contract promotions.yaml POST /promotions/evaluate"
      },
      {
       "kind": "primaryButton",
       "label": "Continue",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The ticket type selection list.",
   "error": "Could not load. Names which read failed and leaves the ticket type selection untouched.",
   "emptyFirstRun": "No ticket type selection yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table.",
   "emptyNoResults": "Never shown: `listProductVariants` takes no filter, so an empty list is always the first-run state above.",
   "emptyNoAccess": "**There is no permission to name — a guest holds none** (ADR-0025: `x-ticvai-permission` is what a staff caller must hold; a guest call resolves to the guest's own data). No access here means one of two things, told apart by the response: not signed in, where the guest is offered sign-in and brought back to this screen, or a record that is not theirs, which says so without saying whose it is. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "**The offline banner shows.** What was already loaded stays on screen, marked with its age. Anything that spends money, holds capacity or changes the account waits for the connection, and its button says so rather than failing."
  },
  "apis": [
   {
    "operationId": "evaluatePromotions",
    "contract": "promotions",
    "purpose": "Evaluate promotions against a cart",
    "trigger": "onAction",
    "invalidates": [
     "listProductVariants"
    ]
   },
   {
    "operationId": "listProductVariants",
    "contract": "catalogue",
    "purpose": "List generated variants",
    "trigger": "onLoad"
   },
   {
    "operationId": "listProductCategories",
    "contract": "catalogue",
    "purpose": "Category tiles and the experience filter, with descriptions",
    "trigger": "onLoad"
   },
   {
    "operationId": "listProducts",
    "contract": "catalogue",
    "purpose": "The tickets of a category or level (`categoryId`, `segmentTag`)",
    "trigger": "onLoad"
   },
   {
    "operationId": "getPublishedGuidedChoice",
    "contract": "white-label",
    "purpose": "The venue's published Help me choose (404 = none)",
    "trigger": "onLoad"
   },
   {
    "operationId": "getPublishedBookingFlow",
    "contract": "white-label",
    "purpose": "The published booking flow for this product: which steps it has and in what order (W12)",
    "trigger": "onLoad",
    "provenance": "decided 29 September 2026, W12"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "productId",
     "from": "WEB-004"
    },
    {
     "name": "venueId",
     "from": "session"
    }
   ],
   "coldEntry": "Resolves from the session; a cold arrival is the ordinary case.",
   "preloaded": [
    "ProductVariant.id",
    "ProductVariant.productId",
    "ProductVariant.sku",
    "ProductVariant.axisValues",
    "ProductVariant.isActive"
   ]
  },
  "wireframe": {
   "status": "review",
   "provenance": "client-verified",
   "board": "wireframes/P01 Guest Web.dc.html#web-005",
   "prototype": {
    "file": "sources/designs/guest-rev3-28-september/TICVAI Guest Booking v2.dc.html",
    "rev": "rev 3",
    "verified": "2026-09-28",
    "match": "partial",
    "view": "Header 'Book' (or any card's Book) → step 1 'Tickets' of the booking stepper; e.g. Tidewater Museum → 'Category → subcategory tickets'",
    "differences": "Ticket choice is on the same step as date and time and comes last: 'Date → time → ticket' (Config 'Performance reveal', Rev 3 item 2), whereas YAML goes WEB-005 → WEB-006. Prototype adds category → subcategory browsing, info-only (not bookable) products, 'Help me choose' questions, location switcher ('Booking at' bar), quick tour. Promo codes are entered in the cart, not on this step (YAML keeps evaluatePromotions here)."
   }
  },
  "apisNote": "Rebuilt 9 September 2026 from the 2 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formEvaluatePromotions",
    "component": "modal",
    "trigger": "Evaluate promotions",
    "body": "**Collects what `evaluatePromotions` sends before it is called.** Required: `venueId`, `channel`, `lines`. Optional: `subjectId`, `membershipTierId`, `couponCodes`, `evaluateAt`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "EvaluatePromotionsRequest",
    "confirm": {
     "label": "Evaluate promotions",
     "operation": "evaluatePromotions"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "venueId",
      "channel",
      "lines",
      "subjectId",
      "membershipTierId",
      "couponCodes",
      "evaluateAt"
     ]
    },
    "provenance": "client-verified"
   },
   {
    "id": "helpMeChoose",
    "component": "modal",
    "trigger": "Help me choose (the button, the banner, or once on first arrival when the mode is popupOnArrival)",
    "body": "**One or two questions, three answers each** (title, one-liner, icon, optional badge), from the published `GuidedChoice`. The answer to the last question opens its target through a result card: a product (this step with that product), a product category (its tiles), an event (WEB-006) or a module. **Start over** returns to the first question. Nothing is sent to the server; the guest's answers stay on the device (decided 29 September, rev 3 REV3-11).",
    "bindsTo": "GuidedChoice",
    "confirm": {
     "label": "Show me"
    },
    "dismiss": {
     "label": "Close",
     "discards": [
      "answers"
     ]
    },
    "provenance": "client-verified"
   },
   {
    "id": "quickTour",
    "component": "modal",
    "trigger": "First booking visit on this device, or Quick tour",
    "body": "**Four coach marks** over date, time, tickets and basket, with Back, Next and End tour. Shown once per device (the flag is kept on the device only) and replayable from Quick tour; only when `BookingFlowConfig.quickTour` is on (decided 29 September, rev 3 REV3-20).",
    "dismiss": {
     "label": "End tour",
     "discards": []
    },
    "provenance": "client-verified"
   }
  ],
  "notes": "**Rev 3 (decided 29 September).** **Order (REV3-2):** in the dated flow the guest picks the date, then the time (WEB-006), then tickets here: tickets stay hidden until a time is picked and Continue stays off until both are chosen, per `BookingFlowConfig.performanceReveal` (`dateTimeTicket` default, `allAtOnce` shows all). The two steps may render as one staged page. This screen may also render as a side panel on WEB-002 and WEB-004 (23SEP-5). **Sign-in (REV3-3):** with `signInAt` `afterAddOns` (default) the sign-in or guest code is asked when the guest leaves Add-ons (WEB-008), or on Continue here when the booking has no add-ons step; `atPayment` asks at WEB-012. The basket is kept either way. **Filters:** categories (REV3-16), experience and level (REV3-19). **Info-only** products show their label and open details (REV3-14). **Help me choose** (REV3-11) is a region and a pop-up of this step, not a screen of its own: the prototype draws it as a dialog over the booking step with a banner under the products. **Quick tour** (REV3-20). **Cart (REV3-10):** `cartLayout` may be `floatingIcon`, a round basket button with the count that opens the cart; the cart stays on the right in Arabic unless `cartSideInRtl` is `mirror`. Card layout, size and density are enums (DG-6). Every booking-flow setting named here is read from `getTenantConfig` `bookingFlow`, resolved for the venue the guest picked (audit R267): the tenant's values with that venue's `venueOverrides` entry laid over field by field (decided 29 September, rev 3 CFG-11).\n\n**The step order comes from the published booking flow** (W12, 29 September): `getPublishedBookingFlow` returns the flow the product (or its category, else the venue default for its kind) uses, with its enabled steps in `sortOrder`; this screen renders when that flow has its step and in the order the flow gives. Flow-level settings (`performanceReveal`, `signInAt`, `seatEventDateMode`, `extrasStep`, `quickTour`, `consentQuestionIds`) are read from the flow; venue-wide settings stay on `getTenantConfig` `bookingFlow`.\n\n**29 September.** W4: Help me choose filters. W8: in a product-first flow (workshop) this step comes first and the date follows. W5: surf levels appear only after a time slot.",
  "_platform": {
   "code": "P01",
   "audience": "guest",
   "formFactor": "web",
   "shortName": "Guest Web",
   "name": "Guest Web — Storefront",
   "offlineCapable": false,
   "offlineBanner": {
    "kind": "banner",
    "state": "warning",
    "message": "You're offline. Connect to the internet to book, pay, order or join a queue.",
    "shows": "The moment the connection drops, on every screen, above the screen's own content.",
    "clears": "By itself as soon as the connection is back, with a short \"Back online\" confirmation.",
    "never": "Covers what is already on screen, or appears for a server error — that is the screen's own error state, and a guest told they are offline when the venue is down reconnects for nothing.",
    "provenance": "Decided 12 September 2026 — guest web and guest app behave identically offline and say so with the same banner."
   },
   "app": "guest-web",
   "operator": "guest",
   "targetApp": {
    "app": "guest",
    "name": "TICVAI Guest",
    "shell": "web",
    "siblings": [
     "P02",
     "P05"
    ],
    "note": "**One guest product in three shells.** Web, mobile and kiosk share 73–91% of their operations; the kiosk is the same product in a fixed frame with no keyboard, and is deliberately narrower rather than different.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "WEB-006",
  "name": "Date & Performance Selection",
  "module": "Booking & Selection",
  "requiresModule": "ticketing",
  "wave": 1,
  "capability": "C81",
  "implementation": {
   "app": "guest-web",
   "route": "/booking-and-selection/date-and-session-selection",
   "component": "apps/guest-web/src/routes/booking-and-selection/DateAndSessionSelectionForm.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "WEB-005",
    "WEB-004"
   ],
   "exitTo": [
    "WEB-001",
    "WEB-005",
    "WEB-007",
    "WEB-008",
    "WEB-010"
   ],
   "transitions": [
    {
     "to": "WEB-005",
     "trigger": "Picks a time; the tickets for it appear",
     "provenance": "decided 29 September, rev 3 REV3-2: date → time → ticket (flow F01 step 3→4)",
     "carries": [
      "performanceId"
     ]
    },
    {
     "to": "WEB-008",
     "trigger": "Add-ons & Upsell",
     "provenance": "derived — WEB-008 declares entryState.params bundleId and WEB-006 holds none of them, so the edge carries nothing and WEB-008 opens cold"
    },
    {
     "to": "WEB-010",
     "trigger": "Reviews the cart and may enter a promotion code",
     "provenance": "flow F01 step 4→5",
     "operation": "getAvailability",
     "carries": [
      "cartId"
     ]
    },
    {
     "to": "WEB-007",
     "trigger": "Selects seats on the map",
     "provenance": "flow F02 step 1→2",
     "operation": "getAvailability",
     "carries": [
      "eventId",
      "performanceId"
     ]
    }
   ]
  },
  "notes": "Availability is read live and never cached beyond a few seconds. A guest selecting a session that filled while they were reading is a worse outcome than a slightly slower screen. **Wired 24 August from review**: acquireInventoryHold. **The operations existed and this screen could not call them** — reviewers reported them as missing APIs, which is what an unreachable operation looks like from a wireframe.\n\n**Rev 3 (decided 29 September).** **Date → time → ticket (REV3-2):** this step now comes before the ticket choice (WEB-005); the time sits right after the date and stays hidden until a date is picked, and tickets stay hidden until a time is picked (`BookingFlowConfig.performanceReveal`, default `dateTimeTicket`; `allAtOnce` shows everything). **Times (REV3-1):** compact tiles paged `timesPerPage` at a time, with Morning / Afternoon / Evening chips and counts (`dayPartFilter`, boundaries per venue, default before 12:00, 12:00-17:00, from 17:00, venue time zone). **Seated events (REV3-4, REV3-7):** `seatEventDateMode` `inlineStep` keeps this step before the seat map; `popupOnSeatMap` asks the date and time in a pop-up over WEB-007 instead. **This step is skipped when the event has exactly one on-sale performance.** For a seated event this step and WEB-007 may render as one page (date, time, show — plus language and format for cinema — and the seat map). **Language (REV3-17)**, **experience and level with a four-day calendar (REV3-19)**, **Booking at (REV3-18)**, **Quick tour (REV3-20)**. **Consent questions (REV3-26)** pop up once after the session or date is picked; the prototype's *Swim consent pop-up (on/off)* toggle is dropped because questions are attached per product or flow. Per-guest age and height eligibility, guardian signature and *Remove this guest* are `checkBookingEligibility`, unchanged (DG-3). **Guest-facing copy may say *Session*** (CFG-10, a glossary exception like *Booking* under audit R145); code and contracts keep `Performance`. Floating basket icon and cart side (REV3-10). Every booking-flow setting named here is read from `getTenantConfig` `bookingFlow`, resolved for the venue the guest picked (audit R267): the tenant's values with that venue's `venueOverrides` entry laid over field by field (decided 29 September, rev 3 CFG-11).\n\n**The step order comes from the published booking flow** (W12, 29 September): `getPublishedBookingFlow` returns the flow the product (or its category, else the venue default for its kind) uses, with its enabled steps in `sortOrder`; this screen renders when that flow has its step and in the order the flow gives. Flow-level settings (`performanceReveal`, `signInAt`, `seatEventDateMode`, `extrasStep`, `quickTour`, `consentQuestionIds`) are read from the flow; venue-wide settings stay on `getTenantConfig` `bookingFlow`.\n\n**29 September.** M17-08: the date strip shows the next seven days, with a calendar for later dates. W5: surf products (beginner, intermediate …) only after a time slot. W8: the date-first default no longer overrides product-first flows: order comes from the flow. W11: tours stay date → language → time slot, unchanged.",
  "density": "compact",
  "pattern": "statusTracker",
  "patternReason": "`getAvailability` reads one record and nothing reads a population — the screen is about that one thing",
  "purpose": "Pick a date and time that has capacity.",
  "layout": {
   "template": "detail",
   "regions": [
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Acquire inventory hold",
       "operation": "addCartLine",
       "provenance": "contract catalogue.yaml POST /inventory-holds"
      },
      {
       "kind": "secondaryButton",
       "label": "Check booking eligibility",
       "operation": "checkBookingEligibility",
       "provenance": "contract catalogue.yaml POST /eligibility-checks"
      },
      {
       "kind": "primaryButton",
       "label": "Continue",
       "provenance": "carried from the previous definition"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "banner",
       "label": "Booking at",
       "notes": "The venue this booking is for, with **Change location** (audit R267 venue choice). On a switch the selection clears unless products share a `familyKey`; times and prices refresh. Only when `BookingFlowConfig.locationSwitcher` is on.",
       "provenance": "decided 29 September, rev 3 REV3-18"
      },
      {
       "kind": "selectField",
       "label": "Part of the day",
       "notes": "Morning, Afternoon and Evening chips, each with its count of times, split in the venue time zone at `BookingFlowConfig.dayPartBoundaries` (`afternoonStartsAt` default 12:00, `eveningStartsAt` default 17:00). Shown when `dayPartFilter` is on (default on).",
       "operation": "listPerformances",
       "provenance": "decided 29 September, rev 3 REV3-1"
      },
      {
       "kind": "selectField",
       "label": "Tour language",
       "notes": "EN, AR, FR, DE, ZH, RU; sends `?language=` so only performances in that language are listed. Each time shows `Performance.language`, and for cinema also `Performance.format` (2D, 3D, subtitled).",
       "operation": "listPerformances",
       "provenance": "decided 29 September, rev 3 REV3-17"
      },
      {
       "kind": "datePicker",
       "label": "Next 7 days",
       "notes": "**Date strip of the next `BookingFlowSettings.dateStripDays` days** (default 7, 3-31) with a calendar icon for the full month (M17-08). Surf-style layout: four days side by side, each time with places left and the price per person; the experience and level filters of WEB-005 apply. A layout of the same data, no package change.",
       "operation": "listPerformances",
       "provenance": "decided 29 September, rev 3 REV3-19"
      },
      {
       "kind": "iconButton",
       "label": "Quick tour",
       "notes": "Replays the coach-mark tour when `BookingFlowConfig.quickTour` is on.",
       "provenance": "decided 29 September, rev 3 REV3-20"
      },
      {
       "kind": "datePicker",
       "notes": "Sold-out dates disabled with a reason on hover, not hidden",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "cardList",
       "bindsTo": "PerformanceAvailabilityPage.items",
       "notes": "Session times with remaining counts. Availability is per channel — a session showing sold out here may still have counter allocation, which is correct behaviour and not a defect. **More than 8 times show as compact tiles**, `BookingFlowConfig.timesPerPage` at a time (8, 12, 24 or all; default 24) with Earlier and Later; sold-out times greyed, not hidden. Times stay hidden until a date is picked (`performanceReveal`).",
       "provenance": "carried from the previous definition; decided 29 September, rev 3 REV3-1, REV3-2"
      },
      {
       "kind": "dataTable",
       "label": "Availability",
       "operation": "getAvailability",
       "notes": "From `getAvailability`, now a `PerformanceAvailabilityPage` (a Page of `PerformanceAvailability`, each with `startsAt`): `channelCapacityId`, `performanceId`, `startsAt`, `capacity`, `sold`, `leased`, `remaining`, `byChannel`. The time grid calls it once with `eventId`, `from` and `to` for every performance in the window (decided 29 September, rev 3 REV3-1), not once per tile.",
       "provenance": "contract catalogue.yaml GET /availability",
       "bindsTo": "PerformanceAvailability"
      },
      {
       "kind": "detailPanel",
       "label": "The performance",
       "bindsTo": "Performance",
       "columns": [
        "Performance.id",
        "Performance.eventId",
        "Performance.startsAt",
        "Performance.endsAt",
        "Performance.approvalRequestId",
        "Performance.requiresApprovalToCancel",
        "Performance.status",
        "Performance.admissionRulesId",
        "Performance.seatMapId"
       ],
       "operation": "getPerformance",
       "provenance": "contract catalogue.yaml GET /performances/{performanceId}"
      },
      {
       "kind": "progressIndicator",
       "label": "Booking steps",
       "bindsTo": "BookingFlow",
       "columns": [
        "BookingFlow.steps"
       ],
       "operation": "getPublishedBookingFlow",
       "notes": "The steps of the published flow in their `sortOrder`, this one (date and time) highlighted. A step the flow has turned off is not shown and is skipped by Continue and Back.",
       "provenance": "decided 29 September 2026, W12; CMS-103 Booking Flows"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The date session selection, read by `getPerformance`.",
   "error": "Could not load. Names which read failed and leaves the date session selection untouched.",
   "emptyFirstRun": "No date session selection yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table.",
   "emptyNoAccess": "**There is no permission to name — a guest holds none** (ADR-0025: `x-ticvai-permission` is what a staff caller must hold; a guest call resolves to the guest's own data). No access here means one of two things, told apart by the response: not signed in, where the guest is offered sign-in and brought back to this screen, or a record that is not theirs, which says so without saying whose it is. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "**The offline banner shows.** What was already loaded stays on screen, marked with its age. Anything that spends money, holds capacity or changes the account waits for the connection, and its button says so rather than failing.",
   "emptyNoResults": "No time matches the part of the day or the language picked, and the other times are still there. Names the filter and offers to clear it."
  },
  "apis": [
   {
    "operationId": "checkBookingEligibility",
    "contract": "catalogue",
    "purpose": "Check the party's ages and heights",
    "trigger": "onAction"
   },
   {
    "operationId": "getAvailability",
    "contract": "catalogue",
    "purpose": "Live remaining capacity",
    "trigger": "onLoad"
   },
   {
    "operationId": "addCartLine",
    "contract": "orders",
    "purpose": "Acquire an inventory lease",
    "trigger": "onAction"
   },
   {
    "operationId": "getPerformance",
    "contract": "catalogue",
    "purpose": "The performance being booked",
    "trigger": "onAction"
   },
   {
    "operationId": "listPerformances",
    "contract": "catalogue",
    "purpose": "The times of the event for the picked date or range, filtered by `language`",
    "trigger": "onLoad"
   },
   {
    "operationId": "getCart",
    "contract": "orders",
    "purpose": "The cart's `consentQuestions` after the time is added",
    "trigger": "onAction"
   },
   {
    "operationId": "recordConsentAnswers",
    "contract": "marketing-crm",
    "purpose": "Record the answers to the booking's consent questions",
    "trigger": "onAction",
    "invalidates": [
     "getCart"
    ]
   },
   {
    "operationId": "getPublishedBookingFlow",
    "contract": "white-label",
    "purpose": "The published booking flow for this product: which steps it has and in what order (W12)",
    "trigger": "onLoad",
    "provenance": "decided 29 September 2026, W12"
   }
  ],
  "wireframe": {
   "status": "review",
   "provenance": "client-verified",
   "board": "wireframes/P01 Guest Web.dc.html#web-006",
   "prototype": {
    "file": "sources/designs/guest-rev3-28-september/TICVAI Guest Booking v2.dc.html",
    "rev": "rev 3",
    "verified": "2026-09-28",
    "match": "partial",
    "view": "Book → step 1; e.g. Summit Peaks → 'Timed access — 10-minute slots', Coastal Aqua → 'Surf sessions with filters'",
    "differences": "Merged into the ticket step (date first, time revealed after the date, tickets after the time). Prototype adds morning/afternoon/evening filters, times-per-page paging, sold-out greying, per-guest age/height eligibility dialog with 'Remove this guest', and the water-park 'Are you able to swim?' pop-up. YAML's separate hold call (addCartLine / inventory hold) is implicit."
   }
  },
  "apisNote": "Rebuilt 9 September 2026 from the 2 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "entryState": {
   "params": [
    {
     "name": "performanceId",
     "from": "navigation"
    },
    {
     "name": "cartId",
     "from": "navigation"
    },
    {
     "name": "eventId",
     "from": "WEB-004"
    },
    {
     "name": "venueId",
     "from": "session"
    }
   ]
  },
  "overlays": [
   {
    "id": "formCheckBookingEligibility",
    "component": "modal",
    "trigger": "Check booking eligibility",
    "body": "**Collects what `checkBookingEligibility` sends before it is called.** Required: `productIds`, `party`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "EligibilityCheckRequest",
    "confirm": {
     "label": "Check booking eligibility",
     "operation": "checkBookingEligibility"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "productIds",
      "party"
     ]
    },
    "provenance": "client-verified"
   },
   {
    "id": "formAcquireInventoryHold",
    "component": "modal",
    "trigger": "Add to cart",
    "body": "**Collects what `addCartLine` sends before it is called; the cart takes the hold server-side.** Required: `variantId`, `quantity`. Optional: `performanceId`, `seatIds`, `parentLineId`, `attributes`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "AddCartLineRequest",
    "confirm": {
     "label": "Add to cart",
     "operation": "addCartLine"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "channelCapacityId",
      "requestedUnits",
      "ttlSeconds",
      "channel"
     ]
    },
    "provenance": "client-verified"
   },
   {
    "id": "consentQuestions",
    "component": "modal",
    "trigger": "Once, after the session or date is picked, when the cart has consent questions",
    "body": "**The venue's consent questions for this booking**, e.g. *Are you able to swim?*, *Do you hold a scuba certification?*, *I accept the risk*: one or several, in the order `Cart.consentQuestions` gives (the booking flow's `BookingFlowConfig.consentQuestionIds` and every cart product's `consentQuestionIds`, each question once). A question asked **per person** is asked for each member of the party; one asked **per booking** once. Themed as the prototype's pop-up (Yes / No, Next). Next sends the answers to `recordConsentAnswers`, which stores each as a consent record (question version, answer, who answered, when). **A blocking answer** (e.g. *No* to the swim question) marks the lines it blocks and says so; the guest removes them or answers again. There is no tenant on/off toggle: a question is attached to a product or a flow by the venue (decided 29 September, rev 3 REV3-26).",
    "bindsTo": "ConsentQuestion",
    "confirm": {
     "label": "Next",
     "operation": "recordConsentAnswers"
    },
    "dismiss": {
     "label": "Back",
     "discards": [
      "answers"
     ]
    },
    "provenance": "client-verified"
   }
  ],
  "_platform": {
   "code": "P01",
   "audience": "guest",
   "formFactor": "web",
   "shortName": "Guest Web",
   "name": "Guest Web — Storefront",
   "offlineCapable": false,
   "offlineBanner": {
    "kind": "banner",
    "state": "warning",
    "message": "You're offline. Connect to the internet to book, pay, order or join a queue.",
    "shows": "The moment the connection drops, on every screen, above the screen's own content.",
    "clears": "By itself as soon as the connection is back, with a short \"Back online\" confirmation.",
    "never": "Covers what is already on screen, or appears for a server error — that is the screen's own error state, and a guest told they are offline when the venue is down reconnects for nothing.",
    "provenance": "Decided 12 September 2026 — guest web and guest app behave identically offline and say so with the same banner."
   },
   "app": "guest-web",
   "operator": "guest",
   "targetApp": {
    "app": "guest",
    "name": "TICVAI Guest",
    "shell": "web",
    "siblings": [
     "P02",
     "P05"
    ],
    "note": "**One guest product in three shells.** Web, mobile and kiosk share 73–91% of their operations; the kiosk is the same product in a fixed frame with no keyboard, and is deliberately narrower rather than different.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "WEB-007",
  "name": "Interactive Seat Selection",
  "module": "Booking & Selection",
  "requiresModule": "seating",
  "wave": 2,
  "capability": "C51",
  "implementation": {
   "app": "guest-web",
   "route": "/booking-and-selection/seat-map-selection",
   "component": "apps/guest-web/src/routes/booking-and-selection/SeatMapSelectionCanvas.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "WEB-006",
    "WEB-004",
    "WEB-049"
   ],
   "exitTo": [
    "WEB-001",
    "WEB-005",
    "WEB-006",
    "WEB-008",
    "WEB-010"
   ],
   "transitions": [
    {
     "to": "WEB-005",
     "trigger": "Ticket Type Selection",
     "provenance": "derived — WEB-005 declares entryState.params productId and WEB-007 holds none of them, so the edge carries nothing and WEB-005 opens cold"
    },
    {
     "to": "WEB-008",
     "trigger": "Add-ons & Upsell",
     "provenance": "derived — WEB-008 declares entryState.params bundleId and WEB-007 holds none of them, so the edge carries nothing and WEB-008 opens cold"
    },
    {
     "to": "WEB-006",
     "trigger": "Date & Performance Selection",
     "carries": [
      "eventId",
      "performanceId"
     ],
     "provenance": "derived — WEB-006 declares entryState.params cartId, eventId, performanceId and WEB-007 holds eventId, performanceId, so an edge into it carries them"
    },
    {
     "to": "WEB-010",
     "trigger": "Reviews the cart",
     "provenance": "flow F02 step 2→3",
     "carries": [
      "holdId",
      "performanceId"
     ]
    }
   ]
  },
  "notes": "A map with no geometry falls back to category and best-available selection. Availability returns renderMode: list, and the screen renders groups rather than a plan. Never refuses the seated flow. **Drawn 26 August** — `Seat Board 3.dc.html` frame `seat-3b`. **The frame names this screen on its own face**, which is the first pack to do that: the earlier F&B, POS and Retail boards had to be hand-assigned by purpose after three derivation attempts produced nonsense. **A board that says what it draws removes the guess entirely.** **Renamed 31 August** from *Seat Map Selection*. **A guest surface is one product with two renderings** — a screen named differently on web and app is two screens to a developer and one journey to a guest. **Cross-surface parity, 31 August**: added recommendSeats. **A guest does not know which surface they are on** — the same named screen on web and app now calls the same guest-callable operations.\n\n**Rev 3 (decided 29 September).** Date and time on seated events: an inline step before this map, or a pop-up over it, per `BookingFlowConfig.seatEventDateMode` (REV3-4); a single-performance event opens straight here. Time bar with performance switcher (REV3-6, `seatTimeBar`). View-from-your-seat box placed per `seatViewPosition` (REV3-5) and fed by a section photo or the geometry (23SEP-14). Fixture strip and a direct WEB-004 → WEB-007 path (23SEP-16). With WEB-006 this may render as one step (REV3-7). Seat picker defaults to the bowl (`seatPicker` default `bowl`, CFG-6). **The cabana map is no longer this screen:** a cabana, lounger or other spot placed on a venue map is booked on WEB-047 (REV3-15, GAP-C2). Every booking-flow setting named here is read from `getTenantConfig` `bookingFlow`, resolved for the venue the guest picked (audit R267): the tenant's values with that venue's `venueOverrides` entry laid over field by field (decided 29 September, rev 3 CFG-11).\n\n**The step order comes from the published booking flow** (W12, 29 September): `getPublishedBookingFlow` returns the flow the product (or its category, else the venue default for its kind) uses, with its enabled steps in `sortOrder`; this screen renders when that flow has its step and in the order the flow gives. Flow-level settings (`performanceReveal`, `signInAt`, `seatEventDateMode`, `extrasStep`, `quickTour`, `consentQuestionIds`) are read from the flow; venue-wide settings stay on `getTenantConfig` `bookingFlow`.\n\n**29 September (W2).** Sections first, zoom into a section, scroll or pinch out (or *Whole map*) back to the full map; held seats are kept.",
  "density": "compact",
  "boardFrames": [
   "Seat Board 3.dc.html#seat-3b"
  ],
  "pattern": "statusTracker",
  "patternReason": "`getSeatAvailability` reads one record and nothing reads a population — the screen is about that one thing",
  "purpose": "Choose specific seats.",
  "layout": {
   "template": "detail",
   "regions": [
    {
     "name": "contentBody",
     "slot": "record",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The seat availability",
       "bindsTo": "SeatAvailability",
       "columns": [
        "SeatAvailability.performanceId",
        "SeatAvailability.seatMapId",
        "SeatAvailability.totals",
        "SeatAvailability.byCategory",
        "SeatAvailability.seats"
       ],
       "operation": "getSeatAvailability",
       "provenance": "contract seating.yaml GET /performances/{performanceId}/seat-availability"
      },
      {
       "kind": "banner",
       "notes": "Hold countdown, always visible. A selection that expires silently while a guest enters card details is the worst outcome in this flow",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "seatMap",
       "label": "Choose seats",
       "notes": "**A seat selection screen with no seat map.** `noGeometry` is the state that matters: a map imported from a manifest alone can be sold from a list and not rendered, and the screen has to say which it is rather than showing an empty frame. **At most `VenueSettings.seating.maxSeatsPerGuestOrder` seats per booking** on the guest channel (default 10, bounds 1-50): a `422 seat-limit-exceeded` from `createSeatHold` reads *Up to {maxSeats} seats per booking*, and the basket lists each seat (decided 29 September, rev 3 REV3-7). Section zoom happens on the same map (23SEP-16). **Sections first** (W2): tap a section to zoom in and see its seats; scroll or pinch out, or *← Whole map*, to return and compare sections, keeping held seats.",
       "provenance": "minute 2026-08-03 §Ticket Flow Variations by Product Type"
      },
      {
       "kind": "selectField",
       "label": "Time bar",
       "notes": "Above the map: the chosen performance, the other times of the event to switch to, and **Change date**. Switching releases the seats held for the old performance (`relinquishSeatHold`, the guest's own hold; another's answers 404) and holds new ones for the new one (`createSeatHold`). Shown only when `BookingFlowConfig.seatTimeBar` is on (default on).",
       "operation": "listPerformances",
       "provenance": "decided 29 September, rev 3 REV3-6"
      },
      {
       "kind": "cardList",
       "label": "Fixture strip",
       "notes": "The fixture (teams, date, kick-off) as a strip at the top of the seat step, so a single-performance fixture opens straight on the map.",
       "operation": "listPerformances",
       "provenance": "decided 29 September, rev 3 23SEP-16"
      },
      {
       "kind": "detailPanel",
       "label": "View from this section",
       "bindsTo": "SeatAvailability.sections",
       "notes": "When a section is picked: its photo (`sections[].viewAssetId`) if the venue uploaded one, otherwise a view rendered from the imported geometry (section boundary, stage position, seat positions) — closer sections show a larger stage and fewer rows ahead. Placed per `BookingFlowConfig.seatViewPosition` (bottom default, right, left, top) on wide screens; always below the map on narrow screens.",
       "operation": "getSeatAvailability",
       "provenance": "decided 29 September, rev 3 23SEP-14, REV3-5"
      },
      {
       "kind": "progressIndicator",
       "label": "Booking steps",
       "bindsTo": "BookingFlow",
       "columns": [
        "BookingFlow.steps"
       ],
       "operation": "getPublishedBookingFlow",
       "notes": "The steps of the published flow in their `sortOrder`, this one (seats) highlighted. A step the flow has turned off is not shown and is skipped by Continue and Back.",
       "provenance": "decided 29 September 2026, W12; CMS-103 Booking Flows"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Create seat hold",
       "operation": "createSeatHold",
       "provenance": "contract seating.yaml POST /seat-holds"
      },
      {
       "kind": "secondaryButton",
       "label": "Recommend seats",
       "operation": "recommendSeats",
       "provenance": "contract seating.yaml POST /performances/{performanceId}/seat-recommendations"
      },
      {
       "kind": "primaryButton",
       "label": "Continue to checkout",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The interactive seat selection, read by `getSeatAvailability`.",
   "error": "Could not load. Names which read failed and leaves the interactive seat selection untouched.",
   "emptyFirstRun": "No interactive seat selection yet. Offers Create seat hold (`createSeatHold`).",
   "emptyNoAccess": "**There is no permission to name — a guest holds none** (ADR-0025: `x-ticvai-permission` is what a staff caller must hold; a guest call resolves to the guest's own data). No access here means one of two things, told apart by the response: not signed in, where the guest is offered sign-in and brought back to this screen, or a record that is not theirs, which says so without saying whose it is. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "**The offline banner shows.** What was already loaded stays on screen, marked with its age. Anything that spends money, holds capacity or changes the account waits for the connection, and its button says so rather than failing.",
   "emptyNoResults": "The event has no other time to switch to on the time bar; the chosen performance stays."
  },
  "apis": [
   {
    "operationId": "createSeatHold",
    "contract": "seating",
    "purpose": "Hold specific seats",
    "trigger": "onAction"
   },
   {
    "operationId": "getSeatAvailability",
    "contract": "seating",
    "purpose": "Seat status for a performance",
    "trigger": "onLoad"
   },
   {
    "operationId": "recommendSeats",
    "contract": "seating",
    "purpose": "Recommend seats for a party",
    "trigger": "onAction"
   },
   {
    "operationId": "listPerformances",
    "contract": "catalogue",
    "purpose": "The event's other times, for the time bar and the date and time pop-up",
    "trigger": "onLoad"
   },
   {
    "operationId": "relinquishSeatHold",
    "contract": "seating",
    "purpose": "Release the seats held for the old performance when the guest switches time on the time bar (decided 29 September, rev 3 REV3-6); a guest releases only their own hold",
    "trigger": "onAction"
   },
   {
    "operationId": "getPublishedBookingFlow",
    "contract": "white-label",
    "purpose": "The published booking flow for this product: which steps it has and in what order (W12)",
    "trigger": "onLoad",
    "provenance": "decided 29 September 2026, W12"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "performanceId",
     "from": "deepLink"
    },
    {
     "name": "eventId",
     "from": "WEB-006"
    },
    {
     "name": "holdId",
     "from": "navigation"
    },
    {
     "name": "venueId",
     "from": "session"
    }
   ],
   "coldEntry": "**A link to a performance that has happened.** Offers the next performance of the same event."
  },
  "wireframe": {
   "status": "review",
   "provenance": "client-verified",
   "board": "wireframes/P01 Guest Web.dc.html#web-007",
   "prototype": {
    "file": "sources/designs/guest-rev3-29-september/TICVAI Guest Booking v2.dc.html",
    "rev": "rev 3 (29 September build)",
    "verified": "2026-09-29",
    "match": "exact",
    "view": "Union Arena → 'Flow 1 · Fixed date → zone → seat map' or 'Flow 2 · Choose date & time → seat map'; Grand Playhouse → Flow 1 / Flow 2"
   },
   "derivedFrom": "wireframes/reference/Seat Board 3.dc.html",
   "note": "**Drawn by Claude Design on `Seat Board 3.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
  },
  "apisNote": "Rebuilt 9 September 2026 from the 3 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formCreateSeatHold",
    "component": "modal",
    "trigger": "Create seat hold",
    "body": "**Collects what `createSeatHold` sends before it is called.** Required: `id`, `performanceId`, `seatIds`, `ttlSeconds`. Optional: `subjectId`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "CreateSeatHoldRequest",
    "confirm": {
     "label": "Create seat hold",
     "operation": "createSeatHold"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "performanceId",
      "seatIds",
      "ttlSeconds",
      "subjectId"
     ]
    },
    "provenance": "client-verified"
   },
   {
    "id": "formRecommendSeats",
    "component": "modal",
    "trigger": "Recommend seats",
    "body": "**Collects what `recommendSeats` sends before it is called.** Required: `partySize`, `strategy`. Optional: `categoryIds`, `maxPrice`, `accessibleCount`, `maxOptions`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "SeatRecommendationRequest",
    "confirm": {
     "label": "Recommend seats",
     "operation": "recommendSeats"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "partySize",
      "strategy",
      "categoryIds",
      "maxPrice",
      "accessibleCount",
      "maxOptions"
     ]
    },
    "provenance": "client-verified"
   },
   {
    "id": "dateTimeOnSeatMap",
    "component": "modal",
    "trigger": "The seat map opens for an event with several performances and `seatEventDateMode` is `popupOnSeatMap`",
    "body": "**Pick the date and time over the seat map** instead of a separate step: the dates, then that day's times; choosing one loads that performance's seat availability. Closing it keeps the performance already shown (decided 29 September, rev 3 REV3-4).",
    "bindsTo": "Performance",
    "confirm": {
     "label": "Show seats",
     "to": "WEB-007",
     "carries": [
      "performanceId"
     ]
    },
    "dismiss": {
     "label": "Close",
     "discards": []
    },
    "provenance": "client-verified"
   }
  ],
  "_platform": {
   "code": "P01",
   "audience": "guest",
   "formFactor": "web",
   "shortName": "Guest Web",
   "name": "Guest Web — Storefront",
   "offlineCapable": false,
   "offlineBanner": {
    "kind": "banner",
    "state": "warning",
    "message": "You're offline. Connect to the internet to book, pay, order or join a queue.",
    "shows": "The moment the connection drops, on every screen, above the screen's own content.",
    "clears": "By itself as soon as the connection is back, with a short \"Back online\" confirmation.",
    "never": "Covers what is already on screen, or appears for a server error — that is the screen's own error state, and a guest told they are offline when the venue is down reconnects for nothing.",
    "provenance": "Decided 12 September 2026 — guest web and guest app behave identically offline and say so with the same banner."
   },
   "app": "guest-web",
   "operator": "guest",
   "targetApp": {
    "app": "guest",
    "name": "TICVAI Guest",
    "shell": "web",
    "siblings": [
     "P02",
     "P05"
    ],
    "note": "**One guest product in three shells.** Web, mobile and kiosk share 73–91% of their operations; the kiosk is the same product in a fixed frame with no keyboard, and is deliberately narrower rather than different.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "WEB-008",
  "name": "Add-ons & Upsell",
  "module": "Booking & Selection",
  "requiresModule": "ticketing",
  "wave": 2,
  "capability": "C86",
  "implementation": {
   "app": "guest-web",
   "route": "/booking-and-selection/add-ons-and-upsell",
   "component": "apps/guest-web/src/routes/booking-and-selection/AddOnsAndUpsellDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "WEB-001",
    "WEB-047"
   ],
   "inferred": true,
   "exitTo": [
    "WEB-001",
    "WEB-005",
    "WEB-006",
    "WEB-007",
    "WEB-010",
    "WEB-016"
   ],
   "transitions": [
    {
     "to": "WEB-005",
     "trigger": "Ticket Type Selection",
     "provenance": "derived — WEB-005 declares entryState.params productId and WEB-008 holds none of them, so the edge carries nothing and WEB-005 opens cold"
    },
    {
     "to": "WEB-007",
     "trigger": "Interactive Seat Selection",
     "provenance": "derived — WEB-007 declares entryState.params eventId, holdId, performanceId and WEB-008 holds none of them, so the edge carries nothing and WEB-007 opens cold"
    },
    {
     "to": "WEB-006",
     "trigger": "Date & Performance Selection",
     "carries": [
      "cartId",
      "performanceId"
     ],
     "provenance": "derived — WEB-006 declares entryState.params cartId, eventId, performanceId and WEB-008 holds cartId, performanceId, so an edge into it carries them"
    },
    {
     "to": "WEB-010",
     "trigger": "Shopping Cart",
     "carries": [
      "cartId",
      "code",
      "performanceId"
     ],
     "provenance": "derived — WEB-010 declares entryState.params cartId, code, holdId, lineId, performanceId and WEB-008 holds cartId, code, performanceId, so an edge into it carries them"
    },
    {
     "to": "WEB-016",
     "trigger": "Continue — sign in or use a guest code (when sign-in is asked after add-ons)",
     "carries": [
      "cartId"
     ],
     "precondition": "the guest is not signed in",
     "provenance": "decided 29 September, rev 3 REV3-3: `BookingFlowConfig.signInAt` `afterAddOns` (default) places the gate at this exit; the basket is kept"
    }
   ]
  },
  "notes": "Purpose derived from the screen name and its operations on 17 August, not from a requirement. Add-ons. **`listCatalogueBundles` removed** — Sanket noted the screen shows individual add-ons rather than bundles, and it does. **Rewired on the 20 August review.**\n\n**Rev 3 (decided 29 September).** **Sign-in gate (REV3-3):** with `BookingFlowConfig.signInAt` `afterAddOns` (default), leaving this step asks the guest to sign in, or for a guest code when guest checkout is on (WEB-016); the basket is kept. With `atPayment` the gate is at WEB-012. Floating basket icon and cart side (REV3-10). Every booking-flow setting named here is read from `getTenantConfig` `bookingFlow`, resolved for the venue the guest picked (audit R267): the tenant's values with that venue's `venueOverrides` entry laid over field by field (decided 29 September, rev 3 CFG-11).\n\n**The step order comes from the published booking flow** (W12, 29 September): `getPublishedBookingFlow` returns the flow the product (or its category, else the venue default for its kind) uses, with its enabled steps in `sortOrder`; this screen renders when that flow has its step and in the order the flow gives. Flow-level settings (`performanceReveal`, `signInAt`, `seatEventDateMode`, `extrasStep`, `quickTour`, `consentQuestionIds`) are read from the flow; venue-wide settings stay on `getTenantConfig` `bookingFlow`.",
  "density": "compact",
  "pattern": "statusTracker",
  "patternReason": "`getUpsellSuggestions` reads one record and nothing reads a population — the screen is about that one thing",
  "purpose": "See add-ons & upsell for this venue.",
  "layout": {
   "template": "detail",
   "regions": [
    {
     "name": "contentBody",
     "slot": "record",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The upsell suggestion",
       "bindsTo": "UpsellSuggestion",
       "columns": [
        "UpsellSuggestion.variantId",
        "UpsellSuggestion.bundleId",
        "UpsellSuggestion.name",
        "UpsellSuggestion.price",
        "UpsellSuggestion.discountedPrice",
        "UpsellSuggestion.source",
        "UpsellSuggestion.ruleId",
        "UpsellSuggestion.rank",
        "UpsellSuggestion.rationale"
       ],
       "operation": "getUpsellSuggestions",
       "provenance": "contract promotions.yaml POST /upsell-suggestions"
      },
      {
       "kind": "detailPanel",
       "label": "The bundle",
       "bindsTo": "Bundle",
       "columns": [
        "Bundle.code",
        "Bundle.name",
        "Bundle.description",
        "Bundle.venueId",
        "Bundle.kind",
        "Bundle.price",
        "Bundle.components",
        "Bundle.choiceGroups",
        "Bundle.allocation",
        "Bundle.validFrom",
        "Bundle.validTo",
        "Bundle.id",
        "Bundle.savingsAmount",
        "Bundle.savingsPercentage",
        "Bundle.hasBeenSold",
        "Bundle.isActive"
       ],
       "operation": "getBundle",
       "provenance": "contract promotions.yaml GET /bundles/{bundleId}"
      },
      {
       "kind": "dataTable",
       "label": "Every bundle",
       "bindsTo": "BundleSummary",
       "columns": [
        "BundleSummary.venueId",
        "BundleSummary.publishedAt",
        "BundleSummary.publishedBy",
        "BundleSummary.contentHash",
        "BundleSummary.signatureKeyId",
        "BundleSummary.staleAfter",
        "BundleSummary.sizeBytes",
        "BundleSummary.note",
        "BundleSummary.appliedByWorkstations"
       ],
       "operation": "listCatalogueBundles",
       "provenance": "contract catalogue.yaml GET /catalogue/bundles"
      },
      {
       "kind": "progressIndicator",
       "label": "Booking steps",
       "bindsTo": "BookingFlow",
       "columns": [
        "BookingFlow.steps"
       ],
       "operation": "getPublishedBookingFlow",
       "notes": "The steps of the published flow in their `sortOrder`, this one (extras) highlighted. A step the flow has turned off is not shown and is skipped by Continue and Back.",
       "provenance": "decided 29 September 2026, W12; CMS-103 Booking Flows"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Add cart line",
       "operation": "addCartLine",
       "provenance": "contract orders.yaml POST /carts/{cartId}/lines"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The add-ons upsell, read by `getUpsellSuggestions`.",
   "error": "Could not load. Names which read failed and leaves the add-ons upsell untouched.",
   "emptyFirstRun": "No add-ons upsell yet. Offers Add cart line (`addCartLine`).",
   "emptyNoResults": "Never shown: `listCatalogueBundles` takes no filter, so an empty list is always the first-run state above.",
   "emptyNoAccess": "**There is no permission to name — a guest holds none** (ADR-0025: `x-ticvai-permission` is what a staff caller must hold; a guest call resolves to the guest's own data). No access here means one of two things, told apart by the response: not signed in, where the guest is offered sign-in and brought back to this screen, or a record that is not theirs, which says so without saying whose it is. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "**The offline banner shows.** What was already loaded stays on screen, marked with its age. Anything that spends money, holds capacity or changes the account waits for the connection, and its button says so rather than failing."
  },
  "apis": [
   {
    "operationId": "addCartLine",
    "contract": "orders",
    "purpose": "Add something",
    "trigger": "onAction"
   },
   {
    "operationId": "getBundle",
    "contract": "promotions",
    "purpose": "A bundle offered as an upsell",
    "trigger": "onAction"
   },
   {
    "operationId": "listCatalogueBundles",
    "contract": "catalogue",
    "purpose": "Which bundles apply here",
    "trigger": "onLoad"
   },
   {
    "operationId": "decideRecommendations",
    "contract": "ai",
    "purpose": "Fill a recommendation slot",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "recordRecommendationEvents",
    "contract": "ai",
    "purpose": "Report what happened to recommended items",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "getPublishedBookingFlow",
    "contract": "white-label",
    "purpose": "The published booking flow for this product: which steps it has and in what order (W12)",
    "trigger": "onLoad",
    "provenance": "decided 29 September 2026, W12"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "cartId",
     "from": "session"
    },
    {
     "name": "bundleId",
     "from": "navigation"
    },
    {
     "name": "venueId",
     "from": "session"
    }
   ],
   "coldEntry": "Resolves from the session; a cold arrival is the ordinary case."
  },
  "wireframe": {
   "status": "review",
   "provenance": "client-verified",
   "board": "wireframes/P01 Guest Web.dc.html#web-008",
   "prototype": {
    "file": "sources/designs/guest-rev3-28-september/TICVAI Guest Booking v2.dc.html",
    "rev": "rev 3",
    "verified": "2026-09-28",
    "match": "exact",
    "view": "Book → 'Extras' step (e.g. Summit Peaks → Dated day pass → Continue)",
    "differences": "Sign-in is asked when leaving Add-ons (Config 'Ask to sign in: After add-ons', Rev 3 item 3), so WEB-008 → WEB-016 is a transition YAML does not have. Add-ons also appear on the payment step (combo) and confirmation (upsells). 28 Sep flow review: all add-ons live here only."
   }
  },
  "apisNote": "Rebuilt 9 September 2026 from the 2 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formAddCartLine",
    "component": "modal",
    "trigger": "Add cart line",
    "body": "**Collects what `addCartLine` sends before it is called.** Required: `variantId`, `quantity`. Optional: `performanceId`, `seatIds`, `parentLineId`, `attributes`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "AddCartLineRequest",
    "confirm": {
     "label": "Add cart line",
     "operation": "addCartLine"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "variantId",
      "quantity",
      "performanceId",
      "seatIds",
      "parentLineId",
      "attributes"
     ]
    },
    "provenance": "client-verified"
   }
  ],
  "_platform": {
   "code": "P01",
   "audience": "guest",
   "formFactor": "web",
   "shortName": "Guest Web",
   "name": "Guest Web — Storefront",
   "offlineCapable": false,
   "offlineBanner": {
    "kind": "banner",
    "state": "warning",
    "message": "You're offline. Connect to the internet to book, pay, order or join a queue.",
    "shows": "The moment the connection drops, on every screen, above the screen's own content.",
    "clears": "By itself as soon as the connection is back, with a short \"Back online\" confirmation.",
    "never": "Covers what is already on screen, or appears for a server error — that is the screen's own error state, and a guest told they are offline when the venue is down reconnects for nothing.",
    "provenance": "Decided 12 September 2026 — guest web and guest app behave identically offline and say so with the same banner."
   },
   "app": "guest-web",
   "operator": "guest",
   "targetApp": {
    "app": "guest",
    "name": "TICVAI Guest",
    "shell": "web",
    "siblings": [
     "P02",
     "P05"
    ],
    "note": "**One guest product in three shells.** Web, mobile and kiosk share 73–91% of their operations; the kiosk is the same product in a fixed frame with no keyboard, and is deliberately narrower rather than different.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "WEB-009",
  "name": "Wishlist",
  "module": "Booking & Selection",
  "requiresModule": "marketing",
  "wave": 3,
  "capability": "C79",
  "implementation": {
   "app": "guest-web",
   "route": "/booking-and-selection/wishlist",
   "component": "apps/guest-web/src/routes/booking-and-selection/WishlistDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "WEB-001"
   ],
   "inferred": true,
   "exitTo": [
    "WEB-001",
    "WEB-005",
    "WEB-006",
    "WEB-007"
   ],
   "transitions": [
    {
     "to": "WEB-005",
     "trigger": "Ticket Type Selection",
     "provenance": "derived — WEB-005 declares entryState.params productId and WEB-009 holds none of them, so the edge carries nothing and WEB-005 opens cold"
    },
    {
     "to": "WEB-007",
     "trigger": "Interactive Seat Selection",
     "provenance": "derived — WEB-007 declares entryState.params eventId, holdId, performanceId and WEB-009 holds none of them, so the edge carries nothing and WEB-007 opens cold"
    },
    {
     "to": "WEB-006",
     "trigger": "Date & Performance Selection",
     "carries": [
      "performanceId"
     ],
     "provenance": "derived — WEB-006 declares entryState.params cartId, eventId, performanceId and WEB-009 holds performanceId, so an edge into it carries them"
    }
   ]
  },
  "notes": "Withdrawn products stay in the list marked unavailable. A guest who saved something and finds it silently gone assumes the feature is broken. Purpose derived from the screen name and its operations on 17 August, not from a requirement. Wishlist. **Device operations removed** — Sanket flagged that no device management appears on this screen, and he was right. **Rewired on the 20 August review.**\n\n**Rev 3 (decided 29 September, rev 3 GAP-D3).** Built as one implementation with WEB-024 (the account's devices, wishlist and consent); both ids are kept.",
  "density": "compact",
  "pattern": "statusTracker",
  "patternReason": "`getWishlist` reads one record and nothing reads a population — the screen is about that one thing",
  "purpose": "Find the right one quickly, and act on it without opening it.",
  "layout": {
   "template": "detail",
   "regions": [
    {
     "name": "contentBody",
     "slot": "record",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The wishlist",
       "bindsTo": "Wishlist",
       "columns": [
        "Wishlist.subjectId",
        "Wishlist.items"
       ],
       "operation": "getWishlist",
       "provenance": "contract marketing-crm.yaml GET /guests/{subjectId}/wishlist"
      },
      {
       "kind": "confirmDialog",
       "derived": true,
       "label": "Confirm",
       "notes": "**The consequence goes in the body, not the title.** *Cancel 3 orders worth AED 480* is a confirmation; *are you sure* is not — and a dialog that cannot name what it destroys is a dialog somebody dismisses.\n\n**Added 31 August.** `confirmDialog` and `modal` were both in the component library and used **zero times across 492 screens**, while `destructiveButton` was used 39 times and its own entry reads *always requires confirmation*.",
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
       "label": "Add to wishlist",
       "operation": "addToWishlist",
       "provenance": "contract marketing-crm.yaml POST /guests/{subjectId}/wishlist"
      },
      {
       "kind": "destructiveButton",
       "label": "Remove from wishlist",
       "operation": "removeFromWishlist",
       "provenance": "contract marketing-crm.yaml DELETE /guests/{subjectId}/wishlist/{itemId}"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmRemoveFromWishlist",
    "component": "confirmDialog",
    "trigger": "Remove from wishlist",
    "body": "**Names what `removeFromWishlist` changes and what it leaves alone**, in the consequence rather than the verb. A wishlist this affects should be identified in the dialog, not just counted.",
    "provenance": "client-verified"
   },
   {
    "id": "formAddToWishlist",
    "component": "modal",
    "trigger": "Add to wishlist",
    "body": "**Collects what `addToWishlist` sends before it is called.** Required: `variantId`. Optional: `performanceId`, `note`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Add to wishlist",
     "operation": "addToWishlist"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "variantId",
      "performanceId",
      "note"
     ]
    },
    "provenance": "client-verified"
   }
  ],
  "states": {
   "loading": "Saved items load",
   "error": "Could not load",
   "emptyFirstRun": "Nothing saved — explains what the list is for",
   "emptyNoAccess": "**There is no permission to name — a guest holds none** (ADR-0025: `x-ticvai-permission` is what a staff caller must hold; a guest call resolves to the guest's own data). No access here means one of two things, told apart by the response: not signed in, where the guest is offered sign-in and brought back to this screen, or a record that is not theirs, which says so without saying whose it is. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "**The offline banner shows.** What was already loaded stays on screen, marked with its age. Anything that spends money, holds capacity or changes the account waits for the connection, and its button says so rather than failing."
  },
  "apis": [
   {
    "operationId": "getWishlist",
    "contract": "marketing-crm",
    "purpose": "Read a guest's saved items",
    "trigger": "onLoad"
   },
   {
    "operationId": "addToWishlist",
    "contract": "marketing-crm",
    "purpose": "Save an item",
    "trigger": "onAction"
   },
   {
    "operationId": "removeFromWishlist",
    "contract": "marketing-crm",
    "purpose": "Remove a saved item",
    "trigger": "onAction"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "itemId",
     "from": "deepLink"
    },
    {
     "name": "subjectId",
     "from": "session"
    }
   ],
   "coldEntry": "**A guest arriving cold on a link that no longer resolves is shown what happened and one way onward — never a 404.** A shared ticket, a forwarded confirmation and a push notification opened three weeks late all land here, and the person holding the link did nothing wrong. **The screen names the thing, says it is expired, cancelled or withdrawn, and offers the list it came from.** Arrives with `itemId`."
  },
  "wireframe": {
   "status": "review",
   "provenance": "client-verified",
   "board": "wireframes/P01 Guest Web.dc.html#web-009",
   "prototype": {
    "file": "sources/designs/guest-rev3-28-september/TICVAI Guest Booking v2.dc.html",
    "rev": "rev 3",
    "verified": "2026-09-28",
    "match": "exact",
    "view": "Discover → 'Wishlist' link (discoverLinks)",
    "differences": "No 'withdrawn product stays marked unavailable' state (YAML note). Prototype adds 'Restore removed' and live queue times."
   }
  },
  "apisNote": "Rebuilt 9 September 2026 from the 3 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P01",
   "audience": "guest",
   "formFactor": "web",
   "shortName": "Guest Web",
   "name": "Guest Web — Storefront",
   "offlineCapable": false,
   "offlineBanner": {
    "kind": "banner",
    "state": "warning",
    "message": "You're offline. Connect to the internet to book, pay, order or join a queue.",
    "shows": "The moment the connection drops, on every screen, above the screen's own content.",
    "clears": "By itself as soon as the connection is back, with a short \"Back online\" confirmation.",
    "never": "Covers what is already on screen, or appears for a server error — that is the screen's own error state, and a guest told they are offline when the venue is down reconnects for nothing.",
    "provenance": "Decided 12 September 2026 — guest web and guest app behave identically offline and say so with the same banner."
   },
   "app": "guest-web",
   "operator": "guest",
   "targetApp": {
    "app": "guest",
    "name": "TICVAI Guest",
    "shell": "web",
    "siblings": [
     "P02",
     "P05"
    ],
    "note": "**One guest product in three shells.** Web, mobile and kiosk share 73–91% of their operations; the kiosk is the same product in a fixed frame with no keyboard, and is deliberately narrower rather than different.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "WEB-047",
  "name": "Map Booking — Cabanas & Spots",
  "module": "Booking & Selection",
  "requiresModule": "resources",
  "wave": 3,
  "implementation": {
   "app": "guest-web",
   "route": "/booking-and-selection/map-booking",
   "component": "apps/guest-web/src/routes/booking-and-selection/MapBookingCanvas.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "WEB-004"
   ],
   "exitTo": [
    "WEB-004",
    "WEB-008",
    "WEB-010"
   ],
   "transitions": [
    {
     "to": "WEB-010",
     "trigger": "Go to checkout",
     "operation": "addCartLine",
     "carries": [
      "cartId"
     ],
     "precondition": "a spot is held and added",
     "provenance": "decided 29 September, rev 3 REV3-15"
    },
    {
     "to": "WEB-008",
     "trigger": "Continue to add-ons (rentals, towels)",
     "carries": [
      "cartId"
     ],
     "provenance": "decided 29 September, rev 3 REV3-15; prototype cabana flow add-ons step"
    },
    {
     "to": "WEB-004",
     "trigger": "Back to the product",
     "back": true,
     "provenance": "decided 29 September, rev 3 REV3-15",
     "carries": [
      "productId"
     ]
    }
   ]
  },
  "notes": "**New 29 September** (decided 29 September, rev 3 REV3-15 and GAP-C2). **Cabana maps work like the stadium seat map:** the venue's map is ingested with its cabanas, loungers and other bookable spots (number, zone, capacity, price band), and the guest picks a specific one on the map and buys it. This supersedes audit R073 (c) (*cabanas stay staff-booked*) for resources placed on an ingested map. **Tables on the map are non-dining spots sold like cabanas** (decided 29 September by the user); a restaurant table stays the F&B reservation flow (WEB-036 / GST-070). The map comes from `getVenueMap` (its `resources`: label, kind, zone, capacity, price band, boundary) and the status of every spot for the chosen day from one `getMapResourceAvailability` call, joined on `resourceId`; held, booked and unavailable spots are greyed. Tapping a free spot calls `createResourceHold` and starts the *Remaining time* counter from the hold's `expiresAt` (8 minutes, extendable to 30 in all, audit R169); Add to basket sends `addCartLine` with the spot's price-band `variantId` and the `resourceHoldId`, e.g. *Cabana B09 · Large cabana · Beach, AED 1,855*. Picking another spot releases the first hold (`relinquishResourceHold`).\n\n**29 September (W6).** Map booking of cabanas stays **optional per flow**: the venue picks *Cabana: pick on map* (WEB-047) or *Cabana: by size* (capacity) as its booking flow (CMS-103), and the resource selection policy (`guestMayChoose`, REV3-15) decides whether the guest chooses the unit. Same venue-map back end as F&B and locations.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`getMapResourceAvailability` reads the population of spots and a tap holds one of them — list (as a map), select, act",
  "purpose": "Pick a specific cabana, lounger or other spot on the venue map and hold it while you book.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "datePicker",
       "label": "Date",
       "notes": "Sends `from`/`to` (the venue's opening for the day, or a slot) to `getMapResourceAvailability`.",
       "operation": "getMapResourceAvailability",
       "provenance": "decided 29 September, rev 3 REV3-15"
      },
      {
       "kind": "numberField",
       "label": "Who is coming",
       "notes": "`partySize`; a spot smaller than the party is refused `422 party-exceeds-capacity`.",
       "operation": "createResourceHold",
       "provenance": "decided 29 September, rev 3 REV3-15"
      },
      {
       "kind": "selectField",
       "label": "Area",
       "bindsTo": "PlacedResource.zone",
       "notes": "Beach, Tower, Riverside, Splash zone… from the placed resources' zones.",
       "operation": "getVenueMap",
       "provenance": "decided 29 September, rev 3 REV3-15; prototype cabana map"
      },
      {
       "kind": "seatMap",
       "label": "Venue map",
       "bindsTo": "VenueMapDetail.resources",
       "notes": "The ingested map with every placed spot drawn at its boundary and numbered (R01-R10, T01-T08, S01-S06, B01-B10 on Coastal Aqua). Free spots are tappable; held, booked and unavailable ones greyed.",
       "operation": "getVenueMap",
       "provenance": "decided 29 September, rev 3 REV3-15, GAP-C2"
      },
      {
       "kind": "cardList",
       "label": "Spots",
       "bindsTo": "MapResourceAvailability.resources",
       "notes": "The same spots as a list for the chosen area: number, capacity, price band and price, status. The accessible alternative to the map.",
       "operation": "getMapResourceAvailability",
       "provenance": "decided 29 September, rev 3 REV3-15"
      },
      {
       "kind": "selectField",
       "label": "Map",
       "bindsTo": "BookableVenueMaps.maps",
       "operation": "listBookableVenueMaps",
       "notes": "**Which map to book on.** `listBookableVenueMaps(venueId, productId)` returns the venue's published maps that carry bookable spots; with one map the screen opens it directly and this choice is not shown. The chosen map's `mapId` is what `getVenueMap` (at its `publishedVersion`) and `getMapResourceAvailability` read (decided 29 September, rev 3 REV3-15).",
       "provenance": "contract venue-map.yaml GET /bookable-venue-maps"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "banner",
       "label": "Remaining time",
       "bindsTo": "ResourceHold.expiresAt",
       "notes": "Counts down from the hold's `expiresAt`, always visible. At zero the spot is released and the guest is told.",
       "operation": "getResourceHold",
       "provenance": "decided 29 September, rev 3 REV3-15; audit R169"
      },
      {
       "kind": "detailPanel",
       "label": "The spot you picked",
       "bindsTo": "PlacedResource",
       "columns": [
        "PlacedResource.label",
        "PlacedResource.kind",
        "PlacedResource.zone",
        "PlacedResource.capacity",
        "PlacedResource.priceBandCode"
       ],
       "operation": "getVenueMap",
       "provenance": "decided 29 September, rev 3 REV3-15"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Add to basket",
       "notes": "Sends `variantId` (the spot's price band) and `resourceHoldId`.",
       "operation": "addCartLine",
       "provenance": "decided 29 September, rev 3 REV3-15"
      },
      {
       "kind": "secondaryButton",
       "label": "Keep it longer",
       "operation": "extendResourceHold",
       "provenance": "decided 29 September, rev 3 REV3-15"
      },
      {
       "kind": "secondaryButton",
       "label": "Pick another",
       "notes": "Releases the hold at once so the spot is free for others.",
       "operation": "relinquishResourceHold",
       "provenance": "decided 29 September, rev 3 REV3-15"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The venue map and the status of every spot for the day, read together.",
   "error": "Could not load the map or the spots. Names which read failed; nothing is held.",
   "emptyFirstRun": "**No bookable spots are placed on this map yet.** Says so and offers the venue's other ways to book, rather than an empty map.",
   "emptyNoResults": "Every spot in this area is taken for the day. Names the area and offers another area or day.",
   "emptyNoAccess": "**There is no permission to name — a guest holds none** (ADR-0025: `x-ticvai-permission` is what a staff caller must hold; a guest call resolves to the guest's own data). No access here means one of two things, told apart by the response: not signed in, where the guest is offered sign-in and brought back to this screen, or a record that is not theirs, which says so without saying whose it is. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "**The offline banner shows.** The map and the spots already loaded stay on screen with their age, never shown as free now. Holding a spot and adding it to the basket need the connection — a cabana held offline is a cabana two people think they have."
  },
  "apis": [
   {
    "operationId": "getVenueMap",
    "contract": "venue-map",
    "purpose": "The map with its placed spots (label, kind, zone, capacity, price band)",
    "trigger": "onLoad"
   },
   {
    "operationId": "getMapResourceAvailability",
    "contract": "resources",
    "purpose": "Every spot's status for the day in one call",
    "trigger": "onLoad"
   },
   {
    "operationId": "createResourceHold",
    "contract": "resources",
    "purpose": "Hold the tapped spot for the window",
    "trigger": "onAction",
    "invalidates": [
     "getMapResourceAvailability"
    ]
   },
   {
    "operationId": "getResourceHold",
    "contract": "resources",
    "purpose": "The hold's countdown",
    "trigger": "onInterval"
   },
   {
    "operationId": "extendResourceHold",
    "contract": "resources",
    "purpose": "Keep the hold longer while paying",
    "trigger": "onAction"
   },
   {
    "operationId": "relinquishResourceHold",
    "contract": "resources",
    "purpose": "Release the hold",
    "trigger": "onAction",
    "invalidates": [
     "getMapResourceAvailability"
    ]
   },
   {
    "operationId": "addCartLine",
    "contract": "orders",
    "purpose": "Add the held spot to the basket (`variantId`, `resourceHoldId`)",
    "trigger": "onAction"
   },
   {
    "operationId": "listBookableVenueMaps",
    "contract": "venue-map",
    "purpose": "Find the venue's published map with bookable spots (with productId when the product page opened it); getVenueMap then reads that map's published version (decided 29 September, rev 3 REV3-15)",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "mapId",
     "from": "WEB-004",
     "optional": true
    },
    {
     "name": "productId",
     "from": "WEB-004",
     "optional": true
    },
    {
     "name": "cartId",
     "from": "session"
    },
    {
     "name": "venueId",
     "from": "session"
    },
    {
     "name": "holdId",
     "from": "navigation"
    }
   ],
   "coldEntry": "**A link to a map that is no longer published, or a day that has passed,** says which and offers today on the current map. Nothing is held on arrival."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "client-verified",
   "board": "wireframes/P01 Guest Web.dc.html#web-047",
   "prototype": {
    "file": "sources/designs/guest-rev3-28-september/TICVAI Guest Booking v2.dc.html",
    "rev": "rev 3",
    "verified": "2026-09-28",
    "match": "exact",
    "view": "Coastal Aqua → 'Cabana & locker rentals' → cabana map ('Remaining time' counter)"
   }
  },
  "apisNote": "Authored 29 September 2026 from the rev 3 decisions and the client prototype view named in `wireframe.prototype`; every operation exists in the contracts (decided 29 September, rev 3).",
  "overlays": [
   {
    "id": "confirmReleaseHold",
    "component": "confirmDialog",
    "trigger": "Pick another (or tapping a second spot)",
    "body": "**Release the spot you are holding?** It goes back on the map at once and someone else may take it.",
    "confirm": {
     "label": "Release it",
     "operation": "relinquishResourceHold"
    },
    "dismiss": {
     "label": "Keep it",
     "carries": [
      "holdId"
     ]
    },
    "provenance": "client-verified"
   }
  ],
  "_platform": {
   "code": "P01",
   "audience": "guest",
   "formFactor": "web",
   "shortName": "Guest Web",
   "name": "Guest Web — Storefront",
   "offlineCapable": false,
   "offlineBanner": {
    "kind": "banner",
    "state": "warning",
    "message": "You're offline. Connect to the internet to book, pay, order or join a queue.",
    "shows": "The moment the connection drops, on every screen, above the screen's own content.",
    "clears": "By itself as soon as the connection is back, with a short \"Back online\" confirmation.",
    "never": "Covers what is already on screen, or appears for a server error — that is the screen's own error state, and a guest told they are offline when the venue is down reconnects for nothing.",
    "provenance": "Decided 12 September 2026 — guest web and guest app behave identically offline and say so with the same banner."
   },
   "app": "guest-web",
   "operator": "guest",
   "targetApp": {
    "app": "guest",
    "name": "TICVAI Guest",
    "shell": "web",
    "siblings": [
     "P02",
     "P05"
    ],
    "note": "**One guest product in three shells.** Web, mobile and kiosk share 73–91% of their operations; the kiosk is the same product in a fixed frame with no keyboard, and is deliberately narrower rather than different.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "WEB-048",
  "name": "Book a Space by the Hour",
  "module": "Booking & Selection",
  "requiresModule": "resources",
  "wave": 3,
  "implementation": {
   "app": "guest-web",
   "route": "/booking-and-selection/space-by-the-hour",
   "component": "apps/guest-web/src/routes/booking-and-selection/SpaceByTheHourWizard.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "WEB-004"
   ],
   "exitTo": [
    "WEB-004",
    "WEB-010"
   ],
   "transitions": [
    {
     "to": "WEB-010",
     "trigger": "Add to basket, then review the cart",
     "operation": "addCartLine",
     "carries": [
      "cartId"
     ],
     "precondition": "date, start time, length and room type chosen",
     "provenance": "decided 29 September, rev 3 REV3-13"
    },
    {
     "to": "WEB-004",
     "trigger": "Back to the product",
     "back": true,
     "provenance": "decided 29 September, rev 3 REV3-13",
     "carries": [
      "productId"
     ]
    }
   ]
  },
  "notes": "**New 29 September** (decided 29 September, rev 3 REV3-13: meeting rooms by the hour are in scope). A staged booking: date → start time → length (1 hour, 2 hours, half day, full day) → room type (focus pod, majlis, boardroom, auditorium) → attendees → add-ons (coffee break, working lunch, AV technician). **A room type is a product with `requiresTimeWindow`; a length is one of its variants** (the `length` axis, each value with `durationMinutes`), priced on its own, so the price is the variant's — the room rate for that length. The guest never names a room: `addCartLine` carries `bookedWindow` {startsAt, endsAt}, `endsAt` being the start plus the length, and `allocateResources` picks the room at checkout (26 August minute). Add-ons are lines with `parentLineId`. `422 windowLengthMismatch`, `windowRequired` and `windowNotAllowed` are programming errors; `409 windowUnavailable` says the time filled and offers the next free start.\n\n**29 September (W9).** Availability is checked against date, start time and length together (`listProductStartTimes` with `variantId` = length); changing any of the three re-checks every room, and a busy room shows *free from*. Starts every 15 minutes where the venue sets `stepMinutes` 15.",
  "density": "compact",
  "pattern": "multiStepForm",
  "patternReason": "A staged booking — date, start time, length, room type, attendees, add-ons — ending in one `addCartLine`; the prototype draws it as one step revealing each choice in turn",
  "purpose": "Book a meeting room or other space for a start time and a length; the price is the room rate for that length.",
  "layout": {
   "template": "wizard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "datePicker",
       "label": "Select a date",
       "provenance": "decided 29 September, rev 3 REV3-13"
      },
      {
       "kind": "selectField",
       "label": "Start time",
       "bindsTo": "ProductStartTime",
       "notes": "The start times at which a room of the chosen type is free for the chosen length (`listProductStartTimes` with `productId`, `variantId` = the length, `date`; hourly, 08:00-20:00 in the prototype), each with how many rooms of the type are left. The chosen start and start + length go to `addCartLine` as `bookedWindow`.",
       "operation": "listProductStartTimes",
       "provenance": "decided 29 September, rev 3 REV3-13"
      },
      {
       "kind": "selectField",
       "label": "How long",
       "bindsTo": "ProductVariant",
       "notes": "1 hour, 2 hours, half day (4 h), full day (8 h): the room type's `length` variants, each priced on its own (the prototype shows *Save 10%* and *Save 15%*).",
       "operation": "listProductVariants",
       "provenance": "decided 29 September, rev 3 REV3-13"
      },
      {
       "kind": "cardList",
       "label": "Choose a room",
       "bindsTo": "Product",
       "notes": "Room types (focus pod, majlis room, boardroom, auditorium) with capacity, description, badge and the price for the chosen length.",
       "operation": "listProducts",
       "provenance": "decided 29 September, rev 3 REV3-13"
      },
      {
       "kind": "numberField",
       "label": "Attendees",
       "notes": "For the visitor list at reception; a room type smaller than the party is not offered.",
       "provenance": "decided 29 September, rev 3 REV3-13"
      },
      {
       "kind": "cardList",
       "label": "Add to the booking",
       "bindsTo": "Product",
       "notes": "Coffee break, working lunch, AV technician: add-on lines with `parentLineId`.",
       "operation": "listProducts",
       "provenance": "decided 29 September, rev 3 REV3-13"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "submit",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Add to basket",
       "notes": "`variantId` (the length), `bookedWindow` {startsAt, endsAt}, then the add-on lines.",
       "operation": "addCartLine",
       "provenance": "decided 29 September, rev 3 REV3-13"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The room types and their lengths for this venue.",
   "error": "Could not load. Names which read failed; nothing is booked.",
   "emptyFirstRun": "**This venue sells no space by the hour yet.** Says so rather than an empty list.",
   "emptyNoResults": "No room of the type is free at that time for that length. Offers the next free start time.",
   "emptyNoAccess": "**There is no permission to name — a guest holds none** (ADR-0025: `x-ticvai-permission` is what a staff caller must hold; a guest call resolves to the guest's own data). No access here means one of two things, told apart by the response: not signed in, where the guest is offered sign-in and brought back to this screen, or a record that is not theirs, which says so without saying whose it is. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "**The offline banner shows.** Rooms and times already loaded stay on screen with their age. Picking a start time and adding the booking need the connection — a room held offline is a room two people think they have."
  },
  "apis": [
   {
    "operationId": "listProducts",
    "contract": "catalogue",
    "purpose": "Room types sold by the hour (`requiresTimeWindow`) and their add-ons",
    "trigger": "onLoad"
   },
   {
    "operationId": "listProductVariants",
    "contract": "catalogue",
    "purpose": "The lengths of a room type, each with its price",
    "trigger": "onLoad"
   },
   {
    "operationId": "listProductStartTimes",
    "contract": "resources",
    "purpose": "Start times free for the room type and length on the date",
    "trigger": "onAction"
   },
   {
    "operationId": "addCartLine",
    "contract": "orders",
    "purpose": "Add the room type for the booked window, then the add-ons",
    "trigger": "onAction"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "productId",
     "from": "WEB-004",
     "optional": true
    },
    {
     "name": "cartId",
     "from": "session"
    }
   ],
   "coldEntry": "Resolves the venue from the site and lists its room types; nothing is booked on arrival."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "client-verified",
   "board": "wireframes/P01 Guest Web.dc.html#web-048",
   "prototype": {
    "file": "sources/designs/guest-rev3-28-september/TICVAI Guest Booking v2.dc.html",
    "rev": "rev 3",
    "verified": "2026-09-28",
    "match": "exact",
    "view": "House of Pages → 'Meeting room by the hour'"
   }
  },
  "apisNote": "Authored 29 September 2026 from the rev 3 decisions and the client prototype view named in `wireframe.prototype`; every operation exists in the contracts (decided 29 September, rev 3).",
  "_platform": {
   "code": "P01",
   "audience": "guest",
   "formFactor": "web",
   "shortName": "Guest Web",
   "name": "Guest Web — Storefront",
   "offlineCapable": false,
   "offlineBanner": {
    "kind": "banner",
    "state": "warning",
    "message": "You're offline. Connect to the internet to book, pay, order or join a queue.",
    "shows": "The moment the connection drops, on every screen, above the screen's own content.",
    "clears": "By itself as soon as the connection is back, with a short \"Back online\" confirmation.",
    "never": "Covers what is already on screen, or appears for a server error — that is the screen's own error state, and a guest told they are offline when the venue is down reconnects for nothing.",
    "provenance": "Decided 12 September 2026 — guest web and guest app behave identically offline and say so with the same banner."
   },
   "app": "guest-web",
   "operator": "guest",
   "targetApp": {
    "app": "guest",
    "name": "TICVAI Guest",
    "shell": "web",
    "siblings": [
     "P02",
     "P05"
    ],
    "note": "**One guest product in three shells.** Web, mobile and kiosk share 73–91% of their operations; the kiosk is the same product in a fixed frame with no keyboard, and is deliberately narrower rather than different.",
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
 "addCartLine": {
  "method": "POST",
  "path": "/carts/{cartId}/lines",
  "contract": "orders",
  "summary": "Add something",
  "permission": null,
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
  "requestBody": "AddCartLineRequest",
  "responds": "Cart"
 },
 "addToWishlist": {
  "method": "POST",
  "path": "/guests/{subjectId}/wishlist",
  "contract": "marketing-crm",
  "summary": "Save an item",
  "permission": null,
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "subject",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "Wishlist"
 },
 "checkBookingEligibility": {
  "method": "POST",
  "path": "/eligibility-checks",
  "contract": "catalogue",
  "summary": "Can this party take part",
  "permission": "PRODUCT_VIEW",
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
  "requestBody": "EligibilityCheckRequest",
  "responds": "EligibilityCheckResult"
 },
 "createResourceHold": {
  "method": "POST",
  "path": "/resource-holds",
  "contract": "resources",
  "summary": "Hold a specific resource picked on the map",
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
  "requestBody": "CreateResourceHoldRequest",
  "responds": "ResourceHold"
 },
 "createSeatHold": {
  "method": "POST",
  "path": "/seat-holds",
  "contract": "seating",
  "summary": "Hold specific seats",
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
  "requestBody": "CreateSeatHoldRequest",
  "responds": "SeatHold"
 },
 "decideRecommendations": {
  "method": "POST",
  "path": "/recommendations/decide",
  "contract": "ai",
  "summary": "Fill a recommendation slot",
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
  "responds": "AiRecommendationResult"
 },
 "evaluatePromotions": {
  "method": "POST",
  "path": "/promotions/evaluate",
  "contract": "promotions",
  "summary": "Evaluate promotions against a cart",
  "permission": "PRICE_VIEW",
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
  "requestBody": "EvaluatePromotionsRequest",
  "responds": "PromotionEvaluation"
 },
 "extendResourceHold": {
  "method": "POST",
  "path": "/resource-holds/{holdId}/extend",
  "contract": "resources",
  "summary": "Extend a resource hold",
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
  "responds": "ResourceHold"
 },
 "getAvailability": {
  "method": "GET",
  "path": "/availability",
  "contract": "catalogue",
  "summary": "Live remaining capacity",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "performanceId",
    "in": "query",
    "required": null
   },
   {
    "name": "channelCapacityId",
    "in": "query",
    "required": null
   },
   {
    "name": "eventId",
    "in": "query",
    "required": null
   },
   {
    "name": "from",
    "in": "query",
    "required": null
   },
   {
    "name": "to",
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
  "responds": "PerformanceAvailabilityPage"
 },
 "getBundle": {
  "method": "GET",
  "path": "/bundles/{bundleId}",
  "contract": "promotions",
  "summary": "Read a bundle with components and allocation",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "Bundle"
 },
 "getCart": {
  "method": "GET",
  "path": "/carts/{cartId}",
  "contract": "orders",
  "summary": "The cart, priced and checked, right now",
  "permission": null,
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
  "responds": "Cart"
 },
 "getMapResourceAvailability": {
  "method": "GET",
  "path": "/resource-availability",
  "contract": "resources",
  "summary": "Every bookable resource on a venue map, free or taken, in one call",
  "permission": "RESOURCE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "mapId",
    "in": "query",
    "required": true
   },
   {
    "name": "from",
    "in": "query",
    "required": true
   },
   {
    "name": "to",
    "in": "query",
    "required": true
   },
   {
    "name": "kind",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "MapResourceAvailability"
 },
 "getPerformance": {
  "method": "GET",
  "path": "/performances/{performanceId}",
  "contract": "catalogue",
  "summary": "Read a performance",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "Performance"
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
 "getPublishedGuidedChoice": {
  "method": "GET",
  "path": "/venues/{venueId}/guided-choice",
  "contract": "white-label",
  "summary": "The venue's published Help me choose",
  "permission": null,
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "GuidedChoice"
 },
 "getResourceHold": {
  "method": "GET",
  "path": "/resource-holds/{holdId}",
  "contract": "resources",
  "summary": "Read a resource hold",
  "permission": "ORDER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "ResourceHold"
 },
 "getSeatAvailability": {
  "method": "GET",
  "path": "/performances/{performanceId}/seat-availability",
  "contract": "seating",
  "summary": "Seat status for a performance",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "sectionCode",
    "in": "query",
    "required": null
   },
   {
    "name": "categoryId",
    "in": "query",
    "required": null
   },
   {
    "name": "availableOnly",
    "in": "query",
    "required": null
   },
   {
    "name": "mode",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "SeatAvailability"
 },
 "getVenueMap": {
  "method": "GET",
  "path": "/venue-maps/{mapId}",
  "contract": "venue-map",
  "summary": "A map with its points and paths",
  "permission": "VENUE_MAP_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "version",
    "in": "query",
    "required": null
   },
   {
    "name": "draft",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "VenueMapDetail"
 },
 "getWishlist": {
  "method": "GET",
  "path": "/guests/{subjectId}/wishlist",
  "contract": "marketing-crm",
  "summary": "Read a guest's saved items",
  "permission": null,
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "subject",
  "parameters": [],
  "requestBody": null,
  "responds": "Wishlist"
 },
 "listBookableVenueMaps": {
  "method": "GET",
  "path": "/bookable-venue-maps",
  "contract": "venue-map",
  "summary": "The published maps of a venue that carry bookable spots",
  "permission": "VENUE_MAP_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "venueId",
    "in": "query",
    "required": true
   },
   {
    "name": "productId",
    "in": "query",
    "required": false
   },
   {
    "name": "kind",
    "in": "query",
    "required": false
   }
  ],
  "requestBody": null,
  "responds": "BookableVenueMaps"
 },
 "listCatalogueBundles": {
  "method": "GET",
  "path": "/catalogue/bundles",
  "contract": "catalogue",
  "summary": "List published catalogue bundles",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "BundleSummary"
 },
 "listPerformances": {
  "method": "GET",
  "path": "/events/{eventId}/performances",
  "contract": "catalogue",
  "summary": "List performances of an event",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "from",
    "in": "query",
    "required": null
   },
   {
    "name": "to",
    "in": "query",
    "required": null
   },
   {
    "name": "categoryId",
    "in": "query",
    "required": null
   },
   {
    "name": "language",
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
 "listProductStartTimes": {
  "method": "GET",
  "path": "/resource-start-times",
  "contract": "resources",
  "summary": "Start times a space sold by the hour can be booked at, for one length on one day",
  "permission": "RESOURCE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "productId",
    "in": "query",
    "required": true
   },
   {
    "name": "variantId",
    "in": "query",
    "required": true
   },
   {
    "name": "date",
    "in": "query",
    "required": true
   },
   {
    "name": "stepMinutes",
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
 "listProductVariants": {
  "method": "GET",
  "path": "/products/{productId}/variants",
  "contract": "catalogue",
  "summary": "List generated variants",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": true,
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
  "requestBody": null,
  "responds": "Page"
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
 "recommendSeats": {
  "method": "POST",
  "path": "/performances/{performanceId}/seat-recommendations",
  "contract": "seating",
  "summary": "Recommend seats for a party",
  "permission": "PRODUCT_VIEW",
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
  "requestBody": "SeatRecommendationRequest",
  "responds": null
 },
 "recordConsentAnswers": {
  "method": "POST",
  "path": "/consent-answers",
  "contract": "marketing-crm",
  "summary": "Answer the consent questions a booking asks",
  "permission": "ORDER_CREATE",
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
  "requestBody": "RecordConsentAnswersRequest",
  "responds": null
 },
 "recordRecommendationEvents": {
  "method": "POST",
  "path": "/recommendations/events",
  "contract": "ai",
  "summary": "Report what happened to recommended items",
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
  "responds": null
 },
 "relinquishResourceHold": {
  "method": "DELETE",
  "path": "/resource-holds/{holdId}",
  "contract": "resources",
  "summary": "Give up a resource hold",
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
  "responds": null
 },
 "relinquishSeatHold": {
  "method": "DELETE",
  "path": "/seat-holds/{holdId}",
  "contract": "seating",
  "summary": "Release a hold",
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
  "responds": null
 },
 "removeFromWishlist": {
  "method": "DELETE",
  "path": "/guests/{subjectId}/wishlist/{itemId}",
  "contract": "marketing-crm",
  "summary": "Remove a saved item",
  "permission": null,
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "subject",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": null
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "AddCartLineRequest": {
  "type": "object",
  "x-ticvai-persistence": "none — request only",
  "required": [
   "variantId",
   "quantity"
  ],
  "properties": {
   "variantId": {
    "type": "string",
    "format": "uuid"
   },
   "quantity": {
    "type": "integer",
    "minimum": 1
   },
   "performanceId": {
    "type": "string",
    "format": "uuid"
   },
   "bookedWindow": {
    "$ref": "#/components/schemas/BookedWindow"
   },
   "recommendationId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The `trackingId` of the ai `decideRecommendations` item this line came from (29 September, build, AI system design 2.2 A step 8), so a purchase is attributed to the recommendation that led to it rather than guessed. Optional; sent by a page or till that shows the engine's recommendations. Not validated against the engine: an unknown id only fails to attribute.\n"
   },
   "tableReservationId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "A table deposit line (decided 29 September, rev 3 REV3-8b): the `fnb.TableReservation` in `awaitingDeposit` this pays for, sent with `variantId` set to the booking's `deposit.variantId` and `quantity` 1. The price is the booking's `deposit.amount`. A booking that is not awaiting a deposit is refused 422 `depositNotDue`.\n"
   },
   "seatIds": {
    "type": "array",
    "maxItems": 50,
    "description": "At most `VenueSettings.seating.maxSeatsPerGuestOrder` seats per booking on a guest channel (default 10, bounds 1 to 50, decided 29 September, rev 3 REV3-7); at most 10 per sale on staff and POS (audit R080 (c)). Over the limit is 422 `seatLimitExceeded`.",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "resourceHoldId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "A `resources.ResourceHold` on a resource the guest picked on a venue map (decided 29 September, rev 3 REV3-15); `variantId` is the placed resource's price-band variant and `quantity` is 1. The hold is the line's capacity; no inventory lease is taken."
   },
   "parentLineId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "For an add-on attaching to a ticket already in the cart. **Removing the parent removes the child** — a locker with no admission is not a sale.\n"
   },
   "attributes": {
    "$ref": "#/components/schemas/OrderLineAttributes"
   }
  }
 },
 "AiRecommendationItem": {
  "type": "object",
  "x-ticvai-persistence": "none — held in jsonb on ai.rec_decision.items, through AiRecommendationItemList",
  "description": "One recommended item. **Carries a Pricing price reference, never a computed price** (AIR-029).",
  "required": [
   "trackingId",
   "rank"
  ],
  "properties": {
   "trackingId": {
    "type": "string",
    "format": "uuid",
    "description": "Echoed on every `recordRecommendationEvents` event and as `orders.addCartLine.recommendationId`, so attribution never guesses."
   },
   "productId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The product recommended. **Exactly one of `productId`, `promotionId` or `couponRef`, `rewardId` or `challengeId` is set, by `kind`** (29 September, build): `offer` carries a promotion or coupon, `reward` a loyalty reward, `challenge` a challenge, every other kind a product."
   },
   "promotionId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "For `offer`, a published promotion the guest is eligible for. Promotions computes the discount at the basket, never the engine."
   },
   "couponRef": {
    "type": "string",
    "nullable": true,
    "description": "For `offer`, a coupon campaign; a code is assigned only when the guest takes it (`promotions.assignCoupon`)."
   },
   "rewardId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "For `reward`, a marketing-crm loyalty reward the guest can redeem."
   },
   "challengeId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "For `challenge`, a marketing-crm challenge the guest can join."
   },
   "kind": {
    "type": "string",
    "enum": [
     "upsell",
     "crossSell",
     "upgrade",
     "bundle",
     "addOn",
     "membership",
     "nextBestOffer",
     "offer",
     "reward",
     "challenge"
    ]
   },
   "rank": {
    "type": "integer",
    "minimum": 1
   },
   "priceRef": {
    "type": "string",
    "nullable": true,
    "description": "The Pricing reference the channel resolves to a price. AI never computes a price."
   },
   "reasonTemplateKey": {
    "type": "string",
    "nullable": true,
    "description": "The template reason (decided 29 September, decision 9): no model writes guest-visible reasons."
   },
   "reasonText": {
    "type": "string",
    "nullable": true,
    "description": "The rendered template in the session locale, where the channel shows reasons."
   },
   "confidenceBand": {
    "type": "string",
    "enum": [
     "high",
     "medium",
     "low"
    ],
    "description": "Design 5.6: a band, never a bare percentage."
   },
   "score": {
    "type": "number",
    "nullable": true,
    "description": "Normalised score. **Returned to staff callers only**; a guest response omits it."
   }
  }
 },
 "AiRecommendationResult": {
  "type": "object",
  "x-ticvai-persistence": "none — written as ai.rec_decision after the response",
  "description": "The recommendation slot's content (design 2.2 A). Empty `items` is a valid answer: the slot stays empty.",
  "required": [
   "decisionId",
   "mode",
   "items",
   "expiresAt"
  ],
  "properties": {
   "decisionId": {
    "type": "string",
    "format": "uuid"
   },
   "placement": {
    "type": "string",
    "enum": [
     "productPage",
     "cart",
     "checkout",
     "postPurchase",
     "preVisit",
     "inVenue",
     "posBasket",
     "kioskBasket",
     "fnbMenu",
     "retailBasket",
     "seatUpgrade",
     "membership",
     "email",
     "homepage",
     "loyalty"
    ]
   },
   "mode": {
    "type": "string",
    "enum": [
     "personalised",
     "contextual",
     "rulesOnly",
     "fallback"
    ]
   },
   "items": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/AiRecommendationItem"
    }
   },
   "expiresAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "BookableVenueMapRef": {
  "type": "object",
  "description": "One published map with bookable spots on it: enough to pick it and call `getVenueMap` (with `publishedVersion`) and `resources.getMapResourceAvailability`.\n",
  "required": [
   "mapId",
   "name",
   "kind",
   "publishedVersion",
   "placedResourceCount"
  ],
  "properties": {
   "mapId": {
    "type": "string",
    "format": "uuid"
   },
   "name": {
    "type": "string"
   },
   "kind": {
    "type": "string",
    "enum": [
     "park",
     "floor",
     "zone",
     "parking"
    ]
   },
   "floorLevel": {
    "type": "integer",
    "nullable": true
   },
   "publishedVersion": {
    "type": "integer",
    "description": "The `VenueMap.publishedVersion` a guest is served; send it to `getVenueMap` as `version`."
   },
   "placedResourceCount": {
    "type": "integer",
    "minimum": 1,
    "description": "Placed resources on the published version."
   },
   "kinds": {
    "type": "array",
    "description": "The kinds of spot on this map, e.g. `[cabana, lounger]`, for the picker's chips.",
    "items": {
     "type": "string",
     "enum": [
      "cabana",
      "lounger",
      "table",
      "pitch",
      "other"
     ]
    }
   }
  }
 },
 "BookableVenueMaps": {
  "type": "object",
  "description": "What `listBookableVenueMaps` returns: the published maps of one venue that carry bookable spots (decided 29 September, readiness close-out). **Bounded by the venue**: a venue has a handful of maps, so the list is capped at 50 rather than paged.\n",
  "required": [
   "venueId",
   "maps"
  ],
  "properties": {
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "maps": {
    "type": "array",
    "maxItems": 50,
    "items": {
     "$ref": "#/components/schemas/BookableVenueMapRef"
    }
   }
  }
 },
 "BookedWindow": {
  "type": "object",
  "nullable": true,
  "x-ticvai-persistence": "none — embedded as window_starts_at and window_ends_at on orders.cart_line and orders.order_line",
  "description": "**The booked time window of an hourly product, such as a meeting room** (decided 29 September, rev 3 REV3-13: meeting rooms by the hour are in scope). The guest picks a date, a length and a start time from `resources.listProductStartTimes`; the length is the product's `length` variant (1 hour, 2 hours, half day, full day), priced per variant, so the price is the variant's. **`endsAt` minus `startsAt` must equal the chosen variant's length** (its `length` dimension value's `durationMinutes`), or the line is refused 422 `windowLengthMismatch`. Required on a product with `catalogue.Product.requiresTimeWindow` true and refused on any other (`windowRequired`, `windowNotAllowed`). The room itself is not named here: the window holds capacity of the room type, and `resources.allocateResources` picks the room at checkout (26 August minute: a guest books a meeting room product, never a raw room).\n",
  "required": [
   "startsAt",
   "endsAt"
  ],
  "properties": {
   "startsAt": {
    "type": "string",
    "format": "date-time"
   },
   "endsAt": {
    "type": "string",
    "format": "date-time",
    "description": "After `startsAt`, on the same venue day."
   }
  }
 },
 "BookingConsentRecord": {
  "type": "object",
  "x-ticvai-persistence": "marketing.booking_consent_record",
  "description": "**One answer to one consent question, as given** (decided 29 September, rev 3 REV3-26). Append-only: a changed answer is a new record and this one gets `supersededAt`. Distinct from `ConsentRecord`, which is a guest's standing decision about a data-processing purpose; this is an answer given for a booking.\n",
  "required": [
   "id",
   "questionId",
   "questionVersion",
   "questionKind",
   "answer",
   "scope",
   "source",
   "answeredAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "questionId": {
    "type": "string",
    "format": "uuid"
   },
   "questionVersion": {
    "type": "integer",
    "minimum": 1
   },
   "questionKind": {
    "$ref": "#/components/schemas/ConsentQuestionKind"
   },
   "answer": {
    "type": "string",
    "enum": [
     "yes",
     "no"
    ]
   },
   "scope": {
    "type": "string",
    "enum": [
     "perPerson",
     "perBooking"
    ]
   },
   "blocksBooking": {
    "type": "boolean",
    "readOnly": true,
    "description": "The answer is the question's `blockingAnswer` at that version."
   },
   "cartId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "cartLineId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "orderId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "description": "Set by `orders.checkoutCart` when the cart becomes an order."
   },
   "orderLineId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true
   },
   "personIndex": {
    "type": "integer",
    "minimum": 0,
    "nullable": true
   },
   "personName": {
    "type": "string",
    "maxLength": 120,
    "nullable": true
   },
   "personSubjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "answeredBySubjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "description": "The guest who answered, from the session. Null for an anonymous cart."
   },
   "answeredByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "description": "The staff member who answered on the guest's behalf."
   },
   "source": {
    "$ref": "#/components/schemas/ConsentSource"
   },
   "answeredAt": {
    "type": "string",
    "format": "date-time"
   },
   "supersededAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005). Operations write it at `venue` scope."
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
 "Bundle": {
  "x-ticvai-persistence": "promotions.bundle + promotions.bundle_component",
  "allOf": [
   {
    "$ref": "#/components/schemas/CreateBundleRequest"
   },
   {
    "type": "object",
    "required": [
     "id",
     "savingsAmount",
     "isActive",
     "hasBeenSold"
    ],
    "properties": {
     "id": {
      "type": "string",
      "format": "uuid"
     },
     "savingsAmount": {
      "allOf": [
       {
        "$ref": "../shared/common.yaml#/components/schemas/Money"
       }
      ],
      "description": "Sum of component list prices less the bundle price."
     },
     "savingsPercentage": {
      "type": "number"
     },
     "hasBeenSold": {
      "type": "boolean",
      "description": "True locks components and allocation against amendment."
     },
     "isActive": {
      "type": "boolean"
     }
    }
   }
  ]
 },
 "BundleSummary": {
  "x-ticvai-persistence": "none — projection over bundle",
  "type": "object",
  "description": "One published catalogue bundle — the signed snapshot terminals pull (ADR-0013). Not `promotions.Bundle`, which is a sellable product made of other products.",
  "required": [
   "version",
   "venueId",
   "publishedAt",
   "publishedBy",
   "contentHash",
   "staleAfter",
   "sizeBytes"
  ],
  "properties": {
   "version": {
    "type": "string"
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "publishedAt": {
    "type": "string",
    "format": "date-time"
   },
   "publishedBy": {
    "type": "string",
    "format": "uuid"
   },
   "contentHash": {
    "type": "string"
   },
   "signatureKeyId": {
    "type": "string",
    "description": "Key that signed this bundle. A terminal offline across a key rotation needs a grace window, or it cannot verify the next bundle.\n"
   },
   "staleAfter": {
    "type": "string",
    "format": "date-time"
   },
   "sizeBytes": {
    "type": "integer"
   },
   "note": {
    "type": "string"
   },
   "appliedByWorkstations": {
    "type": "integer"
   }
  }
 },
 "Cart": {
  "type": "object",
  "x-ticvai-persistence": "orders.cart",
  "required": [
   "id",
   "venueId",
   "channel",
   "status",
   "lines"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "token": {
    "type": "string",
    "readOnly": true,
    "description": "**How an anonymous guest returns to their cart**, including from a recovery email. Rotated on claim, so a link shared before signing in does not reach the account after.\n"
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "channel": {
    "$ref": "../shared/common.yaml#/components/schemas/SalesChannel"
   },
   "subjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Null while anonymous. Set by `claimCart`."
   },
   "status": {
    "$ref": "#/components/schemas/CartStatus"
   },
   "lines": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/CartLine"
    }
   },
   "conflicts": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/CartConflict"
    }
   },
   "consentQuestions": {
    "type": "array",
    "readOnly": true,
    "description": "**The consent questions this cart's products and flow ask** (decided 29 September, rev 3 REV3-26), computed on read at their current version as **the union of each line's published booking flow's `white-label.BookingFlow.settings.consentQuestionIds`** (the flow `getPublishedBookingFlow` resolves for the line's product: product, then category, then the venue's flow for the kind; moved from `BookingFlowConfig`, 29 September W12) **and every line's `catalogue.Product.consentQuestionIds`, each question once**: the flow's first, in its order, then each product's in cart-line order, a question already listed not repeated (its `lineIds` gain the line). The client asks them, in the order given, and sends the answers to `marketing.recordConsentAnswers`; `answered` then turns true. One or several, as the venue chose. `checkoutCart` refuses while a required one is unanswered.\n",
    "items": {
     "allOf": [
      {
       "$ref": "../satellite/marketing-crm.yaml#/components/schemas/ConsentQuestion"
      },
      {
       "type": "object",
       "properties": {
        "lineIds": {
         "type": "array",
         "description": "The cart lines that ask it. Empty for a question the flow asks.",
         "items": {
          "type": "string",
          "format": "uuid"
         }
        },
        "answered": {
         "type": "boolean",
         "description": "Every person (for `perPerson`) or the booking (for `perBooking`) has an answer."
        }
       }
      }
     ]
    }
   },
   "subtotal": {
    "x-ticvai-column": "net_amount",
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "discountTotal": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "taxTotal": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "total": {
    "x-ticvai-column": "gross_amount",
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "appliedPromotionIds": {
    "type": "array",
    "description": "**Re-evaluated on every read.** A promotion that expired while the cart sat must not still be applied at checkout, and a promotion that became applicable should be.\n",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "couponCodes": {
    "type": "array",
    "readOnly": true,
    "description": "The promo codes the guest entered through `applyCartPromoCode` (decided 28 September, audit R073 (e)). **Sent as `couponCodes` on every promotions evaluation of this cart**, so a code is re-checked on each read like any promotion; a code that stops qualifying stays listed here and its promotion drops out of `appliedPromotionIds`.\n",
    "items": {
     "type": "string",
     "maxLength": 100
    }
   },
   "expiresAt": {
    "type": "string",
    "format": "date-time",
    "description": "The earliest lease expiry in the cart, or the cart's own window where it holds none."
   },
   "extensionsUsed": {
    "type": "integer",
    "readOnly": true
   },
   "maxExtensions": {
    "type": "integer",
    "readOnly": true
   },
   "locale": {
    "type": "string"
   },
   "createdAt": {
    "type": "string",
    "format": "date-time"
   },
   "updatedAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "CartConflict": {
  "type": "object",
  "x-ticvai-persistence": "none — computed on read",
  "description": "2.9.5. Golf at 13:00 and karting at 13:00 for the same guest. **A prompt, not a refusal** — a party of four may legitimately split, and refusing would be wrong more often than right.\n",
  "properties": {
   "kind": {
    "type": "string",
    "enum": [
     "overlappingTime",
     "sameSessionDifferentVenue",
     "exceedsPartySize",
     "requiresPrerequisite",
     "consentBlocksBooking"
    ]
   },
   "lineIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "message": {
    "type": "string"
   },
   "isBlocking": {
    "type": "boolean",
    "description": "Most are not. `requiresPrerequisite` is — an add-on with no ticket to attach to cannot be sold. So is `consentBlocksBooking`: a consent question answered with the answer the venue set to block the booking (decided 29 September, rev 3 REV3-26).\n"
   }
  }
 },
 "CartLine": {
  "type": "object",
  "x-ticvai-persistence": "orders.cart_line",
  "required": [
   "id",
   "variantId",
   "quantity"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "variantId": {
    "type": "string",
    "format": "uuid"
   },
   "productName": {
    "type": "string",
    "readOnly": true
   },
   "quantity": {
    "type": "integer",
    "minimum": 1
   },
   "performanceId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "bookedWindow": {
    "$ref": "#/components/schemas/BookedWindow"
   },
   "recommendationId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The `trackingId` of the ai `decideRecommendations` item this line came from (29 September, build, AI system design 2.2 A step 8), so a purchase is attributed to the recommendation that led to it rather than guessed. Set from `addCartLine`; checkout copies it to the order line.\n"
   },
   "tableReservationId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Set on a table deposit line only (decided 29 September, rev 3 REV3-8b): the `fnb.TableReservation` this line secures. Priced from the deposit the booking snapshotted, not from the variant. Becomes an `orders.deposit` row at checkout, not revenue. A table booking with no deposit never has a line (rev 3 REV3-8).\n"
   },
   "seatIds": {
    "type": "array",
    "maxItems": 50,
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "resourceHoldId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The `resources.ResourceHold` this line buys (decided 29 September, rev 3 REV3-15). While set, `leaseExpiresAt` is the hold's `expiresAt` and `inventoryHoldId` is null."
   },
   "attributes": {
    "$ref": "#/components/schemas/OrderLineAttributes"
   },
   "parentLineId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The line this add-on is attached to, from `AddCartLineRequest.parentLineId`. Kept on the line because **removing the parent removes the child**, and `removeCartLine` has to be able to find the children.\n"
   },
   "overridePrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "overrideReason": {
    "type": "string",
    "nullable": true,
    "enum": [
     "priceMatch",
     "serviceRecovery",
     "negotiated",
     "damagedGoods",
     "staffSale",
     "error"
    ],
    "description": "BL-085. **An operator could apply an approved discount and not enter a price.** A price match against a competitor and a service-recovery gesture are not discounts off a list — they are a number somebody decided.\n**Escalated above a configured threshold, and the reason is a closed set**: a free-text override reason is an override nobody can report on, and this is the field an auditor reads first.\n"
   },
   "feeKind": {
    "type": "string",
    "nullable": true,
    "enum": [
     "booking",
     "transaction",
     "service",
     "delivery",
     "convenience",
     "cancellation"
    ],
    "description": "**A fee is a line, not an adjustment.** `orders` already separates a service charge from a tip for the reason that applies here: **a guest is entitled to see what they are being charged for**, and a fee folded into the ticket price is a fee nobody can question.\nItemised at checkout, taxed on its own code, and refundable separately — **a cancellation fee is usually the one thing not refunded**, which only works if it is its own line.\n"
   },
   "unitPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "lineTotal": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "inventoryHoldId": {
    "type": "string",
    "nullable": true,
    "description": "The capacity held for this line — a `catalogue.InventoryHold.id`, typed as that id is. **Null for a product with no capacity** — a t-shirt needs stock, not a lease.\n"
   },
   "leaseExpiresAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "Shown to the guest. *\"Your seats are held for 6 minutes\"* is better than discovering it at checkout.\n"
   },
   "isAvailable": {
    "type": "boolean",
    "readOnly": true,
    "description": "Re-checked on every read. **A line can become unavailable while the cart sits** — a lease expiring is not the same as the product selling out, and both land here.\n"
   }
  }
 },
 "CartStatus": {
  "type": "string",
  "enum": [
   "active",
   "expiring",
   "expired",
   "abandoned",
   "checkedOut"
  ]
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
 "ConsentSource": {
  "type": "string",
  "enum": [
   "guestApp",
   "website",
   "kiosk",
   "pos",
   "callCentre",
   "import",
   "agentRecorded",
   "cookieBanner",
   "checkout"
  ],
  "description": "`checkout` (30 September, M18-15): an opt-in ticked beside the terms at checkout, carried on orders `checkoutCart` `marketingConsents[]` and recorded by `recordCheckoutConsents`, bound to the order and the verified contact. `cookieBanner` (29 September, build; BL-073 §4b): a decision made on the cookie banner or preference centre and moved onto the guest by `claimDeviceConsent`. Kept apart from `website`, a form submission, because the audit trail (2.6.56) has to tell the two apart."
 },
 "CreateBundleRequest": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "required": [
   "code",
   "name",
   "venueId",
   "kind",
   "price",
   "components",
   "allocation"
  ],
  "properties": {
   "code": {
    "type": "string",
    "maxLength": 64
   },
   "name": {
    "type": "string",
    "maxLength": 200
   },
   "description": {
    "type": "string",
    "maxLength": 1000
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "kind": {
    "$ref": "#/components/schemas/BundleKind"
   },
   "price": {
    "x-ticvai-column": "list_price",
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "components": {
    "type": "array",
    "minItems": 0,
    "items": {
     "$ref": "#/components/schemas/BundleComponent"
    }
   },
   "choiceGroups": {
    "type": "array",
    "description": "Dynamic bundles (3.5.10). A bundle may carry fixed components and choice groups at once — a family pass with fixed parking and two groups the guest chooses from. **The bundle price does not move with the choice** (ADR-0019).\n",
    "items": {
     "$ref": "#/components/schemas/BundleChoiceGroup"
    }
   },
   "allocation": {
    "type": "object",
    "required": [
     "method",
     "components"
    ],
    "properties": {
     "method": {
      "allOf": [
       {
        "$ref": "#/components/schemas/AllocationMethod"
       }
      ],
      "default": "proRataListPrice",
      "description": "Proportional to list price by default. The rounding remainder in the currency's minor unit goes to the first component (decided 28 September, audit R101).\n"
     },
     "components": {
      "type": "array",
      "items": {
       "$ref": "#/components/schemas/AllocationComponent"
      }
     }
    }
   },
   "validFrom": {
    "type": "string",
    "format": "date-time"
   },
   "validTo": {
    "type": "string",
    "format": "date-time"
   },
   "campaignId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The commercial campaign (`promotions.campaign`) the bundle is sold under. (DM5, 29 September: data model for the agreed operations)"
   },
   "ownerPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The bundle owner (Bundle Definition & Setup). (DM5, 29 September: data model for the agreed operations)"
   },
   "category": {
    "type": "string",
    "maxLength": 100,
    "nullable": true,
    "description": "The bundle category the setup screen files it under. (DM5, 29 September: data model for the agreed operations)"
   },
   "isStandaloneProduct": {
    "type": "boolean",
    "default": true,
    "description": "Whether the bundle appears as a product in its own right, or only as an offer on another product. (DM5, 29 September: data model for the agreed operations)"
   },
   "isRecommendedAtCheckout": {
    "type": "boolean",
    "default": false,
    "description": "Whether checkout recommends the bundle. (DM5, 29 September: data model for the agreed operations)"
   },
   "requiredVariantIds": {
    "type": "array",
    "nullable": true,
    "items": {
     "type": "string",
     "format": "uuid"
    },
    "description": "Products that must already be in the basket for the bundle to be sold (the setup screen's \"requires another product\"). (DM5, 29 September: data model for the agreed operations)"
   }
  }
 },
 "CreateResourceHoldRequest": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "required": [
   "id",
   "mapId",
   "resourceIds",
   "from",
   "to"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "description": "Client-generated UUIDv7, as a seat hold's."
   },
   "mapId": {
    "type": "string",
    "format": "uuid",
    "description": "The published venue map the guest picked from."
   },
   "resourceIds": {
    "type": "array",
    "minItems": 1,
    "maxItems": 10,
    "description": "Placed resources on that map, e.g. two adjoining loungers. All or none are held.",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "from": {
    "type": "string",
    "format": "date-time"
   },
   "to": {
    "type": "string",
    "format": "date-time"
   },
   "partySize": {
    "type": "integer",
    "minimum": 1,
    "nullable": true,
    "description": "Checked against each resource's `capacity`; above it the hold is refused `422`."
   },
   "ttlSeconds": {
    "type": "integer",
    "minimum": 60,
    "maximum": 1800,
    "default": 480,
    "description": "8 minutes by default, 30 in all with extensions (audit R169), as a seat hold."
   },
   "subjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   }
  }
 },
 "CreateSeatHoldRequest": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "required": [
   "id",
   "performanceId",
   "seatIds"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "performanceId": {
    "type": "string",
    "format": "uuid"
   },
   "seatIds": {
    "type": "array",
    "minItems": 1,
    "maxItems": 50,
    "description": "50 is the ceiling of the venue setting, not the limit a caller gets. On a guest channel the limit is `VenueSettings.seating.maxSeatsPerGuestOrder` (default 10, bounds 1 to 50, decided 29 September, rev 3 REV3-7); on a staff channel it stays 10 per sale (audit R080 (c)), as POS-002 shows. Either is refused with `422` `seat-limit-exceeded`.\n",
    "items": {
     "type": "string"
    }
   },
   "ttlSeconds": {
    "type": "integer",
    "minimum": 60,
    "maximum": 1800,
    "default": 480,
    "description": "**8 minutes by default, extendable to 30 in all** (decided 28 September, audit R169). Left out, the hold lasts 480 seconds. No hold, first grant or extended, outlives 1800 seconds from its creation.\n"
   },
   "subjectId": {
    "type": "string",
    "format": "uuid"
   }
  }
 },
 "EligibilityCheckRequest": {
  "type": "object",
  "description": "Request only.",
  "required": [
   "productIds",
   "party"
  ],
  "properties": {
   "productIds": {
    "type": "array",
    "minItems": 1,
    "items": {
     "type": "string"
    }
   },
   "party": {
    "type": "array",
    "minItems": 1,
    "items": {
     "$ref": "#/components/schemas/EligibilityDeclaration"
    }
   }
  }
 },
 "EligibilityCheckResult": {
  "type": "object",
  "x-ticvai-persistence": "none — computed per request",
  "required": [
   "eligible"
  ],
  "properties": {
   "eligible": {
    "type": "boolean"
   },
   "guests": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "index": {
       "type": "integer"
      },
      "eligible": {
       "type": "boolean"
      },
      "reasons": {
       "type": "array",
       "items": {
        "type": "string",
        "enum": [
         "tooYoung",
         "tooOld",
         "tooShort",
         "tooTall",
         "needsAdult",
         "needsGuardianSignature",
         "needsSwimmer"
        ]
       }
      }
     }
    }
   },
   "waiverRequired": {
    "type": "boolean"
   }
  }
 },
 "EligibilityDeclaration": {
  "type": "object",
  "description": "What a guest declares about one member of the party. Declared, not measured.",
  "properties": {
   "ageBand": {
    "type": "string",
    "enum": [
     "infant",
     "child",
     "junior",
     "adult",
     "senior"
    ],
    "description": "Infant under 3, child 3–12, junior 13–17, adult 18–59, senior 60+."
   },
   "ageYears": {
    "type": "integer",
    "nullable": true
   },
   "heightBandIndex": {
    "type": "integer",
    "nullable": true,
    "description": "Which band of the rule's `heightBandsCm`, counting from 0."
   },
   "confidentSwimmer": {
    "type": "boolean",
    "nullable": true,
    "deprecated": true,
    "description": "Superseded by the consent record for the product's swim consent question (decided 29 September, rev 3 REV3-26); see `ProductEligibilityRule.swimAbility`."
   },
   "guardianSigned": {
    "type": "boolean",
    "default": false
   }
  }
 },
 "EvaluatePromotionsRequest": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "required": [
   "venueId",
   "channel",
   "lines"
  ],
  "properties": {
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "channel": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/SalesChannel"
     }
    ],
    "description": "Where the sale is being made. Matched against `PromotionConditions.channels`, so both sides use the one shared vocabulary.\n"
   },
   "subjectId": {
    "type": "string",
    "format": "uuid"
   },
   "membershipTierId": {
    "type": "string",
    "format": "uuid"
   },
   "couponCodes": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "evaluateAt": {
    "type": "string",
    "format": "date-time",
    "description": "For back-office testing of a rule before publishing."
   },
   "orderId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The order (`orders.sales_order`) being priced for payment. Sent only by the order service when it confirms an order; when present the evaluation writes one `promotions.promotion_evaluation_trace` row for it. (decided 29 September, writers pass)"
   },
   "lines": {
    "type": "array",
    "minItems": 1,
    "items": {
     "type": "object",
     "required": [
      "lineId",
      "variantId",
      "quantity",
      "unitPrice"
     ],
     "properties": {
      "lineId": {
       "type": "string"
      },
      "variantId": {
       "type": "string",
       "format": "uuid"
      },
      "performanceId": {
       "type": "string",
       "format": "uuid"
      },
      "quantity": {
       "type": "integer",
       "minimum": 1
      },
      "unitPrice": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      }
     }
    }
   }
  }
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
 "GuidedChoice": {
  "x-ticvai-persistence": "whitelabel.guided_choice + whitelabel.guided_choice_question + whitelabel.guided_choice_answer",
  "type": "object",
  "description": "**Help me choose (decided 29 September, rev 3 REV3-11).** A venue's short set of questions that ends on a result card opening the booking flow, product, category or event that fits. Each question has a few answers with a title, a one-line body, an icon and an optional badge; **the answer the guest picks on the last question decides the result**, and each earlier answer carries a target too, so a one-question setting still ends on a result. Venue configuration, never hard-coded: set up in Venue Management, off unless the venue publishes one.\n**Two sources, one review.** `manual` is written by staff; `aiSuggested` is proposed by the `ai` service from the venue's uploaded products (a suggestion, reviewed and published by a person, never auto-published). Both arrive as `draft`.\n**Help me choose filters the catalogue (decided 29 September, W4).** With `behaviour` `filter`, the default, each answer's `filter` narrows the products the guest sees (web, mobile and kiosk alike, through catalogue `listProducts` and `searchCatalogue` `guidedAnswerIds`), with a \"Show everything\" link; `recommend` keeps the rev 3 result card from the last answer's `target`. **It is never a consent step**: an answer may pre-fill a REV3-26 consent question (`consentPrefill`), which the guest still confirms, so the question is not asked twice and the consent stays explicit.\n",
  "required": [
   "id",
   "venueId",
   "name",
   "mode",
   "questions",
   "status",
   "source"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "UUIDv7."
   },
   "venueId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "From the path of `createGuidedChoice`."
   },
   "name": {
    "type": "string",
    "maxLength": 80,
    "description": "Staff-facing name, e.g. \"Water park day planner\". Not shown to guests."
   },
   "mode": {
    "type": "string",
    "enum": [
     "button",
     "popupOnArrival",
     "off"
    ],
    "default": "button",
    "description": "**How the guest reaches it (rev 3 REV3-11).** `button` puts a Help me choose button on the booking page; `popupOnArrival` also opens it once on the guest's first arrival at the booking page (whether it was seen is kept on the device only); `off` keeps a published choice configured but not shown.\n"
   },
   "showBanner": {
    "type": "boolean",
    "default": true,
    "description": "The dark banner under the products (\"Choose from the experiences above or let us help you decide\") with a Help me choose button. Ignored when `mode` is `off`."
   },
   "behaviour": {
    "type": "string",
    "enum": [
     "filter",
     "recommend"
    ],
    "default": "filter",
    "description": "**`filter` (default) narrows the list; `recommend` ends on one result card (decided 29 September, W4).** With `filter`, every answer needs a `filter` and `target` is optional; with `recommend`, every answer on the last question needs a `target`. `publishGuidedChoice` refuses the other case with 422.\n"
   },
   "showEverything": {
    "type": "boolean",
    "default": true,
    "description": "The \"Show everything\" link under a filtered list, which clears the answers (W4)."
   },
   "questions": {
    "type": "array",
    "minItems": 1,
    "maxItems": 4,
    "description": "**One to four questions** (decided 29 September, W4: the Deep Dive reference asks three or four; rev 3 REV3-11 allowed two). Shown in `sortOrder`.\n",
    "items": {
     "type": "object",
     "required": [
      "title",
      "sortOrder",
      "answers"
     ],
     "properties": {
      "id": {
       "type": "string",
       "format": "uuid",
       "readOnly": true,
       "description": "UUIDv7. The row's own key."
      },
      "title": {
       "$ref": "#/components/schemas/LocalisedText"
      },
      "kind": {
       "type": "string",
       "enum": [
        "choice",
        "yesNo",
        "age",
        "level",
        "certification"
       ],
       "default": "choice",
       "description": "**What the question asks (decided 29 September, W4).** `choice` free answers; `yesNo` two answers (e.g. \"Can everyone swim?\"); `age` answers carrying an age range; `level` answers carrying a level tag; `certification` answers saying whether the guest holds a certificate (e.g. a diving licence). The kind decides which `filter` fields its answers use.\n"
      },
      "sortOrder": {
       "type": "integer",
       "minimum": 0
      },
      "answers": {
       "type": "array",
       "minItems": 2,
       "maxItems": 4,
       "description": "Two to four answers; the prototype shows three (proposed, client to correct, rev 3 REV3-11).",
       "items": {
        "type": "object",
        "required": [
         "title",
         "sortOrder"
        ],
        "properties": {
         "id": {
          "type": "string",
          "format": "uuid",
          "readOnly": true,
          "description": "UUIDv7. The row's own key."
         },
         "title": {
          "$ref": "#/components/schemas/LocalisedText"
         },
         "body": {
          "allOf": [
           {
            "$ref": "#/components/schemas/LocalisedText"
           }
          ],
          "description": "The one-liner under the title, at most 140 characters in each language."
         },
         "icon": {
          "type": "string",
          "maxLength": 40,
          "nullable": true,
          "description": "An icon name from the guest app's icon set."
         },
         "badge": {
          "allOf": [
           {
            "$ref": "#/components/schemas/LocalisedText"
           }
          ],
          "nullable": true,
          "description": "Optional, e.g. \"Best value\". At most 24 characters in each language."
         },
         "sortOrder": {
          "type": "integer",
          "minimum": 0
         },
         "target": {
          "allOf": [
           {
            "$ref": "#/components/schemas/GuidedChoiceTarget"
           }
          ],
          "nullable": true,
          "description": "Required with `behaviour` `recommend` on the last question; optional with `filter`, where it is the card shown above the filtered list."
         },
         "filter": {
          "type": "object",
          "nullable": true,
          "description": "**What this answer keeps in the list (decided 29 September, W4).** Every field set must hold; answers to different questions are combined with AND. Required with `behaviour` `filter`. The server applies it (catalogue `guidedAnswerIds`), so web, mobile and kiosk show the same list.\n",
          "properties": {
           "productIds": {
            "type": "array",
            "items": {
             "type": "string",
             "format": "uuid"
            }
           },
           "productCategoryIds": {
            "type": "array",
            "items": {
             "type": "string",
             "format": "uuid"
            }
           },
           "segmentTags": {
            "type": "array",
            "description": "Catalogue `Product.segmentTags`, e.g. a level tag.",
            "items": {
             "type": "string"
            }
           },
           "minAgeYears": {
            "type": "integer",
            "minimum": 0,
            "nullable": true
           },
           "maxAgeYears": {
            "type": "integer",
            "minimum": 0,
            "nullable": true,
            "description": "With `minAgeYears`, checked against each product's age rule (catalogue `ProductEligibilityRule`)."
           },
           "requiresSwimmer": {
            "type": "boolean",
            "nullable": true,
            "description": "False hides products whose eligibility needs a swimmer; true keeps only those."
           },
           "certificationCode": {
            "type": "string",
            "nullable": true,
            "maxLength": 40,
            "description": "Keeps products that need this certificate, or with `holdsCertification` false, hides them."
           },
           "holdsCertification": {
            "type": "boolean",
            "nullable": true
           }
          }
         },
         "consentPrefill": {
          "type": "object",
          "nullable": true,
          "description": "**Pre-fills a REV3-26 consent question from this answer (decided 29 September, W4).** The guest still ticks it at the consent step; nothing is recorded as consent until they do.\n",
          "required": [
           "consentQuestionId",
           "answer"
          ],
          "properties": {
           "consentQuestionId": {
            "type": "string",
            "format": "uuid"
           },
           "answer": {
            "type": "boolean"
           }
          }
         },
         "result": {
          "type": "object",
          "nullable": true,
          "description": "The result card when this answer decides the result. Absent fields fall back to the target's own name, summary and image.",
          "properties": {
           "title": {
            "$ref": "#/components/schemas/LocalisedText"
           },
           "body": {
            "$ref": "#/components/schemas/LocalisedText"
           },
           "imageAssetRef": {
            "type": "string",
            "format": "uuid",
            "nullable": true
           }
          }
         }
        }
       }
      }
     }
    }
   },
   "status": {
    "allOf": [
     {
      "$ref": "#/components/schemas/GuidedChoiceStatus"
     }
    ],
    "readOnly": true
   },
   "source": {
    "type": "string",
    "enum": [
     "manual",
     "aiSuggested"
    ],
    "readOnly": true,
    "description": "`manual` when staff created it; `aiSuggested` when the `ai` service proposed it (a service caller). Kept after a person edits a suggestion, so a report can say how many AI proposals were published."
   },
   "suggestionRef": {
    "type": "string",
    "nullable": true,
    "readOnly": true,
    "description": "For `aiSuggested`, the id of the `ai` job that proposed it. Null for `manual`."
   },
   "publishedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true
   },
   "publishedBy": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "description": "The person who published it. Never a service."
   },
   "updatedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   }
  }
 },
 "GuidedChoiceStatus": {
  "type": "string",
  "description": "**Draft until a person publishes it (decided 29 September, rev 3 REV3-11).** Guests see only a `published` choice. An AI-proposed choice arrives as `draft` and is never published by the system. Moves as `states/guided-choice.yaml` says: `publishGuidedChoice` and `unpublishGuidedChoice`, and a publish returns the venue's previously published choice to `draft`.\n",
  "enum": [
   "draft",
   "published"
  ],
  "default": "draft"
 },
 "GuidedChoiceTarget": {
  "x-ticvai-persistence": "none — embedded",
  "type": "object",
  "description": "**What an answer opens (decided 29 September, rev 3 REV3-11).** A product (its kind picks the booking flow), a product category (its tickets, as `ticketCategories` shows them), an event, or a module such as `membership`. Each id must belong to the choice's venue and be on sale or enabled when the choice is published, or `publishGuidedChoice` refuses it.\n",
  "required": [
   "kind"
  ],
  "properties": {
   "kind": {
    "type": "string",
    "enum": [
     "product",
     "productCategory",
     "event",
     "module",
     "bookingFlow"
    ]
   },
   "productId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Required when `kind` is `product`. A catalogue `Product`."
   },
   "productCategoryId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Required when `kind` is `productCategory`. A catalogue `ProductCategory`."
   },
   "eventId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Required when `kind` is `event`."
   },
   "moduleKey": {
    "allOf": [
     {
      "$ref": "#/components/schemas/ModuleKey"
     }
    ],
    "nullable": true,
    "description": "Required when `kind` is `module`. The module must be enabled."
   },
   "bookingFlowId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Required when `kind` is `bookingFlow` (decided 29 September, W12; BUILD-YOUR-EXPERIENCE \"each answer points to one booking flow\"). One of the venue's enabled `BookingFlow`s."
   }
  }
 },
 "LocalisedText": {
  "x-ticvai-persistence": "none — jsonb column",
  "type": "object",
  "additionalProperties": {
   "type": "string"
  }
 },
 "MapResourceAvailability": {
  "x-ticvai-persistence": "none — computed from placed resources, bookings, holds and blocks",
  "type": "object",
  "description": "What `getMapResourceAvailability` returns: **every placed resource on one map, for one window, in one answer** (rev 3 REV3-15).\n",
  "required": [
   "mapId",
   "mapVersion",
   "from",
   "to",
   "resources"
  ],
  "properties": {
   "mapId": {
    "type": "string",
    "format": "uuid"
   },
   "mapVersion": {
    "type": "integer",
    "description": "The published `venue-map` version the placements were read from; the client checks it against the map it cached."
   },
   "from": {
    "type": "string",
    "format": "date-time"
   },
   "to": {
    "type": "string",
    "format": "date-time"
   },
   "totals": {
    "type": "object",
    "properties": {
     "total": {
      "type": "integer"
     },
     "available": {
      "type": "integer"
     },
     "held": {
      "type": "integer"
     },
     "booked": {
      "type": "integer"
     },
     "unavailable": {
      "type": "integer"
     }
    }
   },
   "resources": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "resourceId",
      "label",
      "status"
     ],
     "properties": {
      "resourceId": {
       "type": "string",
       "format": "uuid"
      },
      "placedResourceId": {
       "type": "string",
       "format": "uuid",
       "description": "The `venue-map.PlacedResource` it was read from."
      },
      "label": {
       "type": "string",
       "description": "As on the map, e.g. `B09`."
      },
      "kind": {
       "$ref": "#/components/schemas/ResourceKind"
      },
      "zone": {
       "type": "string"
      },
      "capacity": {
       "type": "integer"
      },
      "priceBandCode": {
       "type": "string"
      },
      "variantId": {
       "type": "string",
       "format": "uuid",
       "description": "What the cart line names to buy it."
      },
      "price": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      },
      "status": {
       "type": "string",
       "enum": [
        "available",
        "held",
        "booked",
        "unavailable"
       ],
       "description": "`unavailable` covers maintenance, a blackout, a block and a placement marked not bookable; the map greys all of them the same way.\n"
      }
     }
    }
   }
  }
 },
 "OrderLineAttributes": {
  "type": "object",
  "nullable": true,
  "additionalProperties": true,
  "x-ticvai-persistence": "none — embedded as attributes (jsonb) on orders.cart_line and orders.order_line",
  "description": "Open attributes of a line, kept from the cart to the order line. **`transport` is the one with a defined shape** (decided 29 September, rev 3 REV3-21); other keys are free.\n",
  "properties": {
   "transport": {
    "$ref": "#/components/schemas/TransportLineAttributes"
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
 "Performance": {
  "x-ticvai-persistence": "catalogue.performance",
  "type": "object",
  "required": [
   "id",
   "eventId",
   "startsAt",
   "endsAt",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "eventId": {
    "type": "string",
    "format": "uuid"
   },
   "startsAt": {
    "type": "string",
    "format": "date-time"
   },
   "endsAt": {
    "type": "string",
    "format": "date-time"
   },
   "approvalRequestId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "BL-048. **The approval chain and the occurrence lifecycle sat on different entities**, so neither was complete: `states/performance.yaml` models scheduled, onSale, soldOut, suspended, cancelled and completed properly, and nothing said which of those transitions somebody had to sign.\n**Set on the transition that needs it, not on the performance.** Publishing a performance is routine; cancelling one that has sold is the act somebody signs — and binding approval to the whole entity would have required a signature to reschedule a wet Tuesday.\n"
   },
   "requiresApprovalToCancel": {
    "type": "boolean",
    "default": true,
    "description": "**Cancelling a sold performance is the one transition that needs a name against it.** `assessProductChange` already answers how many tickets are affected; this decides who has to look at that number before the button works.\n"
   },
   "status": {
    "type": "string",
    "enum": [
     "scheduled",
     "onSale",
     "soldOut",
     "suspended",
     "cancelled",
     "completed"
    ]
   },
   "admissionRulesId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "seatMapId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "language": {
    "type": "string",
    "nullable": true,
    "maxLength": 35,
    "pattern": "^[A-Za-z]{2,3}(-[A-Za-z0-9]{1,8})*$",
    "description": "The language the performance is given in, as a BCP 47 tag (`en`, `ar`, `fr`, `de`, `zh`, `ru`, `ar-AE`). **A guided tour at 10:00 in French and one at 10:00 in Arabic are two performances**, so a guest who picks a language sees only the tours in it (`listPerformances` `language`). Null when the performance is not language-specific (decided 29 September, rev 3 REV3-17).\n"
   },
   "format": {
    "type": "string",
    "nullable": true,
    "maxLength": 40,
    "description": "How it is presented, free text the venue chooses, e.g. `2D`, `3D`, `IMAX`, `subtitled`. A cinema screening shows language and format together. Null when it does not apply (decided 29 September, rev 3 REV3-17).\n"
   }
  }
 },
 "PerformanceAvailability": {
  "type": "object",
  "x-ticvai-persistence": "none — computed on read from catalogue.channel_capacity and live leases",
  "description": "Remaining capacity of one channel capacity of one performance (rev 3 REV3-1).",
  "required": [
   "channelCapacityId",
   "performanceId",
   "capacity",
   "sold",
   "leased",
   "remaining"
  ],
  "properties": {
   "channelCapacityId": {
    "type": "string",
    "format": "uuid"
   },
   "performanceId": {
    "type": "string",
    "format": "uuid",
    "description": "The performance this channel capacity belongs to (`ChannelCapacity.performanceId`), so rows for several performances can be told apart."
   },
   "startsAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true,
    "description": "The performance's start, so a time tile and its day part (morning, afternoon, evening, split at the venue's `BookingFlowConfig.dayPartBoundaries`) come from this one call (rev 3 REV3-1)."
   },
   "capacity": {
    "type": "integer"
   },
   "sold": {
    "type": "integer"
   },
   "leased": {
    "type": "integer",
    "description": "Held by terminals but not yet sold."
   },
   "remaining": {
    "type": "integer"
   },
   "byChannel": {
    "type": "array",
    "description": "Per-channel position. A guest seeing sold out online while units remain at the counter is correct behaviour, not a defect.\n",
    "items": {
     "type": "object",
     "properties": {
      "channel": {
       "$ref": "#/components/schemas/Channel"
      },
      "allocated": {
       "type": "integer"
      },
      "sold": {
       "type": "integer"
      },
      "remaining": {
       "type": "integer"
      }
     }
    }
   }
  }
 },
 "PerformanceAvailabilityPage": {
  "x-ticvai-persistence": "none — computed on read",
  "description": "The `getAvailability` answer (named 29 September, rev 3 REV3-1).",
  "allOf": [
   {
    "$ref": "../shared/common.yaml#/components/schemas/Page"
   },
   {
    "type": "object",
    "properties": {
     "items": {
      "type": "array",
      "items": {
       "$ref": "#/components/schemas/PerformanceAvailability"
      }
     }
    }
   }
  ]
 },
 "PlacedResource": {
  "type": "object",
  "x-ticvai-persistence": "venuemap.placed_resource",
  "description": "**A bookable resource where it stands on the map** (decided 29 September, rev 3 REV3-15 and GAP-C2): cabana B09 on the Beach, 15 guests, Large. The resource itself, its bookings and its holds live in `resources`; this row says where it is drawn and what the guest sees. Written into the working draft by `importVenueGeometry` or `setPlacedResource`, copied into the `VenueMapVersion` snapshot at publish. A guest picks one on the published map, holds it with `resources.createResourceHold` and buys it. **Supersedes audit R073 (c) and the 26 August minute for resources on an ingested map.**\n",
  "required": [
   "id",
   "mapId",
   "resourceId",
   "label",
   "kind",
   "zone",
   "capacity",
   "priceBandCode",
   "position"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "mapId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "From the path of the operation that writes it."
   },
   "resourceId": {
    "type": "string",
    "format": "uuid",
    "x-ticvai-references": "resources.Resource",
    "description": "The `resources.Resource` this is. **Availability, holds and bookings are keyed by this**, so a republished map with the cabana moved keeps its bookings.\n"
   },
   "label": {
    "type": "string",
    "maxLength": 40,
    "x-ticvai-unique": "map",
    "description": "What the guest sees and taps, e.g. `B09`. **Unique on the map**, compared without case after digit normalisation; normally the resource's `code`.\n"
   },
   "kind": {
    "type": "string",
    "enum": [
     "cabana",
     "lounger",
     "table",
     "pitch",
     "other"
    ],
    "description": "A subset of `resources.ResourceKind`, the kinds a guest books from a map. A `table` here is a non-dining spot (a beach or event table) sold like a cabana; restaurant tables stay `fnb` table reservations (decided 29 September, rev 3 GAP-C2)."
   },
   "zone": {
    "type": "string",
    "maxLength": 80,
    "description": "The area the guest reads it by, e.g. `Beach`, `River`, `Terrace`."
   },
   "capacity": {
    "type": "integer",
    "minimum": 1,
    "maximum": 500,
    "description": "Guests it takes, e.g. 15. Shown on the map and checked against the party at hold."
   },
   "priceBandCode": {
    "type": "string",
    "maxLength": 40,
    "description": "The band it sells in, e.g. `Large`, one of the `priceBands` given at import. The band's `variantId` prices it; the map holds no price.\n"
   },
   "variantId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "x-ticvai-references": "catalogue.ProductVariant",
    "description": "Resolved from the price band. What a cart line for this resource names."
   },
   "position": {
    "type": "object",
    "required": [
     "x",
     "y"
    ],
    "description": "Drawing coordinates of its label anchor, as on `VenuePoint`.",
    "properties": {
     "x": {
      "type": "number"
     },
     "y": {
      "type": "number"
     }
    }
   },
   "boundary": {
    "type": "array",
    "nullable": true,
    "description": "The shape drawn, as a polygon in drawing coordinates. Null for a pin.",
    "items": {
     "type": "object",
     "properties": {
      "x": {
       "type": "number"
      },
      "y": {
       "type": "number"
      }
     }
    }
   },
   "isBookable": {
    "type": "boolean",
    "default": true,
    "description": "False keeps it on the map and off sale, e.g. a cabana kept for staff use. Shown greyed.\n"
   }
  }
 },
 "Point": {
  "type": "object",
  "required": [
   "x",
   "y"
  ],
  "properties": {
   "x": {
    "type": "number"
   },
   "y": {
    "type": "number"
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
 "ProductStartTime": {
  "x-ticvai-persistence": "none — computed on read",
  "type": "object",
  "description": "One start time a room type can be booked at for the chosen length (rev 3 REV3-13).",
  "required": [
   "startsAt",
   "endsAt",
   "freeCount"
  ],
  "properties": {
   "startsAt": {
    "type": "string",
    "format": "date-time"
   },
   "endsAt": {
    "type": "string",
    "format": "date-time",
    "description": "`startsAt` plus the variant's `durationMinutes`; the cart line's `bookedWindow.endsAt`."
   },
   "freeCount": {
    "type": "integer",
    "minimum": 1,
    "description": "Resources of the room type free for the whole window. Only times with at least one are returned."
   }
  }
 },
 "ProductVariant": {
  "x-ticvai-persistence": "catalogue.variant",
  "type": "object",
  "required": [
   "id",
   "productId",
   "sku",
   "axisValues",
   "isActive"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "productId": {
    "type": "string",
    "format": "uuid"
   },
   "sku": {
    "type": "string"
   },
   "axisValues": {
    "type": "object",
    "additionalProperties": {
     "type": "string"
    }
   },
   "name": {
    "type": "string",
    "maxLength": 150,
    "nullable": true,
    "description": "**Taken from their variant tables, 20 September.** `axisValues` gives `{size: L}` and no string a guest can read. A menu showing *Large* needs somewhere for the word to live.\n"
   },
   "barcode": {
    "type": "string",
    "maxLength": 64,
    "nullable": true,
    "description": "**Taken from their variant tables, 20 September.** `catalogue.alternative_code` is a partner's own code for a variant and **requires `partnerId`**, so a manufacturer's EAN had nowhere to go. One per variant against many per variant is a different cardinality and belongs in a different place — and a POS scan should be an indexed column lookup, not a join.\n"
   },
   "isDefault": {
    "type": "boolean",
    "default": false,
    "description": "Taken from their variant tables. Which variant a product page opens on. Ours had no way to say, so a three-size drink opened on whichever row sorted first.\n"
   },
   "isActive": {
    "type": "boolean",
    "description": "False when retired. Retired variants are never deleted — orders reference them."
   },
   "description": {
    "allOf": [
     {
      "$ref": "#/components/schemas/LocalisedText"
     }
    ],
    "nullable": true,
    "description": "**Who this ticket type is for and what it includes**, shown behind the (i) on each Adult, Child, Senior or Infant row (decided 29 September, 23SEP-6). Each language value at most 300 characters; longer is a `400`. Set with `updateProductVariant`. Whether the guest screen shows it is `BookingFlowConfig.cardInfo` (white-label).\n"
   }
  }
 },
 "PromotionEvaluation": {
  "x-ticvai-persistence": "none — computed",
  "type": "object",
  "required": [
   "totalDiscount",
   "lines",
   "applied",
   "rejected"
  ],
  "properties": {
   "totalDiscount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "lines": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "lineId",
      "originalPrice",
      "discountedPrice",
      "discount"
     ],
     "properties": {
      "lineId": {
       "type": "string"
      },
      "originalPrice": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      },
      "discountedPrice": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      },
      "discount": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      },
      "appliedPromotionIds": {
       "type": "array",
       "items": {
        "type": "string",
        "format": "uuid"
       }
      }
     }
    }
   },
   "applied": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "promotionId",
      "promotionCode",
      "discount"
     ],
     "properties": {
      "promotionId": {
       "type": "string",
       "format": "uuid"
      },
      "promotionCode": {
       "type": "string"
      },
      "promotionName": {
       "type": "string"
      },
      "discount": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      },
      "couponCode": {
       "type": "string",
       "nullable": true
      }
     }
    }
   },
   "rejected": {
    "type": "array",
    "description": "Promotions that matched the products but did not apply, with the reason. This is what a cashier reads to a guest who expected a discount.\n",
    "items": {
     "type": "object",
     "required": [
      "promotionCode",
      "reason"
     ],
     "properties": {
      "promotionCode": {
       "type": "string"
      },
      "promotionName": {
       "type": "string"
      },
      "reason": {
       "type": "string",
       "enum": [
        "conditionsNotMet",
        "supersededByBetterOffer",
        "exclusivePromotionApplied",
        "redemptionLimitReached",
        "budgetExhausted",
        "outsideValidPeriod",
        "wrongChannel",
        "membershipRequired",
        "couponRequired"
       ]
      },
      "detail": {
       "type": "string"
      }
     }
    }
   }
  }
 },
 "RecordConsentAnswersRequest": {
  "type": "object",
  "x-ticvai-persistence": "none — request only",
  "required": [
   "cartId",
   "answers",
   "source",
   "answeredAt"
  ],
  "properties": {
   "cartId": {
    "type": "string",
    "format": "uuid",
    "description": "The cart the answers are given for. `checkoutCart` binds them to its order."
   },
   "answers": {
    "type": "array",
    "minItems": 1,
    "maxItems": 200,
    "items": {
     "type": "object",
     "required": [
      "questionId",
      "questionVersion",
      "answer"
     ],
     "properties": {
      "questionId": {
       "type": "string",
       "format": "uuid"
      },
      "questionVersion": {
       "type": "integer",
       "minimum": 1,
       "description": "The version the guest was shown, from `Cart.consentQuestions`."
      },
      "answer": {
       "type": "string",
       "enum": [
        "yes",
        "no"
       ]
      },
      "cartLineId": {
       "type": "string",
       "format": "uuid",
       "nullable": true,
       "description": "For a `perPerson` question, the line the person is on."
      },
      "personIndex": {
       "type": "integer",
       "minimum": 0,
       "nullable": true,
       "description": "For a `perPerson` question, the person's row in that line's `eligibilityDeclaration`, counting from 0."
      },
      "personName": {
       "type": "string",
       "maxLength": 120,
       "nullable": true
      },
      "personSubjectId": {
       "type": "string",
       "format": "uuid",
       "nullable": true,
       "description": "Where the person is a known guest, such as the booker or a family member."
      }
     }
    }
   },
   "source": {
    "$ref": "#/components/schemas/ConsentSource"
   },
   "answeredAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "ResourceHold": {
  "x-ticvai-persistence": "resources.resource_hold",
  "type": "object",
  "description": "**A guest's pick on the map, held while they pay** (decided 29 September, rev 3 REV3-15). The resource counterpart of `seating.SeatHold`: named resources, short-lived, converted by the order rather than released. States in `states/resource-hold.yaml`.\n",
  "required": [
   "id",
   "mapId",
   "resourceIds",
   "from",
   "to",
   "status",
   "createdAt",
   "expiresAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "mapId": {
    "type": "string",
    "format": "uuid"
   },
   "resourceIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "from": {
    "type": "string",
    "format": "date-time"
   },
   "to": {
    "type": "string",
    "format": "date-time"
   },
   "partySize": {
    "type": "integer",
    "nullable": true
   },
   "status": {
    "type": "string",
    "enum": [
     "held",
     "converted",
     "released",
     "expired"
    ]
   },
   "totalPrice": {
    "x-ticvai-column": "gross_amount",
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "heldByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "subjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "orderId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Set when the order converts it."
   },
   "extensionCount": {
    "type": "integer",
    "default": 0
   },
   "createdAt": {
    "type": "string",
    "format": "date-time"
   },
   "expiresAt": {
    "type": "string",
    "format": "date-time"
   },
   "scopePath": {
    "type": "string",
    "description": "The partition key (ADR-0005), written at `venue` scope."
   }
  }
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
 "SeatAvailability": {
  "x-ticvai-persistence": "none — computed from seat, hold and block",
  "type": "object",
  "required": [
   "performanceId",
   "seatMapId",
   "renderMode",
   "totals",
   "seats"
  ],
  "properties": {
   "performanceId": {
    "type": "string",
    "format": "uuid"
   },
   "seatMapId": {
    "type": "string",
    "format": "uuid"
   },
   "renderMode": {
    "type": "string",
    "enum": [
     "graphical",
     "list"
    ],
    "description": "The mode the server actually used. With `mode=auto` this is how a client knows what it got: `list` means the map has no geometry (the seat map's `noGeometry` state), so the client sells from categories and best-available groups and does not draw a plan. `graphical` means every seat carries `position`.\n"
   },
   "totals": {
    "type": "object",
    "properties": {
     "total": {
      "type": "integer"
     },
     "available": {
      "type": "integer"
     },
     "held": {
      "type": "integer"
     },
     "sold": {
      "type": "integer"
     },
     "blocked": {
      "type": "integer"
     },
     "buffered": {
      "type": "integer"
     }
    }
   },
   "byCategory": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "categoryId": {
       "type": "string",
       "format": "uuid"
      },
      "available": {
       "type": "integer"
      },
      "sold": {
       "type": "integer"
      },
      "price": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      }
     }
    }
   },
   "sections": {
    "type": "array",
    "description": "The map's sections with what a guest screen needs to show the view from each (decided 29 September, rev 3 23SEP-14): the photo where the venue supplied one, otherwise null and the client renders the view from `boundary` and the seat positions. In this response so WEB-007 and GST-049 need no second call.\n",
    "items": {
     "type": "object",
     "required": [
      "code",
      "name"
     ],
     "properties": {
      "code": {
       "type": "string"
      },
      "name": {
       "type": "string"
      },
      "viewAssetId": {
       "type": "string",
       "format": "uuid",
       "nullable": true,
       "description": "As `Section.viewAssetId`. Null means render the view from geometry."
      },
      "boundary": {
       "type": "array",
       "nullable": true,
       "items": {
        "$ref": "#/components/schemas/Point"
       },
       "description": "As `Section.boundary`. Null when `renderMode` is `list`."
      }
     }
    }
   },
   "seats": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "seatId",
      "status"
     ],
     "properties": {
      "seatId": {
       "type": "string"
      },
      "status": {
       "$ref": "#/components/schemas/SeatStatus"
      },
      "categoryId": {
       "type": "string",
       "format": "uuid",
       "nullable": true
      },
      "displayLabel": {
       "type": "string",
       "description": "What the guest sees, e.g. `A2-7-11`, as on `Seat`."
      },
      "position": {
       "allOf": [
        {
         "$ref": "#/components/schemas/Point"
        }
       ],
       "nullable": true,
       "description": "The seat's coordinates on the map, as on `Seat`. Present when `renderMode` is `graphical`; null when it is `list`."
      }
     }
    }
   }
  }
 },
 "SeatHold": {
  "x-ticvai-persistence": "seating.seat_hold",
  "type": "object",
  "required": [
   "id",
   "performanceId",
   "seatIds",
   "status",
   "createdAt",
   "expiresAt"
  ],
  "properties": {
   "id": {
    "type": "string"
   },
   "performanceId": {
    "type": "string",
    "format": "uuid"
   },
   "seatIds": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "bufferedSeatIds": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Neighbours implicitly held by a seating rule."
   },
   "status": {
    "type": "string",
    "enum": [
     "held",
     "converted",
     "released",
     "expired"
    ]
   },
   "totalPrice": {
    "x-ticvai-column": "gross_amount",
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "heldByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "subjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "extensionCount": {
    "type": "integer"
   },
   "createdAt": {
    "type": "string",
    "format": "date-time"
   },
   "expiresAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "SeatRecommendation": {
  "x-ticvai-persistence": "none — computed",
  "type": "object",
  "required": [
   "seatIds",
   "totalPrice",
   "isContiguous",
   "rank"
  ],
  "properties": {
   "seatIds": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "displayLabels": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "totalPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "categoryId": {
    "type": "string",
    "format": "uuid"
   },
   "isContiguous": {
    "type": "boolean"
   },
   "rank": {
    "type": "integer",
    "description": "Best first."
   },
   "rationale": {
    "type": "string",
    "description": "Why this option was chosen — closest to stage, best value in category, only contiguous block remaining. Shown to a call-centre agent, not the guest.\n"
   }
  }
 },
 "SeatRecommendationRequest": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "required": [
   "partySize",
   "strategy"
  ],
  "properties": {
   "partySize": {
    "type": "integer",
    "minimum": 1,
    "maximum": 50
   },
   "strategy": {
    "$ref": "#/components/schemas/SeatRecommendationStrategy"
   },
   "categoryIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "maxPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "accessibleCount": {
    "type": "integer",
    "default": 0,
    "description": "Wheelchair spaces in the party. Companions are added automatically."
   },
   "maxOptions": {
    "type": "integer",
    "default": 3,
    "maximum": 10
   }
  }
 },
 "SeatRecommendationStrategy": {
  "type": "string",
  "enum": [
   "bestAvailable",
   "bestValue",
   "closestToStage",
   "accessible",
   "contiguous"
  ]
 },
 "SeatStatus": {
  "type": "string",
  "enum": [
   "available",
   "held",
   "sold",
   "blocked",
   "buffered",
   "unavailable"
  ]
 },
 "VenueMap": {
  "type": "object",
  "x-ticvai-persistence": "venuemap.map",
  "description": "A park map, or a floor plan. **Several per venue** — a guest on the second floor should not be shown the ground floor's toilets.\n",
  "required": [
   "id",
   "name",
   "venueId",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "name": {
    "type": "string"
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "Derived from `venueId`. Not sent by a client."
   },
   "kind": {
    "type": "string",
    "enum": [
     "park",
     "floor",
     "zone",
     "parking"
    ]
   },
   "floorLevel": {
    "type": "integer",
    "nullable": true
   },
   "status": {
    "type": "string",
    "enum": [
     "draft",
     "published",
     "archived"
    ],
    "readOnly": true,
    "description": "`draft` on create. Moves through `publishVenueMap` (`states/venue-map.yaml`), never by sending a value.\n"
   },
   "publishedVersion": {
    "type": "integer",
    "nullable": true,
    "readOnly": true,
    "description": "The `VenueMapVersion.version` guests are served. Null until the first publish.\n"
   },
   "graphVersion": {
    "type": "integer",
    "readOnly": true,
    "description": "**Bumped by a publish or a closure**, and returned as `VenueMapGraph.version`. Separate from `publishedVersion` because a closure changes the routes without creating a map version, and a closure that looked like a publish would lie about what changed.\n"
   },
   "isGeoreferenced": {
    "type": "boolean",
    "readOnly": true,
    "description": "**Whether a guest can be located on it.** Without a georeference the map is a picture — useful, and not navigable.\n"
   },
   "baseAssetId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "**The illustrated map a guest actually sees**, held in `assets` like any other media.\n**This is not the CAD drawing.** The drawing gives geometry — where things are, and how they connect. The base image is a designed illustration with the venue's own styling, and the two are different artefacts that happen to describe the same place. A park hands you an architect's plan and a beautiful painted map, and **the guest wants the second while the platform needs the first.**\nNull is valid. A map with geometry and no illustration renders as shapes — plain, and navigable.\n",
    "x-ticvai-references": "assets.MediaAsset"
   },
   "baseImageAlignment": {
    "type": "object",
    "nullable": true,
    "description": "**How the illustration lines up with the geometry.** They are drawn at different scales by different people, and a point placed on the plan lands in the wrong place on the painting unless something reconciles them.\nTwo known points is enough. **Without this the illustration is a picture behind the map rather than the map itself.**\n",
    "properties": {
     "imageWidthPx": {
      "type": "integer"
     },
     "imageHeightPx": {
      "type": "integer"
     },
     "anchors": {
      "type": "array",
      "minItems": 2,
      "maxItems": 4,
      "items": {
       "type": "object",
       "properties": {
        "planX": {
         "type": "number"
        },
        "planY": {
         "type": "number"
        },
        "imageX": {
         "type": "number"
        },
        "imageY": {
         "type": "number"
        }
       }
      }
     }
    }
   },
   "tileSetRef": {
    "type": "string",
    "nullable": true,
    "readOnly": true,
    "description": "Where a base image is large enough to need zoom levels. **A 12,000-pixel park map is not something a phone downloads on arrival**, and a guest opening the map on venue wifi at the gate is the worst moment to send twenty megabytes.\nGenerated from the base asset. Null means the image is small enough to serve whole.\n"
   },
   "boundsGeoJson": {
    "type": "string",
    "nullable": true
   },
   "graphStatus": {
    "type": "string",
    "readOnly": true,
    "enum": [
     "notBuilt",
     "connected",
     "disconnected",
     "partial"
    ],
    "description": "**Whether every public point can actually be reached.** Computed at publish.\n`disconnected` means a point has no path to it at all — a toilet nobody can walk to is a toilet that does not exist. `partial` means every point is reachable and at least one only by steps, which is a different and quieter failure: **the map works until a wheelchair user opens it.**\n"
   }
  }
 },
 "VenueMapDetail": {
  "type": "object",
  "description": "19.2.55. **The whole map in one call**, so a client caches it and filters locally.",
  "properties": {
   "version": {
    "type": "integer",
    "nullable": true,
    "readOnly": true,
    "description": "**The published version these points and paths belong to**, which is the number a client caches and sends back as `version`. It can differ from `map.publishedVersion` when an older version was asked for. Null when the draft was read.\n"
   },
   "map": {
    "$ref": "#/components/schemas/VenueMap"
   },
   "points": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/VenuePoint"
    }
   },
   "paths": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/VenuePath"
    }
   },
   "resources": {
    "type": "array",
    "description": "The bookable resources placed on this version of the map (rev 3 REV3-15). Empty on a map that carries none.\n",
    "items": {
     "$ref": "#/components/schemas/PlacedResource"
    }
   }
  }
 },
 "VenuePath": {
  "type": "object",
  "x-ticvai-persistence": "venuemap.path",
  "description": "19.2.56. **The navigation graph.** The map supplies it; routing over it is a client concern, because a phone with the map cached routes offline and a server round-trip per step does not.\n",
  "required": [
   "id",
   "mapId",
   "fromPointId",
   "toPointId"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "mapId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "From the path of the operation that writes the path."
   },
   "fromPointId": {
    "type": "string",
    "format": "uuid"
   },
   "toPointId": {
    "type": "string",
    "format": "uuid"
   },
   "geometry": {
    "type": "string",
    "nullable": true,
    "description": "The centreline this edge follows, as an encoded polyline. **A walkway in a drawing is a polygon and a route is a line down the middle of it**, so extraction thins the polygon to a centreline and splits it at every fork.\nNull where the path was drawn on screen as a straight connection, which is normal for a venue with no walkway layer.\n"
   },
   "distanceMetres": {
    "type": "number",
    "nullable": true,
    "readOnly": true,
    "description": "Computed by the server from `geometry` and the georeference. **Along the centreline, not point to point.** A path that curves round a lake is longer than the distance between its ends, and a guest told 80 metres who walks 200 stops trusting the map.\nRequires a georeference for real units; without one, distances are in drawing units and routing still works because **only the ratios matter to a shortest path.**\n"
   },
   "isStepFree": {
    "type": "boolean",
    "default": true,
    "description": "**The single most important attribute on this object.** A wheelchair user routed up a staircase has been failed by the map, not by the venue.\n"
   },
   "isIndoor": {
    "type": "boolean",
    "default": false
   },
   "restrictedByPointId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "**Where a path is one-way, it is because of a thing on it — not because of the path.** Removed `isOneWay` on 18 August: a pedestrian walkway has no direction, and the three cases that look one-way are all a gate or a queue.\nA turnstile is one-way and `access.AccessPoint.direction` already says so. A queue line is one-way and `queue` owns it. **Putting the restriction on the path duplicated both and would have drifted from them** — a gate reconfigured to bidirectional would leave a path still marked one-way, and nothing would have noticed.\nSet where a path passes through an access point. The router reads the direction from the point.\n"
   },
   "closedReason": {
    "type": "string",
    "nullable": true,
    "readOnly": true,
    "description": "Set by `setPathClosure` during works or an incident, never by sending it here. **A closed path removes routes rather than hiding the path**, so a guest sees why rather than wondering where it went.\n"
   }
  }
 },
 "VenuePoint": {
  "type": "object",
  "x-ticvai-persistence": "venuemap.point",
  "description": "19.2.57 to 19.2.60. **What a venue places on the map**, and what a guest taps.\n",
  "required": [
   "id",
   "mapId",
   "kind",
   "name",
   "position"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "mapId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "From the path of the operation that writes the point."
   },
   "kind": {
    "type": "string",
    "enum": [
     "ride",
     "attraction",
     "show",
     "restaurant",
     "cafe",
     "shop",
     "kiosk",
     "toilet",
     "babyCare",
     "prayerRoom",
     "firstAid",
     "atm",
     "lockers",
     "entrance",
     "exit",
     "emergencyExit",
     "assemblyPoint",
     "parking",
     "guestServices",
     "smokingArea",
     "waterFountain",
     "chargingPoint",
     "photoSpot",
     "junction",
     "other"
    ],
    "description": "**A closed set, and `emergencyExit` is separate from `exit` on purpose.** An exit is where a guest leaves; an emergency exit is where they are sent, and a map that cannot tell them apart is a map that routes a normal departure through a fire door.\n**`junction` is the one that is not a point of interest.** A path connects two points, so a fork in a walkway with nothing at it still needs a node — otherwise every bend has to be named as a destination, and a guest browsing the map sees forty entries called *Path junction 12*.\n**Junctions are hidden from guests and present in the graph.** Generated by extraction where paths meet; a venue never places one by hand.\n"
   },
   "name": {
    "type": "string",
    "x-ticvai-unique": "venue",
    "description": "**Unique per venue** (decided 28 September, audit R108). Two points on a venue's maps never share a name, compared without case, so *Toilets North* names one place; `setVenuePoint` refuses a duplicate with `409` `duplicate-code`. Junctions are named by extraction and are exempt.\n"
   },
   "nameLocalised": {
    "type": "object",
    "nullable": true,
    "additionalProperties": {
     "type": "string"
    }
   },
   "position": {
    "type": "object",
    "required": [
     "x",
     "y"
    ],
    "description": "Drawing coordinates. **Latitude and longitude are derived from the georeference**, not stored, so a map that is re-georeferenced does not need every point moved.\n",
    "properties": {
     "x": {
      "type": "number"
     },
     "y": {
      "type": "number"
     }
    }
   },
   "outletId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "For a restaurant, cafe, shop or kiosk. **Tapping it should open the menu**, and that only works if the map knows which outlet it is.\n"
   },
   "productId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "For a ride or show — links to wait times and to booking. **What a guest is offered from any point, including a restaurant or a shop, is `featuredOffer`** (29 September, MOB-4); this link stays for wait times.\n"
   },
   "accessPointId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "For an entrance or exit. **This is what makes 3.2.64 work** — live admission statistics drawn on the point they came from.\n"
   },
   "isStepFree": {
    "type": "boolean",
    "default": true,
    "description": "Whether the point itself can be reached without steps. **The same name as `VenuePath.isStepFree`, because it is the same concept** (it was `isAccessible` until the 26 September audit). **Placed on the point rather than inferred from the path**, because a step-free route to a building with steps at the door is not a step-free route.\n"
   },
   "openingHours": {
    "type": "string",
    "nullable": true
   },
   "iconRef": {
    "type": "string",
    "nullable": true
   },
   "isActive": {
    "type": "boolean",
    "default": true
   },
   "isNavigable": {
    "type": "boolean",
    "default": true,
    "description": "Whether a route may pass through it. **False for a point that marks a place without being reachable** — a stage a guest cannot walk onto, a zone label.\n"
   },
   "isDestination": {
    "type": "boolean",
    "default": true,
    "description": "**Whether a guest may be routed *to* it, and whether it appears in a list of places.** False for a `junction`, which exists in the graph and nowhere else.\nSeparate from `isNavigable` because the two differ: a junction is navigable and not a destination, and a fenced landmark is a destination you can be shown but not walked into.\n"
   },
   "description": {
    "type": "object",
    "nullable": true,
    "additionalProperties": {
     "type": "string",
     "maxLength": 1000
    },
    "description": "**What the guest reads on Item Detail** (29 September, MOB-4). Keyed by locale, like `nameLocalised`. One screen now serves rides, shows, restaurants and shops (GST-004 and GST-006 merged), and it opens from the map pin, so the point carries the words rather than each kind borrowing them from a different module. Set on BO-094.\n"
   },
   "media": {
    "type": "array",
    "maxItems": 12,
    "description": "**The gallery on Item Detail** (29 September, MOB-4): images and short clips from the asset library, first `isPrimary` shown on the map card. Assets are referenced, never copied, so a replaced photo changes everywhere.\n",
    "items": {
     "type": "object",
     "required": [
      "assetId",
      "kind"
     ],
     "properties": {
      "assetId": {
       "type": "string",
       "format": "uuid",
       "x-ticvai-references": "assets.media_asset"
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
       "default": false
      },
      "altText": {
       "type": "string",
       "nullable": true,
       "maxLength": 200
      }
     }
    }
   },
   "featuredOffer": {
    "type": "object",
    "nullable": true,
    "required": [
     "kind",
     "id"
    ],
    "description": "**The product card on Item Detail, for every kind of point** (29 September, MOB-4). `productId` above links a ride or show to its wait times; this is what the guest is offered from the point, and it may be a bundle: a restaurant offers *meal combo with admission* (`promotions` bundle with an admission and a meal component), which checks out in about three steps (GST-004 → GST-056 → GST-041). A point with none shows no card. **Referenced, not priced here**: the card reads `catalogue.getProduct` or `promotions.getBundle` for the live price and availability.\n",
    "properties": {
     "kind": {
      "type": "string",
      "enum": [
       "product",
       "bundle"
      ]
     },
     "id": {
      "type": "string",
      "format": "uuid",
      "description": "The `catalogue.product` id or the `promotions.bundle` id, by `kind`."
     },
     "label": {
      "type": "string",
      "nullable": true,
      "maxLength": 40,
      "description": "The button text, e.g. *Buy meal combo*. Null uses the product's own call to action."
     }
    }
   },
   "typicalDurationMinutes": {
    "type": "integer",
    "nullable": true,
    "minimum": 1,
    "maximum": 600,
    "description": "**How long a visit to this point usually takes**, ride time and queue excluded (29 September, MOB-6). The visit planner lays out a day with it; the queue comes from `queue.getWaitTimes` on the day. Null for a point the planner never places (a toilet).\n"
   },
   "interestTags": {
    "type": "array",
    "maxItems": 12,
    "description": "**What a guest who says they like this would like here** (29 September, MOB-6): the planner matches the guest's interests against these. A closed list so that the Plan tab's interest chips and the venue's tags are the same words.\n",
    "items": {
     "type": "string",
     "enum": [
      "thrill",
      "family",
      "kids",
      "water",
      "animals",
      "shows",
      "culture",
      "shopping",
      "dining",
      "relaxing",
      "photo",
      "adventure",
      "sport",
      "nightlife",
      "indoor"
     ]
    }
   },
   "cuisineTags": {
    "type": "array",
    "maxItems": 8,
    "description": "**For dining points** (restaurant, cafe, kiosk; 29 September, MOB-6). The planner places meals at points whose cuisine the party chose, at meal times. Free text codes such as `arabic`, `indian`, `italian`, `fastFood`, `vegetarian`, `halal` — cuisines are too many to close, and a wrong enum is worse than an unmatched tag. **Read per venue**: the planner matches a guest's cuisine only against the points of the venue that day is at (30 September, MoM 4.7).\n",
    "items": {
     "type": "string",
     "maxLength": 30
    }
   },
   "retailTags": {
    "type": "array",
    "maxItems": 8,
    "description": "**For retail points** (shop, and a kiosk that sells goods rather than food; 30 September client meeting, MoM 4.7: retail and kiosk shops join F&B as venue-linked planner options). The planner places a shop stop at points whose tags the party chose, on the day of this point's venue only. Free text codes such as `souvenirs`, `toys`, `apparel`, `photo`, `essentials`, for the same reason as `cuisineTags`. A kiosk may carry both lists.\n",
    "items": {
     "type": "string",
     "maxLength": 30
    }
   }
  }
 },
 "Wishlist": {
  "type": "object",
  "required": [
   "subjectId",
   "items"
  ],
  "x-ticvai-persistence": "none — wrapper. The items are the table, keyed by subject",
  "properties": {
   "subjectId": {
    "type": "string",
    "format": "uuid"
   },
   "items": {
    "type": "array",
    "x-ticvai-persistence": "marketing.wishlist_item",
    "items": {
     "type": "object",
     "required": [
      "id",
      "variantId",
      "addedAt",
      "isAvailable"
     ],
     "properties": {
      "id": {
       "type": "string",
       "format": "uuid"
      },
      "variantId": {
       "type": "string",
       "format": "uuid"
      },
      "productName": {
       "type": "string"
      },
      "performanceId": {
       "type": "string",
       "format": "uuid",
       "nullable": true
      },
      "performanceStartsAt": {
       "type": "string",
       "format": "date-time",
       "nullable": true
      },
      "price": {
       "x-ticvai-column": "list_price",
       "$ref": "../shared/common.yaml#/components/schemas/Money",
       "description": "The variant's current list price when the wishlist is read. Stored as `list_price` (naming-and-style 5.1 bans a bare `price` column); the wire keeps `price`."
      },
      "imageAssetRef": {
       "type": "string",
       "nullable": true
      },
      "isAvailable": {
       "type": "boolean",
       "description": "False where the product has been withdrawn or the performance has passed. Returned rather than dropped — a guest who saved something and finds it silently gone assumes the feature is broken.\n"
      },
      "unavailableReason": {
       "type": "string",
       "nullable": true
      },
      "note": {
       "type": "string",
       "nullable": true
      },
      "addedAt": {
       "type": "string",
       "format": "date-time"
      }
     }
    }
   }
  }
 }
}
```
