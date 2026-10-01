# P01-cart-checkout-01 — P01 · Cart & Checkout

**5 screens · 34 operations · 51 schemas · 7 permissions**

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
  `GUEST_VIEW, GUEST_VIEW_PII, ORDER_CREATE, ORDER_REPRINT, ORDER_VIEW, PRICE_VIEW, PRODUCT_VIEW`. A control nobody can use must say so,
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
| `WEB-010` | Shopping Cart | statusTracker | 14 | 7 | — |
| `WEB-011` | Guest Details & Attendee Forms | listDetail | 14 | 7 | — |
| `WEB-012` | Checkout — Payment | statusTracker | 6 | 3 | — |
| `WEB-013` | Booking Confirmation | statusTracker | 3 | 2 | — |
| `WEB-014` | Pay for a Booking | statusTracker | 2 | 1 | — |

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "WEB-010",
  "name": "Shopping Cart",
  "module": "Cart & Checkout",
  "requiresModule": "ticketing",
  "wave": 1,
  "capability": "C02",
  "implementation": {
   "app": "guest-web",
   "route": "/cart-and-checkout/shopping-cart",
   "component": "apps/guest-web/src/routes/cart-and-checkout/ShoppingCartDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "WEB-005",
    "WEB-006",
    "WEB-007",
    "WEB-008",
    "WEB-016",
    "WEB-047",
    "WEB-048",
    "WEB-049"
   ],
   "exitTo": [
    "WEB-001",
    "WEB-011",
    "WEB-012",
    "WEB-013",
    "WEB-016",
    "WEB-030"
   ],
   "transitions": [
    {
     "to": "WEB-012",
     "trigger": "Checkout — Payment",
     "carries": [
      "orderId",
      "paymentId"
     ],
     "provenance": "derived — WEB-012 declares entryState.params orderId, paymentId and WEB-010 holds orderId, paymentId, so an edge into it carries them"
    },
    {
     "to": "WEB-013",
     "trigger": "Booking Confirmation",
     "carries": [
      "orderId"
     ],
     "provenance": "derived — WEB-013 declares entryState.params orderId and WEB-010 holds orderId, so an edge into it carries them"
    },
    {
     "to": "WEB-016",
     "trigger": "Login / Register",
     "carries": [
      "subjectId"
     ],
     "provenance": "derived — WEB-016 declares entryState.params challengeId, subjectId and WEB-010 holds subjectId, so an edge into it carries them"
    },
    {
     "to": "WEB-012",
     "trigger": "Guest code proved or signed in: straight to payment (details skipped)",
     "provenance": "decided 29 September 2026, W1",
     "carries": [
      "orderId",
      "paymentId"
     ]
    },
    {
     "to": "WEB-011",
     "trigger": "Answers attendee forms and consent, only where the cart needs them",
     "provenance": "flow F01 step 5→6, F02 step 3→4, F55 step 1→2"
    },
    {
     "to": "WEB-030",
     "trigger": "They transfer three tickets",
     "provenance": "flow F55 step 3→4",
     "operation": "checkoutCart",
     "carries": [
      "orderId"
     ]
    }
   ]
  },
  "density": "compact",
  "pattern": "statusTracker",
  "patternReason": "`getCart` reads one record and nothing reads a population — the screen is about that one thing",
  "purpose": "Review and confirm what is being bought.",
  "layout": {
   "template": "detail",
   "regions": [
    {
     "name": "contentBody",
     "slot": "record",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The cart",
       "bindsTo": "Cart",
       "columns": [
        "Cart.id",
        "Cart.token",
        "Cart.venueId",
        "Cart.channel",
        "Cart.subjectId",
        "Cart.status",
        "Cart.lines",
        "Cart.conflicts",
        "Cart.subtotal",
        "Cart.discountTotal",
        "Cart.taxTotal",
        "Cart.total",
        "Cart.appliedPromotionIds",
        "Cart.couponCodes",
        "Cart.expiresAt",
        "Cart.extensionsUsed",
        "Cart.maxExtensions"
       ],
       "operation": "getCart",
       "provenance": "contract orders.yaml GET /carts/{cartId}"
      },
      {
       "kind": "detailPanel",
       "label": "The coupon code",
       "bindsTo": "CouponCode",
       "columns": [
        "CouponCode.code",
        "CouponCode.campaignId",
        "CouponCode.batchId",
        "CouponCode.status",
        "CouponCode.assignedSubjectId",
        "CouponCode.redemptionCount",
        "CouponCode.maxRedemptions",
        "CouponCode.discount",
        "CouponCode.invalidReason",
        "CouponCode.validFrom",
        "CouponCode.validTo",
        "CouponCode.redeemedAt",
        "CouponCode.redeemedOrderId",
        "CouponCode.scopePath"
       ],
       "operation": "getCouponCode",
       "provenance": "contract promotions.yaml GET /coupon-codes/{code}"
      },
      {
       "kind": "textField",
       "label": "Promo code",
       "bindsTo": "ApplyCartPromoCodeRequest.code",
       "operation": "applyCartPromoCode",
       "notes": "**Applied to the cart at once** with `applyCartPromoCode` (POST /carts/{cartId}/promo-codes, body `{code}`; decided 28 September, audit R073 (e)). The two refusals read differently: 422 `promoCodeInvalid` says the code does not exist, was voided or is used up; 422 `promoCodeNotApplicable` says the code is real but nothing in this cart qualifies. A 410 `cartExpired` sends the guest back to rebuild the cart. Accepted codes are listed from `Cart.couponCodes` and re-priced on every read.",
       "provenance": "contract orders.yaml POST /carts/{cartId}/promo-codes"
      },
      {
       "kind": "secondaryButton",
       "label": "Apply code",
       "operation": "applyCartPromoCode",
       "provenance": "contract orders.yaml POST /carts/{cartId}/promo-codes"
      },
      {
       "kind": "banner",
       "bindsTo": "PromotionEvaluation.rejected",
       "notes": "When a code does not apply, say which condition failed. \"Expired\" and \"already used\" are very different conversations",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "cardList",
       "label": "Visit date per line",
       "notes": "Each line shows its visit date: `Performance.startsAt` for a line with a performance (the match date for a fixture). A table reservation is not a cart line (REV3-8), so it shows on its confirmation.",
       "operation": "getPerformance",
       "provenance": "decided 29 September, rev 3 23SEP-9"
      },
      {
       "kind": "progressIndicator",
       "label": "Booking steps",
       "bindsTo": "BookingFlow",
       "columns": [
        "BookingFlow.steps"
       ],
       "operation": "getPublishedBookingFlow",
       "notes": "The steps of the published flow in their `sortOrder`, this one (cart) highlighted. A step the flow has turned off is not shown and is skipped by Continue and Back.",
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
      },
      {
       "kind": "secondaryButton",
       "label": "Save cart line",
       "operation": "updateCartLine",
       "provenance": "contract orders.yaml PATCH /carts/{cartId}/lines/{lineId}"
      },
      {
       "kind": "destructiveButton",
       "label": "Remove cart line",
       "operation": "removeCartLine",
       "provenance": "contract orders.yaml DELETE /carts/{cartId}/lines/{lineId}"
      },
      {
       "kind": "secondaryButton",
       "label": "Extend cart",
       "operation": "extendCart",
       "provenance": "contract orders.yaml POST /carts/{cartId}/extend"
      },
      {
       "kind": "secondaryButton",
       "label": "Checkout cart",
       "operation": "checkoutCart",
       "provenance": "contract orders.yaml POST /carts/{cartId}/checkout"
      },
      {
       "kind": "destructiveButton",
       "label": "Abandon cart",
       "operation": "abandonCart",
       "provenance": "contract orders.yaml DELETE /carts/{cartId}"
      },
      {
       "kind": "secondaryButton",
       "label": "Evaluate promotions",
       "operation": "evaluatePromotions",
       "provenance": "contract promotions.yaml POST /promotions/evaluate"
      },
      {
       "kind": "secondaryButton",
       "label": "Create cart",
       "operation": "createCart",
       "provenance": "contract orders.yaml POST /carts"
      },
      {
       "kind": "primaryButton",
       "label": "Checkout",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmRemoveCartLine",
    "component": "confirmDialog",
    "trigger": "Remove cart line",
    "body": "**Names what `removeCartLine` changes and what it leaves alone**, in the consequence rather than the verb. A shopping cart this affects should be identified in the dialog, not just counted.",
    "provenance": "client-verified"
   },
   {
    "id": "confirmAbandonCart",
    "component": "confirmDialog",
    "trigger": "Abandon cart",
    "body": "**Names what `abandonCart` changes and what it leaves alone**, in the consequence rather than the verb. A shopping cart this affects should be identified in the dialog, not just counted.",
    "provenance": "client-verified"
   },
   {
    "id": "formCreateCart",
    "component": "modal",
    "trigger": "Create cart",
    "body": "**Collects what `createCart` sends before it is called.** Required: `venueId`, `channel`. Optional: `subjectId`, `locale`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Create cart",
     "operation": "createCart"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "venueId",
      "channel",
      "subjectId",
      "locale"
     ]
    },
    "provenance": "client-verified"
   },
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
   },
   {
    "id": "formUpdateCartLine",
    "component": "modal",
    "trigger": "Save cart line",
    "body": "**Collects what `updateCartLine` sends before it is called.** Required: `quantity`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Save cart line",
     "operation": "updateCartLine"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "quantity"
     ]
    },
    "provenance": "client-verified"
   },
   {
    "id": "formCheckoutCart",
    "component": "modal",
    "trigger": "Checkout cart",
    "body": "**Collects what `checkoutCart` sends before it is called.** Nothing in the body is required. Optional: `subjectId`, `attendees`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Checkout cart",
     "operation": "checkoutCart"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "subjectId",
      "attendees"
     ]
    },
    "provenance": "client-verified"
   },
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
   }
  ],
  "states": {
   "loading": "The shopping cart, read by `getCart`.",
   "error": "Could not load. Names which read failed and leaves the shopping cart untouched.",
   "emptyFirstRun": "No shopping cart yet. Offers Add cart line (`addCartLine`).",
   "emptyNoAccess": "**The cart is open to anyone** — signed in, unverified or anonymous (ADR-0045, 18 September 2026). Nobody is turned away from it. The fork between signing in and continuing as a guest waits on `WEB-011`, and `checkoutCart` is what refuses.",
   "offline": "**The offline banner shows.** What was already loaded stays on screen, marked with its age. Anything that spends money, holds capacity or changes the account waits for the connection, and its button says so rather than failing."
  },
  "apis": [
   {
    "operationId": "applyCartPromoCode",
    "contract": "orders",
    "purpose": "Apply a promo code to the cart; refused 422 promoCodeInvalid or promoCodeNotApplicable, shown as different messages (decided 28 September, audit R073 (e))",
    "trigger": "onAction",
    "invalidates": [
     "getCart"
    ]
   },
   {
    "operationId": "getCart",
    "contract": "orders",
    "purpose": "The cart, priced and checked, right now",
    "trigger": "onLoad"
   },
   {
    "operationId": "addCartLine",
    "contract": "orders",
    "purpose": "Add something",
    "trigger": "onAction"
   },
   {
    "operationId": "updateCartLine",
    "contract": "orders",
    "purpose": "Change a quantity",
    "trigger": "onAction"
   },
   {
    "operationId": "removeCartLine",
    "contract": "orders",
    "purpose": "Take something out",
    "trigger": "onAction"
   },
   {
    "operationId": "extendCart",
    "contract": "orders",
    "purpose": "Give the guest more time",
    "trigger": "onAction"
   },
   {
    "operationId": "checkoutCart",
    "contract": "orders",
    "purpose": "Turn the cart into an order",
    "trigger": "onAction"
   },
   {
    "operationId": "abandonCart",
    "contract": "orders",
    "purpose": "Empty it deliberately",
    "trigger": "onAction"
   },
   {
    "operationId": "evaluatePromotions",
    "contract": "promotions",
    "purpose": "Evaluate promotions against a cart",
    "trigger": "onAction"
   },
   {
    "operationId": "getCouponCode",
    "contract": "promotions",
    "purpose": "Look up a code",
    "trigger": "onLoad"
   },
   {
    "operationId": "createCart",
    "contract": "orders",
    "purpose": "Start a cart",
    "trigger": "onAction",
    "provenance": "client-verified"
   },
   {
    "operationId": "getPerformance",
    "contract": "catalogue",
    "purpose": "The visit date and time of each line (`Performance.startsAt`)",
    "trigger": "onLoad"
   },
   {
    "operationId": "getResourceHold",
    "contract": "resources",
    "purpose": "The countdown of a cabana or spot held on the venue map (`expiresAt`)",
    "trigger": "onInterval"
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
     "from": "WEB-008"
    },
    {
     "name": "code",
     "from": "deepLink"
    },
    {
     "name": "lineId",
     "from": "deepLink"
    },
    {
     "name": "performanceId",
     "from": "navigation",
     "optional": true
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
   "coldEntry": "**A guest arriving cold on a link that no longer resolves is shown what happened and one way onward — never a 404.** A shared ticket, a forwarded confirmation and a push notification opened three weeks late all land here, and the person holding the link did nothing wrong. **The screen names the thing, says it is expired, cancelled or withdrawn, and offers the list it came from.** Arrives with `code`, `lineId`. **A cold arrival opens the cart whatever the session is** — the identity fork waits until checkout (ADR-0045)."
  },
  "wireframe": {
   "status": "review",
   "provenance": "client-verified",
   "board": "wireframes/P01 Guest Web.dc.html#web-010",
   "prototype": {
    "file": "sources/designs/guest-rev3-28-september/TICVAI Guest Booking v2.dc.html",
    "rev": "rev 3",
    "verified": "2026-09-28",
    "match": "partial",
    "view": "Visible on every booking step as the cart sidebar (Config → Layout & locale → 'Cart & summary' changes it to slide-in, bottom sheet, floating icon or single column)",
    "differences": "Not a separate screen: a persistent sidebar/drawer through the stepper, with a Rev 3 option to mirror it in Arabic. No 'extend hold' action (extendCart) — only hold timers on the seat step. Exit-intent dialog (exit.open) is a prototype addition."
   }
  },
  "apisNote": "Rebuilt 9 September 2026 from the 9 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "notes": "**Rev 3 (decided 29 September).** Visit date per line (23SEP-9). **Layout (REV3-10):** `cartLayout` may be `floatingIcon` (a round basket button with the count); in Arabic the cart stays on the right unless `cartSideInRtl` is `mirror` (default `keepRight`). **A line holding a cabana or spot from the venue map** (`resourceHoldId`) counts down from its `ResourceHold.expiresAt` (REV3-15). **Consent (REV3-26):** `checkoutCart` answers `422 consentRequired` while a required consent question is unanswered, and `consentAnswerBlocks` when an answer blocks a line; both send the guest back to the questions (WEB-006 pop-up, or WEB-011 for a flow with no date step). Promo code and abandon are declared (`applyCartPromoCode`, `abandonCart`; GAP-B3, already). Every booking-flow setting named here is read from `getTenantConfig` `bookingFlow`, resolved for the venue the guest picked (audit R267): the tenant's values with that venue's `venueOverrides` entry laid over field by field (decided 29 September, rev 3 CFG-11).\n\n**The step order comes from the published booking flow** (W12, 29 September): `getPublishedBookingFlow` returns the flow the product (or its category, else the venue default for its kind) uses, with its enabled steps in `sortOrder`; this screen renders when that flow has its step and in the order the flow gives. Flow-level settings (`performanceReveal`, `signInAt`, `seatEventDateMode`, `extrasStep`, `quickTour`, `consentQuestionIds`) are read from the flow; venue-wide settings stay on `getTenantConfig` `bookingFlow`.",
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
  "id": "WEB-011",
  "name": "Guest Details & Attendee Forms",
  "module": "Cart & Checkout",
  "requiresModule": "marketing",
  "wave": 1,
  "capability": "C03",
  "implementation": {
   "app": "guest-web",
   "route": "/cart-and-checkout/guest-details-and-attendee-forms",
   "component": "apps/guest-web/src/routes/cart-and-checkout/GuestDetailsAndAttendeeFormsForm.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "WEB-010",
    "WEB-016"
   ],
   "exitTo": [
    "WEB-001",
    "WEB-010",
    "WEB-012",
    "WEB-016"
   ],
   "transitions": [
    {
     "to": "WEB-016",
     "trigger": "Chooses to sign in rather than continue as a guest",
     "precondition": "no verified guest session — this is the fork of matrix 2.6.1 §2.4, offered here rather than in front of the cart",
     "carries": [
      "cartId"
     ],
     "returnsTo": "WEB-011",
     "provenance": "ADR-0045, 18 September 2026 — the gate is the checkout page, not the cart; moved from WEB-010 where it was placed on 17 September"
    },
    {
     "to": "WEB-012",
     "trigger": "Pays",
     "provenance": "flow F01 step 6→7, F02 step 4→5"
    },
    {
     "to": "WEB-012",
     "trigger": "Skipped: nothing to ask (guest code proved, or signed in, and no attendee forms)",
     "provenance": "decided 29 September 2026, W1"
    },
    {
     "to": "WEB-010",
     "trigger": "They check out",
     "provenance": "flow F55 step 2→3",
     "carries": [
      "cartId",
      "performanceId"
     ]
    }
   ]
  },
  "notes": "**Wired 24 August from review**: updateMyProfile. **The operations existed and this screen could not call them** — reviewers reported them as missing APIs, which is what an unreachable operation looks like from a wireframe.\n\n**Rev 3 (decided 29 September).** Booking consent questions not yet answered are asked here (REV3-26). The sign-in gate may already have been passed at the Add-ons exit (`signInAt` `afterAddOns`, REV3-3); a guest who signed in there arrives with their details filled.\n\n**The step order comes from the published booking flow** (W12, 29 September): `getPublishedBookingFlow` returns the flow the product (or its category, else the venue default for its kind) uses, with its enabled steps in `sortOrder`; this screen renders when that flow has its step and in the order the flow gives. Flow-level settings (`performanceReveal`, `signInAt`, `seatEventDateMode`, `extrasStep`, `quickTour`, `consentQuestionIds`) are read from the flow; venue-wide settings stay on `getTenantConfig` `bookingFlow`.\n\n**29 September (W1).** **Skipped after the guest code, and when signed in**, unless the cart needs attendee forms or unanswered consent questions: no name, email or phone is asked again. The profile is created and completed later (WEB-020).",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listGuestDevices` reads the population and `getWishlist` reads one of them — list, select, act",
  "purpose": "Collect who is coming and how to reach them.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every guest device",
       "bindsTo": "GuestDevice",
       "columns": [
        "GuestDevice.id",
        "GuestDevice.subjectId",
        "GuestDevice.platform",
        "GuestDevice.tokenFingerprint",
        "GuestDevice.appVersion",
        "GuestDevice.osVersion",
        "GuestDevice.deviceModel",
        "GuestDevice.locale",
        "GuestDevice.status",
        "GuestDevice.failureCount",
        "GuestDevice.registeredAt",
        "GuestDevice.lastSeenAt"
       ],
       "operation": "listGuestDevices",
       "provenance": "contract marketing-crm.yaml GET /guests/{subjectId}/devices"
      },
      {
       "kind": "dataTable",
       "label": "Every consent purpose config",
       "bindsTo": "ConsentPurposeConfig",
       "columns": [
        "ConsentPurposeConfig.purpose",
        "ConsentPurposeConfig.displayName",
        "ConsentPurposeConfig.description",
        "ConsentPurposeConfig.channels",
        "ConsentPurposeConfig.noticeVersion",
        "ConsentPurposeConfig.isRequiredForService",
        "ConsentPurposeConfig.expiresAfterMonths"
       ],
       "operation": "listConsentPurposes",
       "provenance": "contract marketing-crm.yaml GET /consent-purposes"
      },
      {
       "kind": "textField",
       "label": "Full name",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "textField",
       "label": "Email",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "textField",
       "label": "Mobile",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "detailPanel",
       "bindsTo": "EntitlementTemplate.isNameBound",
       "notes": "Per-attendee fields appear only where the entitlement is name-bound. Most are not — identity and entitlement are separate concerns",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "consentBlock",
       "bindsTo": "ConsentPurposeConfig[]",
       "notes": "Marketing consent is opt-in and unticked. Transactional is required for service and is presented differently, not as a choice dressed as one",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "consentBlock",
       "label": "Booking consent questions",
       "bindsTo": "Cart.consentQuestions",
       "notes": "Any consent question in `Cart.consentQuestions` not answered yet (a flow with no date step, or a product added later): per person or once per booking, as each question says; answers go to `recordConsentAnswers`. Distinct from marketing consent above.",
       "operation": "getCart",
       "provenance": "decided 29 September, rev 3 REV3-26"
      },
      {
       "kind": "progressIndicator",
       "label": "Booking steps",
       "bindsTo": "BookingFlow",
       "columns": [
        "BookingFlow.steps"
       ],
       "operation": "getPublishedBookingFlow",
       "notes": "The steps of the published flow in their `sortOrder`, this one (details) highlighted. A step the flow has turned off is not shown and is skipped by Continue and Back.",
       "provenance": "decided 29 September 2026, W12; CMS-103 Booking Flows"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected guest device",
       "bindsTo": "GuestDevice",
       "columns": [
        "GuestDevice.id",
        "GuestDevice.subjectId",
        "GuestDevice.platform",
        "GuestDevice.tokenFingerprint",
        "GuestDevice.tokenRef",
        "GuestDevice.appVersion",
        "GuestDevice.osVersion",
        "GuestDevice.deviceModel",
        "GuestDevice.locale",
        "GuestDevice.status",
        "GuestDevice.failureCount",
        "GuestDevice.registeredAt",
        "GuestDevice.lastSeenAt",
        "GuestDevice.revokedAt"
       ],
       "operation": "listGuestDevices",
       "provenance": "contract marketing-crm.yaml GET /guests/{subjectId}/devices"
      },
      {
       "kind": "detailPanel",
       "label": "The guest profile",
       "bindsTo": "GuestProfileDetail",
       "columns": [
        "GuestProfileDetail.id",
        "GuestProfileDetail.subjectId",
        "GuestProfileDetail.displayName",
        "GuestProfileDetail.email",
        "GuestProfileDetail.phone",
        "GuestProfileDetail.preferredLanguage",
        "GuestProfileDetail.preferredChannel",
        "GuestProfileDetail.guestLinkId",
        "GuestProfileDetail.tags",
        "GuestProfileDetail.engagementScore",
        "GuestProfileDetail.engagementTier",
        "GuestProfileDetail.lifetimeValue",
        "GuestProfileDetail.visitCount",
        "GuestProfileDetail.lastVisitAt",
        "GuestProfileDetail.isActive",
        "GuestProfileDetail.mergedIntoSubjectId"
       ],
       "operation": "getGuestProfile",
       "provenance": "contract marketing-crm.yaml GET /guests/{subjectId}"
      },
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
       "kind": "secondaryButton",
       "label": "Record consent",
       "operation": "recordConsent",
       "provenance": "contract marketing-crm.yaml POST /guests/{subjectId}/consents"
      },
      {
       "kind": "secondaryButton",
       "label": "Register guest device",
       "operation": "registerGuestDevice",
       "provenance": "contract marketing-crm.yaml POST /guests/{subjectId}/devices"
      },
      {
       "kind": "destructiveButton",
       "label": "Remove from wishlist",
       "operation": "removeFromWishlist",
       "provenance": "contract marketing-crm.yaml DELETE /guests/{subjectId}/wishlist/{itemId}"
      },
      {
       "kind": "destructiveButton",
       "label": "Revoke guest device",
       "operation": "revokeGuestDevice",
       "provenance": "contract marketing-crm.yaml DELETE /guests/{subjectId}/devices/{deviceId}"
      },
      {
       "kind": "secondaryButton",
       "label": "Save my profile",
       "operation": "updateMyProfile",
       "provenance": "contract marketing-crm.yaml PATCH /guests/me/profile"
      },
      {
       "kind": "secondaryButton",
       "label": "Upload guest document",
       "operation": "uploadGuestDocument",
       "provenance": "contract marketing-crm.yaml POST /guest-documents"
      },
      {
       "kind": "primaryButton",
       "label": "Continue to payment",
       "provenance": "carried from the previous definition"
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
    "body": "**Names what `removeFromWishlist` changes and what it leaves alone**, in the consequence rather than the verb. A guest attendee forms this affects should be identified in the dialog, not just counted.",
    "provenance": "client-verified"
   },
   {
    "id": "confirmRevokeGuestDevice",
    "component": "confirmDialog",
    "trigger": "Revoke guest device",
    "body": "**Names what `revokeGuestDevice` changes and what it leaves alone**, in the consequence rather than the verb. A guest attendee forms this affects should be identified in the dialog, not just counted.",
    "provenance": "client-verified"
   },
   {
    "id": "formUploadGuestDocument",
    "component": "modal",
    "trigger": "Upload guest document",
    "body": "**Collects what `uploadGuestDocument` sends before it is called.** Required: `id`, `subjectId`, `kind`, `storageRef`, `retainUntil`. Optional: `contentType`, `consentPurposeId`, `uploadedAt`, `uploadedByPrincipalId`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "GuestDocument",
    "confirm": {
     "label": "Upload guest document",
     "operation": "uploadGuestDocument"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "subjectId",
      "kind",
      "storageRef",
      "retainUntil",
      "contentType",
      "consentPurposeId",
      "uploadedAt",
      "uploadedByPrincipalId"
     ]
    },
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
   },
   {
    "id": "formRecordConsent",
    "component": "modal",
    "trigger": "Record consent",
    "body": "**Collects what `recordConsent` sends before it is called.** Required: `purpose`, `decision`, `noticeVersion`, `source`, `recordedAt`. Optional: `channels`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "RecordConsentRequest",
    "confirm": {
     "label": "Record consent",
     "operation": "recordConsent"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "purpose",
      "decision",
      "noticeVersion",
      "source",
      "recordedAt",
      "channels"
     ]
    },
    "provenance": "client-verified"
   },
   {
    "id": "formRegisterGuestDevice",
    "component": "modal",
    "trigger": "Register guest device",
    "body": "**Collects what `registerGuestDevice` sends before it is called.** Required: `platform`, `token`. Optional: `appVersion`, `osVersion`, `deviceModel`, `locale`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Register guest device",
     "operation": "registerGuestDevice"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "platform",
      "token",
      "appVersion",
      "osVersion",
      "deviceModel",
      "locale"
     ]
    },
    "provenance": "client-verified"
   },
   {
    "id": "formUpdateMyProfile",
    "component": "modal",
    "trigger": "Save my profile",
    "body": "**Collects what `updateMyProfile` sends before it is called.** Nothing in the body is required. Optional: `displayName`, `email`, `phone`, `preferredLanguage`, `preferredChannel`, `dietary`, `accessibility`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Save my profile",
     "operation": "updateMyProfile"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "displayName",
      "email",
      "phone",
      "preferredLanguage",
      "preferredChannel",
      "dietary",
      "accessibility"
     ]
    },
    "provenance": "client-verified"
   }
  ],
  "states": {
   "loading": "The guest attendee forms list.",
   "error": "Could not load. Names which read failed and leaves the guest attendee forms untouched.",
   "emptyFirstRun": "No guest attendee forms yet. Offers Add to wishlist (`addToWishlist`).",
   "emptyNoResults": "Never shown: `listGuestDevices` takes no filter, so an empty list is always the first-run state above.",
   "emptyNoAccess": "**There is no permission to name — a guest holds none** (ADR-0025: `x-ticvai-permission` is what a staff caller must hold; a guest call resolves to the guest's own data). No access here means one of two things, told apart by the response: not signed in, where the guest is offered sign-in and brought back to this screen, or a record that is not theirs, which says so without saying whose it is. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "**Not available, and the offline banner says why.** A payment needs the gateway, and pretending otherwise takes money nobody can confirm. What was typed stays on screen so nothing is entered twice."
  },
  "apis": [
   {
    "operationId": "addToWishlist",
    "contract": "marketing-crm",
    "purpose": "Save an item",
    "trigger": "onAction",
    "invalidates": [
     "listGuestDevices"
    ]
   },
   {
    "operationId": "getWishlist",
    "contract": "marketing-crm",
    "purpose": "Read a guest's saved items",
    "trigger": "onLoad"
   },
   {
    "operationId": "listGuestDevices",
    "contract": "marketing-crm",
    "purpose": "A guest's registered devices",
    "trigger": "onLoad"
   },
   {
    "operationId": "recordConsent",
    "contract": "marketing-crm",
    "purpose": "Record a consent decision",
    "trigger": "onAction",
    "invalidates": [
     "listGuestDevices"
    ]
   },
   {
    "operationId": "registerGuestDevice",
    "contract": "marketing-crm",
    "purpose": "Register a device for push",
    "trigger": "onAction",
    "invalidates": [
     "listGuestDevices"
    ]
   },
   {
    "operationId": "removeFromWishlist",
    "contract": "marketing-crm",
    "purpose": "Remove a saved item",
    "trigger": "onAction",
    "invalidates": [
     "listGuestDevices"
    ]
   },
   {
    "operationId": "revokeGuestDevice",
    "contract": "marketing-crm",
    "purpose": "Revoke a device registration",
    "trigger": "onAction",
    "invalidates": [
     "listGuestDevices"
    ]
   },
   {
    "operationId": "getGuestProfile",
    "contract": "marketing-crm",
    "purpose": "Read a guest profile",
    "trigger": "onLoad"
   },
   {
    "operationId": "listConsentPurposes",
    "contract": "marketing-crm",
    "purpose": "Configured consent purposes",
    "trigger": "onLoad"
   },
   {
    "operationId": "updateMyProfile",
    "contract": "marketing-crm",
    "purpose": "A guest correcting their own details",
    "trigger": "onAction",
    "invalidates": [
     "listGuestDevices"
    ]
   },
   {
    "operationId": "uploadGuestDocument",
    "contract": "marketing-crm",
    "purpose": "Provide a document a booking requires",
    "trigger": "onAction"
   },
   {
    "operationId": "getCart",
    "contract": "orders",
    "purpose": "The cart's consent questions still unanswered",
    "trigger": "onLoad"
   },
   {
    "operationId": "recordConsentAnswers",
    "contract": "marketing-crm",
    "purpose": "Record answers to the booking's consent questions",
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
  "entryState": {
   "params": [
    {
     "name": "deviceId",
     "from": "deepLink"
    },
    {
     "name": "itemId",
     "from": "deepLink"
    },
    {
     "name": "subjectId",
     "from": "session"
    },
    {
     "name": "cartId",
     "from": "session"
    },
    {
     "name": "venueId",
     "from": "session"
    }
   ],
   "coldEntry": "**A guest arriving cold on a link that no longer resolves is shown what happened and one way onward — never a 404.** A shared ticket, a forwarded confirmation and a push notification opened three weeks late all land here, and the person holding the link did nothing wrong. **The screen names the thing, says it is expired, cancelled or withdrawn, and offers the list it came from.** Arrives with `deviceId`, `itemId`.",
   "preloaded": [
    "GuestDevice.id",
    "GuestDevice.subjectId",
    "GuestDevice.platform",
    "GuestDevice.tokenFingerprint",
    "GuestDevice.tokenRef"
   ]
  },
  "wireframe": {
   "status": "review",
   "provenance": "client-verified",
   "board": "wireframes/P01 Guest Web.dc.html#web-011",
   "prototype": {
    "file": "sources/designs/guest-rev3-28-september/TICVAI Guest Booking v2.dc.html",
    "rev": "rev 3",
    "verified": "2026-09-28",
    "match": "exact",
    "view": "Book → 'Your details' step (after Extras)",
    "differences": "Sections are driven by the flow's requires list; prototype adds a signature, diving certification and vehicle plate fields. Wishlist/device operations listed in the YAML apis have no counterpart here. Saved guests prefill is described in Account but not shown on this step."
   }
  },
  "apisNote": "Rebuilt 9 September 2026 from the 10 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
  "id": "WEB-012",
  "name": "Checkout — Payment",
  "module": "Cart & Checkout",
  "requiresModule": "ticketing",
  "wave": 1,
  "capability": "C04",
  "implementation": {
   "app": "guest-web",
   "route": "/cart-and-checkout/checkout-payment",
   "component": "apps/guest-web/src/routes/cart-and-checkout/CheckoutPaymentForm.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "WEB-011",
    "WEB-016",
    "WEB-010"
   ],
   "exitTo": [
    "WEB-001",
    "WEB-010",
    "WEB-011",
    "WEB-013",
    "WEB-016"
   ],
   "transitions": [
    {
     "to": "WEB-010",
     "trigger": "Shopping Cart",
     "carries": [
      "performanceId"
     ],
     "provenance": "derived — WEB-010 declares entryState.params cartId, code, holdId, lineId, performanceId and WEB-012 holds performanceId, so an edge into it carries them"
    },
    {
     "to": "WEB-011",
     "trigger": "Guest Details & Attendee Forms",
     "provenance": "derived — WEB-011 declares entryState.params deviceId, itemId and WEB-012 holds none of them. The edge carries nothing: WEB-012 is opened from WEB-011, so this edge is the way back and WEB-011 keeps its own state"
    },
    {
     "to": "WEB-016",
     "trigger": "Sign in or use a guest code (when sign-in is asked at payment)",
     "carries": [
      "cartId"
     ],
     "precondition": "the guest is not signed in",
     "provenance": "decided 29 September, rev 3 REV3-3: `BookingFlowConfig.signInAt` `atPayment`; the basket is kept"
    },
    {
     "to": "WEB-013",
     "trigger": "Receives confirmation and tickets",
     "provenance": "flow F01 step 7→8",
     "carries": [
      "orderId"
     ]
    }
   ]
  },
  "notes": "The unknown outcome is the one to build for. A payment taken but never confirmed must offer inquiry, not a retry — a retry double-charges and the guest finds out. **Card or wallet** (TenderKind `card`, `wallet`; decided 28 September, audit R080 (a)), **both in base currency, so tender currency equals base currency.** A guest paying with a foreign card is converted by their own issuer at their own rate — that is not our conversion and is not recorded as one. The displayed comparison price (`WEB-035`) and the charged amount are different numbers and the screen says so before the guest commits. **Wired 24 August from review**: getOrder. **The operations existed and this screen could not call them** — reviewers reported them as missing APIs, which is what an unreachable operation looks like from a wireframe. **No 'is this you?' at checkout** (decided 28 September, audit R120 (b)): a verified contact that matches an existing profile attaches the order automatically inside `checkoutCart` (ADR-0045), so `checkGuestCheckoutMatch` and `decideGuestCheckoutMatch` were removed from this screen; only unverified matches go to staff review.\n\n**Rev 3 (decided 29 September, rev 3 REV3-3).** With `BookingFlowConfig.signInAt` `atPayment` the sign-in or guest-code gate is here rather than at the Add-ons exit; the basket is kept. Unknown and declined payment outcomes are declared (`inquirePaymentStatus`; GAP-B3, already).\n\n**The step order comes from the published booking flow** (W12, 29 September): `getPublishedBookingFlow` returns the flow the product (or its category, else the venue default for its kind) uses, with its enabled steps in `sortOrder`; this screen renders when that flow has its step and in the order the flow gives. Flow-level settings (`performanceReveal`, `signInAt`, `seatEventDateMode`, `extrasStep`, `quickTour`, `consentQuestionIds`) are read from the flow; venue-wide settings stay on `getTenantConfig` `bookingFlow`.\n\n**29 September.** W1: a guest who proved the contact with the code arrives here from the cart (WEB-011 skipped) and only ticks the T&Cs. M18-15: unticked marketing opt-in.",
  "openQuestions": [
   "Sandbox credentials for Stripe and Network International are outstanding. The recovery paths cannot be tested without them."
  ],
  "density": "compact",
  "pattern": "statusTracker",
  "patternReason": "`getOrder` reads one record and nothing reads a population — the screen is about that one thing",
  "purpose": "Take payment and create the order.",
  "layout": {
   "template": "detail",
   "regions": [
    {
     "name": "contentBody",
     "slot": "record",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The order",
       "bindsTo": "Order",
       "columns": [
        "Order.id",
        "Order.orderNumber",
        "Order.channel",
        "Order.venueId",
        "Order.scopePath",
        "Order.status",
        "Order.currency",
        "Order.currencyScale",
        "Order.grossAmount",
        "Order.taxAmount",
        "Order.netAmount",
        "Order.refundedAmount",
        "Order.totalPriceVariance",
        "Order.lines",
        "Order.payments",
        "Order.principalId"
       ],
       "operation": "getOrder",
       "provenance": "contract orders.yaml GET /orders/{orderId}"
      },
      {
       "kind": "cartPanel",
       "notes": "Order summary stays visible throughout. Never collapsed behind a link",
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
       "notes": "The steps of the published flow in their `sortOrder`, this one (payment) highlighted. A step the flow has turned off is not shown and is skipped by Continue and Back.",
       "provenance": "decided 29 September 2026, W12; CMS-103 Booking Flows"
      },
      {
       "kind": "consentBlock",
       "label": "Terms and conditions",
       "operation": "createOrder",
       "notes": "After the code the guest goes straight to the T&Cs tick and completes (W1).",
       "provenance": "decided 29 September 2026, W1"
      },
      {
       "kind": "toggle",
       "label": "Send me offers and news",
       "operation": "createOrder",
       "notes": "Marketing opt-in beside the T&Cs, **never pre-ticked** (M18-15): `marketingConsents[]` on the order, bound to the verified contact.",
       "provenance": "decided 29 September 2026, M18-15"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Transfer order tickets",
       "operation": "transferOrderTickets",
       "provenance": "contract orders.yaml POST /orders/{orderId}/transfer"
      },
      {
       "kind": "secondaryButton",
       "label": "Create order",
       "operation": "createOrder",
       "provenance": "contract orders.yaml POST /orders"
      },
      {
       "kind": "secondaryButton",
       "label": "Create payment",
       "operation": "createPayment",
       "provenance": "contract orders.yaml POST /payments"
      },
      {
       "kind": "secondaryButton",
       "label": "Inquire payment status",
       "operation": "inquirePaymentStatus",
       "provenance": "contract orders.yaml POST /payments/{paymentId}/inquiry"
      },
      {
       "kind": "primaryButton",
       "label": "Pay now",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The checkout payment, read by `getOrder`.",
   "error": "Could not load. Names which read failed and leaves the checkout payment untouched.",
   "emptyFirstRun": "No checkout payment yet. Offers Create order (`createOrder`).",
   "emptyNoAccess": "**There is no permission to name — a guest holds none** (ADR-0025: `x-ticvai-permission` is what a staff caller must hold; a guest call resolves to the guest's own data). No access here means one of two things, told apart by the response: not signed in, where the guest is offered sign-in and brought back to this screen, or a record that is not theirs, which says so without saying whose it is. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "**Not available, and the offline banner says why.** A payment needs the gateway, and pretending otherwise takes money nobody can confirm. What was typed stays on screen so nothing is entered twice."
  },
  "apis": [
   {
    "operationId": "transferOrderTickets",
    "contract": "orders",
    "purpose": "Transfer tickets to another guest",
    "trigger": "onAction"
   },
   {
    "operationId": "createOrder",
    "contract": "orders",
    "purpose": "Create an order",
    "trigger": "onAction"
   },
   {
    "operationId": "createPayment",
    "contract": "orders",
    "purpose": "Take a payment against an order",
    "trigger": "onAction"
   },
   {
    "operationId": "getOrder",
    "contract": "orders",
    "purpose": "Read an order",
    "trigger": "onLoad"
   },
   {
    "operationId": "inquirePaymentStatus",
    "contract": "orders",
    "purpose": "Ask what happened to a payment that did not answer",
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
     "name": "orderId",
     "from": "deepLink"
    },
    {
     "name": "paymentId",
     "from": "navigation"
    },
    {
     "name": "venueId",
     "from": "session"
    }
   ],
   "coldEntry": "**A guest opening an order link weeks later.** Shows the order if it still resolves; if it was refunded or the performance passed, says which and offers the order list rather than an error."
  },
  "wireframe": {
   "status": "review",
   "provenance": "client-verified",
   "board": "wireframes/P01 Guest Web.dc.html#web-012",
   "prototype": {
    "file": "sources/designs/guest-rev3-28-september/TICVAI Guest Booking v2.dc.html",
    "rev": "rev 3",
    "verified": "2026-09-28",
    "match": "partial",
    "view": "Book → 'Payment' step; Config → Layout & locale → 'Payment outcome (demo)' = Interrupted / Declined for the failure states; Config → Steps & cards → 'Guest checkout (code proof)' for the guest route",
    "differences": "Contradicts 28 Sep decisions: YAML allows card or wallet only (R080) — prototype offers Apple Pay, Tabby split-in-4, pay on arrival and invoice/PO; YAML removed the 'is this you?' match at checkout (R120 b) — prototype still asks the guest to link or keep separate. The unknown-outcome inquiry state matches the YAML ('We couldn't confirm this payment yet… you won't be charged twice')."
   }
  },
  "apisNote": "Rebuilt 9 September 2026 from the 4 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formTransferOrderTickets",
    "component": "modal",
    "trigger": "Transfer order tickets",
    "body": "**Collects what `transferOrderTickets` sends before it is called.** Required: `ticketIds`, `recipient`. Optional: `message`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Transfer order tickets",
     "operation": "transferOrderTickets"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "ticketIds",
      "recipient",
      "message"
     ]
    },
    "provenance": "client-verified"
   },
   {
    "id": "formCreateOrder",
    "component": "modal",
    "trigger": "Create order",
    "body": "**Collects what `createOrder` sends before it is called.** Required: `id`, `venueId`, `channel`, `lines`, `recordedAt`. Optional: `shiftId`, `subjectId`, `guestLinkId`, `catalogueBundleVersion`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "CreateOrderRequest",
    "confirm": {
     "label": "Create order",
     "operation": "createOrder"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "venueId",
      "channel",
      "lines",
      "recordedAt",
      "shiftId",
      "subjectId",
      "guestLinkId",
      "catalogueBundleVersion"
     ]
    },
    "provenance": "client-verified"
   },
   {
    "id": "formCreatePayment",
    "component": "modal",
    "trigger": "Create payment",
    "body": "**Collects what `createPayment` sends before it is called.** Required: `id`, `orderId`, `tender`, `amount`, `recordedAt`. Optional: `tenderCurrency`, `tenderAmount`, `walletAuthorisationId`, `deviceId`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "CreatePaymentRequest",
    "confirm": {
     "label": "Create payment",
     "operation": "createPayment"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "orderId",
      "tender",
      "amount",
      "recordedAt",
      "tenderCurrency",
      "tenderAmount",
      "walletAuthorisationId",
      "deviceId"
     ]
    },
    "provenance": "client-verified"
   }
  ],
  "x-ticvai-make-or-break": "M18-15: may a guest-checkout customer be sent marketing on an opt-in taken at checkout (law and the client's marketing policy)? Until the client confirms, the opt-in is shown unticked and nothing is sent without it.",
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
  "id": "WEB-013",
  "name": "Booking Confirmation",
  "module": "Cart & Checkout",
  "requiresModule": "ticketing",
  "wave": 1,
  "capability": "C03",
  "implementation": {
   "app": "guest-web",
   "route": "/cart-and-checkout/order-confirmation",
   "component": "apps/guest-web/src/routes/cart-and-checkout/OrderConfirmationDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "WEB-012"
   ],
   "exitTo": [
    "WEB-001",
    "WEB-010",
    "WEB-011",
    "WEB-012",
    "WEB-014",
    "WEB-018"
   ],
   "transitions": [
    {
     "to": "WEB-010",
     "trigger": "Shopping Cart",
     "carries": [
      "lineId",
      "performanceId"
     ],
     "provenance": "derived — WEB-010 declares entryState.params cartId, code, holdId, lineId, performanceId and WEB-013 holds lineId, performanceId, so an edge into it carries them"
    },
    {
     "to": "WEB-011",
     "trigger": "Guest Details & Attendee Forms",
     "provenance": "derived — WEB-011 declares entryState.params deviceId, itemId and WEB-013 holds none of them. The edge carries nothing: deviceId, itemId only pre-select (deep link or optional), and WEB-011 opens on its own"
    },
    {
     "to": "WEB-012",
     "trigger": "Checkout — Payment",
     "carries": [
      "orderId",
      "paymentId"
     ],
     "provenance": "derived — WEB-012 declares entryState.params orderId, paymentId and WEB-013 holds orderId, paymentId, so an edge into it carries them"
    },
    {
     "to": "WEB-018",
     "trigger": "My Tickets",
     "carries": [
      "orderId"
     ],
     "provenance": "derived — WEB-018 declares entryState.params entitlementId, orderId and WEB-013 holds orderId, so an edge into it carries them"
    },
    {
     "to": "WEB-014",
     "trigger": "Pay for a Booking",
     "provenance": "derived — WEB-014 declares entryState.params token and WEB-013 holds none of them. The edge carries nothing: token only pre-selects (deep link or optional), and WEB-014 opens on its own"
    }
   ]
  },
  "notes": "**Renamed 31 August** from *Order Confirmation*. **A guest surface is one product with two renderings** — a screen named differently on web and app is two screens to a developer and one journey to a guest.",
  "density": "compact",
  "pattern": "statusTracker",
  "patternReason": "`getOrder` reads one record and nothing reads a population — the screen is about that one thing",
  "purpose": "Confirm the purchase and deliver the tickets.",
  "layout": {
   "template": "detail",
   "regions": [
    {
     "name": "contentBody",
     "slot": "record",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The order",
       "bindsTo": "Order",
       "columns": [
        "Order.id",
        "Order.orderNumber",
        "Order.channel",
        "Order.venueId",
        "Order.scopePath",
        "Order.status",
        "Order.currency",
        "Order.currencyScale",
        "Order.grossAmount",
        "Order.taxAmount",
        "Order.netAmount",
        "Order.refundedAmount",
        "Order.totalPriceVariance",
        "Order.lines",
        "Order.payments",
        "Order.principalId"
       ],
       "operation": "getOrder",
       "provenance": "contract orders.yaml GET /orders/{orderId}"
      },
      {
       "kind": "banner",
       "notes": "Confirmation with the order number prominent",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "secondaryButton",
       "label": "Add to wallet",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "secondaryButton",
       "label": "Resend confirmation",
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
       "label": "Transfer order tickets",
       "operation": "transferOrderTickets",
       "provenance": "contract orders.yaml POST /orders/{orderId}/transfer"
      },
      {
       "kind": "secondaryButton",
       "label": "Reprint order",
       "operation": "reprintOrder",
       "provenance": "contract orders.yaml POST /orders/{orderId}/reprints"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The booking confirmation, read by `getOrder`.",
   "error": "Could not load. Names which read failed and leaves the booking confirmation untouched.",
   "emptyFirstRun": "No booking confirmation yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table.",
   "emptyNoAccess": "**There is no permission to name — a guest holds none** (ADR-0025: `x-ticvai-permission` is what a staff caller must hold; a guest call resolves to the guest's own data). No access here means one of two things, told apart by the response: not signed in, where the guest is offered sign-in and brought back to this screen, or a record that is not theirs, which says so without saying whose it is. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "**The offline banner shows.** What was already loaded stays on screen, marked with its age. Anything that spends money, holds capacity or changes the account waits for the connection, and its button says so rather than failing."
  },
  "apis": [
   {
    "operationId": "transferOrderTickets",
    "contract": "orders",
    "purpose": "Transfer tickets to another guest",
    "trigger": "onAction"
   },
   {
    "operationId": "getOrder",
    "contract": "orders",
    "purpose": "Read an order",
    "trigger": "onLoad"
   },
   {
    "operationId": "reprintOrder",
    "contract": "orders",
    "purpose": "Reprint or resend tickets",
    "trigger": "onAction"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "orderId",
     "from": "WEB-012"
    }
   ],
   "coldEntry": "Resolves from the session; a cold arrival is the ordinary case."
  },
  "wireframe": {
   "status": "review",
   "provenance": "client-verified",
   "board": "wireframes/P01 Guest Web.dc.html#web-013",
   "prototype": {
    "file": "sources/designs/guest-rev3-28-september/TICVAI Guest Booking v2.dc.html",
    "rev": "rev 3",
    "verified": "2026-09-28",
    "match": "exact",
    "view": "Book → final step 'Confirmed' after paying",
    "differences": "Prototype adds editing attendee details after purchase ('Change your details', signed-in only) and Reissue QR. No 'unpaid — pay now' route to WEB-014."
   }
  },
  "apisNote": "Rebuilt 9 September 2026 from the 3 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formTransferOrderTickets",
    "component": "modal",
    "trigger": "Transfer order tickets",
    "body": "**Collects what `transferOrderTickets` sends before it is called.** Required: `ticketIds`, `recipient`. Optional: `message`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Transfer order tickets",
     "operation": "transferOrderTickets"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "ticketIds",
      "recipient",
      "message"
     ]
    },
    "provenance": "client-verified"
   },
   {
    "id": "formReprintOrder",
    "component": "modal",
    "trigger": "Reprint order",
    "body": "**Collects what `reprintOrder` sends before it is called.** Required: `delivery`, `recordedAt`. Optional: `destination`, `lineIds`, `reason`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Reprint order",
     "operation": "reprintOrder"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "delivery",
      "recordedAt",
      "destination",
      "lineIds",
      "reason"
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
  "id": "WEB-014",
  "name": "Pay for a Booking",
  "module": "Cart & Checkout",
  "requiresModule": "ticketing",
  "wave": 1,
  "capability": "C04",
  "implementation": {
   "app": "guest-web",
   "route": "/pay/:token",
   "component": "apps/guest-web/src/routes/cart-and-checkout/PayByLinkForm.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "WEB-013"
   ],
   "entryFrom": [
    "WEB-013"
   ],
   "inferred": false,
   "notes": "**Reached from WEB-013** — an unpaid booking is paid from the confirmation that says it is unpaid. Stated on 4 September: this screen exited somewhere and nothing exited to it, so it was outside the navigation graph entirely.",
   "transitions": [
    {
     "to": "WEB-013",
     "trigger": "Booking Confirmation",
     "carries": [
      "orderId"
     ],
     "provenance": "derived — WEB-013 declares entryState.params orderId and WEB-014 holds orderId, so an edge into it carries them"
    }
   ]
  },
  "notes": "BL-072, rebuilt 20 August. **Declared `getCart` and `checkoutCart` until then, and `createPaymentLink` takes an `orderId`** — the screen was looking for a cart that was never created, and its entryState said `cartId` came from the session when **a guest arriving from an email has no session.** Wired by name-matching rather than by following the journey.",
  "density": "compact",
  "pattern": "statusTracker",
  "patternReason": "`getPaymentLink` reads one record and nothing reads a population — the screen is about that one thing",
  "purpose": "Pay for a booking somebody else took, without an account.",
  "layout": {
   "template": "detail",
   "regions": [
    {
     "name": "contentBody",
     "slot": "record",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The payment link",
       "bindsTo": "PaymentLink",
       "columns": [
        "PaymentLink.id",
        "PaymentLink.orderId",
        "PaymentLink.reservationId",
        "PaymentLink.token",
        "PaymentLink.status",
        "PaymentLink.channel",
        "PaymentLink.sentTo",
        "PaymentLink.expiresAt",
        "PaymentLink.releaseHoldOnExpiry",
        "PaymentLink.viewedAt",
        "PaymentLink.paidAt",
        "PaymentLink.resendCount",
        "PaymentLink.issuedByPrincipalId",
        "PaymentLink.scopePath"
       ],
       "operation": "getPaymentLink",
       "provenance": "contract orders.yaml GET /payment-links/{token}"
      },
      {
       "kind": "detailPanel",
       "bindsTo": "PaymentLink",
       "notes": "Venue, lines, total. **What they are paying for, before how to pay** — a guest who booked by phone may not recognise a reference number.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "banner",
       "notes": "The deadline, counted in time remaining rather than as a timestamp. **Expires in 46 minutes** is actionable; **expires at 14:32** needs arithmetic.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "textField",
       "label": "Email for your tickets (optional)",
       "notes": "**Optional, and only to send the ticket.** Requiring an account before taking money is how a paid booking becomes an abandoned one.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "primaryButton",
       "label": "Pay now",
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
       "label": "Pay by link",
       "operation": "payByLink",
       "provenance": "contract orders.yaml POST /payment-links/{token}/pay"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The lines and the total, with the deadline counting down.",
   "error": "Could not load the booking. **The hold is unaffected** — a failed page load must not release inventory.",
   "emptyFirstRun": "**Not reachable empty** — a link always names an order. An empty state here means the token did not resolve, which is the error state.",
   "emptyNoAccess": "**The token is the credential, so there is no permission case** — either it resolves or it has gone.",
   "offline": "**Not available, and the offline banner says why.** A payment needs the gateway, and pretending otherwise takes money nobody can confirm. What was typed stays on screen so nothing is entered twice."
  },
  "apis": [
   {
    "operationId": "getPaymentLink",
    "contract": "orders",
    "purpose": "What is owed and until when",
    "trigger": "onLoad"
   },
   {
    "operationId": "payByLink",
    "contract": "orders",
    "purpose": "Take the money and convert the reservation",
    "trigger": "onAction"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "token",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**Cold is the only way in.** The guest arrives from an email, an SMS or a WhatsApp message with no session and quite possibly no account. **A link opened three days late is the ordinary case, not an edge** — the screen says the hold was released and offers to book again. Expired, already paid and superseded are three different messages, and **404 is never one of them**: telling somebody their booking does not exist when it expired is how a support call starts."
  },
  "wireframe": {
   "status": "review",
   "provenance": "designed",
   "board": "wireframes/P01 Guest Web.dc.html#web-014",
   "prototype": {
    "file": "sources/designs/guest-rev3-28-september/TICVAI Guest Booking v2.dc.html",
    "rev": "rev 3",
    "match": "none",
    "note": "The prototype has no view for this screen. It was drawn in Claude Design on 29 September in the prototype's style and accepted as its design the same day (the frame on this screen's board): build the layout from that frame."
   }
  },
  "apisNote": "Rebuilt 9 September 2026 from the 2 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formPayByLink",
    "component": "modal",
    "trigger": "Pay by link",
    "body": "**Collects what `payByLink` sends before it is called.** Required: `providerToken`. Optional: `email`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Pay by link",
     "operation": "payByLink"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "providerToken",
      "email"
     ]
    },
    "provenance": "designed"
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
 }
]
```

