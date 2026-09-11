# P08-access-venue-02 — P08 · Access & Venue (2 of 3)

**10 screens · 50 operations · 47 schemas · 20 permissions**

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

- **Every control that can be refused must be gated.** 20 permissions apply here:
  `ACCESS_OVERRIDE, ACCESS_VALIDATE, AI_AUDIT_VIEW, ASSET_MANAGE, ASSET_VIEW, INCIDENT_MANAGE, INCIDENT_REPORT, INCIDENT_VIEW, PRODUCT_CONFIGURE, PRODUCT_VIEW, QUEUE_MANAGE, QUEUE_VIEW`…. A control nobody can use must say so,
  not sit enabled and fail.
- **18 of these operations work offline**: getAsset, getQueue, getVenueMap, getVenueMapGraph, getWaitTimes, listAssets, listGames, listQueues
  — and the rest do not. A surface that looks the same online and off is lying.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-034` | Scan Activity | listDetail | 7 | 1 | — |
| `BO-035` | Override Audit | listDetail | 8 | 1 | — |
| `BO-038` | Reconciliation Queue | listDetail | 9 | 0 | — |
| `BO-069` | Asset Register | listDetail | 11 | 0 | — |
| `BO-071` | Planned Maintenance | listDetail | 4 | 0 | — |
| `BO-072` | Incident Log | listDetail | 5 | 0 | — |
| `BO-092` | Venue Maps | listDetail | 2 | 0 | — |
| `BO-093` | Map Import & Labelling | configEditor | 3 | 0 | — |
| `BO-094` | Map Editor & Publish | statusTracker | 6 | 0 | — |
| `BO-095` | Resources | listDetail | 2 | 0 | — |
