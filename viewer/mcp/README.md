# ADAM context bridge — MCP server

Thirteen tools for a developer's local Claude: **nine read the TICVAI package**, and **four are
about the work scheduled against it** in OpenProject. Phases 1 to 3 of
`viewer/HANDOFF-adam-bridge.md`.

## What a developer runs

A viewer must be reachable — the MCP reads through it and has no other source. **Most developers
should point at the deployed one and run nothing locally:**

```bash
claude mcp add adam -- node C:/path/to/adam/viewer/mcp/server.mjs \
  -e ADAM_VIEWER_URL=https://adam.ainfinite.ai \
  -e ADAM_EMAIL=you@softlabsgroup.com \
  -e ADAM_PASSWORD=...
```

Working on the viewer itself? Run `./start.ps1` and drop `ADAM_VIEWER_URL` for the local default.

| variable | default | what |
|---|---|---|
| `ADAM_EMAIL` | — | your viewer account. Required. |
| `ADAM_PASSWORD` | — | its password. Required. |
| `ADAM_VIEWER_URL` | `http://127.0.0.1:4173` | where the viewer is. `https://adam.ainfinite.ai` is the deployed one. |
| `ADAM_PROJECT` | asked for at startup | only when more than one package is configured |

Both deployed hostnames work: `adam.ainfinite.ai` sends everything to the viewer, which proxies auth
onward itself, and `adamapi.ainfinite.ai` splits them in nginx. TLS terminates at nginx on both and
the session cookie is `Secure`, so credentials do not cross the network in the clear.

**Your own account, not a shared one.** Everything the bridge can read is what *you* can read: the
viewer's audience filter refuses a client account the decisions layer, and the MCP inherits that
refusal rather than reimplementing it. A shared login would hand every reader the widest role in the
building.

## The tools

| tool | takes | gives |
|---|---|---|
| `adam_search` | `q`, optional `kind`, `limit` | hits across every kind, each with file and line |
| `adam_screen` | `id` | one screen, its APIs and states, and the journeys through it |
| `adam_journey` | `id` | one flow, its steps, branches and exit states |
| `adam_contract` | `name`, optional `schema` / `operation` | the contract's map; then one schema or operation in full |
| `adam_table` | `name` | one table, its columns, keys, migration and owning service |
| `adam_service` | none, or `name` + `operations` | all 16 services; one in depth |
| `adam_module` | none, or `name` | all 32 modules; one with its tables |
| `adam_decisions` | none, or `id` / `q` | the ADRs and registers; one ADR in full |
| `adam_file` | `path`, optional `from` / `lines` | one file's source, windowed |
| `adam_board` | nothing | what is open and assigned to you, and what each item touches |
| `adam_work` | `key` | one work package, live, plus the artefacts it touches |
| `adam_links` | `kind`, `id` | what work is scheduled against one artefact |
| `adam_link` | `kind`, `id`, `key` — or `remove` + `linkId` | **writes**: records that a work package is about an artefact |

Start with `adam_search` when you have a name but not a kind. A miss returns candidate spellings
rather than an empty result — a wrong id is usually a wrong spelling of a right one.

**The four work tools read OpenProject as *you*.** They need a token stored on your settings page —
without one they say so and name the page, rather than failing. There is no service account,
deliberately: a shared credential attributes every change to a robot, and the history is most of what
a PMS is for.

**`adam_link` is the only tool here that writes, and all it writes is one row** — that a work package
is about an artefact. It cannot change a status, an assignee or a work package. OpenProject owns
those. The bridge owns the one thing neither system can hold alone: OpenProject cannot say that
WP #1841 is about screen `BO-102` and table `access.entitlement`, because it knows nothing about the
package; the package knows those names and nothing about the schedule.

**`adam_decisions` before proposing an architectural change.** An ADR records the options that
were rejected, what they would have cost and what has since been superseded — contradicting one
already decided is the most expensive mistake available here. The listing flags the case that
misleads: an ADR that is Accepted *and* partly superseded reads as current in a list and is not
current in the part that matters. The record carries the fields; `adam_file` carries the argument.

