# P08-access-venue-01 — P08 · Access & Venue (1 of 3)

**10 screens · 62 operations · 57 schemas · 20 permissions**

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
  `ACCESS_POINT_CONFIGURE, ASSET_MANAGE, ASSET_VIEW, EVENT_CONFIGURE, MAINTENANCE_APPROVE, MAINTENANCE_EXECUTE, MARKETING_MANAGE, MARKETING_SEND, MARKETING_VIEW, ORDER_REFUND_APPROVE, ORDER_REFUND_BULK, PARKING_CONFIGURE`…. A control nobody can use must say so,
  not sit enabled and fail.
- **21 of these operations work offline**: acceptWorkOrder, attachWorkOrderEvidence, completeWorkOrder, createWorkOrder, getAsset, getPerformance, getQueue, getWaitTimes
  — and the rest do not. A surface that looks the same online and off is lying.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-001` | Queue Directory | listDetail | 19 | 0 | — |
| `BO-002` | Queue Configuration | listDetail | 14 | 1 | — |
| `BO-003` | Queue Integration Setup | listDetail | 4 | 0 | — |
| `BO-004` | Manual Wait Time Entry | approvalInbox | 11 | 0 | — |
| `BO-005` | Queue Monitor | listDetail | 19 | 1 | — |
| `BO-006` | Parking Configuration | listDetail | 4 | 0 | — |
| `BO-030` | Work Order Verification | listDetail | 9 | 2 | — |
| `BO-031` | Asset Register | listDetail | 7 | 0 | — |
| `BO-032` | Admission Profiles | listDetail | 3 | 0 | — |
| `BO-033` | Blacklist Management | listDetail | 3 | 1 | — |
