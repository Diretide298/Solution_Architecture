# WS123 — AI Governance board 3

**10 screens · 7 operations · 15 schemas · 2 permissions**

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

- **Every control that can be refused must be gated.** 2 permissions apply here:
  `AI_AUDIT_VIEW, AI_USE`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `ADM-539` | AI Explainability & Audit Command Center | commandCentre | 1 | 0 | — |
| `ADM-540` | AI Decision Explorer & Search | listDetail | 2 | 0 | — |
| `ADM-541` | AI Decision Explanation Workspace | listDetail | 1 | 0 | — |
| `ADM-542` | Data, Feature & Evidence Provenance | listDetail | 1 | 0 | — |
| `ADM-543` | Candidate, Rule & Decision Path Trace | listDetail | 2 | 0 | — |
| `ADM-544` | Model, Provider & AI Runtime Trace | listDetail | 2 | 0 | — |
| `ADM-545` | Governance, Approval & Human Decision Trace | listDetail | 1 | 0 | — |
| `ADM-546` | Execution & Business Outcome Trace | listDetail | 2 | 0 | — |
| `ADM-547` | AI Audit Record & Evidence Package | listDetail | 2 | 0 | — |
| `ADM-548` | AI Trace Investigation & Replay Simulator | listDetail | 2 | 0 | — |

## Thin screens in this batch

**ADM-541, ADM-542, ADM-543, ADM-544, ADM-545, ADM-546, ADM-548 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.
