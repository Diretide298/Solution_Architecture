# P02-membership-loyalty-value-01 — P02 · Membership, Loyalty & Value

**3 screens · 22 operations · 37 schemas · 11 permissions**

Platform P02 Guest App · ships as **guest** ·
guest audience · mobileApp ·
offline-capable

## Who this is for

**guest on mobileApp.** Everything below is how you know what is
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

- **Every control that can be refused must be gated.** 11 permissions apply here:
  `AI_USE, GUEST_MANAGE, GUEST_VIEW, MARKETING_VIEW, ORDER_CREATE, ORDER_VIEW, PAYMENT_VIEW, PRICE_VIEW, PRODUCT_VIEW, WALLET_OPERATE, WALLET_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **3 of these operations work offline**: listLoyaltyProgrammes, listProducts, listPromotions
  — and the rest do not. A surface that looks the same online and off is lying.
- **Offline, every screen shows one banner, the same on web and app:** *"You're offline. Connect to the internet to book, pay, order or join a queue."* The moment the connection drops, on every screen, above the screen's own content. By itself as soon as the connection is back, with a short "Back online" confirmation. **It never** Covers what is already on screen, or appears for a server error — that is the screen's own error state, and a guest told they are offline when the venue is down reconnects for nothing. Each screen's `states.offline` says what stays on screen and what waits.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `GST-011` | Wallet Overview | listDetail | 6 | 0 | — |
| `GST-015` | Memberships | listDetail | 11 | 2 | — |
| `GST-036` | Loyalty & Rewards | listDetail | 5 | 0 | — |

## Thin screens in this batch

**GST-011, GST-036 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "GST-011",
  "name": "Wallet Overview",
  "module": "Membership, Loyalty & Value",
  "requiresModule": "retail",
  "wave": 2,
  "capability": "C37",
  "implementation": {
   "app": "guest-app",
   "route": "/general/wallet-overview",
   "component": "apps/guest-app/src/routes/general/WalletOverviewDashboard.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "GST-001",
    "GST-037"
   ],
   "inferred": true,
   "exitTo": [
    "GST-001",
    "GST-002",
    "GST-020"
   ],
   "transitions": [
    {
     "to": "GST-001",
     "trigger": "Home – Default",
     "provenance": "derived — GST-001 declares entryState.params  and GST-011 holds none of them, so the edge carries nothing and GST-001 opens cold"
    },
    {
     "to": "GST-020",
     "trigger": "Saved items carry across sessions",
     "provenance": "flow F53 step 4→5",
     "carries": [
      "subjectId"
     ]
    }
   ]
  },
  "notes": "States derived from the screen pattern on 17 August, not individually considered. Purpose derived from the screen name and its operations on 17 August, not from a requirement.",
  "density": "comfortable",
  "pattern": "listDetail",
  "patternReason": "`listWalletTransactions` reads the population and `getWallet` reads one of them — list, select, act",
  "purpose": "The screen this app sits on. Everything else is entered from here and returns to it.",
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
    }
   ]
  },
  "states": {
   "loading": "The wallet overview list.",
   "error": "Could not load. Names which read failed and leaves the wallet overview untouched.",
   "emptyFirstRun": "No wallet overview yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table.",
   "emptyNoResults": "Never shown: `listWalletTransactions` takes no filter, so an empty list is always the first-run state above.",
   "emptyNoAccess": "Shown when the caller lacks `WALLET_VIEW`, which `getWallet` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
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
     "name": "subjectId",
     "from": "GST-001"
    },
    {
     "name": "walletId",
     "from": "navigation"
    }
   ],
   "coldEntry": "Resolves from the session; a cold arrival is the ordinary case.",
   "preloaded": [
    "WalletTransaction.id",
    "WalletTransaction.kind",
    "WalletTransaction.amount",
    "WalletTransaction.balanceAfter",
    "WalletTransaction.orderId"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "designed",
   "board": "wireframes/P02 Guest App.dc.html#gst-011",
   "prototype": {
    "file": "sources/designs/guest-rev3-29-september/TICVAI Mobile App v4.dc.html",
    "rev": "Mobile App v4, 29 September 2026",
    "match": "none",
    "note": "Mobile App v4 has no view for this screen. Drawn by Claude Code on 30 September 2026 in the v4 look (the frame on this screen's board, wireframes/frames/gst-011.html, and #GST-011 in handoff/design-batches/apps/1-guest-app/return/TICVAI Guest App.dc.html). NOT client-verified: awaiting the client's design reviewer. Build the layout from that frame and this definition. Mobile v2 (28 September, superseded by v4) showed it at: Account → All screens → Wave 2 → Wallet overview (exact)."
   },
   "source": "Claude Code, 30 September 2026, drawn in the Mobile App v4 look",
   "note": "**Drawn by Claude Code on 30 September 2026 in the Mobile App v4 look; not client-verified, awaiting the client's design reviewer.** `provenance: designed` because the accepted vocabulary has no value for an agent-drawn frame; it is the value the eight Claude Design frames of 29 September carry. Gaps the operations leave are in handoff/design-batches/apps/1-guest-app/return/FINDINGS.md."
  },
  "apisNote": "Rebuilt 9 September 2026 from the 2 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P02",
   "audience": "guest",
   "formFactor": "mobileApp",
   "shortName": "Guest App",
   "name": "Guest App — Mobile",
   "offlineCapable": true,
   "offlineBanner": {
    "kind": "banner",
    "state": "warning",
    "message": "You're offline. Connect to the internet to book, pay, order or join a queue.",
    "shows": "The moment the connection drops, on every screen, above the screen's own content.",
    "clears": "By itself as soon as the connection is back, with a short \"Back online\" confirmation.",
    "never": "Covers what is already on screen, or appears for a server error — that is the screen's own error state, and a guest told they are offline when the venue is down reconnects for nothing.",
    "provenance": "Decided 12 September 2026 — guest web and guest app behave identically offline and say so with the same banner."
   },
   "app": "guest-app",
   "operator": "guest",
   "targetApp": {
    "app": "guest",
    "name": "TICVAI Guest",
    "shell": "mobile",
    "siblings": [
     "P01",
     "P05"
    ],
    "note": "**One guest product in three shells.** Web, mobile and kiosk share 73–91% of their operations; the kiosk is the same product in a fixed frame with no keyboard, and is deliberately narrower rather than different.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "GST-015",
  "name": "Memberships",
  "module": "Membership, Loyalty & Value",
  "requiresModule": "ticketing",
  "wave": 2,
  "capability": "C03",
  "implementation": {
   "app": "guest-app",
   "route": "/general/memberships",
   "component": "apps/guest-app/src/routes/general/MembershipsDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "GST-001"
   ],
   "inferred": true,
   "exitTo": [
    "GST-001",
    "GST-002"
   ],
   "fromFlows": true,
   "transitions": [
    {
     "to": "GST-001",
     "trigger": "Home – Default",
     "provenance": "derived — GST-001 declares entryState.params  and GST-015 holds none of them, so the edge carries nothing and GST-001 opens cold"
    },
    {
     "to": "ADM-003",
     "trigger": "The right is propagated to the other cell",
     "provenance": "flow F19 step 1→2",
     "crossesDevice": true,
     "back": false
    }
   ]
  },
  "notes": "States derived from the screen pattern on 17 August, not individually considered. Purpose derived from the screen name and its operations on 17 August, not from a requirement. Membership. **`listDelegations` and `grantDelegation` are the member list and add-member** Pranay asked for — CF-132 built them as delegated authority rather than a household table. **Rewired on the 20 August review.** **`getGuestLink` restored** — F19 step 1 calls it from here and my rewire dropped it. **A membership that works in another country resolves through the guest link**, and the flow checker caught what the screen edit did not. **Cross-platform navigation removed 24 August**: ADM-003. **A till does not navigate to a back office and a guest app does not navigate to either** — those are device handovers, and a flow declares them with `crossesDevice` rather than a screen pretending there is a link. **Wired 24 August from review**: getSubscription, listSubscriptionInvoices. **The operations existed and this screen could not call them** — reviewers reported them as missing APIs, which is what an unreachable operation looks like from a wireframe. **`getSubscription` and `listSubscriptionInvoices` removed the same day they were wired.** `check-screens` refused them: **both carry a staff permission and this is a guest surface.** The reviewer asked for `GET /memberships/current` — a guest-scoped read that does not exist. **That is the correct finding and the wiring was the wrong fix**: it is a new operation, not a missing link. **`getGuestLink` is `service` audience** — a cross-region pseudonymous lookup (ADR-0010), not something a membership screen calls. Removed 24 August. **`getMyMemberships` and `listGuestMemberships` wired 24 August**, replacing `getGuestLink`. A guest reading their own membership calls a guest operation; **`getGuestLink` is the cross-region pseudonymous lookup a service makes on their behalf** (ADR-0010), and F19 was walking it from a guest screen.\n\n**Rev 3 (decided 29 September).** Billing statement decline states (DG-2, no contract change): soft decline → *Retry now* and *Use another card*; hard decline → another card only; declined again → the next retry date; paid.",
  "density": "comfortable",
  "pattern": "listDetail",
  "patternReason": "`listDelegations` reads the population and `getMyMemberships` reads one of them — list, select, act",
  "purpose": "Find memberships for this venue.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every memberships",
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
       "label": "Grant delegation",
       "operation": "grantDelegation",
       "provenance": "contract identity.yaml POST /guests/{subjectId}/delegations"
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
   "loading": "The memberships list.",
   "error": "Could not load. Names which read failed and leaves the memberships untouched.",
   "emptyFirstRun": "No memberships yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table.",
   "emptyNoResults": "Nothing matches the filter on from, to and the memberships are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `PRODUCT_VIEW`, which `getMyMemberships` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
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
    "operationId": "getMyMemberships",
    "contract": "catalogue",
    "purpose": "A guest's own memberships, benefits and history",
    "trigger": "onLoad"
   },
   {
    "operationId": "listDelegations",
    "contract": "identity",
    "purpose": "Who may act for this guest, and for whom they may act",
    "trigger": "onLoad"
   },
   {
    "operationId": "grantDelegation",
    "contract": "identity",
    "purpose": "Let one guest act for another",
    "trigger": "onAction",
    "invalidates": [
     "listDelegations"
    ]
   },
   {
    "operationId": "listProducts",
    "contract": "catalogue",
    "purpose": "List products",
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
     "name": "guestLinkId",
     "from": "deepLink"
    },
    {
     "name": "subjectId",
     "from": "GST-001"
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
   "coldEntry": "**A guest arriving cold on a link that no longer resolves is shown what happened and one way onward — never a 404.** A shared ticket, a forwarded confirmation and a push notification opened three weeks late all land here, and the person holding the link did nothing wrong. **The screen names the thing, says it is expired, cancelled or withdrawn, and offers the list it came from.** Arrives with `guestLinkId`.",
   "preloaded": [
    "BillingStatement.id",
    "BillingStatement.subjectId",
    "BillingStatement.periodStart",
    "BillingStatement.periodEnd",
    "BillingStatement.lines"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "designed",
   "board": "wireframes/P02 Guest App.dc.html#gst-015",
   "prototype": {
    "file": "sources/designs/guest-rev3-29-september/TICVAI Mobile App v4.dc.html",
    "rev": "Mobile App v4, 29 September 2026",
    "match": "none",
    "note": "Mobile App v4 has no view for this screen. Drawn by Claude Code on 30 September 2026 in the v4 look (the frame on this screen's board, wireframes/frames/gst-015.html, and #GST-015 in handoff/design-batches/apps/1-guest-app/return/TICVAI Guest App.dc.html). NOT client-verified: awaiting the client's design reviewer. Build the layout from that frame and this definition. Mobile v2 (28 September, superseded by v4) showed it at: Account → All screens → Wave 2 → Memberships; billing in \"Also built, not in the plan\" → Membership billing (#billing) (exact). What v2 did differently: Prototype splits the screen in two (benefits and delegation vs billing statement and dunning retries)."
   },
   "source": "Claude Code, 30 September 2026, drawn in the Mobile App v4 look",
   "note": "**Drawn by Claude Code on 30 September 2026 in the Mobile App v4 look; not client-verified, awaiting the client's design reviewer.** `provenance: designed` because the accepted vocabulary has no value for an agent-drawn frame; it is the value the eight Claude Design frames of 29 September carry. Gaps the operations leave are in handoff/design-batches/apps/1-guest-app/return/FINDINGS.md."
  },
  "apisNote": "Rebuilt 9 September 2026 from the 5 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
   }
  ],
  "_platform": {
   "code": "P02",
   "audience": "guest",
   "formFactor": "mobileApp",
   "shortName": "Guest App",
   "name": "Guest App — Mobile",
   "offlineCapable": true,
   "offlineBanner": {
    "kind": "banner",
    "state": "warning",
    "message": "You're offline. Connect to the internet to book, pay, order or join a queue.",
    "shows": "The moment the connection drops, on every screen, above the screen's own content.",
    "clears": "By itself as soon as the connection is back, with a short \"Back online\" confirmation.",
    "never": "Covers what is already on screen, or appears for a server error — that is the screen's own error state, and a guest told they are offline when the venue is down reconnects for nothing.",
    "provenance": "Decided 12 September 2026 — guest web and guest app behave identically offline and say so with the same banner."
   },
   "app": "guest-app",
   "operator": "guest",
   "targetApp": {
    "app": "guest",
    "name": "TICVAI Guest",
    "shell": "mobile",
    "siblings": [
     "P01",
     "P05"
    ],
    "note": "**One guest product in three shells.** Web, mobile and kiosk share 73–91% of their operations; the kiosk is the same product in a fixed frame with no keyboard, and is deliberately narrower rather than different.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "GST-036",
  "name": "Loyalty & Rewards",
  "module": "Membership, Loyalty & Value",
  "requiresModule": "marketing",
  "wave": 2,
  "capability": "C64",
  "implementation": {
   "app": "guest-app",
   "route": "/loyalty-rewards",
   "component": "apps/guest-app/src/routes/LoyaltyRewards.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "GST-001"
   ],
   "inferred": true,
   "exitTo": [
    "GST-001",
    "GST-002"
   ],
   "transitions": [
    {
     "to": "GST-001",
     "trigger": "Home – Default",
     "provenance": "derived — GST-001 declares entryState.params  and GST-036 holds none of them, so the edge carries nothing and GST-001 opens cold"
    },
    {
     "to": "WEB-024",
     "trigger": "They see rewards and manage their devices",
     "provenance": "flow F53 step 1→2",
     "crossesDevice": true,
     "back": false
    }
   ]
  },
  "notes": "Merged with GST-064 on 18 August. **I created GST-064 in the parity sweep without noticing this screen existed** — same two operations, same capability, and the fuzzy match against the client storyboard is what surfaced it. Board 6 panel 6 shows one Loyalty & Rewards screen, not two. **Cross-surface parity, 31 August**: added evaluatePromotions, listPromotions. **The same screen on web and app was calling different operations** — one side could do something the other could not, and nothing recorded the difference as deliberate. **Pull audit, 27 September**: evaluatePromotions removed again. It evaluates a cart — `EvaluatePromotionsRequest` requires venueId, channel and at least one line — and this screen has no cart: no entry params, nothing in a basket. The parity pass copied it across without asking what it would be sent. Promotions are evaluated where the cart is.",
  "density": "comfortable",
  "pattern": "listDetail",
  "patternReason": "`listLoyaltyProgrammes` reads the population and `getLoyaltyPosition` reads one of them — list, select, act",
  "purpose": "Your points, your tier, and what is within reach.",
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
    }
   ]
  },
  "states": {
   "loading": "The loyalty rewards list.",
   "error": "Could not load. Names which read failed and leaves the loyalty rewards untouched.",
   "emptyFirstRun": "No loyalty rewards yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table.",
   "emptyNoResults": "Never shown: `listLoyaltyProgrammes` takes no filter, so an empty list is always the first-run state above.",
   "emptyNoAccess": "Shown when the caller lacks `MARKETING_VIEW`, which `listLoyaltyProgrammes` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
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
  "wireframe": {
   "status": "notStarted",
   "provenance": "designed",
   "board": "wireframes/P02 Guest App.dc.html#gst-036",
   "prototype": {
    "file": "sources/designs/guest-rev3-29-september/TICVAI Mobile App v4.dc.html",
    "rev": "Mobile App v4, 29 September 2026",
    "match": "none",
    "note": "Mobile App v4 has no view for this screen. Drawn by Claude Code on 30 September 2026 in the v4 look (the frame on this screen's board, wireframes/frames/gst-036.html, and #GST-036 in handoff/design-batches/apps/1-guest-app/return/TICVAI Guest App.dc.html). NOT client-verified: awaiting the client's design reviewer. Build the layout from that frame and this definition. Mobile v2 (28 September, superseded by v4) showed it at: Account → All screens → Wave 2 → Loyalty & rewards (exact)."
   },
   "source": "Claude Code, 30 September 2026, drawn in the Mobile App v4 look",
   "note": "**Drawn by Claude Code on 30 September 2026 in the Mobile App v4 look; not client-verified, awaiting the client's design reviewer.** `provenance: designed` because the accepted vocabulary has no value for an agent-drawn frame; it is the value the eight Claude Design frames of 29 September carry. Gaps the operations leave are in handoff/design-batches/apps/1-guest-app/return/FINDINGS.md."
  },
  "apisNote": "Rebuilt 9 September 2026 from the operations this screen declares (4 then; evaluatePromotions removed 27 September), not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P02",
   "audience": "guest",
   "formFactor": "mobileApp",
   "shortName": "Guest App",
   "name": "Guest App — Mobile",
   "offlineCapable": true,
   "offlineBanner": {
    "kind": "banner",
    "state": "warning",
    "message": "You're offline. Connect to the internet to book, pay, order or join a queue.",
    "shows": "The moment the connection drops, on every screen, above the screen's own content.",
    "clears": "By itself as soon as the connection is back, with a short \"Back online\" confirmation.",
    "never": "Covers what is already on screen, or appears for a server error — that is the screen's own error state, and a guest told they are offline when the venue is down reconnects for nothing.",
    "provenance": "Decided 12 September 2026 — guest web and guest app behave identically offline and say so with the same banner."
   },
   "app": "guest-app",
   "operator": "guest",
   "targetApp": {
    "app": "guest",
    "name": "TICVAI Guest",
    "shell": "mobile",
    "siblings": [
     "P01",
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
 }
}
```