## `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
 "abandonCart": {
  "method": "DELETE",
  "path": "/carts/{cartId}",
  "contract": "orders",
  "summary": "Empty it deliberately",
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
  "responds": null
 },
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
   },
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
 "applyCartPromoCode": {
  "method": "POST",
  "path": "/carts/{cartId}/promo-codes",
  "contract": "orders",
  "summary": "Apply a promo code to the cart",
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
  "requestBody": "ApplyCartPromoCodeRequest",
  "responds": "Cart"
 },
 "checkoutCart": {
  "method": "POST",
  "path": "/carts/{cartId}/checkout",
  "contract": "orders",
  "summary": "Turn the cart into an order",
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
  "responds": "Order"
 },
 "createCart": {
  "method": "POST",
  "path": "/carts",
  "contract": "orders",
  "summary": "Start a cart",
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
 "createOrder": {
  "method": "POST",
  "path": "/orders",
  "contract": "orders",
  "summary": "Create an order",
  "permission": "ORDER_CREATE",
  "offlineCapable": true,
  "conflictPolicy": "append",
  "scopeLevel": "workstation",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "CreateOrderRequest",
  "responds": "Order"
 },
 "createPayment": {
  "method": "POST",
  "path": "/payments",
  "contract": "orders",
  "summary": "Take a payment against an order",
  "permission": "ORDER_CREATE",
  "offlineCapable": true,
  "conflictPolicy": "append",
  "scopeLevel": "workstation",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "CreatePaymentRequest",
  "responds": "Payment"
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
 "extendCart": {
  "method": "POST",
  "path": "/carts/{cartId}/extend",
  "contract": "orders",
  "summary": "Give the guest more time",
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
 "getCouponCode": {
  "method": "GET",
  "path": "/coupon-codes/{code}",
  "contract": "promotions",
  "summary": "Look up a code",
  "permission": "PRICE_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "CouponCode"
 },
 "getGuestProfile": {
  "method": "GET",
  "path": "/guests/{subjectId}",
  "contract": "marketing-crm",
  "summary": "Read a guest profile",
  "permission": "GUEST_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "GuestProfileDetail"
 },
 "getOrder": {
  "method": "GET",
  "path": "/orders/{orderId}",
  "contract": "orders",
  "summary": "Read an order",
  "permission": "ORDER_VIEW",
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
  "responds": "Order"
 },
 "getPaymentLink": {
  "method": "GET",
  "path": "/payment-links/{token}",
  "contract": "orders",
  "summary": "What a guest holding a link is being asked to pay for",
  "permission": "ORDER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": null
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
 "inquirePaymentStatus": {
  "method": "POST",
  "path": "/payments/{paymentId}/inquiry",
  "contract": "orders",
  "summary": "Ask the provider what actually happened",
  "permission": "ORDER_CREATE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "workstation",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "Payment"
 },
 "listConsentPurposes": {
  "method": "GET",
  "path": "/consent-purposes",
  "contract": "marketing-crm",
  "summary": "Configured consent purposes",
  "permission": "GUEST_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
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
 "listGuestDevices": {
  "method": "GET",
  "path": "/guests/{subjectId}/devices",
  "contract": "marketing-crm",
  "summary": "A guest's registered devices",
  "permission": null,
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "subject",
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
 "payByLink": {
  "method": "POST",
  "path": "/payment-links/{token}/pay",
  "contract": "orders",
  "summary": "Pay for a booking taken at a till",
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
 "recordConsent": {
  "method": "POST",
  "path": "/guests/{subjectId}/consents",
  "contract": "marketing-crm",
  "summary": "Record a consent decision",
  "permission": null,
  "offlineCapable": false,
  "conflictPolicy": "append",
  "scopeLevel": "subject",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "RecordConsentRequest",
  "responds": "ConsentState"
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
 "registerGuestDevice": {
  "method": "POST",
  "path": "/guests/{subjectId}/devices",
  "contract": "marketing-crm",
  "summary": "Register a device for push",
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
  "responds": "GuestDevice"
 },
 "removeCartLine": {
  "method": "DELETE",
  "path": "/carts/{cartId}/lines/{lineId}",
  "contract": "orders",
  "summary": "Take something out",
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
 },
 "reprintOrder": {
  "method": "POST",
  "path": "/orders/{orderId}/reprints",
  "contract": "orders",
  "summary": "Reprint or resend tickets",
  "permission": "ORDER_REPRINT",
  "offlineCapable": true,
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
 "revokeGuestDevice": {
  "method": "DELETE",
  "path": "/guests/{subjectId}/devices/{deviceId}",
  "contract": "marketing-crm",
  "summary": "Revoke a device registration",
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
 },
 "transferOrderTickets": {
  "method": "POST",
  "path": "/orders/{orderId}/transfer",
  "contract": "orders",
  "summary": "Transfer tickets to another guest",
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
  "responds": null
 },
 "updateCartLine": {
  "method": "PATCH",
  "path": "/carts/{cartId}/lines/{lineId}",
  "contract": "orders",
  "summary": "Change a quantity",
  "permission": null,
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
  "requestBody": null,
  "responds": "Cart"
 },
 "updateMyProfile": {
  "method": "PATCH",
  "path": "/guests/me/profile",
  "contract": "marketing-crm",
  "summary": "A guest correcting their own details",
  "permission": "GUEST_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "lastWriterWins",
  "scopeLevel": "subject",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "GuestProfile"
 },
 "uploadGuestDocument": {
  "method": "POST",
  "path": "/guest-documents",
  "contract": "marketing-crm",
  "summary": "Store a guest photo, ID or signed document",
  "permission": "GUEST_VIEW_PII",
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
  "requestBody": "GuestDocument",
  "responds": "GuestDocument"
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
 "ApplyCartPromoCodeRequest": {
  "type": "object",
  "x-ticvai-persistence": "none — request only",
  "required": [
   "code"
  ],
  "properties": {
   "code": {
    "type": "string",
    "minLength": 1,
    "maxLength": 100,
    "description": "The code as the guest typed it."
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
 "ConsentDecision": {
  "type": "string",
  "enum": [
   "granted",
   "withdrawn",
   "notAsked"
  ]
 },
 "ConsentPurpose": {
  "type": "string",
  "enum": [
   "marketing",
   "personalisation",
   "profiling",
   "thirdPartySharing",
   "aiProcessing",
   "transactional"
  ]
 },
 "ConsentPurposeConfig": {
  "x-ticvai-persistence": "marketing.consent_purpose + marketing.consent_purpose_channel",
  "type": "object",
  "required": [
   "purpose",
   "channels",
   "noticeVersion",
   "isRequiredForService"
  ],
  "properties": {
   "purpose": {
    "$ref": "#/components/schemas/ConsentPurpose"
   },
   "displayName": {
    "type": "string"
   },
   "description": {
    "type": "string"
   },
   "channels": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/MessageChannel"
    }
   },
   "noticeVersion": {
    "type": "string",
    "description": "Current version of the notice. A consent against a superseded version is reported as requiring renewal rather than silently honoured.\n"
   },
   "isRequiredForService": {
    "type": "boolean",
    "description": "True for transactional. Withdrawing it means the service cannot be delivered, so it is presented differently.\n"
   },
   "expiresAfterMonths": {
    "type": "integer",
    "nullable": true
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
 "ConsentState": {
  "x-ticvai-persistence": "none — projection over consent_record",
  "type": "object",
  "required": [
   "subjectId",
   "purposes"
  ],
  "properties": {
   "subjectId": {
    "type": "string",
    "format": "uuid"
   },
   "purposes": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "purpose",
      "decision",
      "requiresRenewal"
     ],
     "properties": {
      "purpose": {
       "$ref": "#/components/schemas/ConsentPurpose"
      },
      "decision": {
       "$ref": "#/components/schemas/ConsentDecision"
      },
      "channels": {
       "type": "array",
       "items": {
        "$ref": "#/components/schemas/MessageChannel"
       }
      },
      "noticeVersion": {
       "type": "string",
       "nullable": true
      },
      "requiresRenewal": {
       "type": "boolean",
       "description": "True where the notice has been superseded since consent was given."
      },
      "decidedAt": {
       "type": "string",
       "format": "date-time",
       "nullable": true
      }
     }
    }
   }
  }
 },
 "CouponCode": {
  "x-ticvai-persistence": "promotions.coupon_code",
  "type": "object",
  "required": [
   "code",
   "campaignId",
   "status"
  ],
  "properties": {
   "code": {
    "type": "string"
   },
   "campaignId": {
    "type": "string",
    "format": "uuid"
   },
   "batchId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The `generateCouponCodes` batch that issued this code. Null where no batch did."
   },
   "status": {
    "$ref": "#/components/schemas/CouponStatus"
   },
   "assignedSubjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "redemptionCount": {
    "type": "integer"
   },
   "maxRedemptions": {
    "type": "integer"
   },
   "discount": {
    "$ref": "#/components/schemas/Discount"
   },
   "invalidReason": {
    "type": "string",
    "nullable": true,
    "description": "Why the code cannot be applied. A cashier reading `expired` to a guest is a very different conversation from reading `already used`.\n",
    "enum": [
     "expired",
     "alreadyRedeemed",
     "voided",
     "notYetValid",
     "wrongVenue",
     "conditionsNotMet",
     "notAssignedToGuest"
    ]
   },
   "validFrom": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "validTo": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "redeemedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "redeemedOrderId": {
    "type": "string",
    "nullable": true
   },
   "scopePath": {
    "type": "string",
    "description": "**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**"
   }
  }
 },
 "CouponStatus": {
  "type": "string",
  "enum": [
   "issued",
   "assigned",
   "redeemed",
   "expired",
   "voided"
  ]
 },
 "CreateOrderLine": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "required": [
   "id",
   "variantId",
   "quantity",
   "quotedUnitPrice"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "description": "Client-generated UUIDv7 of the line. `lineIds` everywhere in this contract are these."
   },
   "variantId": {
    "type": "string",
    "format": "uuid"
   },
   "recommendationId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The `trackingId` of the ai `decideRecommendations` item this line came from (29 September, build, AI system design 2.2 A step 8), so a purchase is attributed to the recommendation that led to it rather than guessed. Carried from the cart line at checkout; stored on `orders.order_line` and sent in `order.completed` lines.\n"
   },
   "performanceId": {
    "type": "string",
    "format": "uuid"
   },
   "bookedWindow": {
    "$ref": "#/components/schemas/BookedWindow"
   },
   "inventoryHoldId": {
    "type": "string",
    "nullable": true,
    "description": "Lease the units were drawn from — a `catalogue.InventoryHold.id`. Absent for uncontended products."
   },
   "seatIds": {
    "type": "array",
    "maxItems": 50,
    "items": {
     "type": "string",
     "format": "uuid"
    },
    "description": "Seated products only, as `seating.Seat.id`. Not available offline. **At most `VenueSettings.seating.maxSeatsPerGuestOrder` seats per booking on a guest channel** (default 10, bounds 1 to 50, decided 29 September, rev 3 REV3-7); **at most 10 per sale on staff and POS** (audit R080 (c)), across all the lines of one order for one performance. `createOrder` refuses more with 422 `seatLimitExceeded` (problem type `seat-limit-exceeded`)."
   },
   "resourceHoldId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "A `resources.ResourceHold` on a resource the guest picked on a venue map (decided 29 September, rev 3 REV3-15); `variantId` is the placed resource's price-band variant. `createOrder` converts the hold into a `ResourceBooking` without releasing it. Not available offline."
   },
   "attributes": {
    "$ref": "#/components/schemas/OrderLineAttributes"
   },
   "quantity": {
    "type": "integer",
    "minimum": 1
   },
   "eligibilityDeclaration": {
    "type": "array",
    "nullable": true,
    "x-ticvai-note": "One row per declared guest in `orders.order_line_eligibility` (named on `OrderLine`), because an array of objects is a child table's rows, not a column.\n",
    "items": {
     "type": "object",
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
       "nullable": true
      },
      "confidentSwimmer": {
       "type": "boolean",
       "nullable": true,
       "description": "**Derived, kept for the gate check** (decided 29 September, rev 3 REV3-26). The swim question is a consent: the answer is a `marketing.BookingConsentRecord` of kind `swim`, and this is filled from it (true for a `yes` covering this person, whether answered for them or once for the booking). A value sent that contradicts the record is ignored and the record wins. No longer the place a swim answer is captured.\n"
      },
      "guardianSigned": {
       "type": "boolean"
      }
     }
    },
    "description": "What was declared for each guest on this line, kept as the record staff check at the gate."
   },
   "quotedUnitPrice": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "description": "What the client charged, from its local bundle."
   },
   "holderName": {
    "type": "string",
    "nullable": true
   },
   "dataMaskValues": {
    "type": "object",
    "additionalProperties": true,
    "description": "**Deliberately open.** Custom fields keyed by the venue's data mask: the field definitions travel in the catalogue bundle (`catalogue.CatalogueBundle.payload`), so the keys are the venue's to define, as on `catalogue`'s own `dataMaskValues`.\n"
   }
  }
 },
 "CreateOrderRequest": {
  "type": "object",
  "required": [
   "id",
   "venueId",
   "channel",
   "lines",
   "recordedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "description": "Client-generated UUIDv7. Also the idempotency key: it must equal the `Idempotency-Key` header, and a replay or a mismatch follows `IdempotencyKey` in `shared/common.yaml`. Offline replay through `syncOrders` carries no header, and this id alone deduplicates there.\n"
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "channel": {
    "$ref": "#/components/schemas/Channel"
   },
   "shiftId": {
    "type": "string",
    "format": "uuid"
   },
   "subjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Null for an anonymous sale. Identity and entitlement are separate."
   },
   "guestLinkId": {
    "type": "string",
    "nullable": true,
    "description": "Present where the guest is linked across cells."
   },
   "catalogueBundleVersion": {
    "type": "string",
    "description": "The bundle the client priced from. Lets the server explain a variance rather than merely report one.\n"
   },
   "lines": {
    "type": "array",
    "minItems": 1,
    "items": {
     "$ref": "#/components/schemas/CreateOrderLine"
    }
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "CreatePaymentRequest": {
  "type": "object",
  "required": [
   "id",
   "orderId",
   "tender",
   "amount",
   "recordedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "description": "Client-generated UUIDv7 of the payment, and its idempotency key — it must equal the `Idempotency-Key` header."
   },
   "orderId": {
    "type": "string",
    "format": "uuid"
   },
   "tender": {
    "$ref": "#/components/schemas/TenderKind"
   },
   "amount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "tenderCurrency": {
    "type": "string",
    "pattern": "^[A-Z]{3}$",
    "nullable": true,
    "description": "The currency the guest handed over, where it is not the venue's — becomes `Payment.tenderCurrency`. Omit for a payment in the venue's own currency."
   },
   "tenderAmount": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "description": "**What the guest handed over**, in `tenderCurrency` — becomes `Payment.tenderAmount`, one name for one concept (renamed from `tenderedAmount` on 26 September). For cash, change is the difference.\n"
   },
   "walletAuthorisationId": {
    "type": "string",
    "nullable": true,
    "description": "Cross-cell wallet hold, where the guest's home cell is elsewhere."
   },
   "walletHoldId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "For a `wallet` tender, the hold `wallet.holdWalletFunds` placed (SD-027). Capture debits it; the order service writes no wallet table."
   },
   "returnUrl": {
    "type": "string",
    "format": "uri",
    "nullable": true,
    "description": "Where the provider returns the guest after a 3-D Secure challenge or hosted page (SD-034). Required for a card payment from the guest web or app."
   },
   "terminalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The card terminal to instruct, for a card payment at a till (ECR flow, SD-034)."
   },
   "deviceId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "Discount": {
  "x-ticvai-persistence": "none — embedded in promotion",
  "type": "object",
  "required": [
   "kind"
  ],
  "properties": {
   "kind": {
    "$ref": "#/components/schemas/DiscountKind"
   },
   "percentage": {
    "type": "number",
    "minimum": 0,
    "maximum": 100
   },
   "amount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "fixedPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "buyQuantity": {
    "type": "integer",
    "minimum": 1
   },
   "getQuantity": {
    "type": "integer",
    "minimum": 1
   },
   "getDiscountPercentage": {
    "type": "number",
    "minimum": 0,
    "maximum": 100,
    "description": "100 makes the free items actually free; lower values give a partial discount."
   },
   "tiers": {
    "type": "array",
    "description": "For `tieredPercentage` — more units, larger discount.",
    "items": {
     "type": "object",
     "required": [
      "minQuantity",
      "percentage"
     ],
     "properties": {
      "minQuantity": {
       "type": "integer",
       "minimum": 1
      },
      "percentage": {
       "type": "number",
       "minimum": 0,
       "maximum": 100
      }
     }
    }
   },
   "maxDiscountAmount": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "description": "Cap on a percentage discount. Prevents an unbounded discount on a large basket."
   },
   "rewardVariantIds": {
    "type": "array",
    "nullable": true,
    "items": {
     "type": "string",
     "format": "uuid"
    },
    "description": "The reward products, where the reward is not the qualifying product: the free gift of `freeItem`, the \"different product\" of a `buyXGetY` (setGiftFreeProduct, setBuyGetBogo). Absent means the reward is taken from the qualifying lines. (DM5, 29 September: data model for the agreed operations)"
   },
   "maxApplicationsPerBasket": {
    "type": "integer",
    "minimum": 1,
    "nullable": true,
    "description": "How many times the offer repeats in one basket: the \"maximum repetitions\" of an N-for-X offer (setFixedPriceOffer). Null repeats for every complete set. (DM5, 29 September: data model for the agreed operations)"
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
 "ExchangeRateDecimal": {
  "type": "string",
  "x-ticvai-persistence-kind": "valueObject",
  "x-ticvai-persistence-column": "numeric(18,6)",
  "description": "**An exchange rate: a decimal string, never a float**, for the reason `Money.amount` is one — a JavaScript client must not round a rate in transit. **Six decimal places**, the precision `finance.FxRate.rate` asks for, and stored at that precision.\n",
  "pattern": "^\\d+(\\.\\d{1,6})?$"
 },
 "GuestDevice": {
  "type": "object",
  "x-ticvai-persistence": "marketing.guest_device",
  "required": [
   "id",
   "subjectId",
   "platform",
   "status",
   "registeredAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "subjectId": {
    "type": "string",
    "format": "uuid"
   },
   "platform": {
    "type": "string",
    "enum": [
     "ios",
     "android",
     "web"
    ]
   },
   "tokenFingerprint": {
    "type": "string",
    "description": "Hash of the token, not the token. The token itself is write-only — returning it would put a push credential in every response a support agent can read.\n"
   },
   "tokenRef": {
    "type": "string",
    "writeOnly": true,
    "description": "**A vault reference to the push token**, written by the server from `registerGuestDevice.token` — the same pattern as `PaymentProvider.credentialRef`. Never the token and never returned; the sender resolves it at send time. Without it a registered device could not be sent to.\n"
   },
   "appVersion": {
    "type": "string",
    "nullable": true
   },
   "osVersion": {
    "type": "string",
    "nullable": true
   },
   "deviceModel": {
    "type": "string",
    "nullable": true
   },
   "locale": {
    "type": "string",
    "nullable": true
   },
   "status": {
    "type": "string",
    "enum": [
     "active",
     "revoked",
     "failed"
    ]
   },
   "failureCount": {
    "type": "integer",
    "description": "Consecutive delivery failures. Past the threshold the device is marked failed and stops being targeted — a dead token retried forever is wasted quota and a misleading delivery rate.\n"
   },
   "registeredAt": {
    "type": "string",
    "format": "date-time"
   },
   "lastSeenAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "revokedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   }
  }
 },
 "GuestDocument": {
  "type": "object",
  "x-ticvai-persistence": "marketing.guest_document",
  "description": "BL-133. **No store for guest photos, avatars, IDs or signed documents anywhere.**\nDeliberately separate from `assets`, which holds a tenant's media library. **A guest's passport scan is not a marketing asset** — it has a different retention clock, a different access rule and a different reason to exist, and putting it in the same store means one careless query returns both.\n",
  "required": [
   "id",
   "subjectId",
   "kind",
   "storageRef",
   "retainUntil"
  ],
  "properties": {
   "id": {
    "readOnly": true,
    "type": "string",
    "format": "uuid"
   },
   "subjectId": {
    "type": "string",
    "format": "uuid"
   },
   "kind": {
    "type": "string",
    "enum": [
     "avatar",
     "idDocument",
     "visa",
     "signedWaiver",
     "medicalNote",
     "accessibilityEvidence",
     "photo",
     "other"
    ]
   },
   "storageRef": {
    "type": "string",
    "description": "**The stored object's key in the guest-document store**, which is deliberately not `assets` (BL-133). No operation in this contract issues one yet: `assets` `createUpload` is staff-only and writes the media library, so the upload step for this store is still to be designed.\n"
   },
   "contentType": {
    "type": "string"
   },
   "consentPurposeId": {
    "type": "string",
    "format": "uuid"
   },
   "retainUntil": {
    "type": "string",
    "format": "date",
    "description": "**Required, not optional.** A guest document with no deletion date is a guest document kept forever, and the retention question is the one CF-64 is open on.\n**Kept until its purpose ends, then for the period client counsel sets (decided 28 September, audit R149).** The caller sets `retainUntil` to the end of the purpose (the visit, the waiver's validity, the visa's expiry) plus that period. **The period per `kind` is an open value**: until counsel names it, it is zero, so the document is deleted when the purpose ends.\n"
   },
   "uploadedAt": {
    "readOnly": true,
    "type": "string",
    "format": "date-time"
   },
   "uploadedByPrincipalId": {
    "readOnly": true,
    "type": "string",
    "format": "uuid",
    "nullable": true
   }
  }
 },
 "GuestProfile": {
  "x-ticvai-persistence": "marketing.guest_profile",
  "type": "object",
  "required": [
   "subjectId",
   "isActive"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"
   },
   "subjectId": {
    "type": "string",
    "format": "uuid",
    "description": "Opaque reference. Personal data lives in the separately erasable store, which is what makes erasure possible against an append-only ledger.\n"
   },
   "displayName": {
    "type": "string",
    "nullable": true
   },
   "email": {
    "type": "string",
    "nullable": true
   },
   "phone": {
    "type": "string",
    "nullable": true
   },
   "preferredLanguage": {
    "type": "string",
    "nullable": true
   },
   "preferredChannel": {
    "$ref": "#/components/schemas/MessageChannel"
   },
   "guestLinkId": {
    "type": "string",
    "nullable": true,
    "description": "Present where the guest is linked across cells. Marketing acts locally."
   },
   "tags": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "engagementScore": {
    "type": "integer",
    "nullable": true,
    "minimum": 0,
    "maximum": 100,
    "description": "22.2.20 and 22.2.21. **`lifetimeValue` and `visitCount` existed, so value was a stored figure and engagement was not.** They are different questions: a guest who spent a lot once and a guest who visits monthly have the same LTV and need opposite treatment.\n**Recency, frequency and breadth, not spend** — spend is already `lifetimeValue`, and folding it in here would make one number twice.\n"
   },
   "engagementTier": {
    "type": "string",
    "nullable": true,
    "enum": [
     "new",
     "active",
     "occasional",
     "lapsing",
     "lapsed",
     "dormant"
    ],
    "description": "5.3.19. **Automatic classification, computed rather than assigned.** `lapsing` is the tier the whole field exists for — **a guest who has not been for a while and still might is the only one marketing can change**, and lumping them with `lapsed` wastes the window.\n"
   },
   "lifetimeValue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "visitCount": {
    "type": "integer"
   },
   "lastVisitAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "isActive": {
    "type": "boolean"
   },
   "mergedIntoSubjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "description": "**Set on the absorbed profile by `mergeGuestProfiles` and `mergeGuests`**, which retain it as a redirect rather than deleting it. A read that lands here follows it; a second merge of a profile that has one is refused as `alreadyMerged`.\n"
   },
   "mergedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true
   }
  }
 },
 "GuestProfileDetail": {
  "x-ticvai-persistence": "marketing.guest_profile",
  "allOf": [
   {
    "$ref": "#/components/schemas/GuestProfile"
   },
   {
    "type": "object",
    "properties": {
     "id": {
      "type": "string",
      "format": "uuid",
      "readOnly": true,
      "description": "**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"
     },
     "consents": {
      "$ref": "#/components/schemas/ConsentState"
     },
     "loyalty": {
      "$ref": "#/components/schemas/LoyaltyPosition"
     },
     "openCaseCount": {
      "type": "integer"
     },
     "recentOrderIds": {
      "type": "array",
      "items": {
       "type": "string"
      }
     },
     "membershipIds": {
      "type": "array",
      "items": {
       "type": "string",
       "format": "uuid"
      }
     },
     "notes": {
      "type": "string",
      "nullable": true
     }
    }
   }
  ]
 },
 "LoyaltyPosition": {
  "x-ticvai-persistence": "marketing.loyalty_position",
  "type": "object",
  "required": [
   "subjectId",
   "programmeId",
   "pointsBalance",
   "tierCode"
  ],
  "properties": {
   "leaderboardNickname": {
    "type": "string",
    "nullable": true,
    "maxLength": 24,
    "description": "BL-173. **The name shown on a leaderboard, chosen by the guest.** Offered whenever they reach the board and changeable afterwards; `setLeaderboardNickname` is the only thing that writes it.\n**Null means the guest has not chosen one yet, and the board shows a generated `Player-4821` in its place** — never `pii.subject.display_name`, which would disclose silently on the day a guest first placed and is the case this field exists to prevent.\n**The generated name is computed at read time and not stored here.** Writing it would make *\"has this guest chosen a name\"* unanswerable, and that flag is what the prompt-on-reaching-the-board depends on.\n"
   },
   "subjectId": {
    "type": "string",
    "format": "uuid"
   },
   "programmeId": {
    "type": "string",
    "format": "uuid"
   },
   "pointsBalance": {
    "type": "integer"
   },
   "lifetimePoints": {
    "type": "integer"
   },
   "tierId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "**The tier this row's `tierCode` and `tierName` are a copy of.** Added 20 September with `marketing.programme_tier`: the two strings were a cache of something that did not exist, and a cache with no source cannot be rebuilt or audited.\n"
   },
   "tierCode": {
    "type": "string"
   },
   "tierName": {
    "type": "string"
   },
   "pointsToNextTier": {
    "type": "integer",
    "nullable": true
   },
   "nextExpiryPoints": {
    "type": "integer",
    "nullable": true
   },
   "nextExpiryAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   }
  }
 },
 "MessageChannel": {
  "type": "string",
  "enum": [
   "email",
   "sms",
   "whatsapp",
   "push",
   "inApp",
   "post"
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
 "Order": {
  "x-ticvai-persistence": "orders.sales_order + orders.order_line",
  "type": "object",
  "required": [
   "id",
   "venueId",
   "scopePath",
   "channel",
   "status",
   "currency",
   "currencyScale",
   "grossAmount",
   "taxAmount",
   "netAmount",
   "lines",
   "createdAt",
   "recordedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "description": "The client UUIDv7 from `CreateOrderRequest.id`."
   },
   "orderNumber": {
    "type": "string",
    "readOnly": true,
    "description": "The number a guest reads and a cashier types. **Server-assigned: the venue prefix and a sequence per venue**, for example `DXB1-000123` (decided 28 September, audit R152). A till holds a reserved range of the venue sequence, so an order taken offline gets its number on the till and keeps it through `syncOrders`. **Not gapless**: an unused reserved range leaves a gap, and that is allowed. Only tax invoices are gapless, per legal entity. The receipt carries this number.\n"
   },
   "channel": {
    "allOf": [
     {
      "$ref": "#/components/schemas/OrderChannel"
     }
    ],
    "description": "Where it came from. Drives revenue attribution, promotion eligibility and the self-service adoption figures the operator will ask for within a month of launch.\n"
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "scopePath": {
    "type": "string"
   },
   "status": {
    "$ref": "#/components/schemas/OrderStatus"
   },
   "currency": {
    "type": "string",
    "pattern": "^[A-Z]{3}$",
    "x-ticvai-persisted": false,
    "description": "**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else. **Kept on the wire , removed from the table** — a client should not walk a hierarchy to read a figure, and the  database should not hold nine million copies of AED. Four tables genuinely differ from their\n region and keep a stored currency: `orders.payment.tender_currency`, `inventory.supplier`, \n`ledger.account`, `control.partner_agreement`.\n"
   },
   "currencyScale": {
    "type": "integer",
    "minimum": 0,
    "maximum": 4,
    "x-ticvai-persisted": false,
    "description": "**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else — storing it per ro w is a copy of a fact that cannot differ. **Kept on the wire, removed from the table**: a cl ient reading a figure should not walk a hierarchy to know what it means, and the database sh ould not hold nine million copies of AED. Four tables genuinely differ from their region and\n keep a stored currency — `orders.payment.tender_currency`, `inventory.supplier`, `ledger.ac\ncount`, `control.partner_agreement`. **A guest paying USD at an AED venue is a real row; a w orkstation with its own currency is a misconfiguration.**\n"
   },
   "grossAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "taxAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "netAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "refundedAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "droppedPromotions": {
    "type": "array",
    "readOnly": true,
    "x-ticvai-persisted": false,
    "description": "**Promotions left off this order at checkout because their budget cap would have been exceeded** (decided 28 September, audit R101 (8)). Empty when none was dropped. Returned by `checkoutCart` and `createOrder`, not stored.\n",
    "items": {
     "type": "object",
     "required": [
      "promotionId"
     ],
     "properties": {
      "promotionId": {
       "type": "string",
       "format": "uuid"
      },
      "name": {
       "type": "string"
      },
      "reason": {
       "type": "string",
       "enum": [
        "budgetCapReached"
       ]
      }
     }
    }
   },
   "totalPriceVariance": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "description": "Sum across lines. Zero on a normal order."
   },
   "lines": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/OrderLine"
    }
   },
   "payments": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/Payment"
    }
   },
   "principalId": {
    "type": "string",
    "format": "uuid"
   },
   "workstationId": {
    "type": "string",
    "format": "uuid"
   },
   "shiftId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "subjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "holdLabel": {
    "type": "string",
    "maxLength": 60,
    "nullable": true,
    "readOnly": true,
    "description": "The `label` a cashier gave when parking it with `holdOrder` — how they find it again. Null on an order never held."
   },
   "heldUntil": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true,
    "description": "When a held order expires and is voided (states/order.yaml), from `holdOrder`'s `holdUntil`. Null on an order not currently held."
   },
   "createdAt": {
    "type": "string",
    "format": "date-time"
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time"
   },
   "syncedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   }
  }
 },
 "OrderChannel": {
  "type": "string",
  "description": "Where the order originated. Added when guest self-ordering was contracted — an order a guest placed on their own phone is commercially and operationally different from one a cashier typed, and reporting that cannot separate them cannot answer whether self-ordering is working.\n",
  "enum": [
   "pos",
   "kiosk",
   "guestApp",
   "guestWeb",
   "callCentre",
   "partner",
   "api",
   "backOffice"
  ]
 },
 "OrderLine": {
  "x-ticvai-persistence": "orders.order_line + orders.order_line_eligibility + orders.order_line_discount",
  "x-ticvai-retired-columns": [
   "promotion_id",
   "name",
   "reason"
  ],
  "allOf": [
   {
    "$ref": "#/components/schemas/CreateOrderLine"
   },
   {
    "type": "object",
    "required": [
     "serverUnitPrice",
     "taxAmount",
     "netAmount",
     "grossAmount"
    ],
    "properties": {
     "serverUnitPrice": {
      "allOf": [
       {
        "$ref": "../shared/common.yaml#/components/schemas/Money"
       }
      ],
      "description": "What the server computed on ingest."
     },
     "priceVariance": {
      "allOf": [
       {
        "$ref": "../shared/common.yaml#/components/schemas/Money"
       }
      ],
      "description": "Server minus quoted. Non-zero means the quoted price was honoured and the difference posted to the variance account.\n"
     },
     "taxAmount": {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     },
     "netAmount": {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     },
     "grossAmount": {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     },
     "entitlementIds": {
      "type": "array",
      "description": "The entitlements this line issued. **These are the ticket ids** — `transferOrderTickets.ticketIds` and `reprintOrder.reissuedTicketIds` take and return them.",
      "items": {
       "type": "string",
       "format": "uuid"
      }
     },
     "crossRegionRightIds": {
      "type": "array",
      "items": {
       "type": "string"
      },
      "description": "Redemption rights propagated to other cells for this line."
     },
     "reprintCount": {
      "type": "integer",
      "minimum": 0,
      "default": 0,
      "readOnly": true,
      "description": "How many times this line's tickets were reprinted or resent. `reprintOrder` increments it; repeated reprints are the signal worth surfacing."
     },
     "venueId": {
      "type": "string",
      "format": "uuid",
      "readOnly": true,
      "description": "The order's venue, copied onto the line (ADR-0044's own example; system-design review SD-008, 29 September) so a line is scoped and partitionable without its order."
     },
     "discounts": {
      "type": "array",
      "readOnly": true,
      "description": "**The discounts applied to this line, one row each** (system-design review SD-008, 29 September). Until then a discount object was flattened into the line as `promotion_id NOT NULL`, so a line with no promotion could not be inserted. A line with no discount has none.",
      "items": {
       "$ref": "#/components/schemas/OrderLineDiscount"
      }
     }
    }
   }
  ]
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
 "OrderLineDiscount": {
  "type": "object",
  "description": "One discount applied to one order line (SD-008). Rows of `orders.order_line_discount`.",
  "required": [
   "id",
   "amount",
   "source"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "promotionId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "x-ticvai-references": "promotions.promotion",
    "description": "The promotion that gave it. Null for a manual discount."
   },
   "source": {
    "type": "string",
    "enum": [
     "promotion",
     "promoCode",
     "manual",
     "bundle",
     "member"
    ]
   },
   "amount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "reason": {
    "type": "string",
    "maxLength": 200,
    "nullable": true,
    "description": "A cashier's reason for a manual discount."
   }
  }
 },
 "OrderStatus": {
  "type": "string",
  "enum": [
   "pending",
   "held",
   "paid",
   "partiallyPaid",
   "completed",
   "voided",
   "refunded",
   "partiallyRefunded",
   "failed"
  ],
  "description": "`held` is a parked sale — the cashier freed the till and the guest will return. It holds no inventory and expires, because a till that accumulates parked sales across a shift cannot be closed.\n"
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
 "Payment": {
  "x-ticvai-persistence": "orders.payment",
  "type": "object",
  "required": [
   "id",
   "orderId",
   "tender",
   "amount",
   "status",
   "recordedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "orderId": {
    "type": "string",
    "format": "uuid"
   },
   "tender": {
    "$ref": "#/components/schemas/TenderKind"
   },
   "tenderCurrency": {
    "type": "string",
    "pattern": "^[A-Z]{3}$",
    "description": "4.6.11. **What the guest actually handed over**, which is not always what the venue books. A tourist paying USD cash at a till is a foreign tender; the sale is still recorded in base currency.\nEqual to the base currency for almost every payment. **Present on all of them so the foreign-tender report has a source** — `getForeignTenderReport` promised *what was taken in which currency* and nothing recorded it until 18 August.\n"
   },
   "tenderAmount": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "description": "The amount in `tenderCurrency`, at that currency's own scale."
   },
   "fxRate": {
    "allOf": [
     {
      "$ref": "#/components/schemas/ExchangeRateDecimal"
     }
    ],
    "nullable": true,
    "description": "The rate applied, **stored on the payment rather than looked up later** (CF-37). A payment reconciled next month is reconciled at the rate of the day it was taken.\n"
   },
   "fxRateSource": {
    "type": "string",
    "nullable": true,
    "enum": [
     "manual",
     "feed",
     "cardScheme"
    ],
    "description": "4.2.8. Manual or fed on a schedule. **`cardScheme` is where the terminal did the conversion and told us** — dynamic currency conversion, the scheme's rate rather than ours.\n"
   },
   "changeCurrency": {
    "type": "string",
    "pattern": "^[A-Z]{3}$",
    "nullable": true,
    "description": "4.6.11 is deliberately asymmetric: **accept foreign currency, refund in local.** A till giving change in five currencies needs five floats and five counts, and the variance becomes unattributable.\n"
   },
   "amount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "changeAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "status": {
    "type": "string",
    "enum": [
     "authorised",
     "captured",
     "pendingConfirmation",
     "declined",
     "failed",
     "voided",
     "refunded"
    ]
   },
   "providerName": {
    "type": "string",
    "nullable": true
   },
   "providerReference": {
    "type": "string",
    "nullable": true,
    "description": "The provider's own id for the charge (Stripe PaymentIntent, NI order reference). What `payments.receivePaymentProviderWebhook` matches an incoming event on (SD-034)."
   },
   "providerIdempotencyKey": {
    "type": "string",
    "nullable": true,
    "readOnly": true,
    "description": "The idempotency key sent to the provider, which is this payment's `id` (SD-034, 29 September). A retried provider call cannot charge twice."
   },
   "terminalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The card terminal a till payment ran on (ECR flow, SD-034)."
   },
   "nextAction": {
    "type": "object",
    "nullable": true,
    "x-ticvai-persisted": false,
    "description": "**What the caller does while the payment is `pendingConfirmation`** (SD-034, 29 September). `redirect`: send the browser to `url` (3-D Secure challenge or hosted page); the provider returns the guest to `returnUrl` and the result arrives by webhook. `terminal`: the card terminal has been instructed; wait for its result. Null once the payment has an outcome.",
    "properties": {
     "kind": {
      "type": "string",
      "enum": [
       "redirect",
       "terminal"
      ]
     },
     "url": {
      "type": "string",
      "format": "uri",
      "nullable": true
     },
     "expiresAt": {
      "type": "string",
      "format": "date-time",
      "nullable": true
     }
    }
   },
   "lastInquiryAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time"
   },
   "syncedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   }
  }
 },
 "PaymentLinkView": {
  "type": "object",
  "x-ticvai-persistence": "none — projection of orders.payment_link for its holder",
  "description": "What an anonymous holder of a payment link is shown about the link itself.",
  "required": [
   "status",
   "expiresAt"
  ],
  "properties": {
   "status": {
    "type": "string",
    "enum": [
     "issued",
     "viewed",
     "paid",
     "expired",
     "cancelled",
     "superseded"
    ]
   },
   "expiresAt": {
    "type": "string",
    "format": "date-time"
   },
   "releaseHoldOnExpiry": {
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
 "RecordConsentRequest": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "required": [
   "purpose",
   "decision",
   "noticeVersion",
   "source",
   "recordedAt"
  ],
  "properties": {
   "purpose": {
    "$ref": "#/components/schemas/ConsentPurpose"
   },
   "decision": {
    "$ref": "#/components/schemas/ConsentDecision"
   },
   "channels": {
    "type": "array",
    "description": "Omit to apply to every channel the purpose covers.",
    "items": {
     "$ref": "#/components/schemas/MessageChannel"
    }
   },
   "noticeVersion": {
    "type": "string"
   },
   "source": {
    "$ref": "#/components/schemas/ConsentSource"
   },
   "recordedAt": {
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
 "SalesChannel": {
  "type": "string",
  "description": "**Where a sale came from.** Restored 24 August — this was lost in the `Money` rewrite and nine references across four contracts were pointing at nothing.\n**Not interchangeable with the local `Channel` enums.** `catalogue.Channel` and `orders.Channel` are byte-identical duplicates of each other listing `pos, kiosk, web, mobile, b2b, ota, callCentre`; `orders.OrderChannel` lists `guestApp, guestWeb, partner, api, backOffice` on top. **Pointing the nine at a local enum would silently narrow them** — and the duplication between the two `Channel` enums is the reason a shared one existed in the first place.\n**This is the reporting dimension**: attribution, promotion eligibility and settlement all group by it, which is why it has to mean the same thing in `orders`, `catalogue`, `subscription` and `marketing-crm` rather than four things that nearly line up.\n",
  "enum": [
   "pos",
   "kiosk",
   "guestApp",
   "guestWeb",
   "callCentre",
   "partner",
   "api",
   "backOffice",
   "b2b",
   "ota"
  ]
 },
 "TenderKind": {
  "type": "string",
  "description": "`wallet` is a **digital wallet** (Apple Pay, Google Pay and the like, taken through the gateway), the value the guest channels accept beside `card` (decided 28 September, audit R080 (a)). **The stored-value TICVAI wallet is a separate tender**: it is spent through `authoriseStoredValue` and `captureStoredValue` (`StoredValueKind` `wallet`), never as this value, so the client can see which of the two the decision meant.\n",
  "enum": [
   "cash",
   "card",
   "wallet",
   "voucher",
   "bankTransfer",
   "hotelCharge",
   "installment",
   "giftCard",
   "complimentary"
  ]
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
