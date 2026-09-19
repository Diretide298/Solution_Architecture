# P02-in-venue-services-01 — P02 · In-venue Services

**10 screens · 28 operations · 40 schemas · 7 permissions**

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

- **Every control that can be refused must be gated.** 7 permissions apply here:
  `ACCESS_POINT_CONFIGURE, ORDER_MODIFY, PRODUCT_VIEW, QUEUE_VIEW, RESOURCE_BOOK, RESOURCE_VIEW, VENUE_MAP_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **8 of these operations work offline**: getTenantAppStatus, getVenueMap, getVenueMapGraph, getWaitTimes, joinRestaurantWaitlist, listParkingFacilities, listProducts, listQueues
  — and the rest do not. A surface that looks the same online and off is lying.
- **Offline, every screen shows one banner, the same on web and app:** *"You're offline. Connect to the internet to book, pay, order or join a queue."* The moment the connection drops, on every screen, above the screen's own content. By itself as soon as the connection is back, with a short "Back online" confirmation. **It never** Covers what is already on screen, or appears for a server error — that is the screen's own error state, and a guest told they are offline when the venue is down reconnects for nothing. Each screen's `states.offline` says what stays on screen and what waits.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `GST-021` | Interactive Map | listDetail | 4 | 0 | — |
| `GST-022` | Attraction Wait Times | statusTracker | 1 | 0 | — |
| `GST-023` | Virtual Queue | statusTracker | 5 | 0 | — |
| `GST-024` | F&B – Browse & Order | listDetail | 8 | 0 | — |
| `GST-025` | F&B – Order Tracking | statusTracker | 3 | 0 | — |
| `GST-027` | Parking – Reserve & Pay | listDetail | 3 | 0 | — |
| `GST-028` | Parking – Reservation Confirmed | listDetail | 2 | 0 | — |
| `GST-029` | Venue Info & Services | listDetail | 2 | 0 | — |
| `GST-038` | Digital Companion Mode | listDetail | 3 | 0 | — |
| `GST-070` | Reserve a Table or Cabana | statusTracker | 7 | 0 | — |

## Thin screens in this batch

**GST-022, GST-023, GST-025, GST-028, GST-029, GST-038 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.
