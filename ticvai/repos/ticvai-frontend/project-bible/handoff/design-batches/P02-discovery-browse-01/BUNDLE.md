# P02-discovery-browse-01 — P02 · Discovery & Browse

**7 screens · 23 operations · 69 schemas · 6 permissions**

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

- **Every control that can be refused must be gated.** 6 permissions apply here:
  `AI_USE, GUEST_VIEW, ORDER_VIEW, PRODUCT_VIEW, TENANT_CONFIGURE, VENUE_MAP_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **13 of these operations work offline**: getBundle, getPerformance, getProduct, getPublishedGuidedChoice, getTenantAppStatus, getVenueMap, getWaitTimes, listContentPages
  — and the rest do not. A surface that looks the same online and off is lying.
- **Offline, every screen shows one banner, the same on web and app:** *"You're offline. Connect to the internet to book, pay, order or join a queue."* The moment the connection drops, on every screen, above the screen's own content. By itself as soon as the connection is back, with a short "Back online" confirmation. **It never** Covers what is already on screen, or appears for a server error — that is the screen's own error state, and a guest told they are offline when the venue is down reconnects for nothing. Each screen's `states.offline` says what stays on screen and what waits.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `GST-001` | Home | listDetail | 13 | 1 | — |
| `GST-002` | Explore | listDetail | 3 | 0 | — |
| `GST-003` | Buy Tickets | listDetail | 5 | 0 | — |
| `GST-004` | Item Detail | listDetail | 7 | 0 | — |
| `GST-005` | What's On | listDetail | 2 | 0 | — |
| `GST-006` | Item Detail – Event / Exhibition | statusTracker | 2 | 0 | — |
| `GST-057` | Accessibility Information | listDetail | 1 | 0 | — |

## Thin screens in this batch

**GST-006 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "GST-001",
  "name": "Home",
  "module": "Discovery & Browse",
  "requiresModule": "marketing",
  "wave": 1,
  "capability": "C02",
  "implementation": {
   "app": "guest-app",
   "route": "/general/home-default",
   "component": "apps/guest-app/src/routes/general/HomeDefaultDashboard.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "isEntryPoint": true,
   "inferred": true,
   "exitTo": [
    "GST-002",
    "GST-003",
    "GST-004",
    "GST-005",
    "GST-006",
    "GST-007",
    "GST-008",
    "GST-009",
    "GST-010",
    "GST-011",
    "GST-012",
    "GST-013",
    "GST-014",
    "GST-015",
    "GST-016",
    "GST-017",
    "GST-018",
    "GST-019",
    "GST-020",
    "GST-021",
    "GST-022",
    "GST-023",
    "GST-024",
    "GST-025",
    "GST-026",
    "GST-027",
    "GST-028",
    "GST-029",
    "GST-030",
    "GST-031",
    "GST-032",
    "GST-033",
    "GST-034",
    "GST-035",
    "GST-036",
    "GST-037",
    "GST-038",
    "GST-039",
    "GST-040",
    "GST-041",
    "GST-042",
    "GST-043",
    "GST-044",
    "GST-045",
    "GST-046",
    "GST-047",
    "GST-048",
    "GST-049",
    "GST-050",
    "GST-051",
    "GST-052",
    "GST-053",
    "GST-054",
    "GST-055",
    "GST-056",
    "GST-057",
    "GST-058",
    "GST-059",
    "GST-061",
    "GST-062",
    "GST-063",
    "GST-068",
    "GST-070",
    "GST-076"
   ],
   "transitions": [
    {
     "to": "GST-002",
     "trigger": "Explore Categories",
     "provenance": "structural — GST-001 is P02's home screen and its exits are its launcher"
    },
    {
     "to": "GST-003",
     "trigger": "Event & Attraction Listing",
     "provenance": "structural — GST-001 is P02's home screen and its exits are its launcher",
     "carries": [
      "eventId"
     ]
    },
    {
     "to": "GST-004",
     "trigger": "Attraction Details",
     "provenance": "structural — GST-001 is P02's home screen and its exits are its launcher",
     "carries": [
      "productId"
     ]
    },
    {
     "to": "GST-005",
     "trigger": "What's On",
     "provenance": "derived — GST-005 declares entryState.params eventId and GST-001 holds none of them, so the edge carries nothing and GST-005 opens cold"
    },
    {
     "to": "GST-006",
     "trigger": "Event / Exhibition Details",
     "carries": [
      "productId"
     ],
     "provenance": "derived — GST-006 declares entryState.params performanceId, productId and GST-001 holds productId, so an edge into it carries them"
    },
    {
     "to": "GST-007",
     "trigger": "Select Date & Time",
     "carries": [
      "eventId"
     ],
     "provenance": "derived — GST-007 declares entryState.params eventId and GST-001 holds eventId, so an edge into it carries them"
    },
    {
     "to": "GST-008",
     "trigger": "Tickets & Add-ons",
     "carries": [
      "productId"
     ],
     "provenance": "derived — GST-008 declares entryState.params performanceId, productId and GST-001 holds productId, so an edge into it carries them"
    },
    {
     "to": "GST-009",
     "trigger": "Review & Payment",
     "carries": [
      "orderId"
     ],
     "provenance": "derived — GST-009 declares entryState.params orderId, paymentId, token and GST-001 holds orderId, so an edge into it carries them"
    },
    {
     "to": "GST-010",
     "trigger": "Booking Confirmation",
     "carries": [
      "orderId"
     ],
     "provenance": "derived — GST-010 declares entryState.params orderId and GST-001 holds orderId, so an edge into it carries them"
    },
    {
     "to": "GST-011",
     "trigger": "Wallet Overview",
     "carries": [
      "subjectId"
     ],
     "provenance": "derived — GST-011 declares entryState.params subjectId, walletId and GST-001 holds subjectId, so an edge into it carries them"
    },
    {
     "to": "GST-012",
     "trigger": "My Tickets",
     "carries": [
      "entitlementId",
      "orderId"
     ],
     "provenance": "derived — GST-012 declares entryState.params entitlementId, orderId and GST-001 holds entitlementId, orderId, so an edge into it carries them"
    },
    {
     "to": "GST-013",
     "trigger": "Ticket Details",
     "carries": [
      "entitlementId",
      "orderId"
     ],
     "provenance": "derived — GST-013 declares entryState.params credentialId, entitlementId, orderId and GST-001 holds entitlementId, orderId, so an edge into it carries them"
    },
    {
     "to": "GST-014",
     "trigger": "Ticket Transfer",
     "carries": [
      "orderId"
     ],
     "provenance": "derived — GST-014 declares entryState.params orderId, transferId and GST-001 holds orderId, so an edge into it carries them"
    },
    {
     "to": "GST-015",
     "trigger": "Memberships",
     "carries": [
      "subjectId"
     ],
     "provenance": "derived — GST-015 declares entryState.params caseId, guestLinkId, statementId, subjectId and GST-001 holds subjectId, so an edge into it carries them"
    },
    {
     "to": "GST-016",
     "trigger": "My Reservations",
     "provenance": "derived — GST-016 declares entryState.params reservationId and GST-001 holds none of them, so the edge carries nothing and GST-016 opens cold"
    },
    {
     "to": "GST-017",
     "trigger": "Reservation Details",
     "provenance": "derived — GST-017 declares entryState.params reservationId and GST-001 holds none of them, so the edge carries nothing and GST-017 opens cold"
    },
    {
     "to": "GST-018",
     "trigger": "Add to Calendar / Reminders",
     "carries": [
      "orderId"
     ],
     "provenance": "derived — GST-018 declares entryState.params orderId and GST-001 holds orderId, so an edge into it carries them"
    },
    {
     "to": "GST-019",
     "trigger": "Order History",
     "carries": [
      "orderId"
     ],
     "provenance": "derived — GST-019 declares entryState.params documentId, invoiceId, orderId and GST-001 holds orderId, so an edge into it carries them"
    },
    {
     "to": "GST-020",
     "trigger": "Saved Items / Wishlist",
     "carries": [
      "subjectId"
     ],
     "provenance": "derived — GST-020 declares entryState.params itemId, subjectId and GST-001 holds subjectId, so an edge into it carries them"
    },
    {
     "to": "GST-021",
     "trigger": "Interactive Map",
     "provenance": "derived — GST-021 declares entryState.params mapId and GST-001 holds none of them, so the edge carries nothing and GST-021 opens cold"
    },
    {
     "to": "GST-023",
     "trigger": "Virtual Queue",
     "provenance": "derived — GST-023 declares entryState.params entryId and GST-001 holds none of them, so the edge carries nothing and GST-023 opens cold"
    },
    {
     "to": "GST-024",
     "trigger": "F&B – Browse & Order",
     "carries": [
      "orderId"
     ],
     "provenance": "derived — GST-024 declares entryState.params orderId, outletId and GST-001 holds orderId, so an edge into it carries them"
    },
    {
     "to": "GST-025",
     "trigger": "F&B – Order Tracking",
     "carries": [
      "orderId"
     ],
     "provenance": "derived — GST-025 declares entryState.params orderId and GST-001 holds orderId, so an edge into it carries them"
    },
    {
     "to": "GST-026",
     "trigger": "Retail / Merchandise",
     "provenance": "derived — GST-026 declares entryState.params cardCode and GST-001 holds none of them, so the edge carries nothing and GST-026 opens cold"
    },
    {
     "to": "GST-027",
     "trigger": "Parking – Reserve & Pay",
     "carries": [
      "entitlementId"
     ],
     "provenance": "derived — GST-027 declares entryState.params entitlementId and GST-001 holds entitlementId, so an edge into it carries them"
    },
    {
     "to": "GST-031",
     "trigger": "AI Concierge – Home",
     "provenance": "derived — GST-031 declares entryState.params conversationId, outletId and GST-001 holds none of them, so the edge carries nothing and GST-031 opens cold"
    },
    {
     "to": "GST-032",
     "trigger": "AI Concierge – Chat",
     "carries": [
      "orderId"
     ],
     "provenance": "derived — GST-032 declares entryState.params conversationId, messageId, orderId and GST-001 holds orderId, so an edge into it carries them"
    },
    {
     "to": "GST-033",
     "trigger": "AI Concierge – Contextual Help",
     "provenance": "derived — GST-033 declares entryState.params conversationId and GST-001 holds none of them, so the edge carries nothing and GST-033 opens cold"
    },
    {
     "to": "GST-034",
     "trigger": "Lost & Found",
     "carries": [
      "orderId"
     ],
     "provenance": "derived — GST-034 declares entryState.params caseId, orderId and GST-001 holds orderId, so an edge into it carries them"
    },
    {
     "to": "GST-037",
     "trigger": "Offers & Promotions",
     "provenance": "derived — GST-037 declares entryState.params code, promotionId and GST-001 holds none of them, so the edge carries nothing and GST-037 opens cold"
    },
    {
     "to": "GST-039",
     "trigger": "Profile",
     "carries": [
      "subjectId"
     ],
     "provenance": "derived — GST-039 declares entryState.params subjectId and GST-001 holds subjectId, so an edge into it carries them"
    },
    {
     "to": "GST-040",
     "trigger": "Help & Support",
     "provenance": "derived — GST-040 declares entryState.params caseId and GST-001 holds none of them, so the edge carries nothing and GST-040 opens cold"
    },
    {
     "to": "GST-041",
     "trigger": "Checkout Entry",
     "carries": [
      "productId"
     ],
     "provenance": "derived — GST-041 declares entryState.params holdId, lineId, performanceId, productId and GST-001 holds productId, so an edge into it carries them"
    },
    {
     "to": "GST-042",
     "trigger": "Simple Registration & OTP",
     "carries": [
      "subjectId"
     ],
     "provenance": "derived — GST-042 declares entryState.params challengeId, subjectId and GST-001 holds subjectId, so an edge into it carries them"
    },
    {
     "to": "GST-045",
     "trigger": "Ticket Delivery & Sharing",
     "carries": [
      "orderId"
     ],
     "provenance": "derived — GST-045 declares entryState.params orderId and GST-001 holds orderId, so an edge into it carries them"
    },
    {
     "to": "GST-046",
     "trigger": "Branded Queue / Waiting Room",
     "provenance": "derived — GST-046 declares entryState.params entryId and GST-001 holds none of them, so the edge carries nothing and GST-046 opens cold"
    },
    {
     "to": "GST-049",
     "trigger": "Interactive Seat Selection",
     "provenance": "derived — GST-049 declares entryState.params eventId, holdId, performanceId and GST-001 holds none of them, so the edge carries nothing and GST-049 opens cold"
    },
    {
     "to": "GST-052",
     "trigger": "Suggested Itineraries",
     "provenance": "derived — GST-052 declares entryState.params  and GST-001 holds none of them, so the edge carries nothing and GST-052 opens cold"
    },
    {
     "to": "GST-054",
     "trigger": "AI Optimized Itinerary",
     "provenance": "derived — GST-054 declares entryState.params conversationId, planId and GST-001 holds none of them, so the edge carries nothing and GST-054 opens cold"
    },
    {
     "to": "GST-055",
     "trigger": "Dynamic QR Ticket",
     "carries": [
      "entitlementId",
      "orderId"
     ],
     "provenance": "derived — GST-055 declares entryState.params credentialId, entitlementId, orderId and GST-001 holds entitlementId, orderId, so an edge into it carries them"
    },
    {
     "to": "GST-056",
     "trigger": "Bundle Package",
     "provenance": "derived — GST-056 declares entryState.params bundleId and GST-001 holds none of them, so the edge carries nothing and GST-056 opens cold"
    },
    {
     "to": "GST-059",
     "trigger": "Plan My Day – In Progress",
     "provenance": "derived — GST-059 declares entryState.params itemId, planId and GST-001 holds none of them, so the edge carries nothing and GST-059 opens cold"
    },
    {
     "to": "GST-061",
     "trigger": "Menu Item Detail",
     "provenance": "derived — GST-061 declares entryState.params outletId and GST-001 holds none of them, so the edge carries nothing and GST-061 opens cold"
    },
    {
     "to": "GST-070",
     "trigger": "Reserve a Table",
     "provenance": "derived — GST-070 declares entryState.params entryId, reservationId and GST-001 holds none of them, so the edge carries nothing and GST-070 opens cold"
    },
    {
     "to": "GST-022",
     "trigger": "Attraction Wait Times",
     "provenance": "structural — GST-001 is P02's home screen and its exits are its launcher"
    },
    {
     "to": "GST-028",
     "trigger": "Parking – Reservation Confirmed",
     "provenance": "structural — GST-001 is P02's home screen and its exits are its launcher",
     "carries": [
      "orderId"
     ]
    },
    {
     "to": "GST-029",
     "trigger": "Venue Info & Services",
     "provenance": "structural — GST-001 is P02's home screen and its exits are its launcher"
    },
    {
     "to": "GST-030",
     "trigger": "In-Venue Notifications",
     "provenance": "structural — GST-001 is P02's home screen and its exits are its launcher"
    },
    {
     "to": "GST-035",
     "trigger": "Feedback & Ratings",
     "provenance": "structural — GST-001 is P02's home screen and its exits are its launcher"
    },
    {
     "to": "GST-036",
     "trigger": "Loyalty & Rewards",
     "provenance": "structural — GST-001 is P02's home screen and its exits are its launcher"
    },
    {
     "to": "GST-038",
     "trigger": "Digital Companion Mode",
     "provenance": "structural — GST-001 is P02's home screen and its exits are its launcher"
    },
    {
     "to": "GST-043",
     "trigger": "Arabic / RTL Experience",
     "provenance": "structural — GST-001 is P02's home screen and its exits are its launcher"
    },
    {
     "to": "GST-044",
     "trigger": "Multi-Currency & Pricing",
     "provenance": "structural — GST-001 is P02's home screen and its exits are its launcher"
    },
    {
     "to": "GST-047",
     "trigger": "Maintenance / Upgrade Page",
     "provenance": "structural — GST-001 is P02's home screen and its exits are its launcher"
    },
    {
     "to": "GST-048",
     "trigger": "Upsell / Cross-Sell",
     "provenance": "structural — GST-001 is P02's home screen and its exits are its launcher"
    },
    {
     "to": "GST-050",
     "trigger": "Resource Booking – Cabana",
     "provenance": "structural — GST-001 is P02's home screen and its exits are its launcher"
    },
    {
     "to": "GST-051",
     "trigger": "Plan Your Adventure – Start",
     "provenance": "structural — GST-001 is P02's home screen and its exits are its launcher"
    },
    {
     "to": "GST-053",
     "trigger": "Build Your Own Itinerary",
     "provenance": "structural — GST-001 is P02's home screen and its exits are its launcher"
    },
    {
     "to": "GST-057",
     "trigger": "Accessibility Information",
     "provenance": "structural — GST-001 is P02's home screen and its exits are its launcher"
    },
    {
     "to": "GST-058",
     "trigger": "Resource Availability (Cabana)",
     "provenance": "structural — GST-001 is P02's home screen and its exits are its launcher"
    },
    {
     "to": "GST-062",
     "trigger": "Shop & Drop Collection",
     "provenance": "structural — GST-001 is P02's home screen and its exits are its launcher"
    },
    {
     "to": "GST-063",
     "trigger": "Search",
     "provenance": "structural — GST-001 is P02's home screen and its exits are its launcher"
    },
    {
     "to": "GST-068",
     "trigger": "Help & My Cases",
     "provenance": "structural — GST-001 is P02's home screen and its exits are its launcher"
    },
    {
     "to": "GST-076",
     "trigger": "Book a trip (a transport venue)",
     "provenance": "decided 29 September, rev 3 REV3-21: the transport venue's home call to action"
    },
    {
     "to": "GST-004",
     "trigger": "Opens a highlight (Item Detail)",
     "carries": [
      "productId"
     ],
     "provenance": "decided 29 September 2026, MOB-3, MOB-4"
    },
    {
     "to": "GST-051",
     "trigger": "Plan tab",
     "provenance": "decided 29 September 2026, MOB-1, MOB-6"
    }
   ],
   "entryFrom": [
    "GST-076"
   ],
   "uses": [
    "appTabs"
   ]
  },
  "notes": "States derived from the screen pattern on 17 August, not individually considered. Purpose derived from the screen name and its operations on 17 August, not from a requirement. Landing. **Declared only a health check.** Pranay asked for guest details and tickets; Chitrangi asked for search. All three existed and none were wired. **Rewired on the 20 August review.** **Venue selection added 28 September** (decided 28 September, audit R267) — a venue picker on first open, remembered on the device, **Change venue**, and a visit-day suggestion from the guest's ticket (`listMyEntitlements`). Nothing in `getTenantAppStatus.venues` supplies the options, the tenant's active venues, public and cacheable.\n\n**Rev 3 (decided 29 September).** The in-venue notifications feed (GST-030) is back in the first release (GAP-C1, reversing audit R242). A transport venue's home opens the trip search (GST-076, REV3-21). The venue picked here (audit R267) is the venue whose booking-flow settings apply; the booking screens' *Booking at* bar changes it (REV3-18). Every booking-flow setting named here is read from `getTenantConfig` `bookingFlow`, resolved for the venue the guest picked (audit R267): the tenant's values with that venue's `venueOverrides` entry laid over field by field (decided 29 September, rev 3 CFG-11).\n\n**Mobile v4 (decided 29 September, MOB-1, MOB-3, MOB-5).** Retitled **Home** and made the Home tab root: hero (carousel, video, poster or split), the venue overview (description, opening hours, info), type tiles and one or two highlights per type; tapping a highlight opens Item Detail (GST-004). GST-005 What's On and GST-029 Venue Info & Services stay and are linked from here. The optional intro video is a first-launch state of this screen, not a screen. The Plan tab (GST-051) is in Block A (29 September re-plan, superseding audit R187 and rev 3 GAP-C3), so its links no longer carry a later-release precondition.",
  "density": "comfortable",
  "pattern": "listDetail",
  "patternReason": "`listMyEntitlements` reads the population and `getTenantAppStatus` reads one of them — list, select, act",
  "purpose": "The Home tab: what this venue is, when it is open and what there is to do, with one or two highlights per type, from which everything else is entered.",
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
       "notes": "**The guest picks a venue on first open** (decided 28 September, audit R267): shown before anything else when the device has no venue remembered, and remembered on the device after that. The chosen `venueId` is what every screen that declares `venueId` `from: session` reads. The options are `getTenantAppStatus.venues` (venue id, name, city, today's opening hours), the tenant's active venues, returned without a session.",
       "provenance": "contract white-label.yaml GET /tenant-config/status (TenantAppStatus.venues, audit R267)"
      },
      {
       "kind": "secondaryButton",
       "label": "Change venue",
       "notes": "Reopens the venue picker; the new choice replaces the remembered one on this device and every venue-scoped screen reloads for it (decided 28 September, audit R267).",
       "provenance": "decided 28 September 2026, audit R267"
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
       "kind": "selectField",
       "label": "State",
       "operation": "listMyEntitlements",
       "notes": "Sends `?state=` to `listMyEntitlements`.",
       "provenance": "contract access.yaml GET /guests/me/entitlements"
      },
      {
       "kind": "toggle",
       "label": "Include shared",
       "operation": "listMyEntitlements",
       "notes": "Sends `?includeShared=` to `listMyEntitlements`.",
       "provenance": "contract access.yaml GET /guests/me/entitlements"
      },
      {
       "kind": "dataTable",
       "label": "Every entitlement",
       "bindsTo": "Entitlement",
       "columns": [
        "Entitlement.id",
        "Entitlement.templateId",
        "Entitlement.productId",
        "Entitlement.orderId",
        "Entitlement.orderLineId",
        "Entitlement.subjectId",
        "Entitlement.venueId",
        "Entitlement.scopePath",
        "Entitlement.mediaCode",
        "Entitlement.status",
        "Entitlement.statusNote",
        "Entitlement.validFrom"
       ],
       "operation": "listMyEntitlements",
       "provenance": "contract access.yaml GET /guests/me/entitlements"
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
       "kind": "banner",
       "label": "Hero",
       "bindsTo": "TenantConfig.homepage",
       "operation": "getTenantConfig",
       "notes": "The venue hero in the style the venue set on the Home section (`heroStyle`: carousel, video, poster or split). Video heroes stream; a missing asset falls back to the poster image.",
       "provenance": "decided 29 September 2026, MOB-3"
      },
      {
       "kind": "detailPanel",
       "label": "Venue overview",
       "bindsTo": "TenantAppStatus.venues",
       "operation": "getTenantAppStatus",
       "notes": "**Home is a venue overview** (MOB-3): the venue description, today's opening hours (from `getTenantAppStatus.venues`), getting here and before-you-go info.",
       "provenance": "decided 29 September 2026, MOB-3"
      },
      {
       "kind": "cardList",
       "label": "Type tiles",
       "operation": "listProductCategories",
       "notes": "Rides, dining, events and shops (the venue's own categories). A tile opens Explore (GST-002) on that type.",
       "provenance": "decided 29 September 2026, MOB-3"
      },
      {
       "kind": "cardList",
       "label": "Highlights per type",
       "operation": "listProducts",
       "notes": "One or two items per type (`itemsPerSection`, 1-2, set on CMS-007); a highlight opens Item Detail (GST-004). Each card shows its own primary image or clip (`Product.media`).",
       "provenance": "decided 29 September 2026, MOB-3"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected entitlement",
       "bindsTo": "Entitlement",
       "columns": [
        "Entitlement.id",
        "Entitlement.templateId",
        "Entitlement.productId",
        "Entitlement.orderId",
        "Entitlement.orderLineId",
        "Entitlement.subjectId",
        "Entitlement.venueId",
        "Entitlement.scopePath",
        "Entitlement.mediaCode",
        "Entitlement.status",
        "Entitlement.statusNote",
        "Entitlement.validFrom",
        "Entitlement.validTo",
        "Entitlement.entriesUsed",
        "Entitlement.entriesAllowed",
        "Entitlement.lastEntryAt"
       ],
       "operation": "listMyEntitlements",
       "provenance": "contract access.yaml GET /guests/me/entitlements"
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
    }
   ]
  },
  "states": {
   "loading": "The home default list.",
   "error": "Could not load. Names which read failed and leaves the home default untouched.",
   "emptyFirstRun": "No home default yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table.",
   "emptyNoResults": "Nothing matches the filter on state, includeShared and the home default are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `GUEST_VIEW`, which `getGuestProfile` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "**The offline banner shows.** What was already loaded stays on screen, marked with its age. Anything that spends money, holds capacity or changes the account waits for the connection, and its button says so rather than failing.",
   "introVideo": "First-launch state (MOB-5): the intro video overlay plays over Home while Home loads behind it; Skip introduction reveals Home."
  },
  "apis": [
   {
    "operationId": "getTenantAppStatus",
    "contract": "white-label",
    "purpose": "App status and recent changes",
    "trigger": "onLoad"
   },
   {
    "operationId": "getGuestProfile",
    "contract": "marketing-crm",
    "purpose": "Read a guest profile",
    "trigger": "onLoad"
   },
   {
    "operationId": "listMyEntitlements",
    "contract": "access",
    "purpose": "Every ticket, pass and membership this guest holds; on a visit day, the ticket's venue is suggested (decided 28 September, audit R267)",
    "trigger": "onLoad"
   },
   {
    "operationId": "searchCatalogue",
    "contract": "catalogue",
    "purpose": "Find something by name",
    "trigger": "onAction"
   },
   {
    "operationId": "getTenantConfig",
    "contract": "white-label",
    "purpose": "Branding, currency and what this venue enables",
    "trigger": "onLoad"
   },
   {
    "operationId": "getCookieConsentRuntime",
    "contract": "marketing-crm",
    "purpose": "Tracking consent prompt on first launch and the SDK gate",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "recordDeviceConsent",
    "contract": "marketing-crm",
    "purpose": "Accept, reject or customise tracking on first launch",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "listAnalyticsProviders",
    "contract": "white-label",
    "purpose": "Analytics SDKs to start once their consent category is granted",
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
    "purpose": "App-shell beacon of hashed browsing behaviour for fraud prevention",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "listProducts",
    "contract": "catalogue",
    "purpose": "One or two highlights per type (rides, dining, events, shops) for the Home sections (MOB-3)",
    "trigger": "onLoad",
    "provenance": "decided 29 September 2026, MOB-3"
   },
   {
    "operationId": "listProductCategories",
    "contract": "catalogue",
    "purpose": "The type tiles on Home (rides, dining, events, shops)",
    "trigger": "onLoad",
    "provenance": "decided 29 September 2026, MOB-3"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "subjectId",
     "from": "session"
    }
   ],
   "coldEntry": "Resolves from the session; a cold arrival is the ordinary case. **The venue comes from the device** (decided 28 September, audit R267): on first open the guest picks one, it is remembered on the device and changeable from this screen, and on a visit day the ticket's venue is suggested. Every guest screen that declares `venueId` `from: session` reads that remembered choice.",
   "preloaded": [
    "Entitlement.id",
    "Entitlement.templateId",
    "Entitlement.productId",
    "Entitlement.orderId",
    "Entitlement.orderLineId"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "client-verified",
   "board": "wireframes/P02 Guest App.dc.html#gst-001",
   "prototype": {
    "file": "sources/designs/guest-rev3-29-september/TICVAI Mobile App v4.dc.html",
    "rev": "mobile v4 (29 September build)",
    "verified": "2026-09-30",
    "match": "exact",
    "view": "Home tab (Summit Peaks, after the intro)",
    "differences": "The v4 home shows no ticket strip; `listMyEntitlements` feeds the visit-day venue suggestion only."
   }
  },
  "apisNote": "Rebuilt 9 September 2026 from the 4 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "introVideo",
    "component": "modal",
    "trigger": "App start, when `BrandIdentity.introVideoMode` is `firstLaunch` (first open on this device) or `everyLaunch`; never when it is `off` (the default)",
    "body": "The venue's intro video, full screen and muted, streamed from `BrandIdentity.introVideoAssetRef` so a new video needs no app rebuild. **Skip introduction** is always shown; the video ending has the same effect.",
    "bindsTo": "TenantConfig.brand",
    "dismiss": {
     "label": "Skip introduction",
     "to": "GST-001",
     "carries": [],
     "discards": [
      "the rest of the video"
     ]
    },
    "provenance": "decided 29 September 2026, MOB-5; mobile v4 prototype, launch screen"
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
  "id": "GST-002",
  "name": "Explore",
  "module": "Discovery & Browse",
  "requiresModule": "ticketing",
  "wave": 1,
  "capability": "C02",
  "implementation": {
   "app": "guest-app",
   "route": "/general/explore-categories",
   "component": "apps/guest-app/src/routes/general/ExploreCategoriesList.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "GST-001"
   ],
   "inferred": true,
   "exitTo": [
    "GST-001",
    "GST-003",
    "GST-004",
    "GST-063"
   ],
   "transitions": [
    {
     "to": "GST-001",
     "trigger": "Home – Default",
     "provenance": "derived — GST-001 declares entryState.params  and GST-002 holds none of them, so the edge carries nothing and GST-001 opens cold"
    },
    {
     "to": "GST-003",
     "trigger": "Event & Attraction Listing",
     "provenance": "derived — GST-003 declares entryState.params eventId and GST-002 holds none of them, so the edge carries nothing and GST-003 opens cold"
    },
    {
     "to": "GST-004",
     "trigger": "Attraction Details",
     "carries": [
      "productId"
     ],
     "provenance": "derived — GST-004 declares entryState.params bundleId, eventId, productId and GST-002 holds productId, so an edge into it carries them"
    },
    {
     "to": "GST-063",
     "trigger": "Searches (results in place)",
     "provenance": "decided 29 September 2026, MOB-1"
    }
   ],
   "uses": [
    "appTabs"
   ]
  },
  "notes": "States derived from the screen pattern on 17 August, not individually considered. Purpose derived from the screen name and its operations on 17 August, not from a requirement.\n\n**Rev 3 (decided 29 September).** Category → subcategory tiles or a flat list per `ticketCategories` (REV3-16); grid or row per `cardLayout` (the retired `categoryDisplay` is removed, W7). Info-only products are listed with their label and open details (REV3-14). Every booking-flow setting named here is read from `getTenantConfig` `bookingFlow`, resolved for the venue the guest picked (audit R267): the tenant's values with that venue's `venueOverrides` entry laid over field by field (decided 29 September, rev 3 CFG-11).\n\n**Mobile v4 (decided 29 September, MOB-1).** Retitled **Explore** and made the Explore tab root: search, category tiles and inline video previews. **GST-063 Search is its search-results state: one implementation, both ids kept** (as GAP-D3). Rows versus grid is `cardLayout`; `categoryDisplay` is retired (W7).",
  "density": "comfortable",
  "pattern": "listDetail",
  "patternReason": "`listProducts` reads a population and nothing reads one of them; the detail is the row until a `get` exists",
  "purpose": "The Explore tab: search the venue, browse its categories and preview items before opening one.",
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
       "notes": "`BookingFlowConfig.ticketCategories` `categoryThenSubcategory` (default): the category tiles, then that category's products (`listProducts?categoryId=`); `flatList` skips them. Grid or one scrolling row per `cardLayout` (W7).",
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
       "kind": "searchField",
       "label": "Search the venue",
       "operation": "searchCatalogue",
       "notes": "Sends `?q=` to `searchCatalogue`; results replace the tiles in place (GST-063, the same implementation).",
       "provenance": "decided 29 September 2026, MOB-1"
      },
      {
       "kind": "cardList",
       "label": "Inline video previews",
       "operation": "listProducts",
       "notes": "Cards play the product's own short clip muted in place (`Product.media` kind video, M17-10) and show the primary image otherwise; a card opens Item Detail (GST-004).",
       "provenance": "decided 29 September 2026, MOB-1"
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
       "operation": "listProducts",
       "provenance": "contract catalogue.yaml GET /products"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The explore categories list.",
   "error": "Could not load. Names which read failed and leaves the explore categories untouched.",
   "emptyFirstRun": "No explore categories yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table.",
   "emptyNoResults": "Nothing matches the filter on venueId, kind, isSellable and the explore categories are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `PRODUCT_VIEW`, which `listProducts` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
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
    "operationId": "listProductCategories",
    "contract": "catalogue",
    "purpose": "The category tiles (a tree, with images and descriptions)",
    "trigger": "onLoad"
   },
   {
    "operationId": "searchCatalogue",
    "contract": "catalogue",
    "purpose": "Search from the top of Explore; results are GST-063, a state of this screen",
    "trigger": "onAction",
    "provenance": "decided 29 September 2026, MOB-1"
   }
  ],
  "entryState": {
   "preloaded": [
    "Product.id",
    "Product.code",
    "Product.name",
    "Product.description",
    "Product.kind"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "client-verified",
   "board": "wireframes/P02 Guest App.dc.html#gst-002",
   "prototype": {
    "file": "sources/designs/guest-rev3-29-september/TICVAI Mobile App v4.dc.html",
    "rev": "mobile v4 (29 September build)",
    "verified": "2026-09-30",
    "match": "exact",
    "view": "Explore tab"
   }
  },
  "apisNote": "Rebuilt 9 September 2026 from the 1 operation this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
  "id": "GST-003",
  "name": "Buy Tickets",
  "module": "Discovery & Browse",
  "requiresModule": "ticketing",
  "wave": 1,
  "capability": "C02",
  "implementation": {
   "app": "guest-app",
   "route": "/general/attractions-list",
   "component": "apps/guest-app/src/routes/general/AttractionsList.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "GST-001"
   ],
   "inferred": true,
   "exitTo": [
    "GST-001",
    "GST-002",
    "GST-004",
    "GST-007",
    "GST-008",
    "GST-074",
    "GST-075",
    "GST-056"
   ],
   "fromFlows": true,
   "transitions": [
    {
     "to": "GST-001",
     "trigger": "Home – Default",
     "provenance": "derived — GST-001 declares entryState.params  and GST-003 holds none of them, so the edge carries nothing and GST-001 opens cold"
    },
    {
     "to": "GST-004",
     "trigger": "Attraction Details",
     "carries": [
      "eventId",
      "productId"
     ],
     "provenance": "derived — GST-004 declares entryState.params bundleId, eventId, productId and GST-003 holds eventId, productId, so an edge into it carries them"
    },
    {
     "to": "GST-007",
     "trigger": "Book (a dated product: date, then time, then tickets)",
     "carries": [
      "productId"
     ],
     "provenance": "decided 29 September 2026, MOB-2"
    },
    {
     "to": "GST-008",
     "trigger": "Book (an undated product, or a product-first flow such as a workshop)",
     "carries": [
      "productId"
     ],
     "provenance": "decided 29 September 2026, MOB-2, W8"
    },
    {
     "to": "GST-074",
     "trigger": "Book (a spot on the venue map, where the flow picks on the map)",
     "carries": [
      "productId"
     ],
     "provenance": "decided 29 September 2026, MOB-2, W6"
    },
    {
     "to": "GST-075",
     "trigger": "Book (a space by the hour)",
     "carries": [
      "productId"
     ],
     "provenance": "decided 29 September 2026, MOB-2, W9"
    },
    {
     "to": "GST-056",
     "trigger": "Book a bundle (e.g. meal combo with admission)",
     "provenance": "decided 29 September 2026, MOB-2, MOB-4"
    },
    {
     "to": "BO-005",
     "trigger": "A supervisor sees the queue building",
     "provenance": "flow F21 step 2→3",
     "crossesDevice": true,
     "back": false,
     "carries": [
      "queueId"
     ]
    }
   ]
  },
  "notes": "States derived from the screen pattern on 17 August, not individually considered. Purpose derived from the screen name and its operations on 17 August, not from a requirement. **Cross-platform navigation removed 24 August**: BO-005. **A till does not navigate to a back office and a guest app does not navigate to either** — those are device handovers, and a flow declares them with `crossesDevice` rather than a screen pretending there is a link. **Renamed 31 August** from *Attractions List*. **A guest surface is one product with two renderings** — a screen named differently on web and app is two screens to a developer and one journey to a guest. **Cross-surface parity, 31 August**: added listPerformances, searchCatalogue. **A guest does not know which surface they are on** — the same named screen on web and app now calls the same guest-callable operations.\n\n**Rev 3 (decided 29 September).** **Info-only products** (`Product.guestListing` `infoOnly`) show `notBookableLabel` (default *Info only / Not bookable online*) and open their details instead of adding to the basket; hidden when `BookingFlowConfig.showInfoOnly` is off (REV3-14). Categories per `ticketCategories` (REV3-16). Each product shows its own primary image (`Product.media`, 23SEP-4). Card layout, size and density are the enums of DG-6. Every booking-flow setting named here is read from `getTenantConfig` `bookingFlow`, resolved for the venue the guest picked (audit R267): the tenant's values with that venue's `venueOverrides` entry laid over field by field (decided 29 September, rev 3 CFG-11).\n\n**Mobile v4 (decided 29 September, MOB-2).** Retitled **Buy Tickets**: every bookable product and flow (cabanas, surf, transport and the rest stay available, MOB-1). The persistent Buy tickets button of the app shell opens it from any screen except the booking and checkout steps. The booking steps behind it are unchanged and follow the published booking flow (W12). **W4:** Help me choose filters this list (`listProducts` `guidedAnswerIds`) with a *Show everything* link. **W3:** info-only products show Call sales / Email sales instead of Book.",
  "density": "comfortable",
  "pattern": "listDetail",
  "patternReason": "`listProducts` reads the population and `getWaitTimes` reads one of them — list, select, act",
  "purpose": "Every bookable product and booking flow of the venue, one tap from any screen.",
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
       "kind": "banner",
       "label": "Help me choose",
       "operation": "getPublishedGuidedChoice",
       "notes": "**Help me choose filters the list** (W4): the answers are sent as `guidedAnswerIds` to `listProducts` and only the suitable products stay; `GuidedChoice.behaviour` `recommend` opens one product instead. It is never a consent step.",
       "provenance": "decided 29 September 2026, W4"
      },
      {
       "kind": "secondaryButton",
       "label": "Show everything",
       "operation": "listProducts",
       "notes": "Clears the Help me choose filter and lists every product again (`GuidedChoice.showEverything`, on by default).",
       "provenance": "decided 29 September 2026, W4"
      },
      {
       "kind": "cardList",
       "label": "Contact sales",
       "bindsTo": "Product.salesContact",
       "operation": "listProducts",
       "notes": "**View-only products** (W3): a product with `guestListing` `infoOnly` shows its details and, instead of Book, **Call sales** and **Email sales** from `Product.salesContact` (the venue contact when it has none). Hidden when `showInfoOnly` is off.",
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
   "emptyNoAccess": "Shown when the caller lacks `PRODUCT_VIEW`, which `listProducts` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
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
    "operationId": "getWaitTimes",
    "contract": "queue",
    "purpose": "Wait times across a venue",
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
    "operationId": "getPublishedGuidedChoice",
    "contract": "white-label",
    "purpose": "Help me choose: the venue's questions whose answers filter this list (W4)",
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
   "coldEntry": "**Named, expired or withdrawn — never a 404** (ADR-0030). A guest holding a link that no longer resolves did nothing wrong; the screen says what happened and offers the list it came from.",
   "preloaded": [
    "WaitTime.queueId",
    "WaitTime.queueName",
    "WaitTime.attractionProductId",
    "WaitTime.status",
    "WaitTime.waitMinutes"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "client-verified",
   "board": "wireframes/P02 Guest App.dc.html#gst-003",
   "prototype": {
    "file": "sources/designs/guest-rev3-29-september/TICVAI Mobile App v4.dc.html",
    "rev": "mobile v4 (29 September build)",
    "verified": "2026-09-30",
    "match": "exact",
    "view": "Buy tickets (the centre tab)"
   }
  },
  "apisNote": "Rebuilt 9 September 2026 from the 4 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
  "id": "GST-004",
  "name": "Item Detail",
  "module": "Discovery & Browse",
  "requiresModule": "ticketing",
  "wave": 1,
  "capability": "C02",
  "implementation": {
   "app": "guest-app",
   "route": "/general/attraction-details",
   "component": "apps/guest-app/src/routes/general/AttractionDetailsDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "GST-001",
    "GST-002",
    "GST-003"
   ],
   "inferred": true,
   "exitTo": [
    "GST-001",
    "GST-002",
    "GST-003",
    "GST-007",
    "GST-008",
    "GST-049",
    "GST-074",
    "GST-075",
    "GST-056",
    "GST-038"
   ],
   "transitions": [
    {
     "to": "GST-001",
     "trigger": "Home – Default",
     "provenance": "derived — GST-001 declares entryState.params  and GST-004 holds none of them, so the edge carries nothing and GST-001 opens cold"
    },
    {
     "to": "GST-003",
     "trigger": "Event & Attraction Listing",
     "carries": [
      "eventId"
     ],
     "provenance": "derived — GST-003 declares entryState.params eventId and GST-004 holds eventId, so an edge into it carries them"
    },
    {
     "to": "GST-007",
     "trigger": "Book (a dated product: date, then time, then tickets)",
     "carries": [
      "eventId"
     ],
     "provenance": "decided 29 September, rev 3 REV3-2"
    },
    {
     "to": "GST-008",
     "trigger": "Book (an undated product: tickets straight away)",
     "carries": [
      "productId"
     ],
     "provenance": "decided 29 September, rev 3 REV3-2 and GAP-D3"
    },
    {
     "to": "GST-049",
     "trigger": "Book (a fixture with one on-sale performance opens straight on the seat map)",
     "carries": [
      "performanceId"
     ],
     "provenance": "decided 29 September, rev 3 23SEP-16 and REV3-4"
    },
    {
     "to": "GST-074",
     "trigger": "Book (a cabana, lounger or other spot on the venue map)",
     "carries": [
      "productId"
     ],
     "provenance": "decided 29 September, rev 3 REV3-15 and GAP-C2"
    },
    {
     "to": "GST-075",
     "trigger": "Book (a space sold by the hour)",
     "carries": [
      "productId"
     ],
     "provenance": "decided 29 September, rev 3 REV3-13"
    },
    {
     "to": "GST-056",
     "trigger": "Buy meal combo (a bundle that includes admission)",
     "carries": [
      "bundleId"
     ],
     "provenance": "decided 29 September 2026, MOB-4"
    },
    {
     "to": "GST-038",
     "trigger": "Show on the map (At the Venue, Map view)",
     "provenance": "decided 29 September 2026, MOB-4"
    }
   ]
  },
  "notes": "States derived from the screen pattern on 17 August, not individually considered. Purpose derived from the screen name and its operations on 17 August, not from a requirement. **Cross-surface parity, 31 August**: added listPerformances. **A guest does not know which surface they are on** — the same named screen on web and app now calls the same guest-callable operations.\n\n**Rev 3 (decided 29 September).** Ticket tags (23SEP-3) and the product's own photo or video (23SEP-4); an info-only product shows its label and no Book (REV3-14). Book goes to the date and time (GST-007) for a dated product (REV3-2), straight to the seat map for a single-performance fixture (23SEP-16, REV3-4), to the map booking for a spot on a venue map (GST-074, REV3-15), or to the space booking (GST-075, REV3-13). Help me choose sits on the booking step (GST-008), not here (REV3-11). The event banner lists dates only when `eventBannerDates` is on (23SEP-19).\n\n**Mobile v4 (decided 29 September, MOB-4).** GST-004 and GST-006 become one **Item Detail** screen for rides, shows, restaurants and shops: **one implementation, both ids kept** (as GAP-D3). Gallery, the 2D/3D map pin (`getVenueMap`) and a product card from `VenuePoint.featuredOffer` (product or bundle). *Buy meal combo* adds the required admission because the bundle carries it. **W3:** an info-only product shows Call sales / Email sales instead of Book.\n\n**Video plays directly (client meeting 30 September, MoM 4.8, Qossai; agreed by Chinmay).** On a ride or attraction the info button reveals the details and plays the video straight away; the loader that stood in front of it is removed. While the video buffers its poster frame shows; a video that cannot play leaves the poster and the details, never an error screen.",
  "density": "comfortable",
  "pattern": "listDetail",
  "patternReason": "`listPerformances` reads the population and `getProduct` reads one of them — list, select, act",
  "purpose": "One detail screen for a ride, show, restaurant or shop: what it is, where it is on the map, and the product to buy for it.",
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
       "kind": "cardList",
       "label": "Ticket tags",
       "bindsTo": "Product.displayTags",
       "notes": "Up to six tags with an icon by kind (clock, height, free, calendar, id); derived on read where the product has none. Only when `BookingFlowConfig.ticketTags` is on.",
       "operation": "getProduct",
       "provenance": "decided 29 September, rev 3 23SEP-3"
      },
      {
       "kind": "detailPanel",
       "label": "Photo and video",
       "bindsTo": "Product.media",
       "notes": "**The video plays directly, with no loader in front of it** (client meeting 30 September, MoM 4.8, Qossai; agreed by Chinmay). The info button reveals the ride details and starts the primary video in place, as the header video does elsewhere; while it buffers the poster frame (the primary image, or the video's first frame) shows, never a spinner or loading screen. Read more opens on the primary video or photo.",
       "operation": "getProduct",
       "provenance": "decided 29 September, rev 3 23SEP-4; decided 30 September 2026, client meeting MoM 4.8 (Qossai)"
      },
      {
       "kind": "detailPanel",
       "label": "Gallery",
       "bindsTo": "VenuePoint",
       "columns": [
        "VenuePoint.description",
        "VenuePoint.media"
       ],
       "operation": "getVenueMap",
       "notes": "Photos and clips from `VenuePoint.media` (else `Product.media`), with the point's description. A clip plays in place from its poster frame, with no loader (client meeting 30 September, MoM 4.8).",
       "provenance": "decided 29 September 2026, MOB-4"
      },
      {
       "kind": "seatMap",
       "label": "Where it is",
       "operation": "getVenueMap",
       "notes": "The item's pin on the venue map, 2D or 3D per the venue; tapping it opens At the Venue on the Map view (GST-038 / GST-021) with directions.",
       "provenance": "decided 29 September 2026, MOB-4"
      },
      {
       "kind": "cardList",
       "label": "The product for it",
       "bindsTo": "VenuePoint.featuredOffer",
       "operation": "getBundle",
       "notes": "**The right product** (MOB-4): `VenuePoint.featuredOffer` names a product (`getProduct`) or a bundle (`getBundle`), on any kind of point. A restaurant proposes **Buy meal combo**: a bundle with an admission component and a meal component, so the park ticket is included and checkout is about three steps (GST-056 → GST-041).",
       "provenance": "decided 29 September 2026, MOB-4"
      },
      {
       "kind": "secondaryButton",
       "label": "Call sales / Email sales",
       "bindsTo": "Product.salesContact",
       "operation": "getProduct",
       "notes": "**View-only product** (W3): with `guestListing` `infoOnly` there is no Book; the sales contact from `Product.salesContact` (phone, email, note; the venue contact when absent) is shown instead.",
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
    }
   ]
  },
  "states": {
   "loading": "**The video is not part of loading** (client meeting 30 September, MoM 4.8): the attraction renders as it arrives and no loader or loading screen is ever drawn over the video.",
   "videoBuffering": "**Poster frame, not a loader** (client meeting 30 September, MoM 4.8): from the info button until the first frames arrive the ride's poster (primary image, else the video's first frame) fills the video area and playback starts in place as soon as it can; no spinner, overlay or blocking screen. The details beside it stay usable throughout.",
   "videoUnavailable": "The video cannot play (no video, a failed stream, data saver on). The poster stays and the details are unaffected; no error screen and no loader.",
   "error": "Could not load. Names which read failed and leaves the attraction untouched.",
   "emptyFirstRun": "No attraction yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table.",
   "emptyNoResults": "Nothing matches the filter on from, to and the attraction are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `PRODUCT_VIEW`, which `getProductEligibilityRule` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
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
   },
   {
    "operationId": "listPerformances",
    "contract": "catalogue",
    "purpose": "List performances of an event",
    "trigger": "onLoad"
   },
   {
    "operationId": "getVenueMap",
    "contract": "venue-map",
    "purpose": "The item's point on the 2D/3D venue map, with its description, media and featured offer (MOB-4)",
    "trigger": "onLoad",
    "provenance": "decided 29 September 2026, MOB-4"
   },
   {
    "operationId": "getBundle",
    "contract": "promotions",
    "purpose": "The featured offer when it is a bundle, e.g. meal combo with admission (MOB-4)",
    "trigger": "onLoad",
    "provenance": "decided 29 September 2026, MOB-4"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "productId",
     "from": "deepLink"
    },
    {
     "name": "eventId",
     "from": "deepLink"
    },
    {
     "name": "mapId",
     "from": "session",
     "optional": true
    },
    {
     "name": "bundleId",
     "from": "navigation",
     "optional": true
    }
   ],
   "coldEntry": "**A shared product link after the product retired.** Shows what replaced it where a successor exists, and the catalogue where none does.",
   "preloaded": [
    "Performance.id",
    "Performance.eventId",
    "Performance.startsAt",
    "Performance.endsAt",
    "Performance.approvalRequestId"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "client-verified",
   "board": "wireframes/P02 Guest App.dc.html#gst-004",
   "prototype": {
    "file": "sources/designs/guest-rev3-29-september/TICVAI Mobile App v4.dc.html",
    "rev": "mobile v4 (29 September build)",
    "verified": "2026-09-30",
    "match": "exact",
    "view": "Explore → Summit Coaster (Item detail)"
   }
  },
  "apisNote": "Rebuilt 9 September 2026 from the 4 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
  "id": "GST-005",
  "name": "What's On",
  "module": "Discovery & Browse",
  "requiresModule": "ticketing",
  "wave": 1,
  "capability": "C84",
  "implementation": {
   "app": "guest-app",
   "route": "/general/whats-on",
   "component": "apps/guest-app/src/routes/general/WhatsOnList.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "GST-001"
   ],
   "inferred": true,
   "exitTo": [
    "GST-001",
    "GST-002",
    "GST-003"
   ],
   "transitions": [
    {
     "to": "GST-001",
     "trigger": "Home – Default",
     "provenance": "derived — GST-001 declares entryState.params  and GST-005 holds none of them, so the edge carries nothing and GST-001 opens cold"
    },
    {
     "to": "GST-003",
     "trigger": "Event & Attraction Listing",
     "carries": [
      "eventId"
     ],
     "provenance": "derived — GST-003 declares entryState.params eventId and GST-005 holds eventId, so an edge into it carries them"
    }
   ]
  },
  "notes": "States derived from the screen pattern on 17 August, not individually considered. Purpose derived from the screen name and its operations on 17 August, not from a requirement. **Drawn 31 August** — `Guest Mobile Board 1.dc.html` frame `gm-1b`. **Matched on frame title against screen name, constrained to this board’s platforms.** These packs label by board position (`GM-6C`) rather than naming the screen, so the title is the only join — *What's On* matched at 1.0. **A cross-platform title match was refused**: `Outlet Management` scored 0.85 against a partner-portal screen, which is how a mapping goes wrong quietly.",
  "density": "comfortable",
  "boardFrames": [
   "Guest Mobile Board 1.dc.html#gm-1b"
  ],
  "pattern": "listDetail",
  "patternReason": "`listPerformances` reads a population and nothing reads one of them; the detail is the row until a `get` exists",
  "purpose": "Find what's on for this venue.",
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
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The what's list.",
   "error": "Could not load. Names which read failed and leaves the what's untouched.",
   "emptyFirstRun": "No what's yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table.",
   "emptyNoResults": "Nothing matches the filter on from, to and the what's are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `PRODUCT_VIEW`, which `listPerformances` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "**The offline banner shows.** What was already loaded stays on screen, marked with its age. Anything that spends money, holds capacity or changes the account waits for the connection, and its button says so rather than failing."
  },
  "apis": [
   {
    "operationId": "listPerformances",
    "contract": "catalogue",
    "purpose": "List performances of an event",
    "trigger": "onLoad"
   },
   {
    "operationId": "listProducts",
    "contract": "catalogue",
    "purpose": "List products",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "eventId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A guest arriving cold on a link that no longer resolves is shown what happened and one way onward — never a 404.** A shared ticket, a forwarded confirmation and a push notification opened three weeks late all land here, and the person holding the link did nothing wrong. **The screen names the thing, says it is expired, cancelled or withdrawn, and offers the list it came from.** Arrives with `eventId`.",
   "preloaded": [
    "Performance.id",
    "Performance.eventId",
    "Performance.startsAt",
    "Performance.endsAt",
    "Performance.approvalRequestId"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "client-verified",
   "board": "wireframes/P02 Guest App.dc.html#gst-005",
   "prototype": {
    "file": "sources/designs/guest-rev3-28-september/TICVAI Guest Booking Mobile v2.dc.html",
    "rev": "rev 3",
    "verified": "2026-09-28",
    "match": "exact",
    "view": "Account → All screens → Wave 1 → What’s on"
   },
   "derivedFrom": "wireframes/reference/Guest Mobile Board 1.dc.html",
   "note": "**Drawn by Claude Design on `Guest Mobile Board 1.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
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
  "id": "GST-006",
  "name": "Item Detail – Event / Exhibition",
  "module": "Discovery & Browse",
  "requiresModule": "ticketing",
  "wave": 1,
  "capability": "C84",
  "implementation": {
   "app": "guest-app",
   "route": "/general/event-exhibition-details",
   "component": "apps/guest-app/src/routes/general/EventExhibitionDetailsDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "GST-001"
   ],
   "inferred": true,
   "exitTo": [
    "GST-001",
    "GST-002",
    "GST-003",
    "GST-007"
   ],
   "transitions": [
    {
     "to": "GST-001",
     "trigger": "Home – Default",
     "provenance": "derived — GST-001 declares entryState.params  and GST-006 holds none of them, so the edge carries nothing and GST-001 opens cold"
    },
    {
     "to": "GST-003",
     "trigger": "Event & Attraction Listing",
     "carries": [
      "eventId"
     ],
     "provenance": "derived — GST-003 declares entryState.params eventId and GST-006 holds eventId, so an edge into it carries them"
    },
    {
     "to": "GST-007",
     "trigger": "Book (date, then time, then tickets)",
     "carries": [
      "productId"
     ],
     "provenance": "decided 29 September 2026, MOB-4, W12"
    }
   ]
  },
  "notes": "States derived from the screen pattern on 17 August, not individually considered. Purpose derived from the screen name and its operations on 17 August, not from a requirement.\n\n**Mobile v4 (decided 29 September, MOB-4).** The event and exhibition reading of **Item Detail**: **one implementation with GST-004, both ids kept** (as GAP-D3). Book follows the event's published booking flow (W12).",
  "density": "comfortable",
  "pattern": "statusTracker",
  "patternReason": "`getPerformance` reads one record and nothing reads a population — the screen is about that one thing",
  "purpose": "See event / exhibition details for this venue.",
  "layout": {
   "template": "detail",
   "regions": [
    {
     "name": "contentBody",
     "slot": "record",
     "components": [
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
    }
   ]
  },
  "states": {
   "loading": "The event exhibition, read by `getPerformance`.",
   "error": "Could not load. Names which read failed and leaves the event exhibition untouched.",
   "emptyFirstRun": "No event exhibition yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table.",
   "emptyNoAccess": "Shown when the caller lacks `PRODUCT_VIEW`, which `getPerformance` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "**The offline banner shows.** What was already loaded stays on screen, marked with its age. Anything that spends money, holds capacity or changes the account waits for the connection, and its button says so rather than failing."
  },
  "apis": [
   {
    "operationId": "getPerformance",
    "contract": "catalogue",
    "purpose": "Read a performance",
    "trigger": "onLoad"
   },
   {
    "operationId": "getProduct",
    "contract": "catalogue",
    "purpose": "Read a product",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "performanceId",
     "from": "deepLink"
    },
    {
     "name": "productId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A link to a performance that has happened.** Offers the next performance of the same event. **A shared product link after the product retired.** Shows what replaced it where a successor exists, and the catalogue where none does."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "client-verified",
   "board": "wireframes/P02 Guest App.dc.html#gst-006",
   "prototype": {
    "file": "sources/designs/guest-rev3-29-september/TICVAI Mobile App v4.dc.html",
    "rev": "mobile v4 (29 September build)",
    "verified": "2026-09-30",
    "match": "exact",
    "view": "Explore → Shows → Night of Nine → More info (Item detail, an event)"
   }
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
  "id": "GST-057",
  "name": "Accessibility Information",
  "module": "Discovery & Browse",
  "requiresModule": "core",
  "wave": 2,
  "capability": "C17",
  "implementation": {
   "app": "guest-app",
   "route": "/general/accessibility-information",
   "component": "apps/guest-app/src/routes/general/AccessibilityInformationForm.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "GST-001"
   ],
   "inferred": true,
   "exitTo": [
    "GST-001",
    "GST-002",
    "GST-003"
   ],
   "transitions": [
    {
     "to": "GST-001",
     "trigger": "Home – Default",
     "provenance": "derived — GST-001 declares entryState.params  and GST-057 holds none of them, so the edge carries nothing and GST-001 opens cold"
    },
    {
     "to": "GST-003",
     "trigger": "Event & Attraction Listing",
     "provenance": "derived — GST-003 declares entryState.params eventId and GST-057 holds none of them, so the edge carries nothing and GST-003 opens cold"
    }
   ]
  },
  "notes": "Minuted 10 Aug §4.1: custom content pages *\"with accessibility-guideline compliance to be followed\"*. **Tenant-authored content, not a built feature.**",
  "density": "comfortable",
  "pattern": "listDetail",
  "patternReason": "`listContentPages` reads a population and nothing reads one of them; the detail is the row until a `get` exists",
  "purpose": "Step-free routes, facilities and what to expect.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "textField",
       "label": "Status",
       "operation": "listContentPages",
       "notes": "Sends `?status=` to `listContentPages`.",
       "provenance": "contract white-label.yaml GET /tenant-config/pages"
      },
      {
       "kind": "textField",
       "label": "Category code",
       "operation": "listContentPages",
       "notes": "Sends `?categoryCode=` to `listContentPages`.",
       "provenance": "contract white-label.yaml GET /tenant-config/pages"
      },
      {
       "kind": "textField",
       "label": "Slug",
       "operation": "listContentPages",
       "notes": "Sends `?slug=` to `listContentPages`.",
       "provenance": "contract white-label.yaml GET /tenant-config/pages"
      },
      {
       "kind": "dataTable",
       "label": "Every content page",
       "bindsTo": "ContentPage",
       "columns": [
        "ContentPage.id",
        "ContentPage.slug",
        "ContentPage.title",
        "ContentPage.body",
        "ContentPage.isEnabled",
        "ContentPage.status",
        "ContentPage.iconAssetRef",
        "ContentPage.categoryCode",
        "ContentPage.sortOrder",
        "ContentPage.isReferenced",
        "ContentPage.scopePath"
       ],
       "operation": "listContentPages",
       "provenance": "contract white-label.yaml GET /tenant-config/pages"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected content page",
       "bindsTo": "ContentPage",
       "columns": [
        "ContentPage.id",
        "ContentPage.slug",
        "ContentPage.title",
        "ContentPage.body",
        "ContentPage.isEnabled",
        "ContentPage.status",
        "ContentPage.iconAssetRef",
        "ContentPage.categoryCode",
        "ContentPage.sortOrder",
        "ContentPage.isReferenced",
        "ContentPage.scopePath"
       ],
       "operation": "listContentPages",
       "provenance": "contract white-label.yaml GET /tenant-config/pages"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The accessibility information list.",
   "error": "Could not load. Names which read failed and leaves the accessibility information untouched.",
   "emptyFirstRun": "No accessibility information yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table.",
   "emptyNoResults": "Nothing matches the filter on status, categoryCode, slug and the accessibility information are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `TENANT_CONFIGURE`, which `listContentPages` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "**The offline banner shows.** Help already loaded stays readable, marked with its age. **Raising a case is disabled offline** — it needs the connection (decided 28 September, audit R148) — and the screen says how to reach staff in person instead: the guest services desk, or any member of staff."
  },
  "apis": [
   {
    "operationId": "listContentPages",
    "contract": "white-label",
    "purpose": "List custom content pages",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "ContentPage.id",
    "ContentPage.slug",
    "ContentPage.title",
    "ContentPage.body",
    "ContentPage.isEnabled"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "client-verified",
   "board": "wireframes/P02 Guest App.dc.html#gst-057",
   "prototype": {
    "file": "sources/designs/guest-rev3-28-september/TICVAI Guest Booking Mobile v2.dc.html",
    "rev": "rev 3",
    "verified": "2026-09-28",
    "match": "exact",
    "view": "Account → All screens → Wave 2 → Accessibility information"
   }
  },
  "apisNote": "Rebuilt 9 September 2026 from the 1 operation this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
 "listContentPages": {
  "method": "GET",
  "path": "/tenant-config/pages",
  "contract": "white-label",
  "summary": "List custom content pages",
  "permission": "TENANT_CONFIGURE",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "status",
    "in": "query",
    "required": null
   },
   {
    "name": "categoryCode",
    "in": "query",
    "required": null
   },
   {
    "name": "slug",
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
 "ContentPage": {
  "x-ticvai-persistence": "whitelabel.content_page",
  "type": "object",
  "required": [
   "id",
   "slug",
   "title",
   "body",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "slug": {
    "type": "string",
    "pattern": "^[a-z0-9-]+$"
   },
   "title": {
    "$ref": "#/components/schemas/LocalisedText"
   },
   "body": {
    "$ref": "#/components/schemas/LocalisedRichText"
   },
   "isEnabled": {
    "type": "boolean",
    "default": true,
    "description": "BL-005. **Enablement is not publication.** A published page that is disabled exists, keeps its URL and its history, and does not render — which is what a tenant wants when a section is seasonal.\n**Unpublishing loses the version; disabling does not.** Collapsing them means a venue turning off its water-park section for winter has to republish it every spring.\n"
   },
   "status": {
    "allOf": [
     {
      "$ref": "#/components/schemas/ContentStatus"
     }
    ],
    "readOnly": true,
    "description": "Created as `draft`, published by `publishTenantConfig`, archived through `updateContentPage` (`states/content.yaml`)."
   },
   "iconAssetRef": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "categoryCode": {
    "type": "string",
    "nullable": true
   },
   "sortOrder": {
    "type": "integer"
   },
   "isReferenced": {
    "type": "boolean",
    "readOnly": true,
    "x-ticvai-derived": "onWrite",
    "description": "True when navigation or the homepage links to this page. Blocks deletion. Maintained by `setNavigation` and `setHomepageLayout` in the same transaction as the links they write."
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `tenant` scope.**"
   }
  }
 },
 "ContentStatus": {
  "type": "string",
  "enum": [
   "draft",
   "published",
   "archived"
  ]
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
 "LocalisedRichText": {
  "x-ticvai-persistence": "none — jsonb column",
  "type": "object",
  "description": "Keyed by language code. Values are sanitised HTML.",
  "additionalProperties": {
   "type": "string"
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
