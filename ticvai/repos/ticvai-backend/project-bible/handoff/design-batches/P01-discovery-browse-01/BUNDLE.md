# P01-discovery-browse-01 — P01 · Discovery & Browse

**5 screens · 23 operations · 61 schemas · 4 permissions**

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

- **Every control that can be refused must be gated.** 4 permissions apply here:
  `AI_USE, ORDER_VIEW, PRODUCT_VIEW, TENANT_CONFIGURE`. A control nobody can use must say so,
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
| `WEB-001` | Home / Landing | listDetail | 10 | 0 | — |
| `WEB-002` | Event & Attraction Listing | listDetail | 6 | 0 | — |
| `WEB-003` | Search Results | listDetail | 2 | 0 | — |
| `WEB-004` | Attraction Details | listDetail | 5 | 0 | — |
| `WEB-050` | Plan Your Visit | multiStepForm | 7 | 0 | — |

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "WEB-001",
  "name": "Home / Landing",
  "module": "Discovery & Browse",
  "requiresModule": "ticketing",
  "wave": 1,
  "capability": "C79",
  "implementation": {
   "app": "guest-web",
   "route": "/discovery-and-browse/home-landing",
   "component": "apps/guest-web/src/routes/discovery-and-browse/HomeLandingDashboard.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "isEntryPoint": true,
   "exitTo": [
    "WEB-002",
    "WEB-003",
    "WEB-004",
    "WEB-008",
    "WEB-009",
    "WEB-016",
    "WEB-017",
    "WEB-018",
    "WEB-019",
    "WEB-020",
    "WEB-021",
    "WEB-022",
    "WEB-023",
    "WEB-024",
    "WEB-025",
    "WEB-026",
    "WEB-027",
    "WEB-028",
    "WEB-029",
    "WEB-032",
    "WEB-033",
    "WEB-034",
    "WEB-036",
    "WEB-037",
    "WEB-038",
    "WEB-039",
    "WEB-040",
    "WEB-041",
    "WEB-042",
    "WEB-043",
    "WEB-044",
    "WEB-045",
    "WEB-046",
    "WEB-049",
    "WEB-050"
   ],
   "transitions": [
    {
     "to": "WEB-002",
     "trigger": "Event & Attraction Listing",
     "provenance": "structural — WEB-001 is P01's home screen and its exits are its launcher",
     "carries": [
      "eventId"
     ]
    },
    {
     "to": "WEB-003",
     "trigger": "Search Results",
     "provenance": "structural — WEB-001 is P01's home screen and its exits are its launcher"
    },
    {
     "to": "WEB-016",
     "trigger": "Login / Register",
     "provenance": "structural — WEB-001 is P01's home screen and its exits are its launcher"
    },
    {
     "to": "WEB-036",
     "trigger": "F&B – Browse & Order",
     "provenance": "structural — WEB-001 is P01's home screen and its exits are its launcher"
    },
    {
     "to": "WEB-037",
     "trigger": "Menu Item Detail",
     "provenance": "structural — WEB-001 is P01's home screen and its exits are its launcher"
    },
    {
     "to": "WEB-038",
     "trigger": "F&B – Order Tracking",
     "provenance": "structural — WEB-001 is P01's home screen and its exits are its launcher"
    },
    {
     "to": "WEB-039",
     "trigger": "Venue Map & Wait Times",
     "provenance": "structural — WEB-001 is P01's home screen and its exits are its launcher"
    },
    {
     "to": "WEB-040",
     "trigger": "Virtual Queue",
     "provenance": "structural — WEB-001 is P01's home screen and its exits are its launcher"
    },
    {
     "to": "WEB-041",
     "trigger": "Parking – Reserve & Pay",
     "provenance": "structural — WEB-001 is P01's home screen and its exits are its launcher",
     "carries": [
      "entitlementId"
     ]
    },
    {
     "to": "WEB-042",
     "trigger": "Retail & Shop and Drop",
     "provenance": "structural — WEB-001 is P01's home screen and its exits are its launcher"
    },
    {
     "to": "WEB-043",
     "trigger": "Loyalty & Rewards",
     "provenance": "structural — WEB-001 is P01's home screen and its exits are its launcher"
    },
    {
     "to": "WEB-044",
     "trigger": "AI Concierge – Home",
     "provenance": "structural — WEB-001 is P01's home screen and its exits are its launcher"
    },
    {
     "to": "WEB-045",
     "trigger": "Help Centre & Accessibility",
     "provenance": "structural — WEB-001 is P01's home screen and its exits are its launcher"
    },
    {
     "to": "WEB-046",
     "trigger": "In-Venue Notifications",
     "provenance": "structural — WEB-001 is P01's home screen and its exits are its launcher"
    },
    {
     "to": "WEB-008",
     "trigger": "Add-ons & Upsell",
     "provenance": "derived — WEB-008 declares entryState.params bundleId and WEB-001 holds none of them. The edge carries nothing: WEB-008 opens on listCatalogueBundles, and bundleId has no source on WEB-008 yet (a gap in WEB-008, not in this edge)"
    },
    {
     "to": "WEB-009",
     "trigger": "Wishlist",
     "provenance": "derived — WEB-009 declares entryState.params itemId and WEB-001 holds none of them. The edge carries nothing: itemId only pre-selects (deep link or optional), and WEB-009 opens on its own"
    },
    {
     "to": "WEB-017",
     "trigger": "My Account Dashboard",
     "provenance": "derived — WEB-017 declares entryState.params deviceId, itemId, token and WEB-001 holds none of them. The edge carries nothing: deviceId, itemId, token only pre-select (deep link or optional), and WEB-017 opens on its own"
    },
    {
     "to": "WEB-018",
     "trigger": "My Tickets",
     "carries": [
      "entitlementId",
      "orderId"
     ],
     "provenance": "derived — WEB-018 declares entryState.params entitlementId, orderId and WEB-001 holds entitlementId, orderId, so an edge into it carries them"
    },
    {
     "to": "WEB-019",
     "trigger": "Order History",
     "provenance": "derived — WEB-019 declares entryState.params documentId, invoiceId, orderId and WEB-001 holds none of them. The edge carries nothing: orderId only pre-selects (deep link or optional); WEB-019 finds invoiceId (listTaxInvoices) itself; WEB-019 opens on listMyOrders, and documentId has no source on WEB-019 yet (a gap in WEB-019, not in this edge)"
    },
    {
     "to": "WEB-021",
     "trigger": "Wallet & Gift Cards",
     "provenance": "derived — WEB-021 declares entryState.params cardCode, walletId and WEB-001 holds none of them. The edge carries nothing: cardCode only pre-selects (deep link or optional); WEB-021 finds walletId (getWallet) itself, and WEB-021 opens on its own"
    },
    {
     "to": "WEB-022",
     "trigger": "Membership Plans",
     "carries": [
      "productId"
     ],
     "provenance": "derived — WEB-022 declares entryState.params productId and WEB-001 holds productId, so an edge into it carries them"
    },
    {
     "to": "WEB-023",
     "trigger": "Membership Management",
     "provenance": "derived — WEB-023 declares entryState.params caseId, orderId, statementId and WEB-001 holds none of them. The edge carries nothing: orderId only pre-selects (deep link or optional); WEB-023 finds statementId (listBillingStatements) itself; WEB-023 opens on listBillingStatements, and caseId has no source on WEB-023 yet (a gap in WEB-023, not in this edge)"
    },
    {
     "to": "WEB-024",
     "trigger": "Devices, Wishlist & Consent",
     "provenance": "derived — WEB-024 declares entryState.params deviceId, enrolmentId, itemId, methodId and WEB-001 holds none of them. The edge carries nothing: deviceId, itemId only pre-select (deep link or optional); WEB-024 finds methodId (enrolMfaMethod) itself; WEB-024 opens on getWishlist, and enrolmentId has no source on WEB-024 yet (a gap in WEB-024, not in this edge)"
    },
    {
     "to": "WEB-027",
     "trigger": "Newsletter Subscription",
     "provenance": "derived — WEB-027 declares entryState.params deviceId, itemId and WEB-001 holds none of them. The edge carries nothing: deviceId, itemId only pre-select (deep link or optional), and WEB-027 opens on its own"
    },
    {
     "to": "WEB-032",
     "trigger": "Offers & Promotions",
     "provenance": "derived — WEB-032 declares entryState.params promotionId and WEB-001 holds none of them. The edge carries nothing: promotionId only pre-selects (deep link or optional), and WEB-032 opens on its own"
    },
    {
     "to": "WEB-033",
     "trigger": "Shop",
     "provenance": "derived — WEB-033 declares entryState.params outletId and WEB-001 holds none of them. The edge carries nothing: outletId only pre-selects (deep link or optional), and WEB-033 opens on its own"
    },
    {
     "to": "WEB-034",
     "trigger": "Lost & Found",
     "provenance": "derived — WEB-034 declares entryState.params caseId and WEB-001 holds none of them. The edge carries nothing: caseId only pre-selects (deep link or optional), and WEB-034 opens on its own"
    },
    {
     "to": "WEB-020",
     "trigger": "Profile & Preferences",
     "provenance": "structural — WEB-001 is P01's home screen and its exits are its launcher"
    },
    {
     "to": "WEB-025",
     "trigger": "Help Centre / FAQ",
     "provenance": "structural — WEB-001 is P01's home screen and its exits are its launcher"
    },
    {
     "to": "WEB-026",
     "trigger": "Survey & Feedback",
     "provenance": "structural — WEB-001 is P01's home screen and its exits are its launcher"
    },
    {
     "to": "WEB-028",
     "trigger": "Contact & Venue Information",
     "provenance": "structural — WEB-001 is P01's home screen and its exits are its launcher"
    },
    {
     "to": "WEB-029",
     "trigger": "Error / Sold Out / Maintenance",
     "provenance": "structural — WEB-001 is P01's home screen and its exits are its launcher"
    },
    {
     "to": "WEB-049",
     "trigger": "Book a trip (a transport venue)",
     "provenance": "decided 29 September, rev 3 REV3-21: transport ticketing is in scope; the transport venue's home call to action opens the route and schedule screen"
    },
    {
     "to": "WEB-050",
     "trigger": "Plan your visit (header)",
     "provenance": "decided 29 September 2026, MOB-6; web build Plan your visit"
    },
    {
     "to": "WEB-004",
     "trigger": "Opens a product and decides",
     "provenance": "flow F01 step 1→2",
     "carries": [
      "productId"
     ]
    }
   ],
   "entryFrom": [
    "WEB-049"
   ]
  },
  "notes": "**Venue selection added 28 September** (decided 28 September, audit R267): a venue picker on first open, remembered on the device, **Change venue** in the header, and a visit-day suggestion from the guest's ticket. The options come from `getTenantAppStatus.venues`, the tenant's active venues, public and cacheable.\n\n**Rev 3 (decided 29 September).** Category cards render as a grid or as one scrolling row per `BookingFlowConfig.cardLayout` (the retired `categoryDisplay` of 23SEP-18 is removed, W7). The event banner lists dates only when `BookingFlowConfig.eventBannerDates` is on (default off; 23SEP-19); the date picker always sits at the top of the booking step. The venue picked here (audit R267) is the venue whose booking-flow settings apply on every booking screen, and the booking screens' *Booking at* bar changes it (REV3-18). Every booking-flow setting named here is read from `getTenantConfig` `bookingFlow`, resolved for the venue the guest picked (audit R267): the tenant's values with that venue's `venueOverrides` entry laid over field by field (decided 29 September, rev 3 CFG-11). The UI preset stays `BookingFlowConfig.preset` (CFG-1, no change); the search box in the banner is off by default (`searchInBanner` default false, CFG-6). The in-venue notifications link is live again: WEB-046 is back in the first release (GAP-C1, reversing audit R242).\n\n**29 September.** *Plan your visit* in the header opens WEB-050 full screen (MOB-6). W7: `categoryDisplay` is retired.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listProducts` reads the population and `getTenantAppStatus` reads one of them — list, select, act",
  "purpose": "Show a guest what is on and give them one obvious way to start booking.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "selectField",
       "label": "Your venue",
       "bindsTo": "TenantAppStatus.venues",
       "operation": "getTenantAppStatus",
       "notes": "**The guest picks a venue on first open** (decided 28 September, audit R267): shown before anything else when the device has no venue remembered, and remembered on the device after that. The chosen `venueId` is what every screen that declares `venueId` `from: session` reads, and it is sent as `?venueId=` to `listProducts`. The options are `getTenantAppStatus.venues` (venue id, name, city, today's opening hours), the tenant's active venues, returned without a session.",
       "provenance": "contract white-label.yaml GET /tenant-config/status (TenantAppStatus.venues, audit R267)"
      },
      {
       "kind": "banner",
       "label": "Visiting today?",
       "bindsTo": "Entitlement",
       "columns": [
        "Entitlement.venueId",
        "Entitlement.validFrom",
        "Entitlement.validTo"
       ],
       "operation": "listMyEntitlements",
       "notes": "**On a visit day the app suggests the ticket's venue** (decided 28 September, audit R267): for a signed-in guest, an entitlement from `listMyEntitlements` (`state=upcoming`) valid today at a venue other than the chosen one offers **Switch to that venue**; the guest decides, the app never switches by itself.",
       "provenance": "contract access.yaml GET /guests/me/entitlements"
      },
      {
       "kind": "banner",
       "label": "Sold out or closed today",
       "bindsTo": "TenantAppStatus.availabilityMessage",
       "operation": "getTenantAppStatus",
       "notes": "From `getTenantAppStatus.availability` (`open`, `soldOut`, `closed`) and `availabilityMessage` (decided 28 September, audit R073 (f)); nothing shows while it is `open`.",
       "provenance": "contract white-label.yaml GET /tenant-config/status"
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
       "kind": "banner",
       "bindsTo": "TenantAppStatus.maintenanceMessage",
       "notes": "Only when isInMaintenance. Tenant-branded, never a generic error page",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "cardList",
       "bindsTo": "HomepageLayout.sections",
       "notes": "Section order comes from tenant configuration (WLB-011), not from code. A section referencing a disabled module must not render at all",
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
        "Product.categoryId",
        "Product.lifecycleState",
        "Product.isSellable",
        "Product.isStockTracked"
       ],
       "operation": "listProducts",
       "provenance": "contract catalogue.yaml GET /products"
      },
      {
       "kind": "detailPanel",
       "label": "The tenant config",
       "bindsTo": "TenantConfig",
       "columns": [
        "TenantConfig.isDraft",
        "TenantConfig.brand",
        "TenantConfig.appIcons",
        "TenantConfig.bookingFlow",
        "TenantConfig.theme",
        "TenantConfig.fonts",
        "TenantConfig.footer",
        "TenantConfig.notificationBranding",
        "TenantConfig.enabledPaymentMethods",
        "TenantConfig.accessibility",
        "TenantConfig.header",
        "TenantConfig.navigation",
        "TenantConfig.homepage",
        "TenantConfig.modules",
        "TenantConfig.features",
        "TenantConfig.languages"
       ],
       "operation": "getTenantConfig",
       "provenance": "contract white-label.yaml GET /tenant-config"
      },
      {
       "kind": "detailPanel",
       "label": "The tenant app status",
       "bindsTo": "TenantAppStatus",
       "columns": [
        "TenantAppStatus.isPublished",
        "TenantAppStatus.publishedVersion",
        "TenantAppStatus.publishedAt",
        "TenantAppStatus.draftVersion",
        "TenantAppStatus.hasUnpublishedChanges",
        "TenantAppStatus.activeModuleCount",
        "TenantAppStatus.licensedModuleCount",
        "TenantAppStatus.activePageCount",
        "TenantAppStatus.isInMaintenance",
        "TenantAppStatus.maintenanceMessage",
        "TenantAppStatus.expectedBackAt",
        "TenantAppStatus.recentChanges"
       ],
       "operation": "getTenantAppStatus",
       "provenance": "contract white-label.yaml GET /tenant-config/status"
      }
     ]
    },
    {
     "name": "header",
     "slot": "carried",
     "components": [
      {
       "kind": "iconButton",
       "label": "Search",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "secondaryButton",
       "label": "Sign in",
       "notes": "Becomes an account menu once authenticated",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "secondaryButton",
       "label": "Change venue",
       "notes": "Reopens the venue picker; the new choice replaces the remembered one on this device and every venue-scoped screen reloads for it (decided 28 September, audit R267).",
       "provenance": "decided 28 September 2026, audit R267"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The home landing list.",
   "error": "Could not load. Names which read failed and leaves the home landing untouched.",
   "emptyFirstRun": "No home landing yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table.",
   "emptyNoResults": "Nothing matches the filter on venueId, kind, isSellable and the home landing are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "**There is no permission to name — a guest holds none** (ADR-0025: `x-ticvai-permission` is what a staff caller must hold; a guest call resolves to the guest's own data). No access here means one of two things, told apart by the response: not signed in, where the guest is offered sign-in and brought back to this screen, or a record that is not theirs, which says so without saying whose it is. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "**The offline banner shows.** What was already loaded stays on screen, marked with its age. Anything that spends money, holds capacity or changes the account waits for the connection, and its button says so rather than failing."
  },
  "apis": [
   {
    "operationId": "getTenantAppStatus",
    "purpose": "Maintenance check before rendering anything",
    "trigger": "onLoad",
    "contract": "white-label"
   },
   {
    "operationId": "getTenantConfig",
    "contract": "white-label",
    "purpose": "Full working configuration",
    "trigger": "onLoad"
   },
   {
    "operationId": "listProducts",
    "contract": "catalogue",
    "purpose": "List products",
    "trigger": "onLoad"
   },
   {
    "operationId": "listMyEntitlements",
    "contract": "access",
    "purpose": "The guest's upcoming tickets, so a visit day can suggest the ticket's venue (decided 28 September, audit R267); only when signed in",
    "trigger": "onLoad"
   },
   {
    "operationId": "getCookieConsentRuntime",
    "contract": "marketing-crm",
    "purpose": "Cookie banner on first visit and what the tag loader may load",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "recordDeviceConsent",
    "contract": "marketing-crm",
    "purpose": "Accept all, reject non-essential or save preferences from the banner",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "listAnalyticsProviders",
    "contract": "white-label",
    "purpose": "Analytics tags to inject once their consent category is granted",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
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
   },
   {
    "operationId": "recordStorefrontSessionEvents",
    "contract": "white-label",
    "purpose": "Runtime-shell beacon of hashed browsing behaviour for fraud prevention (every page of the session; bound on the home screen as the shell's entry)",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   }
  ],
  "entryState": {
   "coldEntry": "**A cold arrival is the ordinary case.** **The venue comes from the device** (decided 28 September, audit R267): on first open the guest picks one, it is remembered on the device and changeable from the header, and on a visit day the ticket's venue is suggested. Every guest screen that declares `venueId` `from: session` reads that remembered choice.",
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
   "board": "wireframes/P01 Guest Web.dc.html#web-001",
   "prototype": {
    "file": "sources/designs/guest-rev3-28-september/TICVAI Guest Booking v2.dc.html",
    "rev": "rev 3",
    "verified": "2026-09-28",
    "match": "partial",
    "view": "Header 'Discover' (default view on load)",
    "differences": "No first-open venue picker remembered on the device and no 'Change venue' in the header (YAML R267); the prototype shows 'Browse by venue' tiles instead and switches venue from the Config drawer. Prototype adds a resume-booking card, a video 'Tonight in the city' panel, live queue times on cards and footer links to Contact / Accessibility / Service status. YAML emptyNoAccess/offline states are not drawn on Home (offline exists only as a demo tweak)."
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
  "id": "WEB-002",
  "name": "Event & Attraction Listing",
  "module": "Discovery & Browse",
  "requiresModule": "ticketing",
  "wave": 1,
  "capability": "C79",
  "implementation": {
   "app": "guest-web",
   "route": "/discovery-and-browse/event-and-attraction-listing",
   "component": "apps/guest-web/src/routes/discovery-and-browse/EventAndAttractionListingList.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "WEB-001",
    "WEB-003"
   ],
   "exitTo": [
    "WEB-001",
    "WEB-003",
    "WEB-004",
    "WEB-005"
   ],
   "transitions": [
    {
     "to": "WEB-004",
     "trigger": "Attraction Details",
     "carries": [
      "eventId",
      "productId"
     ],
     "provenance": "derived — WEB-004 declares entryState.params eventId, productId and WEB-002 holds eventId, productId, so an edge into it carries them"
    },
    {
     "to": "WEB-005",
     "trigger": "Book (the ticket counters open as a side panel on the listing)",
     "carries": [
      "productId"
     ],
     "provenance": "decided 29 September, rev 3 23SEP-5: WEB-005 may render as a side panel on WEB-002 and WEB-004"
    }
   ]
  },
  "notes": "**Cross-surface parity, 31 August**: added getWaitTimes. **A guest does not know which surface they are on** — the same named screen on web and app now calls the same guest-callable operations.\n\n**Rev 3 (decided 29 September).** Categories: tiles from `listProductCategories`, then `listProducts?categoryId=`, or one flat list, per `BookingFlowConfig.ticketCategories` (REV3-16); tiles as a grid or a row per `cardLayout` (`categoryDisplay` retired, W7). **Info-only products** (`Product.guestListing` `infoOnly`) are listed with `notBookableLabel` (default *Info only / Not bookable online*) and open their details instead of adding to the basket; they are hidden when `BookingFlowConfig.showInfoOnly` is off (REV3-14). Each card shows the product's own primary image (`Product.media` `isPrimary`, `searchCatalogue` `primaryMedia`; 23SEP-4). **Book** opens the ticket counters (WEB-005) as a side panel on this listing rather than a new page (23SEP-5). Card layout, size and density are the enums `cardLayout` [stackedRows, splitRows, cardsAcross, posterCards], `cardSize` [compact, standard, large, extraLarge] and `density` [compact, standard, roomy] (DG-6). Every booking-flow setting named here is read from `getTenantConfig` `bookingFlow`, resolved for the venue the guest picked (audit R267): the tenant's values with that venue's `venueOverrides` entry laid over field by field (decided 29 September, rev 3 CFG-11).\n\n**29 September.** W4: Help me choose filters this list, with *Show everything*. W3: view-only products show Call sales / Email sales. W7: `categoryDisplay` retired.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listProducts` reads the population and `getWaitTimes` reads one of them — list, select, act",
  "purpose": "Browse and filter everything bookable.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "cardList",
       "label": "Category tiles",
       "bindsTo": "ProductCategory",
       "notes": "Shown when `BookingFlowConfig.ticketCategories` is `categoryThenSubcategory` (the default): the category tiles (name, image) first, then that category's products through `listProducts?categoryId=`. `flatList` skips the tiles. Tiles lay out as a grid or one scrolling row per `BookingFlowConfig.cardLayout` (W7).",
       "operation": "listProductCategories",
       "provenance": "decided 29 September, rev 3 REV3-16, 23SEP-18"
      },
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
       "label": "Every performance",
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
       "operation": "listPerformances",
       "provenance": "contract catalogue.yaml GET /events/{eventId}/performances"
      },
      {
       "kind": "dataTable",
       "label": "Every money",
       "bindsTo": "Money",
       "columns": [
        "Money.amount",
        "Money.currency",
        "Money.scale"
       ],
       "operation": "searchCatalogue",
       "provenance": "contract catalogue.yaml GET /search"
      },
      {
       "kind": "searchField",
       "label": "Search events and attractions",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "multiSelect",
       "label": "Category",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "datePicker",
       "label": "Date",
       "notes": "Format from region settings, not a locale guess",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "cardList",
       "bindsTo": "Product[]",
       "notes": "Cursor pagination. Infinite scroll with an explicit load-more fallback",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "banner",
       "label": "Help me choose",
       "operation": "getPublishedGuidedChoice",
       "notes": "**The answers filter the list** (W4): sent as `guidedAnswerIds` to `listProducts` (and `searchCatalogue`), so web, app and kiosk filter the same way on the server.",
       "provenance": "decided 29 September 2026, W4"
      },
      {
       "kind": "secondaryButton",
       "label": "Show everything",
       "operation": "listProducts",
       "notes": "Clears the Help me choose filter (W4).",
       "provenance": "decided 29 September 2026, W4"
      },
      {
       "kind": "cardList",
       "label": "Contact sales",
       "bindsTo": "Product.salesContact",
       "operation": "listProducts",
       "notes": "**View-only products** (W3): Call sales / Email sales from `Product.salesContact` instead of Book.",
       "provenance": "decided 29 September 2026, W3"
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
        "Product.categoryId",
        "Product.lifecycleState",
        "Product.isSellable",
        "Product.isStockTracked"
       ],
       "operation": "listProducts",
       "provenance": "contract catalogue.yaml GET /products"
      },
      {
       "kind": "detailPanel",
       "label": "The wait time",
       "bindsTo": "WaitTime",
       "columns": [
        "WaitTime.queueId",
        "WaitTime.queueName",
        "WaitTime.attractionProductId",
        "WaitTime.attractionCategoryId",
        "WaitTime.status",
        "WaitTime.waitMinutes",
        "WaitTime.source",
        "WaitTime.isStale",
        "WaitTime.heightRequirementCm",
        "WaitTime.zone",
        "WaitTime.asOf"
       ],
       "operation": "getWaitTimes",
       "provenance": "contract queue.yaml GET /queues/wait-times"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The event attraction listing list.",
   "error": "Could not load. Names which read failed and leaves the event attraction listing untouched.",
   "emptyFirstRun": "No event attraction listing yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table.",
   "emptyNoResults": "Nothing matches the filter on venueId, kind, isSellable and the event attraction listing are still there. Names the active filter and offers to clear it.",
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
    "operationId": "listPerformances",
    "contract": "catalogue",
    "purpose": "List performances of an event",
    "trigger": "onLoad"
   },
   {
    "operationId": "searchCatalogue",
    "contract": "catalogue",
    "purpose": "Find something by name",
    "trigger": "onAction"
   },
   {
    "operationId": "getWaitTimes",
    "contract": "queue",
    "purpose": "Wait times across a venue",
    "trigger": "onLoad"
   },
   {
    "operationId": "listProductCategories",
    "contract": "catalogue",
    "purpose": "The category tiles (a tree: parentId, displayOrder, image)",
    "trigger": "onLoad"
   },
   {
    "operationId": "getPublishedGuidedChoice",
    "contract": "white-label",
    "purpose": "Help me choose: the questions whose answers filter this list (W4)",
    "trigger": "onLoad",
    "provenance": "decided 29 September 2026, W4"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "eventId",
     "from": "deepLink"
    },
    {
     "name": "venueId",
     "from": "session"
    }
   ],
   "coldEntry": "**A guest arriving cold on a link that no longer resolves is shown what happened and one way onward — never a 404.** A shared ticket, a forwarded confirmation and a push notification opened three weeks late all land here, and the person holding the link did nothing wrong. **The screen names the thing, says it is expired, cancelled or withdrawn, and offers the list it came from.** Arrives with `eventId`.",
   "preloaded": [
    "WaitTime.queueId",
    "WaitTime.queueName",
    "WaitTime.attractionProductId",
    "WaitTime.status",
    "WaitTime.waitMinutes"
   ]
  },
  "wireframe": {
   "status": "review",
   "provenance": "client-verified",
   "board": "wireframes/P01 Guest Web.dc.html#web-002",
   "prototype": {
    "file": "sources/designs/guest-rev3-29-september/TICVAI Guest Booking v2.dc.html",
    "rev": "rev 3 (29 September build)",
    "verified": "2026-09-29",
    "match": "exact",
    "view": "Header 'What's on'"
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
  "id": "WEB-003",
  "name": "Search Results",
  "module": "Discovery & Browse",
  "requiresModule": "ticketing",
  "wave": 1,
  "capability": "C79",
  "implementation": {
   "app": "guest-web",
   "route": "/discovery-and-browse/search-results",
   "component": "apps/guest-web/src/routes/discovery-and-browse/SearchResultsList.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "WEB-001"
   ],
   "exitTo": [
    "WEB-001",
    "WEB-002",
    "WEB-004"
   ],
   "inferred": true,
   "transitions": [
    {
     "to": "WEB-002",
     "trigger": "Event & Attraction Listing",
     "provenance": "derived — WEB-002 declares entryState.params eventId and WEB-003 holds none of them. The edge carries nothing: eventId only pre-selects (deep link or optional), and WEB-002 opens on its own"
    },
    {
     "to": "WEB-004",
     "trigger": "Attraction Details",
     "carries": [
      "productId"
     ],
     "provenance": "derived — WEB-004 declares entryState.params eventId, productId and WEB-003 holds productId, so an edge into it carries them"
    }
   ]
  },
  "notes": "Purpose derived from the screen name and its operations on 17 August, not from a requirement.\n\n**Rev 3 (decided 29 September, rev 3 REV3-14).** `searchCatalogue` now also returns info-only products, flagged (`guestListing` `infoOnly`): the result shows `notBookableLabel` (default *Info only / Not bookable online*) and opens the details (WEB-004), never Add to basket. Hidden when `BookingFlowConfig.showInfoOnly` is off. Each result shows its own primary image (23SEP-4).",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`searchCatalogue` reads a population and nothing reads one of them; the detail is the row until a `get` exists",
  "purpose": "Find something when the guest does not know what it is called.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "searchField",
       "label": "Q",
       "operation": "searchCatalogue",
       "notes": "Sends `?q=` to `searchCatalogue`.",
       "provenance": "contract catalogue.yaml GET /search"
      },
      {
       "kind": "textField",
       "label": "Venue id",
       "operation": "searchCatalogue",
       "notes": "Sends `?venueId=` to `searchCatalogue`.",
       "provenance": "contract catalogue.yaml GET /search"
      },
      {
       "kind": "selectField",
       "label": "Kind",
       "operation": "searchCatalogue",
       "notes": "Sends `?kind=` to `searchCatalogue`.",
       "provenance": "contract catalogue.yaml GET /search"
      },
      {
       "kind": "dataTable",
       "label": "Every money",
       "bindsTo": "Money",
       "columns": [
        "Money.amount",
        "Money.currency",
        "Money.scale"
       ],
       "operation": "searchCatalogue",
       "provenance": "contract catalogue.yaml GET /search"
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
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected money",
       "bindsTo": "Money",
       "columns": [
        "Money.amount",
        "Money.currency",
        "Money.scale"
       ],
       "operation": "searchCatalogue",
       "provenance": "contract catalogue.yaml GET /search"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The search results list.",
   "error": "Could not load. Names which read failed and leaves the search results untouched.",
   "emptyFirstRun": "No search results yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table.",
   "emptyNoResults": "Nothing matches the filter on q, venueId, kind and the search results are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "**There is no permission to name — a guest holds none** (ADR-0025: `x-ticvai-permission` is what a staff caller must hold; a guest call resolves to the guest's own data). No access here means one of two things, told apart by the response: not signed in, where the guest is offered sign-in and brought back to this screen, or a record that is not theirs, which says so without saying whose it is. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "**The offline banner shows.** Results come only from what was already loaded, with a note that newer items may exist."
  },
  "apis": [
   {
    "operationId": "searchCatalogue",
    "contract": "catalogue",
    "purpose": "Find something by name",
    "trigger": "onAction"
   },
   {
    "operationId": "listProducts",
    "contract": "catalogue",
    "purpose": "List products",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "Money.amount",
    "Money.currency",
    "Money.scale"
   ]
  },
  "wireframe": {
   "status": "review",
   "provenance": "client-verified",
   "board": "wireframes/P01 Guest Web.dc.html#web-003",
   "prototype": {
    "file": "sources/designs/guest-rev3-28-september/TICVAI Guest Booking v2.dc.html",
    "rev": "rev 3",
    "verified": "2026-09-28",
    "match": "partial",
    "view": "Discover → search box in the hero (opens the search panel) → Enter lands on What's on filtered by the query",
    "differences": "No separate results page: results render as a type-ahead overlay and then in the WEB-002 listing with the query applied. Recent and popular searches are prototype additions not in the YAML."
   }
  },
  "apisNote": "Rebuilt 9 September 2026 from the 2 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
  "id": "WEB-004",
  "name": "Attraction Details",
  "module": "Discovery & Browse",
  "requiresModule": "ticketing",
  "wave": 1,
  "capability": "C79",
  "implementation": {
   "app": "guest-web",
   "route": "/discovery-and-browse/event-attraction-detail",
   "component": "apps/guest-web/src/routes/discovery-and-browse/EventAttractionDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "WEB-001",
    "WEB-002",
    "WEB-003",
    "WEB-047",
    "WEB-048"
   ],
   "exitTo": [
    "WEB-001",
    "WEB-002",
    "WEB-003",
    "WEB-005",
    "WEB-006",
    "WEB-007",
    "WEB-047",
    "WEB-048"
   ],
   "transitions": [
    {
     "to": "WEB-002",
     "trigger": "Event & Attraction Listing",
     "carries": [
      "eventId"
     ],
     "provenance": "derived — WEB-002 declares entryState.params eventId and WEB-004 holds eventId, so an edge into it carries them"
    },
    {
     "to": "WEB-005",
     "trigger": "Chooses ticket types and quantities",
     "provenance": "flow F01 step 2→3",
     "carries": [
      "productId"
     ]
    },
    {
     "to": "WEB-006",
     "trigger": "Book (a dated product: date first, then time, then tickets)",
     "carries": [
      "productId"
     ],
     "provenance": "decided 29 September, rev 3 REV3-2: the dated flow runs date → time → ticket; flow F01 step 2→3"
    },
    {
     "to": "WEB-007",
     "trigger": "Book (a fixture with one on-sale performance opens straight on the seat map)",
     "carries": [
      "performanceId"
     ],
     "provenance": "decided 29 September, rev 3 23SEP-16 and REV3-4: WEB-006 is skipped when the event has exactly one on-sale performance"
    },
    {
     "to": "WEB-047",
     "trigger": "Book (a cabana, lounger or other spot placed on the venue map)",
     "carries": [
      "productId"
     ],
     "provenance": "decided 29 September, rev 3 REV3-15 and GAP-C2"
    },
    {
     "to": "WEB-048",
     "trigger": "Book (a space sold by the hour, e.g. a meeting room)",
     "carries": [
      "productId"
     ],
     "provenance": "decided 29 September, rev 3 REV3-13"
    }
   ]
  },
  "notes": "**Renamed 31 August** from *Event / Attraction Detail*. **A guest surface is one product with two renderings** — a screen named differently on web and app is two screens to a developer and one journey to a guest. **Cross-surface parity, 31 August**: added getAvailability, getWaitTimes. **A guest does not know which surface they are on** — the same named screen on web and app now calls the same guest-callable operations.\n\n**Rev 3 (decided 29 September).** Ticket tags from `Product.displayTags` when `BookingFlowConfig.ticketTags` is on (23SEP-3); Read more opens on the product's own video or photo (`Product.media`, 23SEP-4). An info-only product shows its `notBookableLabel` and no Book button (REV3-14). **Book** opens the ticket counters as a side panel here (23SEP-5); a dated product goes to the date and time first (WEB-006, REV3-2); a fixture with a single on-sale performance opens straight on the seat map with the fixture as a strip at its top (WEB-007, 23SEP-16, REV3-4); a product placed on a venue map opens the map booking (WEB-047, REV3-15); a product sold by the hour opens the space booking (WEB-048, REV3-13). The event banner lists dates only when `BookingFlowConfig.eventBannerDates` is on (default off, 23SEP-19). Help me choose sits on the booking step (WEB-005), where the prototype draws it, not here (REV3-11).\n\n**29 September.** W3: view-only products show Call sales / Email sales instead of Book. M18-13: in single-event mode, a banner or video hero and only the next seven days, with a calendar for later dates (M17-08).\n\n**Video plays directly (client meeting 30 September, MoM 4.8, Qossai; the same page as the app's GST-004, so the same behaviour).** The ride or attraction video starts in place with no loader in front of it; its poster frame shows while it buffers, and a video that cannot play leaves the poster and the details, never an error screen.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listPerformances` reads the population and `getProduct` reads one of them — list, select, act",
  "purpose": "Decide whether to book this.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "datePicker",
       "label": "From",
       "operation": "listPerformances",
       "notes": "Sends `?from=` to `listPerformances`.",
       "provenance": "contract catalogue.yaml GET /events/{eventId}/performances"
      },
      {
       "kind": "datePicker",
       "label": "To",
       "operation": "listPerformances",
       "notes": "Sends `?to=` to `listPerformances`.",
       "provenance": "contract catalogue.yaml GET /events/{eventId}/performances"
      },
      {
       "kind": "dataTable",
       "label": "Every performance",
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
       "operation": "listPerformances",
       "provenance": "contract catalogue.yaml GET /events/{eventId}/performances"
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
       "kind": "banner",
       "bindsTo": "Product.lifecycleState",
       "notes": "Shown only when withdrawn — reachable via a stale link but no longer sellable. A silent 404 on a shared link is a bad guest experience",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "cardList",
       "label": "Ticket tags",
       "bindsTo": "Product.displayTags",
       "notes": "Up to six tags (clock, height, free, calendar, id) with an icon by kind, e.g. *2 Hours*, *Min 1.10 m*, *Valid 90 days*. Where the product has none, derived on read from duration, validity and the height rule. Shown only when `BookingFlowConfig.ticketTags` is on (default on).",
       "operation": "getProduct",
       "provenance": "decided 29 September, rev 3 23SEP-3"
      },
      {
       "kind": "detailPanel",
       "label": "Photo and video",
       "bindsTo": "Product.media",
       "notes": "**The video plays directly, with no loader in front of it** (client meeting 30 September, MoM 4.8): the info button reveals the details and starts the primary video in place; the poster frame (the primary image, or the video's first frame) shows while it buffers, never a spinner or loading screen. Read more opens on the primary video or photo (`Product.media`, `isPrimary`).",
       "operation": "getProduct",
       "provenance": "decided 29 September, rev 3 23SEP-4; decided 30 September 2026, client meeting MoM 4.8 (Qossai)"
      },
      {
       "kind": "secondaryButton",
       "label": "Call sales / Email sales",
       "bindsTo": "Product.salesContact",
       "operation": "getProduct",
       "notes": "**View-only product** (W3): no Book; the sales contact from `Product.salesContact` (phone, email, note; the venue contact when absent).",
       "provenance": "decided 29 September 2026, W3"
      },
      {
       "kind": "datePicker",
       "label": "Next 7 days",
       "operation": "listPerformances",
       "notes": "**Single-event page** (M18-13): banner or video hero, a brief description, and a date strip of the next `dateStripDays` days (default 7) with a calendar icon for later dates (M17-08).",
       "provenance": "decided 29 September 2026, M18-13, M17-08"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected performance",
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
       "operation": "listPerformances",
       "provenance": "contract catalogue.yaml GET /events/{eventId}/performances"
      },
      {
       "kind": "detailPanel",
       "label": "The product eligibility rule",
       "bindsTo": "ProductEligibilityRule",
       "columns": [
        "ProductEligibilityRule.id",
        "ProductEligibilityRule.productId",
        "ProductEligibilityRule.minAgeYears",
        "ProductEligibilityRule.maxAgeYears",
        "ProductEligibilityRule.minHeightCm",
        "ProductEligibilityRule.maxHeightCm",
        "ProductEligibilityRule.heightBandsCm",
        "ProductEligibilityRule.accompaniedBelowAge",
        "ProductEligibilityRule.guardianSignatureAgeFrom",
        "ProductEligibilityRule.guardianSignatureAgeTo",
        "ProductEligibilityRule.waiverRequired",
        "ProductEligibilityRule.swimAbility",
        "ProductEligibilityRule.refundableIfIneligibleAtGate",
        "ProductEligibilityRule.scopePath"
       ],
       "operation": "getProductEligibilityRule",
       "provenance": "contract catalogue.yaml GET /products/{productId}/eligibility-rule"
      },
      {
       "kind": "detailPanel",
       "label": "The wait time",
       "bindsTo": "WaitTime",
       "columns": [
        "WaitTime.queueId",
        "WaitTime.queueName",
        "WaitTime.attractionProductId",
        "WaitTime.attractionCategoryId",
        "WaitTime.status",
        "WaitTime.waitMinutes",
        "WaitTime.source",
        "WaitTime.isStale",
        "WaitTime.heightRequirementCm",
        "WaitTime.zone",
        "WaitTime.asOf"
       ],
       "operation": "getWaitTimes",
       "provenance": "contract queue.yaml GET /queues/wait-times"
      },
      {
       "kind": "detailPanel",
       "label": "The product",
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
        "Product.categoryId",
        "Product.lifecycleState",
        "Product.isSellable",
        "Product.isStockTracked"
       ],
       "operation": "getProduct",
       "provenance": "contract catalogue.yaml GET /products/{productId}"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "carried",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Select tickets",
       "notes": "Disabled with a stated reason when not sellable",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "**The video is not part of loading** (client meeting 30 September, MoM 4.8): the attraction renders as it arrives and no loader or loading screen is ever drawn over the video.",
   "videoBuffering": "**Poster frame, not a loader** (client meeting 30 September, MoM 4.8): until the first frames arrive the poster (primary image, else the video's first frame) fills the video area and playback starts in place as soon as it can; no spinner, overlay or blocking screen. The details beside it stay usable throughout.",
   "videoUnavailable": "The video cannot play (no video, a failed stream, data saver on). The poster stays and the details are unaffected; no error screen and no loader.",
   "error": "Could not load. Names which read failed and leaves the attraction untouched.",
   "emptyFirstRun": "No attraction yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table.",
   "emptyNoResults": "Nothing matches the filter on from, to and the attraction are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "**There is no permission to name — a guest holds none** (ADR-0025: `x-ticvai-permission` is what a staff caller must hold; a guest call resolves to the guest's own data). No access here means one of two things, told apart by the response: not signed in, where the guest is offered sign-in and brought back to this screen, or a record that is not theirs, which says so without saying whose it is. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "**The offline banner shows.** What was already loaded stays on screen, marked with its age. Anything that spends money, holds capacity or changes the account waits for the connection, and its button says so rather than failing."
  },
  "apis": [
   {
    "operationId": "getProductEligibilityRule",
    "contract": "catalogue",
    "purpose": "Age and height limits",
    "trigger": "onLoad"
   },
   {
    "operationId": "getProduct",
    "contract": "catalogue",
    "purpose": "Read a product",
    "trigger": "onLoad"
   },
   {
    "operationId": "listPerformances",
    "contract": "catalogue",
    "purpose": "List performances of an event",
    "trigger": "onLoad"
   },
   {
    "operationId": "getAvailability",
    "contract": "catalogue",
    "purpose": "Live remaining capacity",
    "trigger": "onLoad"
   },
   {
    "operationId": "getWaitTimes",
    "contract": "queue",
    "purpose": "Wait times across a venue",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "eventId",
     "from": "WEB-002"
    },
    {
     "name": "productId",
     "from": "WEB-001"
    }
   ],
   "coldEntry": "Resolves from the session; a cold arrival is the ordinary case.",
   "preloaded": [
    "Performance.id",
    "Performance.eventId",
    "Performance.startsAt",
    "Performance.endsAt",
    "Performance.approvalRequestId"
   ]
  },
  "wireframe": {
   "status": "review",
   "provenance": "client-verified",
   "board": "wireframes/P01 Guest Web.dc.html#web-004",
   "prototype": {
    "file": "sources/designs/guest-rev3-29-september/TICVAI Guest Booking v2.dc.html",
    "rev": "rev 3 (29 September build)",
    "verified": "2026-09-29",
    "match": "partial",
    "view": "Config → Marketing layer → 'Single-event page' on, then Book; or any product card → 'Read more' dialog; or a listing card's preview aside",
    "differences": "No standing attraction-detail page in the default flow: details are a banner above the booking step (behind a Config toggle), a pop-up per product, or the listing preview. Eligibility rule display (getProductEligibilityRule) appears only as tags. Prototype labels it WEB-003b, not WEB-004."
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
  "id": "WEB-050",
  "name": "Plan Your Visit",
  "module": "Discovery & Browse",
  "requiresModule": "ticketing",
  "wave": 1,
  "capability": "AI-35",
  "implementation": {
   "app": "guest-web",
   "route": "/plan-your-visit",
   "component": "apps/guest-web/src/routes/PlanYourVisit.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "inferred": false,
   "entryFrom": [
    "WEB-001"
   ],
   "exitTo": [
    "WEB-010",
    "WEB-001",
    "WEB-004"
   ],
   "transitions": [
    {
     "to": "WEB-010",
     "trigger": "Book this plan",
     "operation": "bookVisitPlan",
     "carries": [
      "cartId"
     ],
     "onFailure": [
      {
       "when": "an item sold out since the plan was made",
       "to": "WEB-050",
       "note": "Names it and offers a swap; the rest of the plan is kept."
      }
     ],
     "provenance": "decided 29 September 2026, MOB-6; web build: Book this plan goes straight into booking"
    },
    {
     "to": "WEB-004",
     "trigger": "Opens an item on the plan",
     "carries": [
      "productId"
     ],
     "provenance": "decided 29 September 2026, MOB-6"
    },
    {
     "to": "WEB-001",
     "trigger": "Back to tickets",
     "provenance": "decided 29 September 2026, MOB-6"
    }
   ]
  },
  "notes": "**Added 29 September**: the 29 September web build has *Plan your visit* in the header, opening the planner full screen, and *Book this plan* goes straight into booking. The web twin of the Plan tab (GST-051 questions, GST-053 plan), binding the same planner operations (venue-map `generateVisitPlan`, `getVisitPlan`, `updateVisitPlan`, `listVisitPlanAlternatives`, `bookVisitPlan`). Block A (29 September re-plan, superseding R187 and GAP-C3). Rules-based; the AI planner chat is app-only for now. Hidden when the venue turns module `visitPlanner` off.\n\n**Multi-venue intelligence (client meeting 30 September, MoM 4.7, Allam).** As on the app: each day is at one park and uses only that park's rides, dining and retail (shops and kiosks, added beside F&B); a preference the park cannot meet is said, never filled from another park.",
  "density": "compact",
  "pattern": "multiStepForm",
  "patternReason": "The Visit Planner prototype: six questions, then the plan with Book this plan",
  "purpose": "Plan a visit on the website: answer six questions, get a day-by-day plan, edit it, and book it in one go.",
  "layout": {
   "template": "fullscreen",
   "regions": [
    {
     "name": "progress",
     "slot": "progress",
     "components": [
      {
       "kind": "progressIndicator",
       "label": "Plan your visit · n of 6",
       "notes": "Who, heights (skipped with no children), days (up to 3), pace, interests, lunch.",
       "provenance": "decided 29 September 2026, MOB-6; Visit Planner prototype"
      }
     ]
    },
    {
     "name": "fields",
     "slot": "fields",
     "components": [
      {
       "kind": "numberField",
       "label": "Adults and children",
       "notes": "Adults 1-8 (12+), children 0-8 (3-11).",
       "provenance": "decided 29 September 2026, MOB-6"
      },
      {
       "kind": "selectField",
       "label": "How tall are the children?",
       "operation": "listProducts",
       "notes": "Per child; rides over the limit are left out (`ProductEligibilityRule`).",
       "provenance": "decided 29 September 2026, MOB-6"
      },
      {
       "kind": "multiSelect",
       "label": "Which days are you visiting?",
       "notes": "Up to three.",
       "provenance": "decided 29 September 2026, MOB-6"
      },
      {
       "kind": "selectField",
       "label": "Which park each day?",
       "bindsTo": "TenantAppStatus.venues",
       "operation": "getTenantAppStatus",
       "notes": "**Only in a multi-venue tenant**; hidden otherwise. One choice per chosen day, defaulting to the venue picked in the header; sent as `VisitPlanRequest.dayVenues`. Each day is then planned from that park's own rides, dining and shops only (client meeting 30 September, MoM 4.7).",
       "provenance": "decided 30 September 2026, client meeting MoM 4.7 (Allam)"
      },
      {
       "kind": "selectField",
       "label": "How busy should each day be?",
       "notes": "Packed, Balanced or Relaxed.",
       "provenance": "decided 29 September 2026, MOB-6"
      },
      {
       "kind": "multiSelect",
       "label": "What are you most interested in?",
       "operation": "listProducts",
       "notes": "Interest tags of the venue.",
       "provenance": "decided 29 September 2026, MOB-6"
      },
      {
       "kind": "multiSelect",
       "label": "Any shops you'd like to visit?",
       "notes": "Shown when Shopping is chosen (client meeting 30 September, MoM 4.7: retail and kiosk shops join F&B in the planner). The `retailTags` of the chosen parks' shops and retail kiosks; sent as `VisitPlanRequest.retailTags`.",
       "provenance": "decided 30 September 2026, client meeting MoM 4.7 (Allam)"
      },
      {
       "kind": "selectField",
       "label": "What would you like for lunch?",
       "notes": "Cuisines of the chosen parks' dining points only (restaurants, cafes, food kiosks; client meeting 30 September, MoM 4.7). In a multi-venue plan each cuisine names the park(s) that serve it, and lunch is planned only at a restaurant of that day's park.",
       "provenance": "decided 29 September 2026, MOB-6; decided 30 September 2026, client meeting MoM 4.7 (Allam)"
      },
      {
       "kind": "primaryButton",
       "label": "Make my plan",
       "operation": "generateVisitPlan",
       "notes": "Runs the rules planner.",
       "provenance": "decided 29 September 2026, MOB-6"
      }
     ]
    },
    {
     "name": "review",
     "slot": "review",
     "components": [
      {
       "kind": "timeline",
       "label": "Your plan",
       "bindsTo": "VisitPlanItem",
       "operation": "getVisitPlan",
       "notes": "Day tabs, each naming its park (`VisitPlan.days[].venueId`); arrival, timed items, lunch and shop or kiosk stops, every one at that day's park (`VisitPlanItem.venueId`; client meeting 30 September, MoM 4.7).",
       "provenance": "decided 29 September 2026, MOB-6; decided 30 September 2026, client meeting MoM 4.7 (Allam)"
      },
      {
       "kind": "banner",
       "label": "Not at this park",
       "bindsTo": "VisitPlan.unmatchedPreferences",
       "operation": "getVisitPlan",
       "notes": "Per day, a cuisine or shop the day's park cannot offer, and the park that can (from `availableAtVenueIds`), e.g. *No Indian restaurant at Summit Peaks. Indian food is at Aqua Park (day 2).* Hidden when every preference is met (client meeting 30 September, MoM 4.7).",
       "provenance": "decided 30 September 2026, client meeting MoM 4.7 (Allam)"
      },
      {
       "kind": "secondaryButton",
       "label": "Swap / + Add something",
       "operation": "listVisitPlanAlternatives",
       "notes": "Candidates that suit everyone in the group, from the day's park only (client meeting 30 September, MoM 4.7).",
       "provenance": "decided 29 September 2026, MOB-6"
      },
      {
       "kind": "secondaryButton",
       "label": "Remove / Undo changes",
       "operation": "updateVisitPlan",
       "notes": "Each change is a new version.",
       "provenance": "decided 29 September 2026, MOB-6"
      },
      {
       "kind": "toggle",
       "label": "Add Fast Track",
       "operation": "updateVisitPlan",
       "notes": "Per guest, with the queuing time saved.",
       "provenance": "decided 29 September 2026, MOB-6"
      },
      {
       "kind": "detailPanel",
       "label": "Estimated total",
       "operation": "getVisitPlan",
       "notes": "Estimate for the group; confirmed in booking.",
       "provenance": "decided 29 September 2026, MOB-6"
      }
     ]
    },
    {
     "name": "submit",
     "slot": "submit",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Book this plan",
       "operation": "bookVisitPlan",
       "notes": "Cart lines from the plan; opens the cart.",
       "provenance": "decided 29 September 2026, MOB-6"
      },
      {
       "kind": "secondaryButton",
       "label": "Change answers",
       "notes": "Back to the questions.",
       "provenance": "decided 29 September 2026, MOB-6"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The plan builds in place; the answers stay on screen.",
   "error": "Could not build or load the plan. Names what failed; the answers are kept.",
   "emptyFirstRun": "No plan yet: the first question is shown.",
   "emptyNoResults": "Nothing suits the whole group on that day: says which answer ruled everything out and offers to change it.",
   "preferenceNotAtVenue": "**A preference a day's park cannot meet** (client meeting 30 September, MoM 4.7): before *Make my plan* the chip is marked *Not at the parks you chose* (naming a park of the tenant that has it); after it, the day shows the *Not at this park* banner and nothing from another park is placed. *Change answers* lets the guest move that day to the park that has it.",
   "emptyNoAccess": "A guest holds no permission. Anyone can build a plan; signing in is asked only to save it, and booking follows the cart's own sign-in gate.",
   "offline": "**The offline banner shows.** What was already loaded stays on screen, marked with its age. Anything that spends money, holds capacity or changes the account waits for the connection, and its button says so rather than failing."
  },
  "apis": [
   {
    "operationId": "listProducts",
    "contract": "catalogue",
    "purpose": "Interests and height limits of what the planner may include",
    "trigger": "onLoad",
    "provenance": "decided 29 September 2026, MOB-6"
   },
   {
    "operationId": "generateVisitPlan",
    "contract": "venue-map",
    "purpose": "Build a rules plan from the inputs (party, heights, dates, park per day, pace, interests, shops, cuisine); each day from its own park's points only",
    "trigger": "onAction",
    "provenance": "decided 29 September 2026, MOB-6; decided 30 September 2026, client meeting MoM 4.7 (Allam)"
   },
   {
    "operationId": "getVisitPlan",
    "contract": "venue-map",
    "purpose": "The plan: days, timed items and add-on suggestions, at its current version",
    "trigger": "onLoad",
    "provenance": "decided 29 September 2026, MOB-6"
   },
   {
    "operationId": "updateVisitPlan",
    "contract": "venue-map",
    "purpose": "Swap, remove, add or undo: each change is a new version, so undo goes back one",
    "trigger": "onAction",
    "provenance": "decided 29 September 2026, MOB-6"
   },
   {
    "operationId": "listVisitPlanAlternatives",
    "contract": "venue-map",
    "purpose": "Swap candidates for one item that suit everyone in the party",
    "trigger": "onAction",
    "provenance": "decided 29 September 2026, MOB-6"
   },
   {
    "operationId": "bookVisitPlan",
    "contract": "venue-map",
    "purpose": "Book this plan: turns the plan (and chosen add-ons) into cart lines and returns the cart",
    "trigger": "onAction",
    "provenance": "decided 29 September 2026, MOB-6"
   },
   {
    "operationId": "getTenantAppStatus",
    "contract": "white-label",
    "purpose": "The tenant's active venues, for the park-per-day choice in a multi-venue tenant",
    "trigger": "onLoad",
    "provenance": "decided 30 September 2026, client meeting MoM 4.7 (Allam)"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "venueId",
     "from": "session"
    },
    {
     "name": "planId",
     "from": "deepLink",
     "optional": true
    },
    {
     "name": "itemId",
     "from": "navigation",
     "optional": true
    }
   ],
   "coldEntry": "Starts at the first question; a saved-plan link opens the plan, or says it has passed and offers to plan again. `itemId` is the plan item the guest taps Swap on, picked on this screen."
  },
  "wireframe": {
   "status": "review",
   "provenance": "client-verified",
   "board": "wireframes/P01 Guest Web.dc.html#web-050",
   "prototype": {
    "file": "sources/designs/guest-rev3-30-september/TICVAI Visit Planner.dc.html",
    "rev": "Visit Planner (30 September build)",
    "verified": "2026-10-01",
    "match": "exact",
    "view": "Visit Planner → the six questions (defaults) → Make my plan (Your plan)",
    "differences": "Single-park planner: no \"Which park each day?\" step, no shops or kiosks as plan stops and no preferenceNotAtVenue (MoM 4.7, 30 September); these are pending in design: specified, and built from the definition until the design shows it (handoff/design-batches/apps/1-guest-app/README.md)."
   }
  },
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
 "bookVisitPlan": {
  "method": "POST",
  "path": "/visit-plans/{planId}/booking",
  "contract": "venue-map",
  "summary": "Book this plan — turn it into cart lines",
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
  "responds": "VisitPlanBooking"
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
 "generateVisitPlan": {
  "method": "POST",
  "path": "/visit-plans",
  "contract": "venue-map",
  "summary": "Build a visit plan from the party, the dates and what they like",
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
  "requestBody": "VisitPlanRequest",
  "responds": "VisitPlan"
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
 "getProductEligibilityRule": {
  "method": "GET",
  "path": "/products/{productId}/eligibility-rule",
  "contract": "catalogue",
  "summary": "Who may take part: age, height, supervision",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "productId",
    "in": "path",
    "required": true
   }
  ],
  "requestBody": null,
  "responds": "ProductEligibilityRule"
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
 "getTenantConfig": {
  "method": "GET",
  "path": "/tenant-config",
  "contract": "white-label",
  "summary": "Full working configuration",
  "permission": "TENANT_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "version",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "TenantConfig"
 },
 "getVisitPlan": {
  "method": "GET",
  "path": "/visit-plans/{planId}",
  "contract": "venue-map",
  "summary": "A visit plan, at its current version or an earlier one",
  "permission": null,
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "version",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "VisitPlan"
 },
 "getWaitTimes": {
  "method": "GET",
  "path": "/queues/wait-times",
  "contract": "queue",
  "summary": "Wait times across a venue",
  "permission": null,
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
    "name": "category",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "WaitTime"
 },
 "listAnalyticsProviders": {
  "method": "GET",
  "path": "/tenant-config/analytics-providers",
  "contract": "white-label",
  "summary": "The analytics platforms the storefront and app report to",
  "permission": "TENANT_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "venueId",
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
 "listMyEntitlements": {
  "method": "GET",
  "path": "/guests/me/entitlements",
  "contract": "access",
  "summary": "Every ticket, pass and membership this guest holds",
  "permission": "ORDER_VIEW",
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
    "name": "state",
    "in": "query",
    "required": null
   },
   {
    "name": "includeShared",
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
 "listVisitPlanAlternatives": {
  "method": "GET",
  "path": "/visit-plans/{planId}/items/{itemId}/alternatives",
  "contract": "venue-map",
  "summary": "What could take this item's place",
  "permission": null,
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
 "recordStorefrontSessionEvents": {
  "method": "POST",
  "path": "/storefront/session-events",
  "contract": "white-label",
  "summary": "Report a batch of browsing behaviour for fraud prevention, hashed and without personal data",
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
  "requestBody": "WhiteLabelStorefrontSessionBatch",
  "responds": null
 },
 "searchCatalogue": {
  "method": "GET",
  "path": "/search",
  "contract": "catalogue",
  "summary": "Find something by name",
  "permission": null,
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "q",
    "in": "query",
    "required": true
   },
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
    "name": "guidedAnswerIds",
    "in": "query",
    "required": null
   },
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": null
 },
 "updateVisitPlan": {
  "method": "PUT",
  "path": "/visit-plans/{planId}",
  "contract": "venue-map",
  "summary": "Swap, remove, add, move or undo, as a new version",
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
  "requestBody": "VisitPlanUpdate",
  "responds": "VisitPlan"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "AccessibilitySettings": {
  "type": "object",
  "description": "BL-065, 2.1.27. **POS and kiosk accessibility, which is a legal obligation in most jurisdictions and was unstated.**\n**A kiosk is the hard case.** A guest with low vision using a website brings their own assistive technology; a guest at a kiosk gets whatever the kiosk offers, so the settings have to be on the device rather than in the browser.\n",
  "properties": {
   "largeTextAvailable": {
    "type": "boolean",
    "default": true
   },
   "highContrastAvailable": {
    "type": "boolean",
    "default": true
   },
   "simplifiedNavigationAvailable": {
    "type": "boolean",
    "default": true
   },
   "screenReaderSupported": {
    "type": "boolean",
    "default": true
   },
   "reachableHeightModeAvailable": {
    "type": "boolean",
    "default": false,
    "description": "**Moves the interface to the lower half of the screen** for a guest using a wheelchair. A kiosk mounted at standing height is unusable otherwise, and no software setting fixes the mounting — this is the mitigation.\n"
   },
   "sessionTimeoutMultiplier": {
    "type": "number",
    "default": 1,
    "description": "**Timeouts are an accessibility barrier nobody counts.** A guest who needs three times as long to read a screen should not lose their basket to a 90-second inactivity timer.\n"
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
 "AppIcons": {
  "x-ticvai-persistence": "none — embedded in tenant_config",
  "type": "object",
  "required": [
   "sourceAssetRef",
   "changeScope"
  ],
  "properties": {
   "sourceAssetRef": {
    "type": "string",
    "format": "uuid",
    "description": "The `MediaAsset` id of the 1024×1024 source."
   },
   "derived": {
    "type": "array",
    "readOnly": true,
    "x-ticvai-derived": "onWrite",
    "description": "Generated by `setAppIcons` from the source, one entry per platform and size — the iOS and Android store sets and the web favicons listed on `setAppIcons` (audit R163).",
    "items": {
     "type": "object",
     "properties": {
      "platform": {
       "type": "string",
       "enum": [
        "ios",
        "android",
        "web"
       ]
      },
      "size": {
       "type": "string"
      },
      "assetRef": {
       "type": "string",
       "format": "uuid"
      }
     }
    }
   },
   "changeScope": {
    "allOf": [
     {
      "$ref": "#/components/schemas/ChangeScope"
     }
    ],
    "readOnly": true,
    "description": "Always `buildTime` — icons are baked into the binary."
   },
   "liveVersion": {
    "type": "string",
    "nullable": true,
    "readOnly": true,
    "description": "Icon currently shipped. Differs from the draft until the next release."
   },
   "requiresRebuild": {
    "type": "boolean",
    "readOnly": true,
    "x-ticvai-derived": "onRead",
    "description": "True while the draft's source differs from the icon in `liveVersion`."
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
 "BookingFlowConfig": {
  "x-ticvai-persistence": "none — embedded in tenant_config",
  "description": "**Set per tenant, with a per-venue override (decided 29 September, rev 3 CFG-11).** One tenant with several venues (the Kids Club branches, Coastal Aqua beside Union Arena) needs them to differ. The settings in force at a venue are the tenant's, with that venue's entry in `venueOverrides` laid over them field by field. The guest app resolves them for the venue the guest picked (audit R267); `effectiveForVenueId` on `getBookingFlowConfig` returns them resolved.\n",
  "allOf": [
   {
    "$ref": "#/components/schemas/BookingFlowSettings"
   },
   {
    "type": "object",
    "properties": {
     "venueOverrides": {
      "type": "array",
      "maxItems": 200,
      "default": [],
      "description": "Per-venue overrides, at most one per venue. A `venueId` that is not one of the tenant's active venues, or appears twice, is refused with 400. An override for a venue later closed is kept and has no effect.",
      "items": {
       "$ref": "#/components/schemas/BookingFlowVenueOverride"
      }
     }
    }
   }
  ]
 },
 "BrandIdentity": {
  "x-ticvai-persistence": "none — embedded in tenant_config",
  "type": "object",
  "description": "Every `*AssetRef` here is a `MediaAsset` id from the `assets` library (`createUpload` then `completeUpload`), PNG or SVG and at most 2 MB (decided 28 September, audit R270).\n",
  "required": [
   "logoAssetRef"
  ],
  "properties": {
   "logoAssetRef": {
    "type": "string",
    "format": "uuid",
    "description": "The primary logo."
   },
   "logoDarkAssetRef": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Used on dark backgrounds. Falls back to the primary logo."
   },
   "logoVariant": {
    "type": "string",
    "enum": [
     "light",
     "dark",
     "duotone"
    ],
    "default": "light",
    "description": "**Which lockup sits in the nav bar, and whose colours drive the theme (decided 29 September, rev 3 CFG-4).** `light` uses `logoAssetRef`, `dark` uses `logoDarkAssetRef` (falling back to the primary logo), and `duotone` the two-colour reading of the primary logo.\n"
   },
   "faviconAssetRef": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The browser tab icon for the guest web app."
   },
   "splashImageAssetRefs": {
    "type": "array",
    "description": "Splash images, shown in order. Build-time on the native apps (`splashChangeScope`); immediate on web, reaching guests with the publish (audit R163).",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "splashDurationSeconds": {
    "type": "integer",
    "minimum": 0,
    "maximum": 10,
    "default": 3
   },
   "splashBackgroundColour": {
    "type": "string",
    "pattern": "^#[0-9A-Fa-f]{6}$"
   },
   "showLoadingIndicator": {
    "type": "boolean",
    "default": true
   },
   "splashChangeScope": {
    "allOf": [
     {
      "$ref": "#/components/schemas/ChangeScope"
     }
    ],
    "readOnly": true,
    "description": "Always `buildTime` for native apps. The guest web app takes a splash change at the publish, with no build (audit R163)."
   },
   "introVideoAssetRef": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "**The optional intro video (decided 29 September, MOB-5).** A video `MediaAsset` from the media library (CMS-010). Streamed, so a change reaches guests with the publish and needs no app build.\n"
   },
   "introVideoMode": {
    "type": "string",
    "enum": [
     "off",
     "firstLaunch",
     "everyLaunch"
    ],
    "default": "off",
    "description": "When GST-001 plays it full screen. \"Skip introduction\" is always shown. Anything but `off` needs `introVideoAssetRef`, or 400."
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
 "Entitlement": {
  "type": "object",
  "x-ticvai-persistence": "access.entitlement",
  "description": "**What a guest actually holds.** Found missing on 18 August by the schema audit — 33 tables in `orders`, seven in `access`, and none of them stored an issued ticket.\nThe package sold products, defined `EntitlementTemplate`, recorded `ScanEvent.ticketId`, transferred `ticket_transfer.ticketIds` and issued `wallet_pass.entitlementId` — **five artefacts referring to a thing that did not exist.** `validateAccess` read the *template* and never the instance, and `suspendEntitlement` suspended the template, **which would have suspended it for every guest who held one.**\n**The template is the definition and this is the instance.** A template says *an annual pass admits once a day for a year*; this says *this guest's annual pass, bought on 3 March, used eleven times, frozen for two weeks in July, valid until 2 March.*\n",
  "required": [
   "id",
   "templateId",
   "productId",
   "orderId",
   "subjectId",
   "status",
   "validFrom",
   "validTo"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "description": "A UUIDv7, matching `TicketStatus.ticketId` — **stable for the life of the ticket and independent of the media carrying it.** A guest whose wristband broke keeps the same entitlement with a new `mediaCode`.\n**This is the ticket id.** Wherever an operation takes a `ticketId` or `ticketIds` — `lookupTicket`, `listScans`, `ScanEvent`, the offline package and `transferOrderTickets` — it is this value. An order line's `entitlementIds` are the ticket ids of that line.\n"
   },
   "templateId": {
    "type": "string",
    "format": "uuid",
    "description": "The definition it was issued against. **Pinned at issue** — a template edited next month must not change what this guest bought.\n"
   },
   "productId": {
    "type": "string",
    "format": "uuid"
   },
   "orderId": {
    "type": "string",
    "format": "uuid",
    "description": "The order's id, a UUIDv7 as in `/orders/{orderId}` (`orders.sales_order.id`)."
   },
   "orderLineId": {
    "type": "string",
    "format": "uuid"
   },
   "subjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Who holds it. **Null is legitimate** — a ticket bought as a gift or sold at a till to somebody who gave no details has no subject until it is claimed.\n"
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "scopePath": {
    "type": "string"
   },
   "mediaCode": {
    "type": "string",
    "description": "What is scanned — a QR payload, a wristband serial, a card number. **Rotatable without reissuing**, because a guest whose wristband broke should not need a new ticket.\n"
   },
   "status": {
    "$ref": "../spine/orders.yaml#/components/schemas/EntitlementStatus"
   },
   "statusNote": {
    "type": "string",
    "nullable": true,
    "description": "**Not `TicketStatus` — that is a validation result with a misleading name**, computed at scan time and carrying `isValid` and `isInsideVenue`. The lifecycle is `orders.EntitlementStatus`, and `states/entitlement-status.yaml` has modelled it since before this table existed.\n**Which is the finding in one line: the package had the lifecycle, the state model and the validation result, and no row to hang them on.**\n"
   },
   "validFrom": {
    "type": "string",
    "format": "date-time"
   },
   "validTo": {
    "type": "string",
    "format": "date-time",
    "description": "**Resolved at issue from the template, then owned here.** A freeze extends it, a reissue replaces it, and neither reaches back to the template.\n**What the pre-expiry notice is measured from** (29 September, build pass, group G2; 5.5.30). A daily run in access publishes `entitlement.expiringSoon` once per entitlement and `validTo` when an entitlement in `issued` or `partiallyConsumed` comes within its template's `expiryNoticeDays` (`catalogue.EntitlementTemplate`), and not for one bought inside that window. Marketing turns it into the reminder (a `MessageTrigger` on the event, or a triggered campaign on `entitlementExpiring`); access only says the date is near. A freeze or renewal that moves `validTo` raises the next notice once.\n"
   },
   "entriesUsed": {
    "type": "integer",
    "default": 0,
    "readOnly": true,
    "x-ticvai-derived": "onWrite",
    "description": "**The number `validateAccess` decrements and nothing was decrementing.** A ten-entry pass with no counter is a ten-entry pass that admits forever.\n**Maintained on write**, in the same transaction as the admitting `access.scan_event` row: by `validateAccess`, `validateGroupAccess` (by the count admitted) and `syncScans` for each replayed admission the server accepts. A replayed scan the server downgrades to `denied` does not count.\n"
   },
   "entriesAllowed": {
    "type": "integer",
    "nullable": true
   },
   "lastEntryAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true,
    "x-ticvai-derived": "onWrite",
    "description": "`recordedAt` of the latest admission counted in `entriesUsed`, written by the same writes. A scan replayed late with an earlier `recordedAt` does not move it back.\n"
   },
   "frozenDays": {
    "type": "integer",
    "default": 0,
    "readOnly": true,
    "x-ticvai-derived": "onWrite",
    "description": "Days added by a freeze. **Maintained on write** by the freeze operation (`freezeEntitlement`), in the same write that extends `validTo` by those days. **Held here rather than computed from a freeze log**, because a gate has to answer in under 300ms and cannot replay a history to decide validity.\n"
   },
   "suspendedReason": {
    "type": "string",
    "nullable": true
   },
   "freezeReason": {
    "type": "string",
    "nullable": true,
    "enum": [
     "travelling",
     "injury",
     "personal",
     "seasonal",
     "other"
    ],
    "description": "The `reason` of the latest `freezeEntitlement` (audit R222). Null when never frozen."
   },
   "freezeNote": {
    "type": "string",
    "nullable": true,
    "maxLength": 500,
    "description": "The `note` the latest `freezeEntitlement` took, required there when `reason` is `other` (decided 28 September, audit R222). Kept so the quarterly review of `other` notes has something to read."
   },
   "isNameBound": {
    "type": "boolean",
    "default": false
   },
   "holderName": {
    "type": "string",
    "nullable": true
   },
   "sharedWithSubjectIds": {
    "type": "array",
    "description": "`shareEntitlement`. **The owner keeps it and a second person may present it** — the asymmetry that stops a shared family pass becoming a resale chain.\n",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "issuedVia": {
    "type": "string",
    "enum": [
     "sale",
     "invitation",
     "reissue",
     "transfer",
     "resale",
     "membership",
     "groupBooking"
    ],
    "description": "**How it came to exist, and it matters to finance.** A sold entitlement carries deferred revenue; an invitation carries a marketing cost; a reissue carries neither.\n"
   },
   "supersedesEntitlementId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "For a reissue or a resale. **The chain is traceable** — a ticket appearing from nowhere is indistinguishable from a fraudulent one.\n"
   },
   "walletValueId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Where the template carries stored value. **A `retail.Wallet` bound to the entitlement, not a balance on it** (CF-126).\n"
   },
   "facePassEnrolmentId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "x-ticvai-persisted": false,
    "x-ticvai-derived": "onRead",
    "description": "The active `facePass` enrolment on this entitlement (`FacePassEnrolment.id`), or null when none is. **Computed on read from `pii.subject_biometric` and not stored here** — the PII split keeps the biometric on its own side, and this carries only its id. It is how a screen holding a pass finds the enrolment `getFacePassEnrolment` and `revokeFacePass` take.\n"
   }
  }
 },
 "FeatureToggle": {
  "x-ticvai-persistence": "whitelabel.feature_toggle",
  "type": "object",
  "required": [
   "featureKey",
   "isEnabled",
   "changeScope"
  ],
  "properties": {
   "featureKey": {
    "allOf": [
     {
      "$ref": "#/components/schemas/FeatureKey"
     }
    ],
    "description": "`guestCheckout` is **off by default** (decided 17 September 2026, matrix 2.6.28, placement settled by [ADR-0045](../../docs/adr/0045-every-order-carries-a-proven-contact.md) 18 September): **the venue sets this from the configuration menu**, and it decides which routes the checkout page offers — off, the guest signs in verified at checkout; on, a guest may also check out without an account after proving their contact with a one-time code. **It gates checkout, never the cart.** The kiosk is not governed by it. Rule on `identity` `verifyGuestEmail`.\n"
   },
   "displayName": {
    "type": "string"
   },
   "isEnabled": {
    "type": "boolean"
   },
   "changeScope": {
    "allOf": [
     {
      "$ref": "#/components/schemas/ChangeScope"
     }
    ],
    "readOnly": true,
    "description": "Wallet and payment integrations are `buildTime` on native apps — enabling one needs a release, not a publish.\n"
   },
   "requiresConfiguration": {
    "type": "boolean",
    "description": "True where the feature needs credentials or setup elsewhere first."
   }
  }
 },
 "FontConfig": {
  "x-ticvai-persistence": "none — embedded in tenant_config",
  "type": "object",
  "required": [
   "primaryLatin"
  ],
  "properties": {
   "primaryLatin": {
    "type": "string"
   },
   "primaryArabic": {
    "type": "string",
    "nullable": true,
    "description": "Required when `ar` is among the tenant's languages (audit R163). A Latin face alone leaves Arabic in a system fallback that will not match.\n"
   },
   "secondaryLatin": {
    "type": "string",
    "nullable": true
   },
   "secondaryArabic": {
    "type": "string",
    "nullable": true,
    "description": "Required whenever `secondaryLatin` is set and `ar` is among the tenant's languages (decided 28 September, audit R163)."
   },
   "customFontAssetRefs": {
    "type": "array",
    "description": "Uploaded font files, as `MediaAsset` ids.",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "changeScope": {
    "allOf": [
     {
      "$ref": "#/components/schemas/ChangeScope"
     }
    ],
    "readOnly": true,
    "x-ticvai-derived": "onRead",
    "description": "Custom font files are `buildTime`; selecting a bundled face is `runtime`."
   }
  }
 },
 "FooterConfig": {
  "type": "object",
  "x-ticvai-persistence": "whitelabel.footer_config + whitelabel.footer_config_column + whitelabel.footer_config_social_link",
  "description": "BL-002. **`setHeader` and `HeaderConfig` exist and the footer does not**, which looked like symmetry until you notice it is not: **a header is chrome and a footer is a link surface.**\nA footer carries the legal links — terms, privacy, accessibility statement, cookie preferences — and **those are the ones a regulator checks.** Treating it as a mirror of the header would have given it a logo and no way to reach a privacy notice.\n**Where it is stored.** `legalLinks` and `copyrightText` are columns of `whitelabel.footer_config`; each entry of `columns` is a `whitelabel.footer_config_column` row and each entry of `socialLinks` a `whitelabel.footer_config_social_link` row. Part of the working draft (see the header). **In the tenant's own database, not the control plane (decided 28 September, audit R163)**: it moved from `control.footer_config` and its two child tables.\n",
  "required": [
   "id",
   "scopePath"
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
    "description": "The partition key (ADR-0005), written at `tenant` scope by the server."
   },
   "columns": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "heading": {
       "type": "string"
      },
      "links": {
       "type": "array",
       "items": {
        "type": "object",
        "properties": {
         "label": {
          "type": "string"
         },
         "url": {
          "type": "string"
         },
         "opensCookiePreferences": {
          "type": "boolean",
          "default": false
         }
        }
       }
      }
     }
    }
   },
   "legalLinks": {
    "type": "object",
    "description": "**Required links, held separately from the free-form columns** — a tenant reorganising their footer must not be able to remove the privacy notice by accident.\n",
    "properties": {
     "termsUrl": {
      "type": "string"
     },
     "privacyUrl": {
      "type": "string"
     },
     "accessibilityUrl": {
      "type": "string",
      "nullable": true
     },
     "cookiePolicyUrl": {
      "type": "string",
      "nullable": true
     }
    }
   },
   "copyrightText": {
    "type": "string"
   },
   "socialLinks": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "platform": {
       "type": "string"
      },
      "url": {
       "type": "string"
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
 "HeaderConfig": {
  "x-ticvai-persistence": "none — embedded in tenant_config",
  "type": "object",
  "required": [
   "layout"
  ],
  "properties": {
   "layout": {
    "type": "string",
    "enum": [
     "logoLeft",
     "logoCentre",
     "logoWithMenu"
    ]
   },
   "showLogo": {
    "type": "boolean",
    "default": true
   },
   "showMenu": {
    "type": "boolean",
    "default": true
   },
   "showNotifications": {
    "type": "boolean",
    "default": true
   },
   "backgroundColour": {
    "type": "string",
    "pattern": "^#[0-9A-Fa-f]{6}$"
   }
  }
 },
 "HomepageLayout": {
  "x-ticvai-persistence": "whitelabel.homepage_section",
  "type": "object",
  "required": [
   "sections"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"
   },
   "sections": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "kind",
      "sortOrder",
      "isVisible"
     ],
     "properties": {
      "id": {
       "type": "string",
       "format": "uuid",
       "readOnly": true,
       "description": "**Added 20 August.** The table had no key at all — no id, no parent and no natural key, so **no row could be addressed, updated or deleted.** The response schema returned everything a caller needs and not the row's own identity, which is the difference between an API response and a table.\n"
      },
      "kind": {
       "$ref": "#/components/schemas/HomepageSectionKind"
      },
      "title": {
       "$ref": "#/components/schemas/LocalisedText"
      },
      "sortOrder": {
       "type": "integer"
      },
      "isVisible": {
       "type": "boolean"
      },
      "contentPageId": {
       "type": "string",
       "format": "uuid",
       "nullable": true
      },
      "maxItems": {
       "type": "integer",
       "nullable": true,
       "description": "How many items the section shows. On the mobile Home, `attractions`, `dining`, `whatsOn` and `shop` show 1 or 2 highlights (decided 29 September, MOB-3)."
      },
      "heroStyle": {
       "type": "string",
       "nullable": true,
       "enum": [
        "carousel",
        "video",
        "poster",
        "split",
        null
       ],
       "description": "For `heroBanner` only (decided 29 September, MOB-3)."
      }
     }
    }
   }
  }
 },
 "LanguageConfig": {
  "x-ticvai-persistence": "none — embedded in tenant_config",
  "type": "object",
  "required": [
   "languages",
   "defaultLanguage"
  ],
  "properties": {
   "languages": {
    "type": "array",
    "items": {
     "type": "string",
     "pattern": "^[a-z]{2}$"
    }
   },
   "defaultLanguage": {
    "type": "string",
    "pattern": "^[a-z]{2}$"
   },
   "rtlLanguages": {
    "type": "array",
    "readOnly": true,
    "x-ticvai-derived": "onRead",
    "description": "The enabled languages written right to left — those whose Unicode CLDR character order is `right-to-left` (Arabic, `ar`, among them). Not configured; it follows from `languages`.",
    "items": {
     "type": "string",
     "pattern": "^[a-z]{2}$"
    }
   },
   "translationGaps": {
    "type": "array",
    "readOnly": true,
    "description": "Content lacking a version in an enabled language.",
    "items": {
     "type": "object",
     "properties": {
      "language": {
       "type": "string"
      },
      "missingCount": {
       "type": "integer"
      },
      "areas": {
       "type": "array",
       "items": {
        "type": "string"
       }
      }
     }
    }
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
 "ModuleEnablement": {
  "x-ticvai-persistence": "whitelabel.module_enablement",
  "type": "object",
  "required": [
   "moduleKey",
   "isLicensed",
   "isEnabled"
  ],
  "properties": {
   "moduleKey": {
    "$ref": "#/components/schemas/ModuleKey"
   },
   "displayName": {
    "type": "string"
   },
   "isLicensed": {
    "type": "boolean",
    "description": "From the tenant's subscription. False makes enablement impossible."
   },
   "isEnabled": {
    "type": "boolean"
   },
   "referencedBy": {
    "type": "array",
    "readOnly": true,
    "x-ticvai-derived": "onWrite",
    "description": "Navigation items and homepage sections pointing at this module. Maintained by `setNavigation` and `setHomepageLayout` in the same transaction as the links they write.",
    "items": {
     "type": "string"
    }
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
 "NavigationConfig": {
  "x-ticvai-persistence": "whitelabel.navigation_item",
  "type": "object",
  "description": "**The mobile tab set is venue configuration (decided 29 September, MOB-1; 29 September brief decision 6).** Before a tenant saves its own, `bottomNavigation` is Home, Explore, Plan and Tickets (each an `appSection` link), with the Buy tickets button beside them; Map is an optional tab. Plan is left out while `visitPlanner` is off.\n",
  "required": [
   "kind",
   "items"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"
   },
   "kind": {
    "type": "string",
    "enum": [
     "bottomNavigation",
     "drawer",
     "tabs"
    ]
   },
   "items": {
    "type": "array",
    "maxItems": 12,
    "items": {
     "type": "object",
     "required": [
      "label",
      "target",
      "isVisible",
      "sortOrder"
     ],
     "properties": {
      "id": {
       "type": "string",
       "format": "uuid",
       "readOnly": true,
       "description": "**Added 20 August.** The table had no key at all — no id, no parent and no natural key, so **no row could be addressed, updated or deleted.** The response schema returned everything a caller needs and not the row's own identity, which is the difference between an API response and a table.\n"
      },
      "label": {
       "$ref": "#/components/schemas/LocalisedText"
      },
      "icon": {
       "type": "string"
      },
      "target": {
       "$ref": "#/components/schemas/LinkTarget"
      },
      "isVisible": {
       "type": "boolean",
       "description": "At most five may be visible in bottom navigation; the rest overflow."
      },
      "sortOrder": {
       "type": "integer"
      }
     }
    }
   },
   "buyButton": {
    "type": "object",
    "nullable": true,
    "description": "**The persistent Buy tickets button (decided 29 September, MOB-2).** On every screen of the mobile app except the booking and checkout steps; it opens GST-003. Read with `bottomNavigation`.\n",
    "properties": {
     "style": {
      "type": "string",
      "enum": [
       "raised",
       "floating",
       "flat",
       "hidden"
      ],
      "default": "raised",
      "description": "`raised` sits in the centre of the tab bar, as the v4 prototype shows; `hidden` turns it off."
     },
     "label": {
      "$ref": "#/components/schemas/LocalisedText"
     }
    }
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
 "ProductEligibilityRule": {
  "type": "object",
  "x-ticvai-persistence": "catalogue.product_eligibility_rule",
  "description": "Participation limits for one product. Absent means anyone may take part, and `getProductEligibilityRule` returns that absence as this schema with every limit null, never as a `404`.",
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "productId": {
    "type": "string",
    "readOnly": true
   },
   "minAgeYears": {
    "type": "integer",
    "minimum": 0,
    "nullable": true
   },
   "maxAgeYears": {
    "type": "integer",
    "minimum": 0,
    "nullable": true
   },
   "minHeightCm": {
    "type": "integer",
    "minimum": 50,
    "maximum": 250,
    "nullable": true
   },
   "maxHeightCm": {
    "type": "integer",
    "minimum": 50,
    "maximum": 250,
    "nullable": true
   },
   "heightBandsCm": {
    "type": "array",
    "items": {
     "type": "integer"
    },
    "default": [
     120,
     140
    ],
    "description": "Band edges the guest chooses between, e.g. under 1.20 m, 1.20–1.40 m, 1.40 m and over."
   },
   "accompaniedBelowAge": {
    "type": "integer",
    "nullable": true,
    "description": "Under this age an adult must be present, e.g. 8 at the kids club."
   },
   "guardianSignatureAgeFrom": {
    "type": "integer",
    "nullable": true
   },
   "guardianSignatureAgeTo": {
    "type": "integer",
    "nullable": true,
    "description": "Ages needing a guardian's signature, e.g. 12–15 on a thrill ride."
   },
   "waiverRequired": {
    "type": "boolean",
    "default": false
   },
   "swimAbility": {
    "type": "string",
    "enum": [
     "notRequired",
     "confident"
    ],
    "default": "notRequired",
    "deprecated": true,
    "description": "**Superseded for the guest's answer** (decided 29 September, rev 3 REV3-26): the swim question is a consent, not a data field. A venue attaches *Are you able to swim?* as a consent question (`Product.consentQuestionIds`), with its own text, version and whether it is asked per person or once per booking, and the answer is a consent record. Kept so existing rules read; a new product should use a consent question instead.\n"
   },
   "refundableIfIneligibleAtGate": {
    "type": "boolean",
    "default": false
   },
   "requiredCertificationCode": {
    "type": "string",
    "nullable": true,
    "maxLength": 60,
    "description": "**A certification the participant must hold** (decided 29 September, W4; added 30 September), e.g. `padiOpenWater` for a dive. Null means none. Help me choose reads it: an answer whose `filter.certificationCode` names it with `holdsCertification: false` leaves the product out, and with `holdsCertification: true` (or no flag) keeps only products needing that certification or none. Proof, where the venue asks for it, is a consent question on the product (REV3-26), not this field."
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005). Operations write it at `venue` scope."
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
 "QueueStatus": {
  "type": "string",
  "enum": [
   "open",
   "paused",
   "closed",
   "atCapacity"
  ]
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
 "StorefrontAnalyticsProvider": {
  "type": "object",
  "x-ticvai-persistence": "whitelabel.analytics_provider",
  "description": "**One analytics platform the storefront or app reports to** (22.10.29, 29 September build). Venue configuration: a null `venueId` is the tenant-wide default a venue's own row replaces.",
  "required": [
   "provider",
   "measurementId",
   "surfaces",
   "consentCategory",
   "isEnabled"
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
    "nullable": true
   },
   "provider": {
    "type": "string",
    "enum": [
     "googleAnalytics4",
     "googleTagManager",
     "adobeAnalytics",
     "metaPixel",
     "matomo",
     "other"
    ]
   },
   "providerLabel": {
    "type": "string",
    "maxLength": 100,
    "nullable": true,
    "description": "The name, when `provider` is `other`."
   },
   "measurementId": {
    "type": "string",
    "maxLength": 100,
    "description": "What the tag or SDK reports to (GA4 `G-...`, Tag Manager `GTM-...`, a pixel id)."
   },
   "surfaces": {
    "type": "array",
    "minItems": 1,
    "items": {
     "type": "string",
     "enum": [
      "guestWeb",
      "guestApp"
     ]
    }
   },
   "consentCategory": {
    "type": "string",
    "enum": [
     "functional",
     "analytics",
     "personalisation",
     "marketing"
    ],
    "default": "analytics",
    "description": "The cookie category the visitor must grant before this provider loads (marketing-crm `CookieCategory`)."
   },
   "isEnabled": {
    "type": "boolean",
    "default": true
   },
   "reportingPropertyId": {
    "type": "string",
    "maxLength": 100,
    "nullable": true,
    "description": "The property `getStorefrontInsights` asks the reporting API about (a GA4 property id). Staff only."
   },
   "reportingCredentialRef": {
    "type": "string",
    "maxLength": 200,
    "nullable": true,
    "writeOnly": true,
    "description": "The vault reference of the reporting credential. Accepted, never returned."
   },
   "hasReportingCredential": {
    "type": "boolean",
    "readOnly": true,
    "description": "Whether a reporting credential is held, since the reference itself is never returned."
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
 "TenantConfig": {
  "x-ticvai-persistence": "whitelabel.tenant_config",
  "type": "object",
  "description": "**The tenant's working draft**, one row per tenant (see the header). Published versions are `ConfigVersion.snapshot`, not further rows here.\n**Only `tenantId` and `version` are required**, because the draft is built one part at a time: the first `set*` call creates the row with that part alone. A part that is still unset is what `validateTenantConfig` reports (`missingRequiredAsset` and the like) and what blocks `publishTenantConfig` — a storage rule that every part exist would stop the first save.\n",
  "required": [
   "tenantId",
   "version"
  ],
  "properties": {
   "tenantId": {
    "type": "string",
    "format": "uuid"
   },
   "version": {
    "type": "string",
    "description": "The draft's working version label; the published one is `ConfigVersion.version`."
   },
   "isDraft": {
    "type": "boolean",
    "readOnly": true,
    "description": "True for the working draft, which is the only row."
   },
   "brand": {
    "$ref": "#/components/schemas/BrandIdentity"
   },
   "appIcons": {
    "$ref": "#/components/schemas/AppIcons"
   },
   "bookingFlow": {
    "$ref": "#/components/schemas/BookingFlowConfig"
   },
   "bookingFlows": {
    "type": "array",
    "readOnly": true,
    "x-ticvai-derived": "onRead",
    "description": "Every venue's booking flows in the draft (`whitelabel.booking_flow`), so a publish snapshots them with the rest (decided 29 September, W12).",
    "items": {
     "$ref": "#/components/schemas/BookingFlow"
    }
   },
   "theme": {
    "$ref": "#/components/schemas/Theme"
   },
   "fonts": {
    "$ref": "#/components/schemas/FontConfig"
   },
   "footer": {
    "$ref": "#/components/schemas/FooterConfig"
   },
   "notificationBranding": {
    "type": "object",
    "nullable": true,
    "description": "BL-003. **`marketing-crm` holds the templates and nothing said whose identity they wear.** A message sent on behalf of a venue carries that venue's sender name, reply-to and logo — **an operational alert arriving from `noreply@ticvai.com` is one a guest marks as spam.**\nResolved on the template at send time rather than duplicated per template.\n",
    "properties": {
     "senderName": {
      "type": "string"
     },
     "replyToEmail": {
      "type": "string",
      "format": "email"
     },
     "smsSenderId": {
      "type": "string",
      "nullable": true
     },
     "whatsappBusinessId": {
      "type": "string",
      "nullable": true
     },
     "logoAssetId": {
      "type": "string",
      "format": "uuid",
      "nullable": true
     }
    }
   },
   "enabledPaymentMethods": {
    "type": "array",
    "nullable": true,
    "description": "BL-004. **`FeatureToggle` could turn Apple Pay on and could not say which cards a tenant accepts.** Resolved against `orders.PaymentProvider.supportedMethods` — the tenant's choice within what the gateway offers, and **a tenant enabling a method their provider does not support should fail here rather than at checkout.**\n",
    "items": {
     "type": "string"
    }
   },
   "accessibility": {
    "$ref": "#/components/schemas/AccessibilitySettings"
   },
   "header": {
    "$ref": "#/components/schemas/HeaderConfig"
   },
   "navigation": {
    "$ref": "#/components/schemas/NavigationConfig"
   },
   "homepage": {
    "$ref": "#/components/schemas/HomepageLayout"
   },
   "modules": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/ModuleEnablement"
    }
   },
   "features": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/FeatureToggle"
    }
   },
   "languages": {
    "$ref": "#/components/schemas/LanguageConfig"
   },
   "updatedAt": {
    "type": "string",
    "format": "date-time"
   },
   "isInMaintenance": {
    "type": "boolean",
    "default": false,
    "description": "Written by `setMaintenanceMode`; read by `getTenantAppStatus`."
   },
   "maintenanceMessage": {
    "allOf": [
     {
      "$ref": "#/components/schemas/LocalisedText"
     }
    ],
    "nullable": true,
    "description": "The message on the branded maintenance screen."
   },
   "expectedBackAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "minimumAppVersion": {
    "allOf": [
     {
      "$ref": "#/components/schemas/MinimumAppVersion"
     }
    ],
    "description": "Live state, written by `setMaintenanceMode` (audit R073)."
   },
   "contact": {
    "allOf": [
     {
      "$ref": "#/components/schemas/VenueContact"
     }
    ],
    "description": "Live state, written by `setMaintenanceMode` (audit R073)."
   },
   "availability": {
    "allOf": [
     {
      "$ref": "#/components/schemas/AppAvailability"
     }
    ],
    "description": "Live state, written by `setMaintenanceMode` (audit R073)."
   },
   "availabilityMessage": {
    "allOf": [
     {
      "$ref": "#/components/schemas/LocalisedText"
     }
    ],
    "nullable": true,
    "description": "Live state, written by `setMaintenanceMode` (audit R073)."
   },
   "venues": {
    "type": "array",
    "x-ticvai-derived": "onRead",
    "description": "The tenant's active venues, for the guest venue picker on WEB-001 and GST-001 (decided 28 September, audit R267). Public: returned without a session and cached with the rest of the response. Read from `tenancy` venues; a closed or archived venue is left out.\n",
    "items": {
     "type": "object",
     "required": [
      "venueId",
      "name"
     ],
     "properties": {
      "venueId": {
       "type": "string",
       "format": "uuid"
      },
      "name": {
       "$ref": "#/components/schemas/LocalisedText"
      },
      "city": {
       "type": "string",
       "nullable": true
      },
      "openingHours": {
       "allOf": [
        {
         "$ref": "#/components/schemas/LocalisedText"
        }
       ],
       "nullable": true,
       "description": "Today's hours as shown to a guest, e.g. \"10:00 to 22:00\"."
      }
     }
    }
   }
  }
 },
 "Theme": {
  "x-ticvai-persistence": "none — embedded in tenant_config",
  "type": "object",
  "required": [
   "primaryColour",
   "secondaryColour",
   "backgroundColour",
   "textColour"
  ],
  "properties": {
   "primaryColour": {
    "type": "string",
    "pattern": "^#[0-9A-Fa-f]{6}$"
   },
   "secondaryColour": {
    "type": "string",
    "pattern": "^#[0-9A-Fa-f]{6}$"
   },
   "accentColour": {
    "type": "string",
    "pattern": "^#[0-9A-Fa-f]{6}$"
   },
   "backgroundColour": {
    "type": "string",
    "pattern": "^#[0-9A-Fa-f]{6}$"
   },
   "textColour": {
    "type": "string",
    "pattern": "^#[0-9A-Fa-f]{6}$"
   },
   "darkMode": {
    "type": "object",
    "description": "Optional dark variant. Derived from the light theme when absent.",
    "properties": {
     "primaryColour": {
      "type": "string",
      "pattern": "^#[0-9A-Fa-f]{6}$"
     },
     "backgroundColour": {
      "type": "string",
      "pattern": "^#[0-9A-Fa-f]{6}$"
     },
     "textColour": {
      "type": "string",
      "pattern": "^#[0-9A-Fa-f]{6}$"
     }
    }
   },
   "cornerRadius": {
    "type": "integer",
    "minimum": 0,
    "maximum": 32,
    "description": "The prototype's 0 to 22 px slider sits inside these bounds (rev 3 CFG-2, no change). Its named palettes, font pairs and background tones are presets over the colours here and `FontConfig`, not stored values."
   },
   "surfaceStyle": {
    "type": "string",
    "enum": [
     "glass",
     "solid"
    ],
    "default": "glass",
    "description": "Cards and panels as frosted glass or opaque (decided 29 September, rev 3 CFG-3)."
   },
   "buttonStyle": {
    "type": "string",
    "enum": [
     "solid",
     "outline",
     "pill"
    ],
    "default": "solid",
    "description": "Button shape (decided 29 September, rev 3 CFG-3)."
   },
   "componentColours": {
    "type": "object",
    "description": "**Colours for single interactive elements (decided 17 September, M17-11).** Each is optional and falls back to the theme colours. Every pair passes the same contrast check as the theme (`ContrastProblem`), or `setTheme` refuses it with 400. The guest flow stays the standard one; only the colours change.\n",
    "properties": {
     "primaryCta": {
      "$ref": "#/components/schemas/ThemeComponentColour"
     },
     "payButton": {
      "$ref": "#/components/schemas/ThemeComponentColour"
     },
     "addToCart": {
      "$ref": "#/components/schemas/ThemeComponentColour"
     },
     "buyTicketsButton": {
      "$ref": "#/components/schemas/ThemeComponentColour"
     },
     "link": {
      "$ref": "#/components/schemas/ThemeComponentColour"
     },
     "badge": {
      "$ref": "#/components/schemas/ThemeComponentColour"
     }
    }
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
 },
 "VisitPlan": {
  "type": "object",
  "x-ticvai-persistence": "venuemap.visit_plan",
  "description": "**A guest's visit plan** (29 September, MOB-6): the Plan tab. One row per plan; its items are `venuemap.visit_plan_item` rows carrying the version they belong to, so every earlier version stays readable and undo is a new version equal to an old one. **Owned by the guest session**, like a cart: `subjectId` when signed in, `sessionRef` for an anonymous device session, claimed on sign-in.\n",
  "required": [
   "id",
   "venueId",
   "status",
   "version",
   "days"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "Derived from `venueId`."
   },
   "subjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "x-ticvai-references": "marketing.guest_profile",
    "description": "The signed-in guest. From the session, never from the body."
   },
   "sessionRef": {
    "type": "string",
    "nullable": true,
    "readOnly": true,
    "description": "The anonymous device session that owns the plan until sign-in."
   },
   "status": {
    "type": "string",
    "enum": [
     "draft",
     "booked",
     "archived"
    ],
    "readOnly": true,
    "description": "`booked` after `bookVisitPlan`; a booked plan is read-only. `archived` after its last date."
   },
   "version": {
    "type": "integer",
    "minimum": 1,
    "readOnly": true,
    "description": "The current version. Every `updateVisitPlan` adds one."
   },
   "source": {
    "type": "string",
    "enum": [
     "rules",
     "preset",
     "aiAgent"
    ],
    "readOnly": true,
    "description": "What produced the current version: the rules planner, a preset, or the AI planner agent acting for the guest. **The guest sees which**, as every AI answer says what it is based on.\n"
   },
   "inputs": {
    "$ref": "#/components/schemas/VisitPlanRequest"
   },
   "mapVersion": {
    "type": "integer",
    "readOnly": true,
    "description": "The published map version the plan was laid out on."
   },
   "cartId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "x-ticvai-references": "orders.cart",
    "description": "The cart `bookVisitPlan` filled."
   },
   "excluded": {
    "type": "array",
    "readOnly": true,
    "description": "**What was left out and why**, e.g. a coaster excluded because one of the party is under its 120 cm minimum. Shown on GST-053, so the planner never looks as if it forgot.\n",
    "items": {
     "type": "object",
     "properties": {
      "pointId": {
       "type": "string",
       "format": "uuid"
      },
      "productId": {
       "type": "string",
       "format": "uuid",
       "nullable": true
      },
      "reason": {
       "type": "string",
       "enum": [
        "heightRule",
        "ageRule",
        "closedOnDate",
        "notInInterests",
        "noTime",
        "notAtVenue"
       ],
       "description": "`notAtVenue` (30 September, MoM 4.7): a must-include point that is at none of the plan's venues, so no day could hold it.\n"
      }
     }
    }
   },
   "unmatchedPreferences": {
    "type": "array",
    "readOnly": true,
    "x-ticvai-persisted": false,
    "x-ticvai-derived": "onRead",
    "description": "**A preference a day's venue cannot meet is said, never faked** (30 September client meeting, MoM 4.7, Allam's requirement). One entry per day and preference that no point of that day's venue matches: a cuisine (`cuisineTags`), a shop (`retailTags`) or an interest (`interestTags`). `availableAtVenueIds` names the tenant's other active venues whose published map does match, so GST-053 and WEB-050 can say *Indian food is at the other park (day 2)* instead of quietly placing a restaurant the party cannot reach. Empty when every preference is met on every day. Worked out on read for the version read (a swap can meet or lose a preference), never stored.\n",
    "items": {
     "type": "object",
     "required": [
      "date",
      "venueId",
      "preference",
      "tag"
     ],
     "properties": {
      "date": {
       "type": "string",
       "format": "date"
      },
      "venueId": {
       "type": "string",
       "format": "uuid",
       "description": "The day's venue, which has no match."
      },
      "preference": {
       "type": "string",
       "enum": [
        "cuisine",
        "retail",
        "interest"
       ]
      },
      "tag": {
       "type": "string",
       "maxLength": 30
      },
      "availableAtVenueIds": {
       "type": "array",
       "items": {
        "type": "string",
        "format": "uuid"
       },
       "description": "Other active venues of the tenant where the tag is matched. Empty when none is."
      }
     }
    }
   },
   "days": {
    "type": "array",
    "readOnly": true,
    "description": "One per date, in order. The items of the version read.",
    "items": {
     "type": "object",
     "required": [
      "date",
      "venueId",
      "items"
     ],
     "properties": {
      "date": {
       "type": "string",
       "format": "date"
      },
      "venueId": {
       "type": "string",
       "format": "uuid",
       "description": "**The venue this day is planned at** (30 September, MoM 4.7): `VisitPlanRequest.dayVenues` for the date, else `venueId`. Every item of the day is at this venue.\n"
      },
      "opensAt": {
       "type": "string",
       "nullable": true
      },
      "closesAt": {
       "type": "string",
       "nullable": true
      },
      "items": {
       "type": "array",
       "items": {
        "$ref": "#/components/schemas/VisitPlanItem"
       }
      }
     }
    }
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
 "VisitPlanAlternative": {
  "type": "object",
  "x-ticvai-persistence": "none — computed on read",
  "description": "One candidate for a swap (29 September, MOB-6).",
  "required": [
   "kind",
   "venueId",
   "startsAt",
   "reason"
  ],
  "properties": {
   "kind": {
    "type": "string",
    "enum": [
     "attraction",
     "show",
     "meal",
     "shop",
     "rest"
    ]
   },
   "venueId": {
    "type": "string",
    "format": "uuid",
    "description": "The item's day venue; an alternative is never from another venue (30 September, MoM 4.7)."
   },
   "pointId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "productId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "performanceId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "name": {
    "type": "string"
   },
   "startsAt": {
    "type": "string",
    "format": "date-time"
   },
   "durationMinutes": {
    "type": "integer"
   },
   "walkMinutes": {
    "type": "integer",
    "nullable": true
   },
   "expectedWaitMinutes": {
    "type": "integer",
    "nullable": true
   },
   "matchedInterests": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "reason": {
    "type": "string",
    "description": "Why it is offered, in words the sheet shows, e.g. *Same thrill level, 4 minutes closer*."
   }
  }
 },
 "VisitPlanBooking": {
  "type": "object",
  "x-ticvai-persistence": "none — computed; the lines are orders.cart_line rows",
  "description": "What `bookVisitPlan` returns (29 September, MOB-6): the cart handoff.",
  "required": [
   "planId",
   "cartId",
   "added",
   "notAdded"
  ],
  "properties": {
   "planId": {
    "type": "string",
    "format": "uuid"
   },
   "cartId": {
    "type": "string",
    "format": "uuid"
   },
   "added": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "itemId": {
       "type": "string",
       "format": "uuid"
      },
      "cartLineId": {
       "type": "string",
       "format": "uuid"
      },
      "leaseExpiresAt": {
       "type": "string",
       "format": "date-time",
       "nullable": true
      }
     }
    }
   },
   "notAdded": {
    "type": "array",
    "description": "Items that could not be added, with the `addCartLine` refusal each met.",
    "items": {
     "type": "object",
     "properties": {
      "itemId": {
       "type": "string",
       "format": "uuid"
      },
      "reason": {
       "type": "string",
       "description": "The orders `CartProblem` code, e.g. `soldOutForSession`, `productInfoOnly`, `seatLimitExceeded`."
      }
     }
    }
   },
   "freeItems": {
    "type": "integer",
    "description": "Stops that need nothing bought."
   }
  }
 },
 "VisitPlanItem": {
  "type": "object",
  "x-ticvai-persistence": "venuemap.visit_plan_item",
  "description": "**One timed stop on a plan day** (29 September, MOB-6). Rows are kept per `planVersion`: a change writes the day's items again under the new version, and an older version's rows are never updated.\n",
  "required": [
   "id",
   "planId",
   "planVersion",
   "date",
   "sequence",
   "kind",
   "startsAt",
   "endsAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "planId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "x-ticvai-references": "venuemap.visit_plan"
   },
   "planVersion": {
    "type": "integer",
    "minimum": 1,
    "readOnly": true
   },
   "date": {
    "type": "string",
    "format": "date"
   },
   "sequence": {
    "type": "integer",
    "minimum": 1
   },
   "kind": {
    "type": "string",
    "enum": [
     "attraction",
     "show",
     "meal",
     "shop",
     "rest",
     "travel"
    ],
    "description": "`meal` is a stop at a dining point (restaurant, cafe or food kiosk); `shop` is a retail stop at a shop or a retail kiosk (30 September client meeting, MoM 4.7: retail is placed from the day venue's own points, as dining is).\n"
   },
   "venueId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "x-ticvai-persisted": false,
    "x-ticvai-derived": "onRead",
    "description": "**The venue of this stop** (30 September client meeting, MoM 4.7): always the day's venue, and the venue whose map `pointId` is on. Carried on the item so the screens, `bookVisitPlan` and the AI planner agent read it rather than infer it. **Worked out on read, not stored**: from the plan's `inputs` (`dayVenues` for the item's date, else `venueId`). A stored `venue_id` would move the item rows from the plan's own row-level policy to a venue policy and hide a second park's items from the guest who owns the plan.\n"
   },
   "pointId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "x-ticvai-references": "venuemap.point"
   },
   "productId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "x-ticvai-references": "catalogue.product",
    "description": "What is bought for this stop, where it is bought. Null for a free stop."
   },
   "bundleId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "x-ticvai-references": "promotions.bundle",
    "description": "A meal combo or package, from the point's `featuredOffer`."
   },
   "performanceId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "x-ticvai-references": "catalogue.performance"
   },
   "startsAt": {
    "type": "string",
    "format": "date-time"
   },
   "endsAt": {
    "type": "string",
    "format": "date-time"
   },
   "walkMinutesBefore": {
    "type": "integer",
    "minimum": 0,
    "nullable": true
   },
   "expectedWaitMinutes": {
    "type": "integer",
    "minimum": 0,
    "nullable": true,
    "description": "The typical wait at that hour when the plan was laid out; GST-059 replaces it with the live one."
   },
   "addOnSuggestion": {
    "type": "object",
    "nullable": true,
    "description": "A suggested add-on for this stop, e.g. Fast Track where the wait is long. Never added by itself.",
    "properties": {
     "productId": {
      "type": "string",
      "format": "uuid"
     },
     "reason": {
      "type": "string"
     }
    }
   },
   "addOnAccepted": {
    "type": "boolean",
    "default": false
   },
   "pinned": {
    "type": "boolean",
    "default": false,
    "description": "The guest fixed this stop; a re-lay moves other stops around it."
   },
   "note": {
    "type": "string",
    "nullable": true,
    "maxLength": 200
   }
  }
 },
 "VisitPlanRequest": {
  "type": "object",
  "x-ticvai-persistence": "none — request only; kept as `inputs` on venuemap.visit_plan",
  "description": "What `generateVisitPlan` takes (29 September, MOB-6): the Plan tab's form on GST-051 and WEB-050.\n",
  "required": [
   "venueId",
   "dates",
   "party"
  ],
  "properties": {
   "venueId": {
    "type": "string",
    "format": "uuid",
    "description": "The venue the guest picked in the app (GST-001 / WEB-001), which scopes the plan. Every date is planned at this venue unless `dayVenues` puts it somewhere else.\n"
   },
   "dayVenues": {
    "type": "array",
    "maxItems": 7,
    "description": "**Which venue on which date, in a multi-venue tenant** (30 September client meeting, MoM 4.7, Allam's requirement). One entry per date that is not at `venueId`; each date of `dates` at most once. Each venue must be an active venue of the caller's tenant (the options `getTenantAppStatus.venues` lists), else 422 `venue-not-in-tenant`. **Each day is then planned from that venue's own published map only**: its rides, its dining and its retail points, never another venue's.\n",
    "items": {
     "type": "object",
     "required": [
      "date",
      "venueId"
     ],
     "properties": {
      "date": {
       "type": "string",
       "format": "date"
      },
      "venueId": {
       "type": "string",
       "format": "uuid"
      }
     }
    }
   },
   "dates": {
    "type": "array",
    "minItems": 1,
    "maxItems": 7,
    "items": {
     "type": "string",
     "format": "date"
    }
   },
   "party": {
    "type": "array",
    "minItems": 1,
    "maxItems": 20,
    "description": "One entry per person. **Height where the guest knows it, age otherwise**: height is what ride eligibility rules test, and an age band is the fallback the rule may also state. Nothing here identifies a person.\n",
    "items": {
     "type": "object",
     "properties": {
      "heightCm": {
       "type": "integer",
       "minimum": 40,
       "maximum": 230,
       "nullable": true
      },
      "ageYears": {
       "type": "integer",
       "minimum": 0,
       "maximum": 120,
       "nullable": true
      }
     }
    }
   },
   "pace": {
    "type": "string",
    "enum": [
     "packed",
     "relaxed"
    ],
    "default": "relaxed"
   },
   "interestTags": {
    "type": "array",
    "maxItems": 12,
    "description": "The same closed list as `VenuePoint.interestTags`.",
    "items": {
     "type": "string"
    }
   },
   "cuisineTags": {
    "type": "array",
    "maxItems": 8,
    "description": "Matched per day against the `cuisineTags` of that day's venue's dining points only (30 September, MoM 4.7). A cuisine no dining point of the day's venue serves is not forced into the day; it is reported in `VisitPlan.unmatchedPreferences`.\n",
    "items": {
     "type": "string"
    }
   },
   "retailTags": {
    "type": "array",
    "maxItems": 8,
    "description": "**Shops the party would like to visit** (30 September client meeting, MoM 4.7: retail and kiosk shops join F&B as venue-linked planner options), e.g. `souvenirs`, `toys`, `apparel`, `essentials`. Matched per day against `VenuePoint.retailTags` of that day's venue's shops and retail kiosks; an unmatched tag is reported, as a cuisine is.\n",
    "items": {
     "type": "string",
     "maxLength": 30
    }
   },
   "mustIncludePointIds": {
    "type": "array",
    "maxItems": 10,
    "description": "Placed on a day whose venue has the point. A point at none of the plan's venues is listed in `VisitPlan.excluded` with `notAtVenue`, never placed on another venue's day.\n",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "preset": {
    "type": "string",
    "nullable": true,
    "enum": [
     "highlights",
     "family",
     "thrillSeeker",
     "waterDay",
     "relaxed",
     "showsAndDining"
    ],
    "description": "A ready-made day plan (GST-052 Suggested Itineraries): the preset fixes the interests and the pace, and the party still decides eligibility.\n"
   },
   "presetKey": {
    "type": "string",
    "nullable": true,
    "maxLength": 64,
    "pattern": "^[a-z][a-zA-Z0-9]*$",
    "description": "The ready-made plan the guest took on GST-052 (30 September, second wave of the 29 September pass, MOB-6): one of the built-in `preset` keys above, or a key of a ready-made plan the venue defines. **The same rules planner runs**: the preset only supplies interests, pace and must-include points, and the party still decides eligibility. When both `preset` and `presetKey` are sent they must name the same plan; `presetKey` is the field new clients send. An unknown key is refused 422 `unknown-preset`.\n"
   },
   "startTime": {
    "type": "string",
    "nullable": true,
    "pattern": "^([01][0-9]|2[0-3]):[0-5][0-9]$",
    "description": "When the party arrives. Null means opening time."
   },
   "locale": {
    "type": "string",
    "nullable": true
   }
  }
 },
 "VisitPlanUpdate": {
  "type": "object",
  "x-ticvai-persistence": "none — request only; lands as a new version of venuemap.visit_plan_item rows",
  "description": "What `updateVisitPlan` takes (29 September, MOB-6).",
  "required": [
   "baseVersion",
   "changes"
  ],
  "properties": {
   "baseVersion": {
    "type": "integer",
    "minimum": 1
   },
   "changes": {
    "type": "array",
    "minItems": 1,
    "maxItems": 20,
    "items": {
     "type": "object",
     "required": [
      "op"
     ],
     "properties": {
      "op": {
       "type": "string",
       "enum": [
        "swap",
        "remove",
        "add",
        "move",
        "pin",
        "acceptAddOn",
        "declineAddOn",
        "revertTo"
       ]
      },
      "itemId": {
       "type": "string",
       "format": "uuid",
       "nullable": true
      },
      "date": {
       "type": "string",
       "format": "date",
       "nullable": true
      },
      "pointId": {
       "type": "string",
       "format": "uuid",
       "nullable": true
      },
      "performanceId": {
       "type": "string",
       "format": "uuid",
       "nullable": true
      },
      "startsAt": {
       "type": "string",
       "format": "date-time",
       "nullable": true
      },
      "version": {
       "type": "integer",
       "nullable": true,
       "description": "For `revertTo`, the earlier version to restore (undo)."
      }
     }
    }
   }
  }
 },
 "WaitTime": {
  "x-ticvai-persistence": "none — computed from readings and throughput",
  "type": "object",
  "required": [
   "queueId",
   "waitMinutes",
   "source",
   "asOf",
   "isStale"
  ],
  "properties": {
   "queueId": {
    "type": "string",
    "format": "uuid"
   },
   "queueName": {
    "$ref": "#/components/schemas/LocalisedText"
   },
   "attractionProductId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "attractionCategoryId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The catalogue `ProductCategory` the attraction product is filed under — the value the `category` filter on `getWaitTimes` matches. Read from catalogue, not stored here.\n"
   },
   "status": {
    "$ref": "#/components/schemas/QueueStatus"
   },
   "waitMinutes": {
    "type": "integer",
    "nullable": true,
    "description": "Null where the queue is closed or no estimate is available."
   },
   "source": {
    "$ref": "#/components/schemas/WaitTimeSource"
   },
   "isStale": {
    "type": "boolean",
    "description": "The underlying feed has gone quiet past its expected interval. The figure is shown with a caveat rather than frozen and presented as current, and it is not hidden (decided 28 September, audit R080 (b)): the screen shows `waitMinutes` with its `asOf` and a stale marker.\n"
   },
   "heightRequirementCm": {
    "type": "integer",
    "nullable": true
   },
   "zone": {
    "type": "string",
    "nullable": true
   },
   "asOf": {
    "type": "string",
    "format": "date-time",
    "description": "When the figure was produced — the queue's `waitTimeAsOf`."
   }
  }
 },
 "WaitTimeSource": {
  "type": "string",
  "description": "Where the estimate came from. Surfaced so an operator knows whether a figure is measured or guessed.\n",
  "enum": [
   "sensor",
   "throughput",
   "manual",
   "unavailable"
  ]
 },
 "WhiteLabelStorefrontSessionBatch": {
  "type": "object",
  "x-ticvai-persistence": "none — request only; published as storefront.sessionEvent through platform.outbox",
  "description": "One beacon from the storefront or guest-app runtime (8.3.40; decided 29 September, build pass, group G2). **Closed shape** (`additionalProperties: false`): hashes, route families, product ids and counts only.",
  "additionalProperties": false,
  "required": [
   "batchId",
   "sessionRef",
   "surface",
   "sessionStartedAt",
   "interactions"
  ],
  "properties": {
   "batchId": {
    "type": "string",
    "format": "uuid",
    "description": "UUIDv7 minted by the runtime; a retried beacon repeats it."
   },
   "sessionRef": {
    "type": "string",
    "maxLength": 128,
    "description": "The runtime's own session id, SHA-256 hashed in the browser; hashed again with the tenant key on arrival and published as `storefront.sessionEvent.sessionRef`. The checkout passes the same value to `ai.scoreTransactionRisk`."
   },
   "deviceIdHash": {
    "type": "string",
    "maxLength": 128,
    "nullable": true
   },
   "surface": {
    "type": "string",
    "enum": [
     "guestWeb",
     "guestApp"
    ]
   },
   "venueId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "sessionStartedAt": {
    "type": "string",
    "format": "date-time"
   },
   "interactions": {
    "type": "array",
    "minItems": 1,
    "maxItems": 50,
    "items": {
     "type": "object",
     "additionalProperties": false,
     "required": [
      "kind",
      "at"
     ],
     "properties": {
      "kind": {
       "type": "string",
       "enum": [
        "pageView",
        "productView",
        "seatMapOpened",
        "addToCart",
        "removeFromCart",
        "checkoutStarted",
        "paymentPageViewed",
        "promoCodeTried",
        "search"
       ]
      },
      "pageKind": {
       "type": "string",
       "nullable": true,
       "enum": [
        "home",
        "product",
        "seatMap",
        "cart",
        "checkout",
        "account",
        "content",
        null
       ]
      },
      "productId": {
       "type": "string",
       "format": "uuid",
       "nullable": true
      },
      "at": {
       "type": "string",
       "format": "date-time"
      },
      "dwellMs": {
       "type": "integer",
       "minimum": 0,
       "nullable": true
      }
     }
    }
   },
   "automationHints": {
    "type": "object",
    "nullable": true,
    "additionalProperties": false,
    "properties": {
     "webdriver": {
      "type": "boolean"
     },
     "headless": {
      "type": "boolean"
     },
     "pointerEvents": {
      "type": "integer",
      "minimum": 0
     },
     "interactionsPerMinute": {
      "type": "number",
      "minimum": 0
     }
    }
   }
  }
 }
}
```
