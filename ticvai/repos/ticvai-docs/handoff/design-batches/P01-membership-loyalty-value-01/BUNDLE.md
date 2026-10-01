# P01-membership-loyalty-value-01 — P01 · Membership, Loyalty & Value

**5 screens · 52 operations · 65 schemas · 14 permissions**

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

- **Every control that can be refused must be gated.** 14 permissions apply here:
  `AI_USE, GUEST_MANAGE, GUEST_VIEW, GUEST_VIEW_PII, LOYALTY_REDEEM, MARKETING_MANAGE, MARKETING_VIEW, ORDER_CREATE, ORDER_VIEW, PAYMENT_VIEW, PRICE_VIEW, PRODUCT_VIEW`…. A control nobody can use must say so,
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
| `WEB-021` | Wallet & Gift Cards | listDetail | 11 | 2 | — |
| `WEB-022` | Membership Plans | listDetail | 4 | 0 | — |
| `WEB-023` | Membership Management | listDetail | 9 | 2 | — |
| `WEB-024` | Devices, Wishlist & Consent | listDetail | 23 | 8 | — |
| `WEB-043` | Loyalty & Rewards | listDetail | 7 | 2 | — |

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "WEB-021",
  "name": "Wallet & Gift Cards",
  "module": "Membership, Loyalty & Value",
  "requiresModule": "retail",
  "wave": 2,
  "capability": "C21",
  "implementation": {
   "app": "guest-web",
   "route": "/membership-loyalty-and-value/wallet-and-gift-cards",
   "component": "apps/guest-web/src/routes/membership-loyalty-and-value/WalletAndGiftCardsDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "WEB-001"
   ],
   "exitTo": [
    "WEB-001",
    "WEB-022",
    "WEB-023",
    "WEB-024"
   ],
   "inferred": true,
   "transitions": [
    {
     "to": "WEB-022",
     "trigger": "Membership Plans",
     "provenance": "derived — WEB-022 declares entryState.params productId and WEB-021 holds none of them. The edge carries nothing: WEB-022 finds productId (listProducts) itself, and WEB-022 opens on its own"
    },
    {
     "to": "WEB-023",
     "trigger": "Membership Management",
     "carries": [
      "orderId"
     ],
     "provenance": "derived — WEB-023 declares entryState.params caseId, orderId, statementId and WEB-021 holds orderId, so an edge into it carries them"
    },
    {
     "to": "WEB-024",
     "trigger": "Devices, Wishlist & Consent",
     "provenance": "derived — WEB-024 declares entryState.params deviceId, enrolmentId, itemId, methodId and WEB-021 holds none of them. The edge carries nothing: deviceId, itemId only pre-select (deep link or optional); WEB-024 finds methodId (enrolMfaMethod) itself; WEB-024 opens on getWishlist, and enrolmentId has no source on WEB-024 yet (a gap in WEB-024, not in this edge)"
    }
   ]
  },
  "notes": "Purpose derived from the screen name and its operations on 17 August, not from a requirement.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listWalletTransactions` reads the population and `getWallet` reads one of them — list, select, act",
  "purpose": "See wallet & gift cards for this venue.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every wallet transaction",
       "bindsTo": "WalletTransaction",
       "columns": [
        "WalletTransaction.id",
        "WalletTransaction.kind",
        "WalletTransaction.amount",
        "WalletTransaction.balanceAfter",
        "WalletTransaction.orderId",
        "WalletTransaction.venueId",
        "WalletTransaction.reason",
        "WalletTransaction.principalId",
        "WalletTransaction.recordedAt"
       ],
       "operation": "listWalletTransactions",
       "provenance": "contract retail.yaml GET /wallets/{subjectId}/transactions"
      },
      {
       "kind": "dataTable",
       "label": "Every payment token",
       "bindsTo": "PaymentToken",
       "columns": [
        "PaymentToken.id",
        "PaymentToken.subjectId",
        "PaymentToken.providerId",
        "PaymentToken.token",
        "PaymentToken.method",
        "PaymentToken.maskedIdentifier",
        "PaymentToken.expiresAt",
        "PaymentToken.isDefault",
        "PaymentToken.consentPurposeId"
       ],
       "operation": "listPaymentTokens",
       "provenance": "contract orders.yaml GET /payment-tokens"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected wallet transaction",
       "bindsTo": "WalletTransaction",
       "columns": [
        "WalletTransaction.id",
        "WalletTransaction.kind",
        "WalletTransaction.amount",
        "WalletTransaction.balanceAfter",
        "WalletTransaction.orderId",
        "WalletTransaction.venueId",
        "WalletTransaction.reason",
        "WalletTransaction.principalId",
        "WalletTransaction.recordedAt"
       ],
       "operation": "listWalletTransactions",
       "provenance": "contract wallet.yaml GET /wallets/{subjectId}/transactions"
      },
      {
       "kind": "detailPanel",
       "label": "The gift card",
       "bindsTo": "GiftCard",
       "columns": [
        "GiftCard.cardCode",
        "GiftCard.kind",
        "GiftCard.faceValue",
        "GiftCard.balance",
        "GiftCard.status",
        "GiftCard.blockedReason",
        "GiftCard.issuedAt",
        "GiftCard.activatedAt",
        "GiftCard.expiresAt"
       ],
       "operation": "getGiftCard",
       "provenance": "contract wallet.yaml GET /gift-cards/{cardCode}"
      },
      {
       "kind": "detailPanel",
       "label": "The game card",
       "bindsTo": "GameCard",
       "columns": [
        "GameCard.cardCode",
        "GameCard.kind",
        "GameCard.venueId",
        "GameCard.subjectId",
        "GameCard.credits",
        "GameCard.bonusCredits",
        "GameCard.points",
        "GameCard.status",
        "GameCard.blockedReason",
        "GameCard.transferredToCardCode",
        "GameCard.lastPlayedAt",
        "GameCard.issuedAt",
        "GameCard.expiresAt"
       ],
       "operation": "getGameCard",
       "provenance": "contract games.yaml GET /game-cards/{cardCode}"
      },
      {
       "kind": "detailPanel",
       "label": "The wallet",
       "bindsTo": "Wallet",
       "columns": [
        "Wallet.id",
        "Wallet.subjectId",
        "Wallet.balance",
        "Wallet.credits",
        "Wallet.bonusBalance",
        "Wallet.currency",
        "Wallet.status",
        "Wallet.homeCellName",
        "Wallet.expiresAt",
        "Wallet.lastActivityAt"
       ],
       "operation": "getWallet",
       "provenance": "contract wallet.yaml GET /wallets/{subjectId}"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Store payment token",
       "operation": "storePaymentToken",
       "provenance": "contract orders.yaml POST /payment-tokens"
      },
      {
       "kind": "secondaryButton",
       "label": "Transfer wallet balance",
       "operation": "transferWalletBalance",
       "provenance": "contract wallet.yaml POST /wallets/{walletId}/transfer"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The wallet gift cards list.",
   "error": "Could not load. Names which read failed and leaves the wallet gift cards untouched.",
   "emptyFirstRun": "No wallet gift cards yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table.",
   "emptyNoResults": "Never shown: `listWalletTransactions` takes no filter, so an empty list is always the first-run state above.",
   "emptyNoAccess": "**There is no permission to name — a guest holds none** (ADR-0025: `x-ticvai-permission` is what a staff caller must hold; a guest call resolves to the guest's own data). No access here means one of two things, told apart by the response: not signed in, where the guest is offered sign-in and brought back to this screen, or a record that is not theirs, which says so without saying whose it is. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "**The offline banner shows.** Balances and stored cards already loaded stay visible with their age, cards masked. Storing a card and transferring value need the server."
  },
  "apis": [
   {
    "operationId": "getWallet",
    "contract": "wallet",
    "purpose": "Read a guest wallet",
    "trigger": "onLoad"
   },
   {
    "operationId": "listWalletTransactions",
    "contract": "wallet",
    "purpose": "Wallet transaction history",
    "trigger": "onLoad"
   },
   {
    "operationId": "getGiftCard",
    "contract": "wallet",
    "purpose": "Check a gift card balance",
    "trigger": "onAction"
   },
   {
    "operationId": "getGameCard",
    "contract": "games",
    "purpose": "Balance on a game card",
    "trigger": "onAction"
   },
   {
    "operationId": "listPaymentTokens",
    "contract": "orders",
    "purpose": "Saved cards on this account",
    "trigger": "onLoad"
   },
   {
    "operationId": "storePaymentToken",
    "contract": "orders",
    "purpose": "Save a card for next time",
    "trigger": "onAction"
   },
   {
    "operationId": "transferWalletBalance",
    "contract": "wallet",
    "purpose": "Move value between wallets",
    "trigger": "onAction"
   },
   {
    "operationId": "getWalletAutoReloadSetting",
    "contract": "wallet",
    "purpose": "Show auto top-up",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "setWalletAutoReloadSetting",
    "contract": "wallet",
    "purpose": "Set auto top-up",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "getWalletExitBalance",
    "contract": "wallet",
    "purpose": "Balance due / refundable at exit",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "settleWalletAtExit",
    "contract": "wallet",
    "purpose": "Settle the wallet at exit",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "cardCode",
     "from": "deepLink"
    },
    {
     "name": "subjectId",
     "from": "session"
    },
    {
     "name": "walletId",
     "from": "navigation"
    }
   ],
   "coldEntry": "**A guest arriving cold on a link that no longer resolves is shown what happened and one way onward — never a 404.** A shared ticket, a forwarded confirmation and a push notification opened three weeks late all land here, and the person holding the link did nothing wrong. **The screen names the thing, says it is expired, cancelled or withdrawn, and offers the list it came from.** Arrives with `cardCode`.",
   "preloaded": [
    "WalletTransaction.id",
    "WalletTransaction.kind",
    "WalletTransaction.amount",
    "WalletTransaction.balanceAfter",
    "WalletTransaction.orderId"
   ]
  },
  "wireframe": {
   "status": "review",
   "provenance": "client-verified",
   "board": "wireframes/P01 Guest Web.dc.html#web-021",
   "prototype": {
    "file": "sources/designs/guest-rev3-28-september/TICVAI Guest Booking v2.dc.html",
    "rev": "rev 3",
    "verified": "2026-09-28",
    "match": "partial",
    "view": "Account → 'Wallet & gift cards' (and 'Payment methods')",
    "differences": "Rows with toast actions; no transaction list, no gift-card balance lookup. Auto top-up is a prototype addition with no YAML operation. Saved payment tokens are a separate pane."
   }
  },
  "apisNote": "Rebuilt 9 September 2026 from the 3 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formStorePaymentToken",
    "component": "modal",
    "trigger": "Store payment token",
    "body": "**Collects what `storePaymentToken` sends before it is called.** Required: `providerId`, `providerToken`, `consentPurposeId`. Optional: `setDefault`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Store payment token",
     "operation": "storePaymentToken"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "providerId",
      "providerToken",
      "consentPurposeId",
      "setDefault"
     ]
    },
    "provenance": "client-verified"
   },
   {
    "id": "formTransferWalletBalance",
    "component": "modal",
    "trigger": "Transfer wallet balance",
    "body": "**Collects what `transferWalletBalance` sends before it is called.** Required: `amount`. Optional: `toSubjectId`, `toWalletId`, `message`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Transfer wallet balance",
     "operation": "transferWalletBalance"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "amount",
      "toSubjectId",
      "toWalletId",
      "message"
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
  "id": "WEB-022",
  "name": "Membership Plans",
  "module": "Membership, Loyalty & Value",
  "requiresModule": "ticketing",
  "wave": 2,
  "capability": "C31",
  "implementation": {
   "app": "guest-web",
   "route": "/membership-loyalty-and-value/membership-plans",
   "component": "apps/guest-web/src/routes/membership-loyalty-and-value/MembershipPlansDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "WEB-001"
   ],
   "exitTo": [
    "WEB-001",
    "WEB-021",
    "WEB-023",
    "WEB-024"
   ],
   "inferred": true,
   "transitions": [
    {
     "to": "WEB-021",
     "trigger": "Wallet & Gift Cards",
     "provenance": "derived — WEB-021 declares entryState.params cardCode, walletId and WEB-022 holds none of them. The edge carries nothing: cardCode only pre-selects (deep link or optional); WEB-021 finds walletId (getWallet) itself, and WEB-021 opens on its own"
    },
    {
     "to": "WEB-023",
     "trigger": "Membership Management",
     "provenance": "derived — WEB-023 declares entryState.params caseId, orderId, statementId and WEB-022 holds none of them. The edge carries nothing: orderId only pre-selects (deep link or optional); WEB-023 finds statementId (listBillingStatements) itself; WEB-023 opens on listBillingStatements, and caseId has no source on WEB-023 yet (a gap in WEB-023, not in this edge)"
    },
    {
     "to": "WEB-024",
     "trigger": "Devices, Wishlist & Consent",
     "provenance": "derived — WEB-024 declares entryState.params deviceId, enrolmentId, itemId, methodId and WEB-022 holds none of them. The edge carries nothing: deviceId, itemId only pre-select (deep link or optional); WEB-024 finds methodId (enrolMfaMethod) itself; WEB-024 opens on getWishlist, and enrolmentId has no source on WEB-024 yet (a gap in WEB-024, not in this edge)"
    }
   ]
  },
  "notes": "Purpose derived from the screen name and its operations on 17 August, not from a requirement. **Wired 24 August**: getMyMemberships, listGuestMemberships. **The web surface drew the screen and could not fetch what it shows** — the app had these and the browser did not, and there is no reason a membership or a bundle should need an app.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listProducts` reads the population and `getProduct` reads one of them — list, select, act",
  "purpose": "Membership Plans — the screen a person opens when they need to deal with membership plans.",
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
       "operation": "listProducts",
       "notes": "Sends `?venueId=` to `listProducts`.",
       "provenance": "contract catalogue.yaml GET /products"
      },
      {
       "kind": "textField",
       "label": "Kind",
       "operation": "listProducts",
       "notes": "Sends `?kind=` to `listProducts`.",
       "provenance": "contract catalogue.yaml GET /products"
      },
      {
       "kind": "toggle",
       "label": "Is sellable",
       "operation": "listProducts",
       "notes": "Sends `?isSellable=` to `listProducts`.",
       "provenance": "contract catalogue.yaml GET /products"
      },
      {
       "kind": "dataTable",
       "label": "Every product",
       "bindsTo": "Product",
       "columns": [
        "Product.id",
        "Product.code",
        "Product.name",
        "Product.description",
        "Product.kind",
        "Product.venueId",
        "Product.scopePath",
        "Product.createdByPrincipalId",
        "Product.approvedByPrincipalId",
        "Product.responsibleDepartmentId",
        "Product.onSaleFrom",
        "Product.onSaleTo"
       ],
       "operation": "listProducts",
       "provenance": "contract catalogue.yaml GET /products"
      },
      {
       "kind": "dataTable",
       "label": "Every guest membership",
       "bindsTo": "GuestMembership",
       "columns": [
        "GuestMembership.entitlementId",
        "GuestMembership.productId",
        "GuestMembership.name",
        "GuestMembership.tier",
        "GuestMembership.status",
        "GuestMembership.validFrom",
        "GuestMembership.validTo",
        "GuestMembership.frozenDays",
        "GuestMembership.benefits",
        "GuestMembership.renewsOn",
        "GuestMembership.previousTerms"
       ],
       "operation": "listGuestMemberships",
       "provenance": "contract catalogue.yaml GET /guest/memberships"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected product",
       "bindsTo": "Product",
       "columns": [
        "Product.id",
        "Product.code",
        "Product.name",
        "Product.description",
        "Product.kind",
        "Product.venueId",
        "Product.scopePath",
        "Product.createdByPrincipalId",
        "Product.approvedByPrincipalId",
        "Product.responsibleDepartmentId",
        "Product.onSaleFrom",
        "Product.onSaleTo",
        "Product.lifecycleState",
        "Product.isSellable",
        "Product.hasVariants",
        "Product.variantCount"
       ],
       "operation": "getProduct",
       "provenance": "contract catalogue.yaml GET /products/{productId}"
      },
      {
       "kind": "detailPanel",
       "label": "The guest membership",
       "bindsTo": "GuestMembership",
       "columns": [
        "GuestMembership.entitlementId",
        "GuestMembership.productId",
        "GuestMembership.name",
        "GuestMembership.tier",
        "GuestMembership.status",
        "GuestMembership.validFrom",
        "GuestMembership.validTo",
        "GuestMembership.frozenDays",
        "GuestMembership.benefits",
        "GuestMembership.renewsOn",
        "GuestMembership.previousTerms"
       ],
       "operation": "getMyMemberships",
       "provenance": "contract catalogue.yaml GET /guests/me/memberships"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The membership plans list.",
   "error": "Could not load. Names which read failed and leaves the membership plans untouched.",
   "emptyFirstRun": "No membership plans yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table.",
   "emptyNoResults": "Nothing matches the filter on venueId, kind, isSellable and the membership plans are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "**There is no permission to name — a guest holds none** (ADR-0025: `x-ticvai-permission` is what a staff caller must hold; a guest call resolves to the guest's own data). No access here means one of two things, told apart by the response: not signed in, where the guest is offered sign-in and brought back to this screen, or a record that is not theirs, which says so without saying whose it is. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "**The offline banner shows.** What was already loaded stays on screen, marked with its age. Anything that spends money, holds capacity or changes the account waits for the connection, and its button says so rather than failing."
  },
  "apis": [
   {
    "operationId": "listProducts",
    "contract": "catalogue",
    "purpose": "List products",
    "trigger": "onLoad"
   },
   {
    "operationId": "getProduct",
    "contract": "catalogue",
    "purpose": "Read a product",
    "trigger": "onLoad"
   },
   {
    "operationId": "getMyMemberships",
    "contract": "catalogue",
    "purpose": "A guest's own memberships, benefits and history",
    "trigger": "onLoad"
   },
   {
    "operationId": "listGuestMemberships",
    "contract": "catalogue",
    "purpose": "A guest's memberships, benefits and history",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "productId",
     "from": "WEB-001"
    }
   ],
   "coldEntry": "Resolves from the session; a cold arrival is the ordinary case.",
   "preloaded": [
    "Product.id",
    "Product.code",
    "Product.name",
    "Product.description",
    "Product.kind"
   ]
  },
  "wireframe": {
   "status": "review",
   "provenance": "client-verified",
   "board": "wireframes/P01 Guest Web.dc.html#web-022",
   "prototype": {
    "file": "sources/designs/guest-rev3-28-september/TICVAI Guest Booking v2.dc.html",
    "rev": "rev 3",
    "verified": "2026-09-28",
    "match": "partial",
    "view": "Summit Peaks → 'Annual pass / membership' flow; Kids Club → 'Membership pass'; Account → Membership → 'Other plans — Compare'",
    "differences": "Plans are sold as a booking flow, not a plans page; the account 'Compare' action is a toast."
   }
  },
  "apisNote": "Rebuilt 9 September 2026 from the 4 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
  "id": "WEB-023",
  "name": "Membership Management",
  "module": "Membership, Loyalty & Value",
  "requiresModule": "ticketing",
  "wave": 2,
  "capability": "C31",
  "implementation": {
   "app": "guest-web",
   "route": "/membership-loyalty-and-value/membership-management",
   "component": "apps/guest-web/src/routes/membership-loyalty-and-value/MembershipManagementForm.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "WEB-001"
   ],
   "inferred": true,
   "exitTo": [
    "WEB-001",
    "WEB-021",
    "WEB-022",
    "WEB-024"
   ],
   "transitions": [
    {
     "to": "WEB-021",
     "trigger": "Wallet & Gift Cards",
     "provenance": "derived — WEB-021 declares entryState.params cardCode, walletId and WEB-023 holds none of them. The edge carries nothing: cardCode only pre-selects (deep link or optional); WEB-021 finds walletId (getWallet) itself, and WEB-021 opens on its own"
    },
    {
     "to": "WEB-022",
     "trigger": "Membership Plans",
     "carries": [
      "productId"
     ],
     "provenance": "derived — WEB-022 declares entryState.params productId and WEB-023 holds productId, so an edge into it carries them"
    },
    {
     "to": "WEB-024",
     "trigger": "Devices, Wishlist & Consent",
     "provenance": "derived — WEB-024 declares entryState.params deviceId, enrolmentId, itemId, methodId and WEB-023 holds none of them. The edge carries nothing: deviceId, itemId only pre-select (deep link or optional); WEB-024 finds methodId (enrolMfaMethod) itself; WEB-024 opens on getWishlist, and enrolmentId has no source on WEB-024 yet (a gap in WEB-024, not in this edge)"
    }
   ]
  },
  "notes": "Purpose derived from the screen name and its operations on 17 August, not from a requirement. **Wired 24 August**: getMyMemberships, listGuestMemberships. **The web surface drew the screen and could not fetch what it shows** — the app had these and the browser did not, and there is no reason a membership or a bundle should need an app.\n\n**Rev 3 (decided 29 September, rev 3 DG-2, no contract change).** The billing statement shows the decline states: a **soft decline** offers *Retry now* (`retryMyDunningPayment`) and *Use another card*; a **hard decline** offers another card only; **declined again** shows the next retry date; then **paid**.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listGuestMemberships` reads the population and `getMyMemberships` reads one of them — list, select, act",
  "purpose": "Work with membership management for this venue.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every membership",
       "bindsTo": "GuestMembership",
       "columns": [
        "GuestMembership.entitlementId",
        "GuestMembership.productId",
        "GuestMembership.name",
        "GuestMembership.tier",
        "GuestMembership.status",
        "GuestMembership.validFrom",
        "GuestMembership.validTo",
        "GuestMembership.frozenDays",
        "GuestMembership.benefits",
        "GuestMembership.renewsOn",
        "GuestMembership.previousTerms"
       ],
       "operation": "listGuestMemberships",
       "provenance": "contract catalogue.yaml GET /guest/memberships"
      },
      {
       "kind": "datePicker",
       "label": "From",
       "operation": "listBillingStatements",
       "notes": "Sends `?from=` to `listBillingStatements`.",
       "provenance": "contract orders.yaml GET /billing-statements"
      },
      {
       "kind": "datePicker",
       "label": "To",
       "operation": "listBillingStatements",
       "notes": "Sends `?to=` to `listBillingStatements`.",
       "provenance": "contract orders.yaml GET /billing-statements"
      },
      {
       "kind": "dataTable",
       "label": "Every billing statement",
       "bindsTo": "BillingStatement",
       "columns": [
        "BillingStatement.id",
        "BillingStatement.subjectId",
        "BillingStatement.periodStart",
        "BillingStatement.periodEnd",
        "BillingStatement.lines",
        "BillingStatement.total",
        "BillingStatement.isTaxInvoice"
       ],
       "operation": "listBillingStatements",
       "provenance": "contract orders.yaml GET /billing-statements"
      },
      {
       "kind": "dataTable",
       "label": "Every dunning case",
       "bindsTo": "DunningCase",
       "columns": [
        "DunningCase.id",
        "DunningCase.subjectId",
        "DunningCase.orderId",
        "DunningCase.amount",
        "DunningCase.state",
        "DunningCase.declineClass",
        "DunningCase.attemptsMade",
        "DunningCase.nextAttemptAt",
        "DunningCase.firstFailedAt",
        "DunningCase.resolvedAt",
        "DunningCase.resolution",
        "DunningCase.resolutionNote"
       ],
       "operation": "listMyPaymentIssues",
       "provenance": "contract payments.yaml GET /guests/me/payment-issues"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected billing statement",
       "bindsTo": "BillingStatement",
       "columns": [
        "BillingStatement.id",
        "BillingStatement.subjectId",
        "BillingStatement.periodStart",
        "BillingStatement.periodEnd",
        "BillingStatement.lines",
        "BillingStatement.total",
        "BillingStatement.isTaxInvoice"
       ],
       "operation": "getBillingStatement",
       "provenance": "contract orders.yaml GET /billing-statements/{statementId}"
      },
      {
       "kind": "detailPanel",
       "label": "The guest membership",
       "bindsTo": "GuestMembership",
       "columns": [
        "GuestMembership.entitlementId",
        "GuestMembership.productId",
        "GuestMembership.name",
        "GuestMembership.tier",
        "GuestMembership.status",
        "GuestMembership.validFrom",
        "GuestMembership.validTo",
        "GuestMembership.frozenDays",
        "GuestMembership.benefits",
        "GuestMembership.renewsOn",
        "GuestMembership.previousTerms"
       ],
       "operation": "getMyMemberships",
       "provenance": "contract catalogue.yaml GET /guests/me/memberships"
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
       "label": "Retry my dunning payment",
       "operation": "retryMyDunningPayment",
       "provenance": "contract payments.yaml POST /dunning-cases/{caseId}/retry"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "Membership and its benefits",
   "error": "Could not load. Cancellation and renewal are both blocked",
   "emptyFirstRun": "—",
   "emptyNoResults": "Nothing matches the filter on from, to and the membership are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "**There is no permission to name — a guest holds none** (ADR-0025: `x-ticvai-permission` is what a staff caller must hold; a guest call resolves to the guest's own data). No access here means one of two things, told apart by the response: not signed in, where the guest is offered sign-in and brought back to this screen, or a record that is not theirs, which says so without saying whose it is. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "**The offline banner shows.** What was already loaded stays on screen, marked with its age. Anything that spends money, holds capacity or changes the account waits for the connection, and its button says so rather than failing."
  },
  "apis": [
   {
    "operationId": "listBillingStatements",
    "contract": "orders",
    "purpose": "Membership billing statements",
    "trigger": "onLoad"
   },
   {
    "operationId": "getBillingStatement",
    "contract": "orders",
    "purpose": "One statement, line by line",
    "trigger": "onAction"
   },
   {
    "operationId": "listMyPaymentIssues",
    "contract": "payments",
    "purpose": "Declined renewals waiting on the guest",
    "trigger": "onLoad"
   },
   {
    "operationId": "retryMyDunningPayment",
    "contract": "payments",
    "purpose": "Retry a declined payment, on another card if needed",
    "trigger": "onAction"
   },
   {
    "operationId": "transferOrderTickets",
    "contract": "orders",
    "purpose": "Transfer tickets to another guest",
    "trigger": "onAction",
    "invalidates": [
     "listGuestMemberships"
    ]
   },
   {
    "operationId": "getMyMemberships",
    "contract": "catalogue",
    "purpose": "A guest's own memberships, benefits and history",
    "trigger": "onLoad"
   },
   {
    "operationId": "listGuestMemberships",
    "contract": "catalogue",
    "purpose": "A guest's memberships, benefits and history",
    "trigger": "onLoad"
   },
   {
    "operationId": "listInstalmentPlans",
    "contract": "payments",
    "purpose": "Instalment plans and schedule",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "createInstalmentPlan",
    "contract": "payments",
    "purpose": "Pay in instalments",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "orderId",
     "from": "deepLink"
    },
    {
     "name": "caseId",
     "from": "navigation"
    },
    {
     "name": "statementId",
     "from": "navigation"
    }
   ],
   "coldEntry": "**A guest opening an order link weeks later.** Shows the order if it still resolves; if it was refunded or the performance passed, says which and offers the order list rather than an error.",
   "preloaded": [
    "BillingStatement.id",
    "BillingStatement.subjectId",
    "BillingStatement.periodStart",
    "BillingStatement.periodEnd",
    "BillingStatement.lines"
   ]
  },
  "wireframe": {
   "status": "review",
   "provenance": "client-verified",
   "board": "wireframes/P01 Guest Web.dc.html#web-023",
   "prototype": {
    "file": "sources/designs/guest-rev3-28-september/TICVAI Guest Booking v2.dc.html",
    "rev": "rev 3",
    "verified": "2026-09-28",
    "match": "partial",
    "view": "Account → 'Membership' → 'Billing statement — View'",
    "differences": "Billing and dunning retry are well covered. Prototype adds membership transfer to a family member and guest passes; YAML's transferOrderTickets on this screen has no visible use."
   }
  },
  "apisNote": "Rebuilt 9 September 2026 from the 3 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formRetryMyDunningPayment",
    "component": "modal",
    "trigger": "Retry my dunning payment",
    "body": "**Collects what `retryMyDunningPayment` sends before it is called.** Nothing in the body is required. Optional: `paymentTokenId`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "RetryDunningPaymentRequest",
    "confirm": {
     "label": "Retry my dunning payment",
     "operation": "retryMyDunningPayment"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "paymentTokenId"
     ]
    },
    "provenance": "client-verified"
   },
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
  "id": "WEB-024",
  "name": "Devices, Wishlist & Consent",
  "module": "Membership, Loyalty & Value",
  "requiresModule": "marketing",
  "wave": 3,
  "capability": "C93",
  "implementation": {
   "app": "guest-web",
   "route": "/membership-loyalty-and-value/loyalty-and-rewards",
   "component": "apps/guest-web/src/routes/membership-loyalty-and-value/LoyaltyAndRewardsDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "WEB-001"
   ],
   "exitTo": [
    "WEB-001",
    "WEB-021",
    "WEB-022",
    "WEB-023"
   ],
   "inferred": true,
   "transitions": [
    {
     "to": "WEB-021",
     "trigger": "Wallet & Gift Cards",
     "provenance": "derived — WEB-021 declares entryState.params cardCode, walletId and WEB-024 holds none of them. The edge carries nothing: cardCode only pre-selects (deep link or optional); WEB-021 finds walletId (getWallet) itself, and WEB-021 opens on its own"
    },
    {
     "to": "WEB-022",
     "trigger": "Membership Plans",
     "provenance": "derived — WEB-022 declares entryState.params productId and WEB-024 holds none of them. The edge carries nothing: WEB-022 finds productId (listProducts) itself, and WEB-022 opens on its own"
    },
    {
     "to": "WEB-023",
     "trigger": "Membership Management",
     "provenance": "derived — WEB-023 declares entryState.params caseId, orderId, statementId and WEB-024 holds none of them. The edge carries nothing: orderId only pre-selects (deep link or optional); WEB-023 finds statementId (listBillingStatements) itself; WEB-023 opens on listBillingStatements, and caseId has no source on WEB-023 yet (a gap in WEB-023, not in this edge)"
    },
    {
     "to": "GST-037",
     "trigger": "Offers are shown against what they hold",
     "provenance": "flow F53 step 2→3",
     "crossesDevice": true,
     "back": false
    }
   ]
  },
  "notes": "Purpose derived from the screen name and its operations on 17 August, not from a requirement. **Renamed 31 August** from *Loyalty & Rewards*. **A guest surface is one product with two renderings** — a screen named differently on web and app is two screens to a developer and one journey to a guest.\n\n**Rev 3 (decided 29 September).** **Security (GAP-D1):** the devices list and signing out a lost device are here (`listGuestDevices`, `revokeGuestDevice`, already declared). **Face Pass stays mobile-only** (GST-069) until the facial-reader vendor SDK is named and supports web capture; viewing and withdrawing an enrolment stay here. **Two-step verification (GAP-B1, per venue):** enrolment appears only when a venue of the tenant enabled it. **One implementation, several ids (GAP-D3):** WEB-009 and WEB-024 are built as one account area; both ids are kept.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listGuestDevices` reads the population and `getWishlist` reads one of them — list, select, act",
  "purpose": "See loyalty & rewards for this venue.",
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
       "label": "Every delegated access",
       "bindsTo": "DelegatedAccess",
       "columns": [
        "DelegatedAccess.id",
        "DelegatedAccess.principalId",
        "DelegatedAccess.roleId",
        "DelegatedAccess.permission",
        "DelegatedAccess.subjectId",
        "DelegatedAccess.overSubjectId",
        "DelegatedAccess.overObjectRef",
        "DelegatedAccess.delegationKind",
        "DelegatedAccess.quota",
        "DelegatedAccess.isRevocableBySubject",
        "DelegatedAccess.scopePath",
        "DelegatedAccess.effect"
       ],
       "operation": "listDelegations",
       "provenance": "contract identity.yaml GET /guests/{subjectId}/delegations"
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
       "kind": "selectField",
       "label": "Whose Face Pass",
       "bindsTo": "DelegatedAccess",
       "columns": [
        "DelegatedAccess.overSubjectId",
        "DelegatedAccess.delegationKind"
       ],
       "operation": "listDelegations",
       "notes": "**Who is this for** (decided 28 September, audit R205): the signed-in guest and each child linked to them (`heldByThisGuest` with `delegationKind` `familyMember` or `primaryHolder`), so a parent sees and can revoke a child's enrolment here. Enrolling is app-only (GST-069), where the same pick sets the `subjectId` `enrolFacePass` sends; no guardian field is collected — the server records the caller as guardian. A 403 `subject-not-linked` says the person is no longer linked.",
       "provenance": "contract identity.yaml GET /guests/{subjectId}/delegations"
      },
      {
       "kind": "detailPanel",
       "label": "The face pass enrolment",
       "bindsTo": "FacePassEnrolment",
       "columns": [
        "FacePassEnrolment.id",
        "FacePassEnrolment.subjectId",
        "FacePassEnrolment.entitlementId",
        "FacePassEnrolment.kind",
        "FacePassEnrolment.retentionAnchor",
        "FacePassEnrolment.source",
        "FacePassEnrolment.capturedAt",
        "FacePassEnrolment.consentPurposeId",
        "FacePassEnrolment.consentGivenAt",
        "FacePassEnrolment.guardianSubjectId",
        "FacePassEnrolment.isActive",
        "FacePassEnrolment.expiresAt"
       ],
       "operation": "getFacePassEnrolment",
       "provenance": "contract access.yaml GET /face-pass/enrolments/{enrolmentId}"
      },
      {
       "kind": "detailPanel",
       "label": "The consent state",
       "bindsTo": "ConsentState",
       "columns": [
        "ConsentState.subjectId",
        "ConsentState.purposes"
       ],
       "operation": "getGuestConsents",
       "provenance": "contract marketing-crm.yaml GET /guests/{subjectId}/consents"
      },
      {
       "kind": "detailPanel",
       "label": "Waiver status",
       "operation": "getWaiverStatus",
       "notes": "Shows `isSatisfied`, `missingFormIds`, `expiringWithinDays` from `getWaiverStatus`'s inline response. **The response has no named schema**, so this cannot bind until the contract names one.",
       "provenance": "contract marketing-crm.yaml GET /guests/{subjectId}/waiver-status"
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
      },
      {
       "kind": "cardList",
       "label": "Two-step verification",
       "notes": "**Offered only when at least one venue of the tenant has guest two-step verification on** (`VenueSettings.identity.guestTwoStep.enabled`); otherwise the section is not shown. Enrolment is on the guest's account (enrol, verify, remove); the code is then asked only when signing in or acting at a venue that has it on.",
       "operation": "listMfaMethods",
       "provenance": "decided 29 September, rev 3 GAP-B1 (per venue)"
      },
      {
       "kind": "cardList",
       "label": "Signed-in devices",
       "notes": "The devices signed in to this account, with **Sign out this device** for a lost one (`revokeGuestDevice`).",
       "operation": "listGuestDevices",
       "provenance": "decided 29 September, rev 3 GAP-D1"
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
       "kind": "destructiveButton",
       "label": "Delete guest account",
       "operation": "deleteGuestAccount",
       "provenance": "contract identity.yaml DELETE /auth/guest/account"
      },
      {
       "kind": "secondaryButton",
       "label": "Export subject data",
       "operation": "exportSubjectData",
       "provenance": "contract identity.yaml POST /guests/{subjectId}/data-export"
      },
      {
       "kind": "secondaryButton",
       "label": "Grant delegation",
       "operation": "grantDelegation",
       "provenance": "contract identity.yaml POST /guests/{subjectId}/delegations"
      },
      {
       "kind": "destructiveButton",
       "label": "Revoke face pass",
       "operation": "revokeFacePass",
       "provenance": "contract access.yaml DELETE /face-pass/enrolments/{enrolmentId}"
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
    "body": "**Names what `removeFromWishlist` changes and what it leaves alone**, in the consequence rather than the verb. A devices wishlist consent this affects should be identified in the dialog, not just counted.",
    "provenance": "client-verified"
   },
   {
    "id": "confirmRevokeGuestDevice",
    "component": "confirmDialog",
    "trigger": "Revoke guest device",
    "body": "**Names what `revokeGuestDevice` changes and what it leaves alone**, in the consequence rather than the verb. A devices wishlist consent this affects should be identified in the dialog, not just counted.",
    "provenance": "client-verified"
   },
   {
    "id": "confirmDeleteGuestAccount",
    "component": "confirmDialog",
    "trigger": "Delete guest account",
    "body": "**Names what `deleteGuestAccount` changes and what it leaves alone**, in the consequence rather than the verb. A devices wishlist consent this affects should be identified in the dialog, not just counted.",
    "provenance": "client-verified"
   },
   {
    "id": "formGrantDelegation",
    "component": "modal",
    "trigger": "Grant delegation",
    "body": "**Collects what `grantDelegation` sends before it is called.** Required: `overSubjectId`, `delegationKind`, `permission`. Optional: `overObjectRef`, `quota`, `validTo`, `isRevocableBySubject`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Grant delegation",
     "operation": "grantDelegation"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "overSubjectId",
      "delegationKind",
      "permission",
      "overObjectRef",
      "quota",
      "validTo",
      "isRevocableBySubject"
     ]
    },
    "provenance": "client-verified"
   },
   {
    "id": "confirmRevokeFacePass",
    "component": "confirmDialog",
    "trigger": "Revoke face pass",
    "body": "**Names what `revokeFacePass` changes and what it leaves alone**, in the consequence rather than the verb. A devices wishlist consent this affects should be identified in the dialog, not just counted.",
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
   }
  ],
  "states": {
   "loading": "Points and rewards",
   "error": "Could not load",
   "emptyFirstRun": "No points yet — explains how they accrue",
   "emptyNoResults": "Nothing matches the current filters. **The filters are named and clearable from here** — an empty list with the filter state hidden elsewhere is a person who thinks the data is gone. **Added 25 August with the derived list component**: a screen that lists has to say what it shows when the list is empty, and this screen gained the list before it gained the sentence.",
   "emptyNoAccess": "**There is no permission to name — a guest holds none** (ADR-0025: `x-ticvai-permission` is what a staff caller must hold; a guest call resolves to the guest's own data). No access here means one of two things, told apart by the response: not signed in, where the guest is offered sign-in and brought back to this screen, or a record that is not theirs, which says so without saying whose it is. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "**Nothing here is offered offline, and the banner says so.** An erasure request or a device change queued and never sent is worse than one that could not be made — the legal clock starts when the platform receives it, and a device signed out offline is still signed in."
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
    "operationId": "deleteGuestAccount",
    "contract": "identity",
    "purpose": "Ask for the account to be deleted",
    "trigger": "onAction"
   },
   {
    "operationId": "exportSubjectData",
    "contract": "identity",
    "purpose": "Export everything held about this guest",
    "trigger": "onAction"
   },
   {
    "operationId": "getFacePassEnrolment",
    "contract": "access",
    "purpose": "Whether a face pass is enrolled on this account",
    "trigger": "onAction"
   },
   {
    "operationId": "getGuestConsents",
    "contract": "marketing-crm",
    "purpose": "What this guest has consented to",
    "trigger": "onLoad"
   },
   {
    "operationId": "getWaiverStatus",
    "contract": "marketing-crm",
    "purpose": "Which waivers are signed and which are due",
    "trigger": "onLoad"
   },
   {
    "operationId": "grantDelegation",
    "contract": "identity",
    "purpose": "Let somebody else manage a booking",
    "trigger": "onAction"
   },
   {
    "operationId": "listDelegations",
    "contract": "identity",
    "purpose": "Who may act for this guest",
    "trigger": "onLoad"
   },
   {
    "operationId": "revokeFacePass",
    "contract": "access",
    "purpose": "Revoke it after losing the phone that made it",
    "trigger": "onAction"
   },
   {
    "operationId": "listMfaMethods",
    "contract": "identity",
    "purpose": "The guest's enrolled second-factor methods",
    "trigger": "onLoad"
   },
   {
    "operationId": "enrolMfaMethod",
    "contract": "identity",
    "purpose": "Enrol an authenticator (email code as fallback)",
    "trigger": "onAction",
    "invalidates": [
     "listMfaMethods"
    ]
   },
   {
    "operationId": "verifyMfaEnrolment",
    "contract": "identity",
    "purpose": "Confirm the enrolment with a first code",
    "trigger": "onAction",
    "invalidates": [
     "listMfaMethods"
    ]
   },
   {
    "operationId": "removeMfaMethod",
    "contract": "identity",
    "purpose": "Remove a method",
    "trigger": "onAction",
    "invalidates": [
     "listMfaMethods"
    ]
   },
   {
    "operationId": "getCookieConsentRuntime",
    "contract": "marketing-crm",
    "purpose": "Preference centre: categories and the current decision",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "listPublishedTrackingTechnologies",
    "contract": "marketing-crm",
    "purpose": "Each cookie's name, provider, purpose, expiry and party",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "getDeviceConsentHistory",
    "contract": "marketing-crm",
    "purpose": "My cookie decisions so far",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "recordDeviceConsent",
    "contract": "marketing-crm",
    "purpose": "Change or withdraw cookie preferences",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
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
     "name": "enrolmentId",
     "from": "navigation"
    },
    {
     "name": "methodId",
     "from": "navigation"
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
   "board": "wireframes/P01 Guest Web.dc.html#web-024",
   "prototype": {
    "file": "sources/designs/guest-rev3-28-september/TICVAI Guest Booking v2.dc.html",
    "rev": "rev 3",
    "verified": "2026-09-28",
    "match": "partial",
    "view": "Account → 'Security' (devices), 'Face Pass', 'Data & privacy', 'Newsletters' (devices that get notifications)",
    "differences": "Spread across four panes rather than one screen; wishlist is its own view (WEB-009). Security pane includes passkeys and two-step verification, which the YAML does not have for guests. YAML purpose text still says 'See loyalty & rewards' (stale)."
   }
  },
  "apisNote": "Rebuilt 9 September 2026 from the 7 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "gaps": [
   {
    "operation": "getWaiverStatus",
    "why": "**`getWaiverStatus` declares its response inline**, so the component that shows it names fields but binds to no schema. The contract should name the shape.",
    "source": "contract marketing-crm.yaml GET /guests/{subjectId}/waiver-status"
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
  "id": "WEB-043",
  "name": "Loyalty & Rewards",
  "module": "Membership, Loyalty & Value",
  "requiresModule": "marketing",
  "wave": 2,
  "implementation": {
   "app": "guest-web",
   "route": "/loyalty-and-rewards",
   "component": "apps/guest-web/src/routes/LoyaltyRewards.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "WEB-001"
   ],
   "exitTo": [
    "WEB-001"
   ]
  },
  "notes": "**P01 Board 3 drew *Membership* with nothing behind it.** `getLoyaltyPosition` and `listLoyaltyProgrammes` were app-only — **the surface a guest checks their points on between visits is the web one.**\n**`evaluatePromotions` removed 27 September 2026 (audit root R292).** It evaluates promotions against a cart — `EvaluatePromotionsRequest` requires `venueId`, `channel` and at least one line — and this screen arrives with no parameter and holds no cart. Offers apply on WEB-005 and WEB-010, which keep the call.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listLoyaltyProgrammes` reads the population and `getLoyaltyPosition` reads one of them — list, select, act",
  "purpose": "Points, tier, and what the next one needs.",
  "gaps": [
   {
    "operation": "getLoyaltyPosition",
    "why": "**`getLoyaltyPosition` declares its response inline**, so the component that shows it names fields but binds to no schema. The contract should name the shape.",
    "source": "contract marketing-crm.yaml GET /loyalty/position"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every loyalty programme",
       "bindsTo": "LoyaltyProgramme",
       "columns": [
        "LoyaltyProgramme.id",
        "LoyaltyProgramme.code",
        "LoyaltyProgramme.name",
        "LoyaltyProgramme.venueId",
        "LoyaltyProgramme.pointsLiabilityAccountId",
        "LoyaltyProgramme.earnRules",
        "LoyaltyProgramme.tiers",
        "LoyaltyProgramme.pointsExpireAfterMonths",
        "LoyaltyProgramme.isActive"
       ],
       "operation": "listLoyaltyProgrammes",
       "provenance": "contract marketing-crm.yaml GET /loyalty/programmes"
      },
      {
       "kind": "dataTable",
       "label": "Every promotion",
       "bindsTo": "Promotion",
       "columns": [
        "Promotion.code",
        "Promotion.name",
        "Promotion.description",
        "Promotion.venueId",
        "Promotion.discount",
        "Promotion.conditions",
        "Promotion.stackingMode",
        "Promotion.stackingGroup",
        "Promotion.precedence",
        "Promotion.validFrom",
        "Promotion.validTo",
        "Promotion.maxRedemptions"
       ],
       "operation": "listPromotions",
       "provenance": "contract promotions.yaml GET /promotions"
      },
      {
       "kind": "cardList",
       "label": "Loyalty & Rewards",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "detailPanel",
       "label": "Detail",
       "provenance": "carried from the previous definition"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "reads",
     "components": [
      {
       "kind": "detailPanel",
       "label": "Loyalty position",
       "operation": "getLoyaltyPosition",
       "notes": "Shows `subjectId`, `programmeId`, `pointsBalance`, `pointsPending`, `tier`, `nextTier`, `pointsToNextTier`, `expiringPoints`, `expiringAt` from `getLoyaltyPosition`'s inline response. **The response has no named schema**, so this cannot bind until the contract names one.",
       "provenance": "contract marketing-crm.yaml GET /loyalty/position"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Create referral",
       "operation": "createReferral",
       "provenance": "contract marketing-crm.yaml POST /referrals"
      },
      {
       "kind": "secondaryButton",
       "label": "Redeem loyalty points",
       "operation": "redeemLoyaltyPoints",
       "provenance": "contract marketing-crm.yaml POST /loyalty/redemptions"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "Content resolves in place.",
   "error": "Could not load. **The rest of the site is unaffected.**",
   "emptyFirstRun": "**Nothing here yet for this venue.** Names what turns it on rather than showing an empty panel.",
   "emptyNoResults": "Nothing matches.",
   "emptyNoAccess": "**Sign in to see this.** A guest who is not signed in is offered the door, not refused.",
   "offline": "**The offline banner shows.** The last known balance stays with its age, and **points earned since are not shown** — and that is said. Redeeming and referring need the connection."
  },
  "apis": [
   {
    "operationId": "getLoyaltyPosition",
    "contract": "marketing-crm",
    "purpose": "A guest's points, tier and what is within reach",
    "trigger": "onLoad"
   },
   {
    "operationId": "listLoyaltyProgrammes",
    "contract": "marketing-crm",
    "purpose": "List loyalty programmes",
    "trigger": "onLoad"
   },
   {
    "operationId": "listPromotions",
    "contract": "promotions",
    "purpose": "List promotions",
    "trigger": "onLoad"
   },
   {
    "operationId": "createReferral",
    "contract": "marketing-crm",
    "purpose": "Refer a friend",
    "trigger": "onAction"
   },
   {
    "operationId": "redeemLoyaltyPoints",
    "contract": "marketing-crm",
    "purpose": "Spend points",
    "trigger": "onAction"
   },
   {
    "operationId": "decideRecommendations",
    "contract": "ai",
    "purpose": "Recommendation slot (homepage / loyalty placement: products, offers, rewards, challenges)",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "recordRecommendationEvents",
    "contract": "ai",
    "purpose": "Report impressions, clicks and declines of recommended items",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   }
  ],
  "entryState": {
   "params": [],
   "coldEntry": "**A guest arriving cold on a link that no longer resolves is shown what happened and one way onward — never a 404.** A shared link, a scanned code and a forwarded confirmation all land here, and the person holding it did nothing wrong. Arrives with no parameter — the venue comes from the site."
  },
  "wireframe": {
   "status": "review",
   "provenance": "client-verified",
   "board": "wireframes/P01 Guest Web.dc.html#web-043",
   "prototype": {
    "file": "sources/designs/guest-rev3-30-september/TICVAI Guest Booking v2.dc.html",
    "rev": "rev 3 (30 September build)",
    "verified": "2026-10-01",
    "match": "exact",
    "view": "Summit Peaks → header 'At the venue' → Loyalty",
    "differences": "Placed inside the in-venue section; referral code appears under Account → Groups & invitations (YAML createReferral is here)."
   }
  },
  "apisNote": "Rebuilt 9 September 2026 from the 4 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formCreateReferral",
    "component": "modal",
    "trigger": "Create referral",
    "body": "**Collects what `createReferral` sends before it is called.** Required: `id`, `referrerSubjectId`, `code`, `status`. Optional: `refereeSubjectId`, `qualifyingAction`, `referrerRewardId`, `refereeRewardId`, `expiresAt`, `scopePath`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "Referral",
    "confirm": {
     "label": "Create referral",
     "operation": "createReferral"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "referrerSubjectId",
      "code",
      "status",
      "refereeSubjectId",
      "qualifyingAction",
      "referrerRewardId",
      "refereeRewardId",
      "expiresAt",
      "scopePath"
     ]
    },
    "provenance": "client-verified"
   },
   {
    "id": "formRedeemLoyaltyPoints",
    "component": "modal",
    "trigger": "Redeem loyalty points",
    "body": "**Collects what `redeemLoyaltyPoints` sends before it is called.** Required: `subjectId`, `programmeId`, `points`. Optional: `rewardId`, `orderId`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Redeem loyalty points",
     "operation": "redeemLoyaltyPoints"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "subjectId",
      "programmeId",
      "points",
      "rewardId",
      "orderId"
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
 }
]
```

## `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
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
 "createInstalmentPlan": {
  "method": "POST",
  "path": "/instalment-plans",
  "contract": "payments",
  "summary": "Split an order's payment into scheduled instalments on a stored card",
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
  "responds": "PayInstalmentPlan"
 },
 "createReferral": {
  "method": "POST",
  "path": "/referrals",
  "contract": "marketing-crm",
  "summary": "Issue a referral code",
  "permission": "MARKETING_MANAGE",
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
  "requestBody": "Referral",
  "responds": "Referral"
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
 "deleteGuestAccount": {
  "method": "DELETE",
  "path": "/auth/guest/account",
  "contract": "identity",
  "summary": "Self-service account deletion",
  "permission": null,
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
 "enrolMfaMethod": {
  "method": "POST",
  "path": "/auth/mfa/methods",
  "contract": "identity",
  "summary": "Enrol an MFA method",
  "permission": null,
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
  "responds": "MfaEnrolment"
 },
 "exportSubjectData": {
  "method": "POST",
  "path": "/guests/{subjectId}/data-export",
  "contract": "identity",
  "summary": "Everything the platform holds about one guest",
  "permission": "GUEST_VIEW_PII",
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
 "getBillingStatement": {
  "method": "GET",
  "path": "/billing-statements/{statementId}",
  "contract": "orders",
  "summary": "One statement, with its lines",
  "permission": "ORDER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "statementId",
    "in": "path",
    "required": true
   },
   {
    "name": "format",
    "in": "query",
    "required": null
   },
   {
    "name": "language",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "BillingStatement"
 },
 "getCookieConsentRuntime": {
  "method": "GET",
  "path": "/storefront/cookie-consent",
  "contract": "marketing-crm",
  "summary": "What the page must show and what it may load",
  "permission": null,
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "channel",
    "in": "query",
    "required": true
   },
   {
    "name": "brandId",
    "in": "query",
    "required": false
   },
   {
    "name": "language",
    "in": "query",
    "required": false
   },
   {
    "name": "X-Consent-Key",
    "in": "header",
    "required": false
   }
  ],
  "requestBody": null,
  "responds": "CookieConsentRuntime"
 },
 "getDeviceConsentHistory": {
  "method": "GET",
  "path": "/consent/device/history",
  "contract": "marketing-crm",
  "summary": "A visitor's own cookie decisions, oldest first",
  "permission": null,
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "X-Consent-Key",
    "in": "header",
    "required": true
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
 "getFacePassEnrolment": {
  "method": "GET",
  "path": "/face-pass/enrolments/{enrolmentId}",
  "contract": "access",
  "summary": "Whether a pass has a face registered, and when",
  "permission": "GUEST_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "FacePassEnrolment"
 },
 "getGameCard": {
  "method": "GET",
  "path": "/game-cards/{cardCode}",
  "contract": "games",
  "summary": "Read a card's balances",
  "permission": null,
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "GameCard"
 },
 "getGiftCard": {
  "method": "GET",
  "path": "/gift-cards/{cardCode}",
  "contract": "wallet",
  "summary": "Check a gift card balance",
  "permission": "WALLET_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "GiftCard"
 },
 "getGuestConsents": {
  "method": "GET",
  "path": "/guests/{subjectId}/consents",
  "contract": "marketing-crm",
  "summary": "Read a guest's consent state",
  "permission": "GUEST_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "ConsentState"
 },
 "getLoyaltyPosition": {
  "method": "GET",
  "path": "/loyalty/position",
  "contract": "marketing-crm",
  "summary": "A guest's points, tier and what is within reach",
  "permission": null,
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "programmeId",
    "in": "query",
    "required": true
   }
  ],
  "requestBody": null,
  "responds": null
 },
 "getMyMemberships": {
  "method": "GET",
  "path": "/guests/me/memberships",
  "contract": "catalogue",
  "summary": "A guest's own memberships, benefits and history",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "includeLapsed",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "GuestMembership"
 },
 "getProduct": {
  "method": "GET",
  "path": "/products/{productId}",
  "contract": "catalogue",
  "summary": "Read a product",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "Product"
 },
 "getWaiverStatus": {
  "method": "GET",
  "path": "/guests/{subjectId}/waiver-status",
  "contract": "marketing-crm",
  "summary": "Whether this guest may be issued a ticket that requires a waiver",
  "permission": "GUEST_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "productId",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": null
 },
 "getWallet": {
  "method": "GET",
  "path": "/wallets/{subjectId}",
  "contract": "wallet",
  "summary": "Read a guest wallet",
  "permission": "WALLET_VIEW",
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
  "responds": "Wallet"
 },
 "getWalletAutoReloadSetting": {
  "method": "GET",
  "path": "/wallets/{walletId}/auto-reload",
  "contract": "wallet",
  "summary": "A wallet's own auto top-up, if the holder set one",
  "permission": "WALLET_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "WalletAutoReloadSetting"
 },
 "getWalletExitBalance": {
  "method": "GET",
  "path": "/wallets/{walletId}/exit-balance",
  "contract": "wallet",
  "summary": "What the holder owes or is owed on leaving",
  "permission": "WALLET_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "WalletExitBalance"
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
 "grantDelegation": {
  "method": "POST",
  "path": "/guests/{subjectId}/delegations",
  "contract": "identity",
  "summary": "Let one guest act for another",
  "permission": "GUEST_MANAGE",
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
  "responds": "DelegatedAccess"
 },
 "listBillingStatements": {
  "method": "GET",
  "path": "/billing-statements",
  "contract": "orders",
  "summary": "What was charged, when, and against which agreement",
  "permission": "ORDER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
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
 "listDelegations": {
  "method": "GET",
  "path": "/guests/{subjectId}/delegations",
  "contract": "identity",
  "summary": "Who may act for this guest, and for whom they may act",
  "permission": "GUEST_VIEW",
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
 "listGuestMemberships": {
  "method": "GET",
  "path": "/guest/memberships",
  "contract": "catalogue",
  "summary": "A guest's memberships, benefits and history",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "includeLapsed",
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
 "listInstalmentPlans": {
  "method": "GET",
  "path": "/instalment-plans",
  "contract": "payments",
  "summary": "Instalment plans and their schedules",
  "permission": "PAYMENT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "orderId",
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
 "listLoyaltyProgrammes": {
  "method": "GET",
  "path": "/loyalty/programmes",
  "contract": "marketing-crm",
  "summary": "List loyalty programmes",
  "permission": "MARKETING_VIEW",
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
 "listMfaMethods": {
  "method": "GET",
  "path": "/auth/mfa/methods",
  "contract": "identity",
  "summary": "Enrolled MFA methods",
  "permission": null,
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "MfaMethod"
 },
 "listMyPaymentIssues": {
  "method": "GET",
  "path": "/guests/me/payment-issues",
  "contract": "payments",
  "summary": "A guest's own failed recurring payments",
  "permission": null,
  "offlineCapable": false,
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
 "listPaymentTokens": {
  "method": "GET",
  "path": "/payment-tokens",
  "contract": "orders",
  "summary": "A guest's saved payment methods",
  "permission": "ORDER_VIEW",
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
 "listPromotions": {
  "method": "GET",
  "path": "/promotions",
  "contract": "promotions",
  "summary": "List promotions",
  "permission": "PRICE_VIEW",
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
    "name": "status",
    "in": "query",
    "required": null
   },
   {
    "name": "activeAt",
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
 "listPublishedTrackingTechnologies": {
  "method": "GET",
  "path": "/storefront/cookie-consent/technologies",
  "contract": "marketing-crm",
  "summary": "The approved cookie registry, as the preference centre shows it",
  "permission": null,
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "channel",
    "in": "query",
    "required": true
   },
   {
    "name": "category",
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
 "listWalletTransactions": {
  "method": "GET",
  "path": "/wallets/{subjectId}/transactions",
  "contract": "wallet",
  "summary": "Wallet transaction history",
  "permission": "WALLET_VIEW",
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
 "recordDeviceConsent": {
  "method": "POST",
  "path": "/consent/device",
  "contract": "marketing-crm",
  "summary": "Record a visitor's cookie decision, before anyone is known",
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
  "requestBody": "RecordDeviceConsentRequest",
  "responds": "DeviceConsent"
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
 "redeemLoyaltyPoints": {
  "method": "POST",
  "path": "/loyalty/redemptions",
  "contract": "marketing-crm",
  "summary": "Spend points",
  "permission": "LOYALTY_REDEEM",
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
  "responds": "LoyaltyPosition"
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
 "removeMfaMethod": {
  "method": "DELETE",
  "path": "/auth/mfa/methods/{methodId}",
  "contract": "identity",
  "summary": "Remove an MFA method",
  "permission": null,
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
 "retryMyDunningPayment": {
  "method": "POST",
  "path": "/dunning-cases/{caseId}/retry",
  "contract": "payments",
  "summary": "Retry a declined membership payment now",
  "permission": null,
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   },
   {
    "name": "caseId",
    "in": "path",
    "required": true
   }
  ],
  "requestBody": "RetryDunningPaymentRequest",
  "responds": "DunningCase"
 },
 "revokeFacePass": {
  "method": "DELETE",
  "path": "/face-pass/enrolments/{enrolmentId}",
  "contract": "access",
  "summary": "Remove a facial profile",
  "permission": "GUEST_MANAGE",
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
 "setWalletAutoReloadSetting": {
  "method": "PUT",
  "path": "/wallets/{walletId}/auto-reload",
  "contract": "wallet",
  "summary": "Top the wallet up automatically from a stored card when it runs low",
  "permission": "WALLET_OPERATE",
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
  "requestBody": "WalletAutoReloadSetting",
  "responds": "WalletAutoReloadSetting"
 },
 "settleWalletAtExit": {
  "method": "POST",
  "path": "/wallets/{walletId}/exit-settlement",
  "contract": "wallet",
  "summary": "Settle a short balance, or refund a credit, when the holder leaves",
  "permission": "WALLET_OPERATE",
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
  "responds": "WalletExitSettlement"
 },
 "storePaymentToken": {
  "method": "POST",
  "path": "/payment-tokens",
  "contract": "orders",
  "summary": "Save a payment method for future use",
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
  "responds": "PaymentToken"
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
 "transferWalletBalance": {
  "method": "POST",
  "path": "/wallets/{walletId}/transfer",
  "contract": "wallet",
  "summary": "Send balance to another guest",
  "permission": "WALLET_OPERATE",
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
  "responds": "WalletTransaction"
 },
 "verifyMfaEnrolment": {
  "method": "POST",
  "path": "/auth/mfa/methods/{methodId}",
  "contract": "identity",
  "summary": "Complete enrolment",
  "permission": null,
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
  "responds": "MfaMethod"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
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
 "BillingStatement": {
  "x-ticvai-persistence": "none — computed from orders.payment and payments.dunning_case",
  "type": "object",
  "description": "2.14.19-2.14.23, 5.7.96, BL-100. **What a guest was charged over a period, and deliberately not a tax document.**\n**Computed rather than stored**, because a statement assembled at read time cannot disagree with the ledger it describes. A stored statement is a second source of truth about money, and the package already has one of those.\n",
  "required": [
   "id",
   "periodStart",
   "periodEnd",
   "total",
   "isTaxInvoice"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "subjectId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "periodStart": {
    "type": "string",
    "format": "date"
   },
   "periodEnd": {
    "type": "string",
    "format": "date"
   },
   "lines": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/BillingStatementLine"
    }
   },
   "total": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "taxTotal": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "discountTotal": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "pdfUrl": {
    "type": "string",
    "format": "uri",
    "nullable": true,
    "readOnly": true,
    "description": "Set when `getBillingStatement` is called with `format=pdf`; a short-lived link. The PDF is a statement, not a tax invoice; the tax invoices for its charges are linked per line."
   },
   "isTaxInvoice": {
    "type": "boolean",
    "default": false,
    "readOnly": true,
    "description": "**Always false, and stated rather than assumed.** UAE e-invoicing is Peppol five-corner with the FTA as the fifth corner, PINT AE XML and 51 mandatory fields; **CF-133 is open on it and AED 50m+ businesses must appoint an accredited service provider by 30 October 2026.** A statement that implied it was a tax invoice would be wrong in the one direction that has a regulator at the end of it.\n"
   }
  }
 },
 "BillingStatementLine": {
  "type": "object",
  "description": "BL-100. **One charge, refund or failed attempt.** Failures are lines rather than omissions — a statement showing only what succeeded cannot explain why a pass lapsed.\n",
  "required": [
   "occurredAt",
   "kind",
   "amount"
  ],
  "properties": {
   "occurredAt": {
    "type": "string",
    "format": "date-time"
   },
   "kind": {
    "type": "string",
    "enum": [
     "charge",
     "refund",
     "failedAttempt",
     "adjustment"
    ]
   },
   "amount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "description": {
    "type": "string"
   },
   "netAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "discountAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "taxAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "taxRate": {
    "type": "number",
    "nullable": true,
    "description": "2.14.23. The VAT rate the charge was posted with; `amount` is the gross."
   },
   "taxInvoiceId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The finance tax invoice issued for this charge, where one was (`issueTaxInvoice`); the guest downloads it with `getTaxDocumentRendition`."
   },
   "declineClass": {
    "type": "string",
    "nullable": true,
    "description": "**Present on `failedAttempt` only**, and it is what turns *\"your payment failed\"* into something a guest can act on: a soft decline means try again, a hard one means the card needs replacing.\n"
   }
  }
 },
 "BiometricKind": {
  "type": "string",
  "description": "BL-106, CF-35. **Two different legal postures, not two settings on one record.** 3.2.44 describes a temporary facial model taken at a counter or a gate and deleted when the ticket expires; 3.2.43 describes an enduring Face Pass enrolled deliberately on three surfaces. **Storing both as one record with a date makes the stricter rule depend on a field nobody enforces**, which is what BL-106 was raised to stop.\n`facePass` — enduring, explicit consent, revocable by the guest, anchored to the validity of the entitlement it belongs to.\n`faceTag` — same-visit, **consent still explicit and still recorded**, anchored to the ticket and purged at close of the operating day. **PDPL Article 4 is a closed list of exceptions with no legitimate-interests basis**, so a short life does not remove the need for consent — it only shortens what the consent is for.\n",
  "enum": [
   "facePass",
   "faceTag"
  ]
 },
 "BiometricRetentionAnchor": {
  "type": "string",
  "readOnly": true,
  "description": "BL-106, ADR-0047. **What the expiry is measured from, derived from the kind rather than chosen.** A retention period a person can type is a retention period somebody will type wrongly; the anchor follows the kind, and the kind follows how the biometric was taken.\n`entitlementValidity` — `facePass`. The face cannot outlive the pass it was enrolled for.\n`ticketValidity` — `faceTag` against a dated ticket.\n`operatingDayClose` — `faceTag` where the ticket has no end of its own, plus `VenueSettings.biometrics.faceTagPurgeMinutesAfterClose`.\n",
  "enum": [
   "entitlementValidity",
   "ticketValidity",
   "operatingDayClose"
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
 "CookieBannerPreferenceCenterDesignerView": {
  "type": "object",
  "x-ticvai-persistence": "marketing.cookie_banner_design",
  "description": "One version of a cookie banner and preference-centre design (pack 17.1.6).",
  "required": [
   "channel",
   "position",
   "languages",
   "rejectIsOneClick",
   "categories"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "brandId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Null for the corporate design every brand inherits."
   },
   "inheritsFromId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "channel": {
    "type": "string",
    "enum": [
     "b2cWebsite",
     "customerPortal",
     "mobileApp",
     "embeddedCheckout",
     "whiteLabelSite",
     "partnerMicrosite"
    ]
   },
   "logoAssetId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "title": {
    "$ref": "#/components/schemas/LocalisedText"
   },
   "body": {
    "$ref": "#/components/schemas/LocalisedText"
   },
   "position": {
    "type": "string",
    "enum": [
     "top",
     "bottom",
     "popup",
     "modal"
    ]
   },
   "themeId": {
    "type": "string",
    "nullable": true,
    "description": "The white-label theme it takes colours and fonts from."
   },
   "buttons": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "action"
     ],
     "properties": {
      "action": {
       "type": "string",
       "enum": [
        "acceptAll",
        "rejectNonEssential",
        "managePreferences",
        "savePreferences",
        "doNotSellOrShare"
       ]
      },
      "label": {
       "$ref": "#/components/schemas/LocalisedText"
      }
     }
    }
   },
   "rejectIsOneClick": {
    "type": "boolean",
    "default": true,
    "description": "Must be true."
   },
   "links": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "label",
      "policyKind"
     ],
     "properties": {
      "label": {
       "$ref": "#/components/schemas/LocalisedText"
      },
      "policyKind": {
       "type": "string",
       "enum": [
        "privacy",
        "cookie",
        "termsAndConditions"
       ]
      }
     }
    }
   },
   "categories": {
    "type": "array",
    "minItems": 1,
    "items": {
     "type": "object",
     "required": [
      "category",
      "defaultOn"
     ],
     "properties": {
      "category": {
       "type": "string",
       "enum": [
        "strictlyNecessary",
        "functional",
        "analytics",
        "personalisation",
        "marketing"
       ]
      },
      "description": {
       "$ref": "#/components/schemas/LocalisedText"
      },
      "defaultOn": {
       "type": "boolean",
       "description": "True only for `strictlyNecessary`, which is always active."
      }
     }
    }
   },
   "languages": {
    "type": "array",
    "minItems": 1,
    "items": {
     "type": "string",
     "maxLength": 10
    },
    "description": "Every language the storefront serves; Arabic renders right to left."
   },
   "regulatoryRegimes": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "gdpr",
      "ePrivacy",
      "ccpaCpra",
      "lgpd",
      "uaePdpl",
      "saudiPdpl"
     ]
    },
    "description": "2.6.60 (29 September, build). **The laws this design is published to satisfy**, so compliance is stated rather than assumed. The strictest posture (opt-in, one-click reject, every non-essential category off) already meets GDPR/ePrivacy, LGPD and both PDPLs; `ccpaCpra` adds the \"Do not sell or share\" button (`doNotSellOrShare`) and honours a Global Privacy Control signal as that opt-out."
   },
   "recordIpAddress": {
    "type": "boolean",
    "default": false,
    "description": "2.6.55, \"if legally permitted\" (29 September, build). On, `recordDeviceConsent` writes the IP address and user agent to `pii.consent_identifier`; off, they are not kept anywhere. Off by default."
   },
   "noticeVersion": {
    "type": "string",
    "readOnly": true,
    "description": "Moves with the cookie policy (white-label `setPolicy`, kind `cookie`)."
   },
   "version": {
    "type": "integer",
    "minimum": 1,
    "readOnly": true
   },
   "status": {
    "type": "string",
    "enum": [
     "draft",
     "published",
     "superseded"
    ],
    "readOnly": true
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005)."
   },
   "updatedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   }
  }
 },
 "CookieCategory": {
  "type": "string",
  "enum": [
   "strictlyNecessary",
   "functional",
   "analytics",
   "personalisation",
   "marketing"
  ],
  "description": "2.6.53. The five categories the banner design (`CookieBannerPreferenceCenterDesignerView.categories`) offers; the matrix's \"preference\" category is `personalisation` (British spelling, as `ConsentPurpose`)."
 },
 "CookieConsentChannel": {
  "type": "string",
  "enum": [
   "b2cWebsite",
   "customerPortal",
   "mobileApp",
   "embeddedCheckout",
   "whiteLabelSite",
   "partnerMicrosite"
  ],
  "description": "The six governed surfaces, as the registry and the banner design name them (pack 17.1.5-17.1.6)."
 },
 "CookieConsentRuntime": {
  "type": "object",
  "x-ticvai-persistence": "none — assembled at read time from marketing.cookie_banner_design, marketing.tracking_technology and marketing.device_consent",
  "description": "What `getCookieConsentRuntime` gives the storefront tag loader and the app SDK gate (2.6.52, 2.6.58).",
  "required": [
   "banner",
   "noticeVersion",
   "requiresDecision",
   "allowedTechnologies",
   "consentModeSignals"
  ],
  "properties": {
   "banner": {
    "$ref": "#/components/schemas/CookieBannerPreferenceCenterDesignerView"
   },
   "noticeVersion": {
    "type": "string"
   },
   "requiresDecision": {
    "type": "boolean",
    "description": "True with no decision, an expired one, or one given against a superseded notice."
   },
   "decision": {
    "allOf": [
     {
      "$ref": "#/components/schemas/DeviceConsent"
     }
    ],
    "nullable": true,
    "description": "The latest decision for the presented key; null without a key."
   },
   "allowedTechnologies": {
    "type": "array",
    "description": "Per category, the approved technologies it unlocks. Anything not listed never loads.",
    "items": {
     "type": "object",
     "required": [
      "category",
      "technologies"
     ],
     "properties": {
      "category": {
       "$ref": "#/components/schemas/CookieCategory"
      },
      "granted": {
       "type": "boolean",
       "description": "Whether the presented decision grants it; always true for `strictlyNecessary`."
      },
      "technologies": {
       "type": "array",
       "items": {
        "type": "object",
        "required": [
         "name",
         "provider"
        ],
        "properties": {
         "name": {
          "type": "string"
         },
         "provider": {
          "type": "string"
         },
         "technologyType": {
          "type": "string"
         }
        }
       }
      }
     }
    }
   },
   "consentModeSignals": {
    "type": "object",
    "description": "**The decision in Google consent-mode terms** (2.6.65), so Analytics and Tag Manager are told, not left to guess. `denied` wherever no decision grants the category.",
    "properties": {
     "adStorage": {
      "type": "string",
      "enum": [
       "granted",
       "denied"
      ]
     },
     "adUserData": {
      "type": "string",
      "enum": [
       "granted",
       "denied"
      ]
     },
     "adPersonalization": {
      "type": "string",
      "enum": [
       "granted",
       "denied"
      ]
     },
     "analyticsStorage": {
      "type": "string",
      "enum": [
       "granted",
       "denied"
      ]
     },
     "functionalityStorage": {
      "type": "string",
      "enum": [
       "granted",
       "denied"
      ]
     },
     "personalizationStorage": {
      "type": "string",
      "enum": [
       "granted",
       "denied"
      ]
     },
     "securityStorage": {
      "type": "string",
      "enum": [
       "granted"
      ]
     }
    }
   }
  }
 },
 "CreatePromotionRequest": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "required": [
   "code",
   "name",
   "venueId",
   "discount",
   "validFrom"
  ],
  "properties": {
   "code": {
    "type": "string",
    "maxLength": 64,
    "pattern": "^[A-Za-z0-9_-]+$"
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
   "discount": {
    "$ref": "#/components/schemas/Discount"
   },
   "conditions": {
    "$ref": "#/components/schemas/PromotionConditions"
   },
   "stackingMode": {
    "allOf": [
     {
      "$ref": "#/components/schemas/StackingMode"
     }
    ],
    "default": "bestOnly"
   },
   "stackingGroup": {
    "type": "string",
    "maxLength": 64
   },
   "precedence": {
    "type": "integer",
    "default": 0,
    "description": "Higher evaluates first where several could apply."
   },
   "validFrom": {
    "type": "string",
    "format": "date-time"
   },
   "validTo": {
    "type": "string",
    "format": "date-time"
   },
   "maxRedemptions": {
    "type": "integer",
    "nullable": true
   },
   "maxRedemptionsPerGuest": {
    "type": "integer",
    "nullable": true
   },
   "budgetCap": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "description": "Total discount value after which the promotion stops automatically. **Enforced at checkout**, where an order whose discount would take the total past the cap does not receive the promotion (decided 28 September, audit R101)."
   },
   "campaignId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The commercial campaign (`promotions.campaign`) this promotion belongs to; null for a promotion run on its own. The directory, calendar and campaign budget screens group by it. (DM5, 29 September: data model for the agreed operations)"
   },
   "recommendable": {
    "type": "boolean",
    "default": false,
    "description": "**May the recommendation engine show this offer to a guest** (8.6.30 to 8.6.36; 29 September, build pass, group G2, from group G1's handoff). False keeps a promotion to the basket, where `evaluatePromotions` applies it as before. True makes a live promotion a candidate item of kind `offer` in `ai.decideRecommendations` for the guests its conditions and `recommendableSegmentIds` admit: while it is live, `promotions.recommendationStrategyPublished` (kind `offers`) keeps the engine's candidate cache current, and it leaves the cache when it is paused, ends or expires. **The engine shows the offer; the discount is still computed here at the basket**, never by ai."
   },
   "recommendableSegmentIds": {
    "type": "array",
    "nullable": true,
    "description": "The marketing-crm segments the offer may be recommended to; null means every guest its own conditions admit.",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   }
  }
 },
 "DeclineClass": {
  "type": "string",
  "description": "BL-100. **Whether a failed charge may be tried again at all**, and the distinction is a merchant-account risk rather than a courtesy.\n`soft` — insufficient funds, a temporary hold, an issuer timeout. **Worth another attempt on another day**, and the whole reason a dunning schedule exists.\n`hard` — closed account, stolen card, do-not-honour, invalid number. **Never retried.** A hard decline put on a timetable is how a merchant ID gets flagged by the scheme, and the venue finds out when its acquirer calls.\n`unknown` — the provider gave no usable code. **Treated as `hard`**, because guessing `soft` optimises for one more attempt and risks the thing that cannot be undone.\n",
  "enum": [
   "soft",
   "hard",
   "unknown"
  ]
 },
 "DelegatedAccess": {
  "x-ticvai-persistence": "identity.delegated_access",
  "type": "object",
  "required": [
   "id",
   "permission",
   "scopePath",
   "effect"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "principalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "roleId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "permission": {
    "type": "string",
    "description": "From the permission enum. `*` permitted on DENY only."
   },
   "subjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "CF-132, CL-05. **A grant held by a guest rather than a staff principal.**\nSection 5.5 asks for portfolios — a primary holder assigning entitlements, transfer between linked accounts, shared wallets with individual tracking — and it appears ten times across ten sections. **Every one of those reduces to the same question: who may act on whose behalf, over what, and until when.**\n**That is a grant, not a household table.** A primary holder assigning an entitlement is a grant. A group leader holding tickets for twelve is a grant. A corporate account enrolling members is a grant with a quota. **A shared wallet with individual tracking is a grant over a balance, and the transaction log already records who spent.**\n**A household table would answer one of those four.**\n"
   },
   "overSubjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Whose behalf. **Null for a staff grant, which is the existing behaviour** — every grant written before 18 August means exactly what it meant before.\n"
   },
   "overObjectRef": {
    "type": "string",
    "nullable": true,
    "description": "**Where the authority is over a thing rather than a scope** — a wallet, an entitlement, a booking. `scopePath` answers *where*; this answers *what*, and a guest's authority is almost always over a specific object rather than a branch of the tree.\n"
   },
   "delegationKind": {
    "type": "string",
    "nullable": true,
    "enum": [
     "primaryHolder",
     "familyMember",
     "groupLeader",
     "attendee",
     "corporateAdmin",
     "corporateMember",
     "carer"
    ],
    "description": "**What kind of relationship this expresses**, for display and for reporting. The mechanism does not branch on it — a family member and a group attendee are the same grant with different words around them, which is the point.\n"
   },
   "quota": {
    "type": "integer",
    "nullable": true,
    "description": "2.14.15 and 4.3.11. **How many the holder may assign.** A corporate account with fifty allocations and a family with four are the same structure with different numbers.\n"
   },
   "isRevocableBySubject": {
    "type": "boolean",
    "default": true,
    "description": "**Whether the person it is over can end it.** A guest who linked a family member should be able to unlink them; a corporate member should not be able to revoke their employer's oversight — and **a delegation nobody can end is a delegation somebody will regret.**\n"
   },
   "scopePath": {
    "type": "string"
   },
   "effect": {
    "type": "string",
    "enum": [
     "ALLOW",
     "DENY"
    ]
   },
   "permissionId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "**Taken from `identity.user_access`, 20 September, when that table was collapsed into this one.** `permission` above is free text; this names a row in `identity.permission`, the catalogue wired the same day. A grant that names a catalogue row can be checked against the keys the contracts actually enforce — which is the whole point of a catalogue that reported *154 on operations, 35 in roles.yaml, 0 shared*.\nNullable because a role grant carries no permission at all.\n"
   },
   "revokedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true,
    "description": "Taken from `identity.user_access`. This table recorded `revokedBy` and not when, so it could say who revoked a grant and not whether it was before or after the thing somebody is asking about.\n"
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
   "createdByPrincipalId": {
    "type": "string",
    "format": "uuid"
   },
   "createdAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "DeviceConsent": {
  "type": "object",
  "x-ticvai-persistence": "marketing.device_consent + marketing.device_consent_category",
  "description": "**One cookie decision by a visitor nobody has identified yet** (BL-073 §4b, decided 29 September). Append-only: a change of mind is a new row. Keyed for the visitor by `consentKey`, which the platform mints; the categories are child rows. The IP address and user agent, where recorded at all, are in `pii.consent_identifier` (`ConsentCaptureIdentifier`), never here.",
  "required": [
   "consentKey",
   "channel",
   "action",
   "categories",
   "noticeVersion",
   "decidedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "consentKey": {
    "type": "string",
    "maxLength": 64,
    "readOnly": true,
    "description": "**Opaque, minted by us, not a device fingerprint.** It answers 2.6.55's \"user identifier/session ID\" and is the join key `claimDeviceConsent` needs. Shared by all the tenant's domains (2.6.62), never across tenants."
   },
   "channel": {
    "$ref": "#/components/schemas/CookieConsentChannel"
   },
   "brandId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "bannerDesignId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The published `CookieBannerPreferenceCenterDesignerView` version the visitor was shown."
   },
   "action": {
    "$ref": "#/components/schemas/DeviceConsentAction"
   },
   "categories": {
    "type": "array",
    "minItems": 1,
    "description": "Every category of the design, with the decision this row gives it.",
    "items": {
     "type": "object",
     "required": [
      "category",
      "decision"
     ],
     "properties": {
      "category": {
       "$ref": "#/components/schemas/CookieCategory"
      },
      "decision": {
       "type": "string",
       "enum": [
        "granted",
        "declined"
       ]
      }
     }
    }
   },
   "noticeVersion": {
    "type": "string",
    "description": "The cookie notice version decided against (white-label `setPolicy`, kind `cookie`)."
   },
   "language": {
    "type": "string",
    "maxLength": 10,
    "nullable": true
   },
   "globalPrivacyControl": {
    "type": "boolean",
    "default": false,
    "description": "The browser sent a Global Privacy Control signal; honoured as a CCPA/CPRA opt-out of sale and sharing."
   },
   "source": {
    "$ref": "#/components/schemas/ConsentSource"
   },
   "country": {
    "type": "string",
    "pattern": "^[A-Z]{2}$",
    "nullable": true,
    "readOnly": true,
    "description": "The edge's geolocation of the request, for the geographic statistics (2.6.63). The address is not kept here."
   },
   "decidedAt": {
    "type": "string",
    "format": "date-time"
   },
   "expiresAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true,
    "description": "**A device consent expires and a subject consent does not.** Set from the tenant's device-consent term; after it the banner asks again."
   },
   "claimedBySubjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "description": "Set once, by `claimDeviceConsent`. Never cleared."
   },
   "claimedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005), tenant-scoped: a decision with no subject still belongs to one tenant."
   }
  }
 },
 "DeviceConsentAction": {
  "type": "string",
  "enum": [
   "acceptAll",
   "rejectNonEssential",
   "savePreferences",
   "withdraw",
   "doNotSellOrShare"
  ],
  "description": "What the visitor pressed. `doNotSellOrShare` is the CCPA/CPRA opt-out link, shown where the design's `regulatoryRegimes` include `ccpaCpra`."
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
 "DunningCase": {
  "x-ticvai-persistence": "payments.dunning_case",
  "type": "object",
  "description": "BL-100. **One recurring charge being chased**, and the row a venue works from.\n",
  "required": [
   "id",
   "state",
   "attemptsMade",
   "firstFailedAt"
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
   "orderId": {
    "type": "string",
    "description": "The order whose renewal failed."
   },
   "amount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "state": {
    "$ref": "#/components/schemas/DunningState"
   },
   "declineClass": {
    "allOf": [
     {
      "$ref": "#/components/schemas/DeclineClass"
     }
    ],
    "description": "**From the most recent attempt.** A case that begins `soft` and turns `hard` stops immediately rather than finishing its schedule — the card changed underneath it.\n"
   },
   "attemptsMade": {
    "type": "integer"
   },
   "nextAttemptAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "**Null where the case has ended or the decline is hard.** A scheduled time on a case nothing will act on is the field that makes a queue untrustworthy.\n"
   },
   "firstFailedAt": {
    "type": "string",
    "format": "date-time"
   },
   "resolvedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "resolution": {
    "type": "string",
    "nullable": true,
    "enum": [
     "paidByOtherMeans",
     "cardReplaced",
     "writeOff",
     "cancelledByGuest",
     null
    ]
   },
   "resolutionNote": {
    "type": "string",
    "nullable": true,
    "maxLength": 500,
    "description": "**What `resolveDunningCase` was told, which had nowhere to land until now.** The enum above tells `writeOff` from `cardReplaced`; **which invoice, whose phone call and on what authority is the sentence beside it**, and the operation's own reasoning — that these reasons must be told apart afterwards — only works if the sentence survives.\n**Same shape as `marketing.case.resolution_note`**, which is a RAG source for exactly this reason: a resolution note is the most useful free text a support record holds.\n"
   },
   "resolvedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "description": "**Who closed it.** A write-off with no name against it is the one resolution nobody can follow up, and it is also the one that moves money.\n"
   },
   "scopePath": {
    "type": "string",
    "description": "**The partition key** (ADR-0005). Written at `venue` scope.\n"
   }
  }
 },
 "DunningState": {
  "type": "string",
  "enum": [
   "scheduled",
   "inProgress",
   "exhausted",
   "recovered",
   "resolvedManually"
  ],
  "description": "BL-100. **`exhausted` and `recovered` are both endings and only one of them is a failure.** A schedule with a single terminal state cannot tell a venue whether dunning is working, which is the only question a venue asks of it.\n"
 },
 "FacePassEnrolment": {
  "type": "object",
  "x-ticvai-persistence": "pii.subject_biometric",
  "description": "3.2.43. **Metadata about a facial profile. Never the profile.**\n",
  "required": [
   "id",
   "kind",
   "subjectId",
   "entitlementId",
   "source",
   "capturedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "subjectId": {
    "type": "string",
    "format": "uuid"
   },
   "entitlementId": {
    "type": "string",
    "format": "uuid",
    "description": "The `Entitlement.id`, a UUIDv7 (`pii.subject_biometric.entitlement_id`)."
   },
   "kind": {
    "$ref": "#/components/schemas/BiometricKind"
   },
   "retentionAnchor": {
    "allOf": [
     {
      "$ref": "#/components/schemas/BiometricRetentionAnchor"
     }
    ],
    "x-ticvai-derived": "onWrite",
    "description": "BL-106. **Derived from `kind`, never sent.** `facePass` anchors to the entitlement, `faceTag` to the ticket or to the close of the operating day.\n"
   },
   "source": {
    "type": "string",
    "enum": [
     "guestApp",
     "ticketCounter",
     "annualPassCounter",
     "entryGate"
    ],
    "description": "**`entryGate` is valid for `faceTag` only**, and 3.2.43's omission of it from Face Pass is deliberate: an enduring enrolment is a considered act with consent attached, not something done in a queue. 3.2.44 puts a Face Tag at a gate precisely because it dies the same day.\n"
   },
   "capturedAt": {
    "type": "string",
    "format": "date-time"
   },
   "consentPurposeId": {
    "type": "string",
    "format": "uuid"
   },
   "consentGivenAt": {
    "type": "string",
    "format": "date-time"
   },
   "guardianSubjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Where the subject is a minor (3.2.12)."
   },
   "isActive": {
    "type": "boolean",
    "readOnly": true
   },
   "expiresAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "**Bounded by whatever `retentionAnchor` names**, and a face outliving it is a biometric held for no stated purpose.\n**Settled 20 September by ADR-0047**, which CF-64 had been carrying since 6 August: a `facePass` cannot outlive its entitlement and a `faceTag` does not survive the close of the operating day. **These are ceilings rather than defaults** — they cannot be configured upward, because a retention that a tenant can extend without limit is the breach ADR-0047 gave the platform a ceiling to prevent.\n"
   }
  }
 },
 "GameCard": {
  "x-ticvai-persistence": "games.card",
  "type": "object",
  "required": [
   "cardCode",
   "venueId",
   "credits",
   "bonusCredits",
   "points",
   "status",
   "issuedAt"
  ],
  "properties": {
   "cardCode": {
    "type": "string",
    "description": "**A pre-printed card keeps the code printed on it. A generated code** (a digital card, or a card issued with no printed code) **is the venue prefix plus a sequence per venue** (decided 28 September, audit R152). Each till holds a reserved range of that sequence, so a card issued offline takes its code at once. Not gapless; only tax invoices are gapless, per legal entity.\n"
   },
   "kind": {
    "type": "string"
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "subjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "credits": {
    "type": "integer",
    "description": "Bought with money. Buys plays."
   },
   "bonusCredits": {
    "type": "integer",
    "description": "From a promotion. Typically non-refundable and spent before paid credits.\n"
   },
   "points": {
    "type": "integer",
    "description": "Won by playing. Buys prizes. **Not interchangeable with credits** — a guest who wins should not simply be able to play more.\n"
   },
   "status": {
    "type": "string",
    "enum": [
     "active",
     "blocked",
     "expired",
     "transferred"
    ]
   },
   "blockedReason": {
    "type": "string",
    "nullable": true
   },
   "transferredToCardCode": {
    "type": "string",
    "nullable": true
   },
   "lastPlayedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "issuedAt": {
    "type": "string",
    "format": "date-time"
   },
   "expiresAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   }
  }
 },
 "GiftCard": {
  "x-ticvai-persistence": "wallet.gift_card",
  "type": "object",
  "required": [
   "cardCode",
   "faceValue",
   "balance",
   "status",
   "issuedAt"
  ],
  "properties": {
   "cardCode": {
    "type": "string"
   },
   "kind": {
    "type": "string"
   },
   "faceValue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "balance": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "status": {
    "type": "string",
    "enum": [
     "issued",
     "active",
     "partiallyRedeemed",
     "redeemed",
     "expired",
     "blocked"
    ]
   },
   "blockedReason": {
    "type": "string",
    "nullable": true
   },
   "issuedAt": {
    "type": "string",
    "format": "date-time"
   },
   "activatedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "expiresAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   }
  }
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
 "GuestMembership": {
  "type": "object",
  "description": "19.2.26 to 19.2.28. **A view, not a table** — assembled from the entitlement, the product that granted it and the order that bought it.\n",
  "required": [
   "entitlementId",
   "productId",
   "name",
   "status"
  ],
  "properties": {
   "entitlementId": {
    "type": "string",
    "format": "uuid",
    "description": "The `access.Entitlement.id` this membership is — a UUIDv7, like every entitlement id."
   },
   "productId": {
    "type": "string",
    "format": "uuid"
   },
   "name": {
    "type": "string"
   },
   "tier": {
    "type": "string",
    "nullable": true
   },
   "status": {
    "type": "string",
    "enum": [
     "active",
     "frozen",
     "suspended",
     "expired",
     "cancelled"
    ],
    "description": "**Derived from the entitlement, not held here.** This schema is a view assembled from the entitlement, the product that granted it and the order that bought it — the lifecycle lives in `states/entitlement-status.yaml` and `frozen` is what `freezeEntitlement` sets.\nNo state model of its own, deliberately: **two models over one lifecycle drift.**\n"
   },
   "validFrom": {
    "type": "string",
    "format": "date"
   },
   "validTo": {
    "type": "string",
    "format": "date"
   },
   "frozenDays": {
    "type": "integer",
    "description": "Days lost to a freeze and added back to `validTo`. **Shown because a guest who paused a pass will check the maths**, and a validity date that moved without explanation is a support call.\n"
   },
   "benefits": {
    "type": "array",
    "description": "5.4.31. From the product's entitlement template. **Traceable to what grants them**, so a gate can honour what the app promised.\n",
    "items": {
     "type": "object",
     "properties": {
      "code": {
       "type": "string"
      },
      "name": {
       "type": "string"
      },
      "value": {
       "type": "string",
       "nullable": true
      }
     }
    }
   },
   "renewsOn": {
    "type": "string",
    "format": "date",
    "nullable": true
   },
   "previousTerms": {
    "type": "array",
    "description": "Prior terms, including lapsed ones.",
    "items": {
     "type": "object",
     "properties": {
      "validFrom": {
       "type": "string",
       "format": "date"
      },
      "validTo": {
       "type": "string",
       "format": "date"
      },
      "endedBecause": {
       "type": "string",
       "enum": [
        "expired",
        "renewed",
        "cancelled",
        "upgraded"
       ]
      }
     }
    }
   }
  }
 },
 "GuestPromotion": {
  "x-ticvai-persistence": "none — guest projection of promotions.promotion",
  "type": "object",
  "description": "**What a guest may see of a promotion.** `Promotion` carries the commercial internals (`budgetCap`, `maxRedemptions`, `redemptionCount`, `discountGiven`, `precedence`, `stackingGroup`), and `listPromotions` and `getPromotion` are guest-audience. A guest caller receives this shape instead. `additionalProperties: false` is the point: a server that adds an internal field to it fails validation instead of publishing the field.\n",
  "additionalProperties": false,
  "required": [
   "id",
   "code",
   "name",
   "discount",
   "validFrom"
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
   "description": {
    "type": "string"
   },
   "discount": {
    "$ref": "#/components/schemas/Discount"
   },
   "conditions": {
    "$ref": "#/components/schemas/PromotionConditions"
   },
   "stackingMode": {
    "$ref": "#/components/schemas/StackingMode"
   },
   "validFrom": {
    "type": "string",
    "format": "date-time"
   },
   "validTo": {
    "type": "string",
    "format": "date-time"
   },
   "maxRedemptionsPerGuest": {
    "type": "integer",
    "nullable": true
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
 "LoyaltyProgramme": {
  "x-ticvai-persistence": "marketing.loyalty_programme + marketing.points_earning_rule + marketing.programme_tier",
  "type": "object",
  "required": [
   "id",
   "code",
   "name",
   "earnRules",
   "tiers"
  ],
  "properties": {
   "tiers": {
    "type": "array",
    "description": "**Rows of `marketing.programme_tier`**, the same shape `MarketingProgrammeTier` has — one definition of a tier, not a second copy that cannot round-trip. `loyaltyProgrammeId` and `id` are the server's on create.\n",
    "items": {
     "$ref": "#/components/schemas/MarketingProgrammeTier"
    }
   },
   "id": {
    "readOnly": true,
    "type": "string",
    "format": "uuid"
   },
   "code": {
    "type": "string",
    "x-ticvai-unique": "tenant",
    "description": "**Unique per tenant** (decided 28 September, audit R108). A code already used by any loyalty programme in the tenant, at any venue, is refused with `409 duplicate-code`.\n"
   },
   "name": {
    "type": "string"
   },
   "venueId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "pointsLiabilityAccountId": {
    "type": "string",
    "format": "uuid",
    "description": "Points post here on accrual. They are a liability from the moment they are earned, not from the moment they are spent.\n"
   },
   "earnRules": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "trigger",
      "points"
     ],
     "properties": {
      "trigger": {
       "type": "string",
       "enum": [
        "perCurrencyUnit",
        "perVisit",
        "perProduct",
        "onSignup",
        "onBirthday",
        "onReview"
       ]
      },
      "points": {
       "type": "number"
      },
      "productKinds": {
       "type": "array",
       "description": "Limits a `perProduct` or `perCurrencyUnit` rule to these kinds. Empty means every kind.",
       "items": {
        "$ref": "../spine/catalogue.yaml#/components/schemas/ProductKind"
       }
      },
      "multiplier": {
       "type": "number"
      }
     }
    }
   },
   "pointsExpireAfterMonths": {
    "type": "integer",
    "nullable": true
   },
   "isActive": {
    "type": "boolean"
   }
  }
 },
 "MarketingProgrammeTier": {
  "type": "object",
  "x-ticvai-persistence": "marketing.programme_tier",
  "description": "**The tier definition decision 8 promised and nobody built.** `marketing.loyalty_position` carried `tierCode`, `tierName` and `pointsToNextTier` as denormalised strings and a number, with no table saying what tiers exist or what each one requires — so `pointsToNextTier` was computed from a threshold that lived nowhere.\n**Not named `marketing.loyalty_tier`**: that name is recorded in `schema-history.json` as renamed to `marketing.points_earning_rule` on 20 September, and a rename record that contradicts the schema is worse than a longer name. Not named `marketing.tier` either, because `subscription.tier_allowance` is a SaaS plan's tier and one bare `tier` in a package with two tier concepts is how `plan_id` came to point at `subscription.plan`.\n**The denormalised copy on the position stays.** A till rendering *Gold* beside a balance must not join, and must certainly not cross a cell boundary to print a word. This table is the source of truth and those columns are its cache.\n",
  "required": [
   "loyaltyProgrammeId",
   "code",
   "name",
   "rank"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "loyaltyProgrammeId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "code": {
    "type": "string",
    "maxLength": 40
   },
   "name": {
    "type": "string",
    "maxLength": 120
   },
   "rank": {
    "type": "integer",
    "description": "**Order, not threshold.** Two tiers can share a qualifying rule and still have an order, and sorting by points breaks the moment a tier is granted rather than earned.\n"
   },
   "minLifetimePoints": {
    "type": "integer",
    "nullable": true,
    "description": "What reaching this tier requires. **`pointsToNextTier` on the position is this minus the guest's lifetime points**, and until now it was this minus nothing.\n"
   },
   "retainLifetimePoints": {
    "type": "integer",
    "nullable": true,
    "description": "What keeping it requires, per review period. **Usually lower than reaching it**, and a scheme that cannot express the difference either never demotes or demotes on the day a guest stops earning.\n"
   },
   "validityMonths": {
    "type": "integer",
    "nullable": true,
    "description": "Null means the tier does not lapse on its own."
   },
   "benefits": {
    "type": "array",
    "description": "What the tier gives, as the guest reads it. Text shown, not rules enforced.",
    "items": {
     "type": "string"
    }
   },
   "earnMultiplier": {
    "type": "number",
    "nullable": true,
    "description": "Applied to every earn rule while the guest holds this tier. Null means 1."
   },
   "isActive": {
    "type": "boolean",
    "default": true
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
 "MfaEnrolment": {
  "x-ticvai-persistence": "none — transient",
  "type": "object",
  "required": [
   "methodId",
   "kind"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "**Added 20 August.** The table had no key at all — no id, no parent and no natural key, so **no row could be addressed, updated or deleted.** The response schema returned everything a caller needs and not the row's own identity, which is the difference between an API response and a table.\n"
   },
   "methodId": {
    "type": "string",
    "format": "uuid"
   },
   "kind": {
    "$ref": "#/components/schemas/MfaKind"
   },
   "secret": {
    "type": "string",
    "nullable": true,
    "description": "TOTP shared secret. Returned once, at enrolment, and never again."
   },
   "qrCodeUri": {
    "type": "string",
    "nullable": true
   },
   "recoveryCodes": {
    "type": "array",
    "description": "Returned once, in this enrolment response (`enrolMfaMethod` writes them, hashed, to `identity.mfa_recovery_code`). Not retrievable afterwards — `verifyMfaEnrolment` does not return them.\n",
    "items": {
     "type": "string"
    }
   },
   "expiresAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "MfaKind": {
  "type": "string",
  "enum": [
   "totp",
   "smsOtp",
   "emailOtp",
   "biometric",
   "hardwareToken"
  ]
 },
 "MfaMethod": {
  "x-ticvai-persistence": "identity.mfa_method",
  "type": "object",
  "required": [
   "id",
   "kind",
   "isActive",
   "enrolledAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "kind": {
    "$ref": "#/components/schemas/MfaKind"
   },
   "label": {
    "type": "string",
    "nullable": true
   },
   "maskedTarget": {
    "type": "string",
    "nullable": true,
    "description": "Partially masked destination, so a person can tell two methods apart."
   },
   "isActive": {
    "type": "boolean"
   },
   "isPrimary": {
    "type": "boolean"
   },
   "enrolledAt": {
    "type": "string",
    "format": "date-time"
   },
   "lastUsedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   }
  }
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
 "PayInstalment": {
  "type": "object",
  "description": "One scheduled charge in an instalment plan.",
  "required": [
   "sequence",
   "dueDate",
   "amount",
   "status"
  ],
  "properties": {
   "sequence": {
    "type": "integer",
    "minimum": 1
   },
   "dueDate": {
    "type": "string",
    "format": "date"
   },
   "amount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "status": {
    "type": "string",
    "enum": [
     "scheduled",
     "paid",
     "failed",
     "waived",
     "cancelled"
    ]
   },
   "paymentId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "dunningCaseId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "attemptedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   }
  }
 },
 "PayInstalmentPlan": {
  "type": "object",
  "x-ticvai-persistence": "payments.instalment_plan + payments.instalment",
  "description": "4.2.17. A schedule of charges for one order, independent of the product's term.",
  "required": [
   "id",
   "orderId",
   "frequency",
   "status",
   "total",
   "instalments"
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
   "subjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "frequency": {
    "type": "string",
    "enum": [
     "monthly",
     "quarterly",
     "custom"
    ]
   },
   "paymentTokenId": {
    "type": "string",
    "format": "uuid"
   },
   "status": {
    "type": "string",
    "enum": [
     "active",
     "completed",
     "inArrears",
     "cancelled"
    ]
   },
   "total": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "paidToDate": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "nextDueDate": {
    "type": "string",
    "format": "date",
    "nullable": true
   },
   "instalments": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/PayInstalment"
    }
   },
   "createdAt": {
    "type": "string",
    "format": "date-time"
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005). Written at the scope of the venue the order was sold at."
   }
  }
 },
 "PaymentToken": {
  "type": "object",
  "x-ticvai-persistence": "payments.token",
  "description": "BL-116. **A stored credential, held by the provider and referenced here.** The platform never sees a card number, which is what keeps PCI scope where it belongs.\n**A token is provider-scoped.** A card tokenised with one gateway does not work with another, so a routing change does not silently move a guest's saved card — it means asking them again, and the model should make that visible rather than surprising.\n",
  "required": [
   "id",
   "subjectId",
   "providerId",
   "token",
   "isDefault"
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
   "providerId": {
    "type": "string",
    "format": "uuid"
   },
   "token": {
    "type": "string",
    "format": "password",
    "writeOnly": true,
    "description": "**Write-only, never returned.** The provider's reference to a credential it holds. Required on the stored row; absent from every response.\n"
   },
   "method": {
    "type": "string"
   },
   "maskedIdentifier": {
    "type": "string",
    "description": "What a guest sees — the last four digits, the card brand. **Enough to choose between two saved cards and not enough to use one.**\n"
   },
   "expiresAt": {
    "type": "string",
    "format": "date",
    "nullable": true
   },
   "isDefault": {
    "type": "boolean"
   },
   "consentPurposeId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "**Storing a card for future use is a purpose a guest consents to**, separate from the payment they are making now. A token taken without it is a card kept on a guest's behalf that they never agreed to.\n"
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
 "Promotion": {
  "x-ticvai-persistence": "promotions.promotion",
  "allOf": [
   {
    "$ref": "#/components/schemas/CreatePromotionRequest"
   },
   {
    "type": "object",
    "required": [
     "id",
     "status"
    ],
    "properties": {
     "id": {
      "type": "string",
      "format": "uuid"
     },
     "status": {
      "$ref": "#/components/schemas/PromotionStatus"
     },
     "isPaused": {
      "type": "boolean"
     },
     "redemptionCount": {
      "type": "integer"
     },
     "discountGiven": {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     },
     "publishedAt": {
      "type": "string",
      "format": "date-time",
      "nullable": true
     },
     "version": {
      "type": "integer",
      "minimum": 1,
      "readOnly": true,
      "description": "Starts at 1 and goes up by one on every saved change. The version the directory, the audit history (`promotions.promotion_audit`) and the channel publication monitor (`promotions.promotion_channel_publication`) name. (DM5, 29 September: data model for the agreed operations)"
     }
    }
   }
  ]
 },
 "PromotionConditions": {
  "x-ticvai-persistence": "none — embedded in promotion",
  "type": "object",
  "description": "All conditions must hold. An empty object matches everything.",
  "properties": {
   "variantIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "productKinds": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "categoryIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "minQuantity": {
    "type": "integer",
    "minimum": 1
   },
   "minBasketValue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "channels": {
    "type": "array",
    "description": "Empty or absent matches every channel.",
    "items": {
     "$ref": "../shared/common.yaml#/components/schemas/SalesChannel"
    }
   },
   "purchaseGate": {
    "type": "boolean",
    "default": false,
    "description": "BL-037. **`evaluatePromotions` gates a price and nothing gated a sale.** A non-member could buy a member-only product at the member price refused, which is a discount failure rather than an eligibility one.\nTrue makes these conditions a **precondition of purchase**: fail them and the line cannot be added, not merely charged more. **Evaluated at add-to-cart**, because a guest told at payment has already entered a card.\n"
   },
   "paymentMethod": {
    "type": "array",
    "nullable": true,
    "description": "BL-113. **Card-issuer and payment-type promotions** — *10% with a Network International card* is a real campaign a bank co-funds, and it was unexpressible.\n**Evaluated at payment, not at cart**, which is the awkward part: the discount appears after the tender is chosen, and the basket total must be allowed to move at that point.\n",
    "items": {
     "type": "string"
    }
   },
   "issuerBins": {
    "type": "array",
    "nullable": true,
    "description": "Card BIN ranges, where the campaign is issuer-specific rather than scheme-specific. **The bank supplies these and they change**, so they are data rather than configuration.\n",
    "items": {
     "type": "string"
    }
   },
   "componentRedemption": {
    "type": "string",
    "nullable": true,
    "enum": [
     "allTogether",
     "independently",
     "sequenced"
    ],
    "description": "BL-112. **Per-component redemption inside a bundle was unstated.** A park-plus-lunch bundle where lunch may be used another day behaves differently from one where both must be used on the same visit, and **the difference is revenue recognition, not just convenience.**\n"
   },
   "daysOfWeek": {
    "type": "array",
    "items": {
     "type": "integer",
     "minimum": 0,
     "maximum": 6
    }
   },
   "startTime": {
    "type": "string",
    "pattern": "^([01]\\d|2[0-3]):[0-5]\\d$"
   },
   "endTime": {
    "type": "string",
    "pattern": "^([01]\\d|2[0-3]):[0-5]\\d$"
   },
   "membershipTierIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "requiresCoupon": {
    "type": "boolean",
    "default": false
   },
   "firstPurchaseOnly": {
    "type": "boolean",
    "default": false
   },
   "performanceIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "advanceDaysMin": {
    "type": "integer",
    "description": "Early-bird — booked at least this many days ahead."
   },
   "advanceDaysMax": {
    "type": "integer",
    "description": "Last-minute — booked no more than this many days ahead."
   },
   "eligibilityRuleIds": {
    "type": "array",
    "nullable": true,
    "items": {
     "type": "string",
     "format": "uuid"
    },
    "description": "Reusable eligibility rules (`promotions.promotion_rule` rows of `ruleType: eligibility` with no promotion of their own, saved by setEligibilityRule) that must also hold. Each is evaluated with its own `effect`. (DM5, 29 September: data model for the agreed operations)"
   }
  }
 },
 "PromotionStatus": {
  "type": "string",
  "enum": [
   "draft",
   "scheduled",
   "live",
   "paused",
   "expired",
   "ended"
  ]
 },
 "PublishedTrackingTechnology": {
  "type": "object",
  "x-ticvai-persistence": "none — the approved rows of marketing.tracking_technology, guest-facing fields only",
  "description": "One approved technology as the preference centre shows it (2.6.54).",
  "required": [
   "name",
   "provider",
   "category",
   "isThirdParty"
  ],
  "properties": {
   "name": {
    "type": "string"
   },
   "provider": {
    "type": "string"
   },
   "category": {
    "$ref": "#/components/schemas/CookieCategory"
   },
   "technologyType": {
    "type": "string"
   },
   "purpose": {
    "type": "string",
    "nullable": true
   },
   "durationDays": {
    "type": "integer",
    "nullable": true,
    "description": "Null for session storage."
   },
   "isThirdParty": {
    "type": "boolean"
   },
   "privacyInformation": {
    "type": "string",
    "nullable": true
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
 "RecordDeviceConsentRequest": {
  "type": "object",
  "x-ticvai-persistence": "none — request only",
  "description": "What the banner or preference centre sends to `recordDeviceConsent`.",
  "required": [
   "channel",
   "action",
   "noticeVersion",
   "decidedAt"
  ],
  "properties": {
   "consentKey": {
    "type": "string",
    "maxLength": 64,
    "nullable": true,
    "description": "The key the browser or app already holds; omitted on a first decision, and one is minted."
   },
   "channel": {
    "$ref": "#/components/schemas/CookieConsentChannel"
   },
   "brandId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "bannerDesignId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "action": {
    "$ref": "#/components/schemas/DeviceConsentAction"
   },
   "categories": {
    "type": "array",
    "description": "Required for `savePreferences`; ignored for the other actions, which decide every category themselves.",
    "items": {
     "type": "object",
     "required": [
      "category",
      "decision"
     ],
     "properties": {
      "category": {
       "$ref": "#/components/schemas/CookieCategory"
      },
      "decision": {
       "type": "string",
       "enum": [
        "granted",
        "declined"
       ]
      }
     }
    }
   },
   "noticeVersion": {
    "type": "string"
   },
   "language": {
    "type": "string",
    "maxLength": 10,
    "nullable": true
   },
   "globalPrivacyControl": {
    "type": "boolean",
    "default": false
   },
   "source": {
    "$ref": "#/components/schemas/ConsentSource"
   },
   "decidedAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "Referral": {
  "type": "object",
  "x-ticvai-persistence": "marketing.referral",
  "description": "BL-034. **No referrer, no reward, nothing anywhere.**\n**The reward fires on the referee's qualifying act, not on the sign-up**, because a referral that pays on registration pays for accounts rather than for guests.\n",
  "required": [
   "id",
   "referrerSubjectId",
   "code",
   "status"
  ],
  "properties": {
   "id": {
    "readOnly": true,
    "type": "string",
    "format": "uuid"
   },
   "referrerSubjectId": {
    "type": "string",
    "format": "uuid"
   },
   "refereeSubjectId": {
    "readOnly": true,
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "code": {
    "readOnly": true,
    "type": "string"
   },
   "status": {
    "readOnly": true,
    "type": "string",
    "enum": [
     "issued",
     "registered",
     "qualified",
     "rewarded",
     "expired",
     "void"
    ]
   },
   "qualifyingAction": {
    "type": "string",
    "enum": [
     "firstPurchase",
     "firstVisit",
     "membershipPurchase"
    ]
   },
   "referrerRewardId": {
    "readOnly": true,
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "refereeRewardId": {
    "readOnly": true,
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "expiresAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "scopePath": {
    "readOnly": true,
    "type": "string",
    "description": "**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**"
   }
  }
 },
 "RetryDunningPaymentRequest": {
  "type": "object",
  "description": "Request only.",
  "properties": {
   "paymentTokenId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "A saved card other than the one that failed: the id of one of the guest's own `PaymentToken` rows (`payments.token`, stored through `storePaymentToken`), **not** a `payments.method` id, which names a kind of method in the catalogue rather than a card. Required after a hard decline.\n"
   }
  }
 },
 "StackingMode": {
  "type": "string",
  "description": "How this promotion combines with others. Declared, never inferred from creation order — two reasonable promotions can otherwise combine into a free ticket.\n",
  "enum": [
   "exclusive",
   "stackable",
   "bestOnly",
   "stackWithGroup"
  ]
 },
 "Wallet": {
  "x-ticvai-persistence": "wallet.wallet + wallet.credit_lot",
  "type": "object",
  "required": [
   "subjectId",
   "balance",
   "currency",
   "status"
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
    "format": "uuid"
   },
   "balance": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "credits": {
    "type": "array",
    "description": "4.3.5 and 4.3.19. **One balance and one bonus balance with one expiry could not express what the requirement asks for** — cash, bonus and redemption credit, each with its own expiry.\n**The expiries are the reason this is a list.** Cash a guest paid for should outlive a promotional credit they were given, and a single `expiresAt` either expires the money they paid or never expires the promotion.\n**Consumed first-expiry-first-out across all three** (4.3.19), which is also the order that is fairest to the guest — spend what is about to die before what is not.\n**One entry per `active` lot in `wallet.credit_lot`** for this wallet: `amount` is the lot's `remaining_amount`, `expiresAt` its `expires_at`, `sourceRef` its `source_reference`. `kind` and `isRefundable` are not stored on the lot; they come from the lot's credit type (`listCreditLots` returns the lots themselves).\n",
    "items": {
     "type": "object",
     "required": [
      "kind",
      "amount"
     ],
     "properties": {
      "kind": {
       "type": "string",
       "enum": [
        "cash",
        "bonus",
        "redemption",
        "refund",
        "goodwill"
       ],
       "description": "**`cash` is money the guest paid and the others are not.** That distinction decides what is refundable, what expires, and what shows as a liability.\n",
       "x-ticvai-persisted": false
      },
      "amount": {
       "x-ticvai-column": "remaining_amount",
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      },
      "expiresAt": {
       "type": "string",
       "format": "date-time",
       "nullable": true
      },
      "sourceRef": {
       "type": "string",
       "nullable": true,
       "x-ticvai-column": "source_reference"
      },
      "isRefundable": {
       "type": "boolean",
       "default": false,
       "x-ticvai-persisted": false,
       "description": "**True only for `cash`.** A guest cannot cash out a promotional credit, and a wallet that lets them has given away the promotion twice.\n"
      }
     }
    }
   },
   "bonusBalance": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "description": "Promotional value. Typically non-refundable and spent first."
   },
   "currency": {
    "type": "string",
    "pattern": "^[A-Z]{3}$"
   },
   "status": {
    "type": "string",
    "enum": [
     "active",
     "suspended",
     "closed"
    ]
   },
   "homeCellName": {
    "type": "string",
    "nullable": true,
    "description": "Where the authoritative balance lives. Present when the guest is linked across cells.\n"
   },
   "expiresAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "lastActivityAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   }
  }
 },
 "WalletAutoReloadSetting": {
  "type": "object",
  "x-ticvai-persistence": "wallet.auto_reload_setting",
  "description": "4.2.17, 4.3.28. Also the `setWalletAutoReloadSetting` body. One per wallet; the holder's own setting within the venue's `WalletFundingRules.autoReload`.",
  "required": [
   "enabled"
  ],
  "properties": {
   "walletId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "subjectId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "enabled": {
    "type": "boolean"
   },
   "thresholdAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "reloadAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "paymentTokenId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "maximumPerDay": {
    "type": "integer",
    "minimum": 1,
    "nullable": true
   },
   "status": {
    "type": "string",
    "readOnly": true,
    "enum": [
     "active",
     "suspendedAfterDecline",
     "disabledByVenue"
    ]
   },
   "lastReloadAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005). Written at the wallet's venue scope."
   }
  }
 },
 "WalletExitBalance": {
  "type": "object",
  "x-ticvai-persistence": "none — computed from wallet.wallet, wallet.credit_lot and held offline transactions",
  "required": [
   "walletId",
   "balance",
   "amountDue",
   "refundable"
  ],
  "properties": {
   "walletId": {
    "type": "string",
    "format": "uuid"
   },
   "balance": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "pendingOfflineAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "amountDue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "refundable": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "nonRefundableCredit": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "waiveAllowedUpTo": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "asAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "WalletExitSettlement": {
  "type": "object",
  "x-ticvai-persistence": "wallet.exit_settlement",
  "description": "4.3.4. One settlement of a wallet at exit.",
  "required": [
   "id",
   "walletId",
   "action",
   "amount",
   "settledAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "walletId": {
    "type": "string",
    "format": "uuid"
   },
   "action": {
    "type": "string",
    "enum": [
     "collect",
     "refund",
     "waive"
    ]
   },
   "method": {
    "type": "string",
    "nullable": true,
    "enum": [
     "card",
     "cash",
     "storedCard",
     "originalPayment"
    ]
   },
   "amount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "balanceBefore": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "paymentId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "refundId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "walletTransactionId": {
    "type": "string",
    "nullable": true
   },
   "reason": {
    "type": "string",
    "nullable": true
   },
   "settledByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "settledAt": {
    "type": "string",
    "format": "date-time"
   },
   "scopePath": {
    "type": "string",
    "readOnly": true
   }
  }
 },
 "WalletTransaction": {
  "x-ticvai-persistence": "wallet.wallet_transaction",
  "type": "object",
  "required": [
   "id",
   "kind",
   "amount",
   "balanceAfter",
   "recordedAt"
  ],
  "properties": {
   "id": {
    "type": "string"
   },
   "walletId": {
    "type": "string",
    "format": "uuid",
    "x-ticvai-references": "wallet.wallet",
    "description": "The wallet this movement is on (SD-027, 29 September). A shared wallet has many subjects, so the subject alone cannot say which balance moved."
   },
   "walletHoldId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "x-ticvai-references": "wallet.hold",
    "description": "The hold a spend settled, where it came through `holdWalletFunds`."
   },
   "kind": {
    "$ref": "#/components/schemas/WalletTransactionKind"
   },
   "amount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "balanceAfter": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "orderId": {
    "type": "string",
    "nullable": true
   },
   "venueId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "reason": {
    "type": "string",
    "nullable": true
   },
   "principalId": {
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
 "WalletTransactionKind": {
  "type": "string",
  "enum": [
   "topUp",
   "spend",
   "refund",
   "adjustment",
   "bonus",
   "expiry",
   "transfer"
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