**Listings trim prose; single lookups keep it.** `storageReason` explains why a table exists with no
contract schema behind it, and the package answers at length — **160 fields across the 395 tables
are over 2 KB and every one of them is a `storageReason`**, the largest at 25,450 characters.
Returned whole, three of those made one module's table list 59 KB. So a listing trims to a sentence
and says it has; `adam_table` on that one table keeps the whole thing, because there the prose is
the answer you asked for.

**`adam_contract` answers in two steps on purpose.** `contracts/spine/access.yaml` is 756 KB; a tool
that returned every schema with its properties would fill a context window in one call and leave no
room to use what it fetched. So the first call gives the map — operations with methods and paths,
and the names of the schemas — and a second names the one thing you want in full. Every tool result
is capped at roughly 30k tokens; over that you get a legible refusal rather than a wedged session.

## How it works, and why it is shaped this way

**It is a selector, not a proxy.** The viewer's routes are bulk payloads — `/api/journeys` returns
every flow *and* every screen, `/api/backend` the whole data model — because they were built for a
browser that loads a layer once and holds it. There is no `/api/screen?id=BO-102` to forward to. So
a layer is fetched whole, held, and indexed into; after the first call a tool costs no HTTP.

**The cache asks the server, never a timer.** `If-None-Match` against the viewer's ETag: one
conditional request settles it, and the 3.25 MB index comes back as a 0-byte 304. This did not work
at first — the route answered `no-store` with no validator at all, so revalidation never fired and
every call re-downloaded the whole layer, silently. Fixed in the viewer as **V-46**.

`/api/summary`.`generatedAt` is kept as a fallback, for a deployed viewer that predates that fix. It
costs a second round trip per read. Both paths stay, because a developer points their MCP at
whichever viewer is deployed, and that is not always this one. A TTL would be a second opinion about
freshness, and the wrong one.

**Auth is a cookie, because that is all there is.** `lib/session.mjs` reads `req.headers.cookie` and
has no bearer path. The MCP signs in at `/api/auth/login` — which the viewer proxies to the accounts
service and forwards `Set-Cookie` back from, so one base URL covers both halves — and re-signs in
when the 14-day session lapses underneath it.

**Zero dependencies.** MCP over stdio is newline-delimited JSON-RPC 2.0 and the handshake is four
methods. That is less code than a README explaining how to install an SDK, it matches the rest of
this codebase, and a dependency-free folder can be handed to somebody rather than onboarded onto.

**stdout is protocol and nothing else.** A stray `console.log` corrupts the stream, and the failure
presents as the client hanging. Everything human goes to stderr.

## Checking it

```bash
node viewer/mcp/mcp-check.mjs
```

36 checks with a credential stored, 32 without. The handshake and tool-listing ones need nothing running. The live calls need the viewer
and your credentials, and report as skipped without them — a viewer that is not up is not a broken
MCP server. The two halves are probed separately, so a live viewer with a dead accounts service says
so rather than sending you to the wrong log.

The live checks drive their lookups off whatever `adam_search` just found, rather than hardcoding
ids that a re-derivation can move. Two guard sizes, because both regressions would be invisible
until something broke: `adam_contract('access')` — the 756 KB one — must stay under the ceiling, and
**every one of the 32 modules** is walked and must answer under 40 KB, since the module carrying the
25 KB essays is whichever one carries them this week.

**Nothing here skips quietly.** A lookup that finds nothing to test fails rather than skipping: two
real bugs sat behind a benign-looking `skip` line for a while, and a check that skips quietly is a
check that lies.

## What is deliberately not here

The `.adam/` local cache and `/adam propose`. Those are phase 4 — see
`viewer/HANDOFF-adam-bridge.md`, and note that `propose` has an unresolved problem logged as V-49.

Anything that changes a work package. Status, assignee, dates and the work packages themselves are
OpenProject's, and a second system writing them is the failure `delivery-plan-vs-package.md` already
has open as CF-124: two independent plans over the same work, neither referencing the other.

**`adam_impl` is not here and cannot be yet.** It was meant to start from the file you have open and
return the screen behind it. `ticvai/repos/ticvai-frontend/` is a real Nx monorepo with six apps and
**every one of them is `export {};`** — only `packages/offline-core` has code. There is no route file
to resolve against, so the tool would answer "not implemented" for every input. The screen records
already carry `app` and `route`, so this becomes small the day the apps grow routes.
