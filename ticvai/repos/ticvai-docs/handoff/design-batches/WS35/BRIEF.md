# WS35 — Pricing   Revenue Management board 2

**10 screens · 10 operations · 10 schemas · 1 permissions**

Platform P09 TICVAI Web · ships as **ticvai-control** ·
platformAdmin audience · web ·
online only

## Who this is for

**platformAdmin on web.** Everything below is how you know what is
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

- **Every control that can be refused must be gated.** 1 permissions apply here:
  `PRODUCT_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **0 of these operations work offline**
  
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `ADM-058` | Pricing Rule Command Center | commandCentre | 1 | 1 | — |
| `ADM-059` | Customer Segment & Profile Pricing Rules | configEditor | 1 | 0 | — |
| `ADM-060` | Membership & Loyalty Pricing Rules | configEditor | 1 | 0 | — |
| `ADM-061` | Residency, Nationality & Market Pricing Rules | configEditor | 1 | 0 | — |
| `ADM-062` | Channel-Based Pricing Rules | listDetail | 1 | 0 | — |
| `ADM-063` | Location, Venue & Event Pricing Rules | configEditor | 1 | 0 | — |
| `ADM-064` | Quantity, Group & Volume Pricing Rules | listDetail | 1 | 0 | — |
| `ADM-065` | Effective Date, Season & Day-Based Pricing Rules | configEditor | 1 | 0 | — |
| `ADM-066` | Timeslot, Performance & Time-of-Day Pricing Rules | listDetail | 1 | 0 | — |
| `ADM-067` | Pricing Rule Priority, Conflict Resolution & Testing | listDetail | 1 | 0 | — |

## Thin screens in this batch

**ADM-062, ADM-064, ADM-066, ADM-067 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.
