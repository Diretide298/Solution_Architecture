# Handoff: the Adam context bridge

Written 8 Sep 2026 at the end of the planning session, then **revised twice the same day** — once
after reading the code rather than trusting the first pass, and again after auditing what had been
built against it. **Phases 1 and 2 are built and proven** — `viewer/mcp/`, nine tools, 30 checks
passing against live data, and **no new server route in either phase**. **The settings page (V-45)
and the ETag (V-46) are built too**, which clears everything that stood in front of phase 3 on this
side. Phases 3 and 4 are still research and decisions, recorded here so the session that builds them
does not start by re-deriving what is already known.

Everything the revisions changed is marked **REVISED**. The load-bearing ones: the MCP is a selector
and not a proxy; auth is cookie-only; `sendCachedJson` had no ETag until V-46; the `/api/*` URL spelling
drifts in production and `/pkg/<id>/` does not; the PMS is OpenProject and its TICVAI project is
empty; and phase 3 is a join to it, not a task table of our own.

**Where a claim here and the code disagree, check the code.** This file has been confidently wrong
four times, and every one survived a careful read: the `uiux`-versus-`journeys` mix-up, the ETag that
does not exist, "the three missing routes" of which two were already served, and `adam_impl` having
frontend source to point at. Three were caught only by running something.

Plan, rendered: https://claude.ai/code/artifact/4a3bf20d-4623-46e4-a87a-cac98f718d98

## What it is

An MCP server that lets a developer's local Claude fetch context out of the TICVAI package, plus a
link between package artefacts and the **OpenProject** work packages that schedule them, plus a local
markdown cache the agent can grep.

## The distinction everything follows from

Two kinds of data want opposite things.

**Derived** — screens, journeys, modules, services, contracts, tables. Produced by `ticvai/tools/*.py`
from the contracts, guarded by eleven checks, living in git. **Read-only from the bridge.** A write
that bypasses the tools makes the package disagree with itself; that has already happened once, when
an unrun derivation left an orphan table behind.

**Coordination** — what is being worked on, by whom, against which milestone. Written by people
during a working day and absurd to route through a commit. **REVISED:** this belongs in the PMS the
company already runs — **OpenProject at `pms.softlabsgroup.in`** — and not in a table of our own. See
decisions 1 and 1b: the plan holds 23 epics, 444 features, 2,173 tasks and six milestones, and the
OpenProject project for TICVAI exists but is **empty**, so the first piece of phase 3 is a load and
not a link.

What the bridge stores is the **join**: which artefact a work package is about, which nothing else
can say. **Read and write, server-side, in the SQLite behind `:8787`.** Review findings — the existing
`verdict` table — stay here too, and are not tasks.

So "a better way to update project files" is two answers. Coordination: stop using git for it, and
do not rebuild what OpenProject already does. Package files: keep git, but let the agent propose
without needing a terminal on the server.

---

## What already exists — do not rebuild these

### Node viewer, `:4173`, `viewer/server.mjs` (1,328 lines)

Routing is **not** Express. `resolveRoute()` at line ~250 parses the path; the handlers are a chain
of `if (route === '…')` from line ~774. Adding a route means adding one of those.

Twenty read routes, all live off the package on disk:

```
session  summary  index  detail  journeys  backend  domain  diagrams
diagrams/detail   lineage  tooltips  decisions  domains  cicd  platforms
uiux  search  file  tree  events
```

Builders are in `viewer/lib/*.mjs` — `indexer`, `journeys`, `backend`, `domain`, `domains`,
`platforms`, `lineage`, `decisions`, `cicd`, `uiux`, `search`, `diagrams`, `structure`, `wireframes`,
`audience`, `session`, `projects`.

**Multi-project already works.** `viewer/projects.json` maps ids to package roots;
`/api/pkg/<id>/…` is the prefixed form and bare `/api/…` answers for the default. Only `ticvai` is
configured. Adding a package is a config entry and a restart.

**REVISED, then FIXED — `sendCachedJson` had no ETag.** A draft of the MCP client sent
`If-None-Match` and expected a 304. The route buffered the body and answered `Cache-Control:
no-store` with no validator at all, so the revalidation never fired and every tool call
re-downloaded the whole layer — 1.9 MB of index to read one contract. Silent, too: the answers were
right and only slow.

**Fixed as V-46.** SHA-1 of the body it already buffers, computed on the same miss that gzips it, so
it costs nothing; the 3.25 MB index now becomes a 0-byte 304. **`no-store` is unchanged and that is
deliberate** — these are gated payloads and do not belong in a browser's disk cache, and a browser
told `no-store` never sends a conditional request anyway, so the browser's behaviour did not change.
This is for a client holding its own cache in memory. The MCP prefers the ETag and keeps the
`generatedAt` path as a fallback for a deployed viewer that predates the fix.

**REVISED — use the `/pkg/<id>/` spelling, never bare `/api/`.** `deploy/nginx/adamapi.ainfinite.ai`
forwards `location /pkg/` wholesale but names the `/api/*` routes one at a time, and **that list is
already missing `cicd`** — tolerated, because the `/pkg/` rule covers it, and the deploy script's
drift check deliberately stops reporting names once it sees that rule. A client on the bare spelling
works locally and 404s in production on whichever route nobody remembered to add. The MCP resolves
the default project from `/api/projects` and uses the prefixed form, which cannot drift.

**REVISED — the deployment is not plain HTTP.** A comment in `server.mjs` says it is; `deploy.sh`
disagrees and is right. nginx terminates TLS for `adam.ainfinite.ai` and `adamapi.ainfinite.ai`,
`SECURE_COOKIE=1`, `COOKIE_DOMAIN=.ainfinite.ai`. **Developers should point `ADAM_VIEWER_URL` at
`https://adam.ainfinite.ai` and run no viewer locally** — an earlier draft of the MCP README told
them to run `start.ps1`, which is only right for somebody working on the viewer itself.

**REVISED — the routes are bulk payloads, not per-entity lookups.** This shapes the whole build and
the first draft of this document missed it. There is no `/api/screen?id=BO-102`. `/api/uiux` returns
the entire UI/UX payload, `/api/backend` the whole data model (`modules`, `tables`, `columns` —
`lib/backend.mjs:932`), `/api/search` the whole corpus, `/api/index` 1.9 MB slim. They were built for
a browser that loads a layer once and holds it.

So **the MCP is a selector with a warm cache, not a proxy.** It fetches a layer once, holds it, and
answers `adam_screen("BO-102")` by indexing into it. Better than proxying — a tool call costs no HTTP
after the first — but it means cache invalidation belongs in phase 1, not phase 2. Key it on the
ETag, with `/api/summary`.`generatedAt` as the fallback. Never on a TTL.

**REVISED — auth is cookie-only.** `lib/session.mjs:131` `whoIs()` reads `req.headers.cookie` and
nothing else. There is **no `Authorization: Bearer` path and no personal-access-token concept**. The
MCP must hold a `ticvai_session` token and send it as a cookie header. `/api/auth/login` mints one;
it lasts 14 days (`api/security.py:34`).

**Audience gating is one route name.** `lib/audience.mjs` denies exactly `decisions`, plus a path rule
for ADRs read through `/api/file`. Inheriting it is free: send the cookie, let the server 403, surface
the 403 as the tool's error. **Do not reimplement the check inside the MCP** — a second copy is the
one that drifts.

**Neither service runs by default.** Both ports were down when this was written; `viewer/start.ps1`
brings them up. Node 22, npm registry reachable.

### FastAPI, `:8787`, `viewer/api/`

`main.py`, `db.py`, `security.py`, `decisions.py`, and `secrets.py` since V-45. SQLite, nine tables:

```
account  reset  invite  session  verdict  mention  project  account_project
account_secret
```

**`account_secret` is the odd one and is meant to be.** Everything else secret in that store is a
one-way hash. This holds credentials that must be usable later — encrypted with Fernet, key in
`TICVAI_SECRET_KEY` and never in the file. Its own table rather than a column on `account`, so the
many places that read an account cannot carry a credential out by accident.

**`verdict` is the closest thing to a task that exists.** Its columns:

```
id  target_kind  target_id  layer  tag  audience  verdict  note  account_id
created_at  done_at  done_by  done_response  sent_back_at  sent_back_by  sent_back_note
```

Owner, target artefact, note, and a full done / send-back lifecycle. Read this table before
designing a task table.

Endpoints already there: accounts, auth (login/logout/bootstrap/redeem/reset/password/me/state),
invites, mentions, mentionable, validation, verdicts (+ done, + send-back), export, decisions
preview/apply, health.

### Derived data in the package

`ticvai/handoff/` has the JSON the new routes need — no parsing of YAML required:

```
modules.json              service-decomposition.json   screen-index.json
platform-P01…P16.json     platform-index.json          traceability.json
relationship-graph.json   schema-reference.json        api-data-lineage.json
status.json               links.json                   screen-redundancy.json
```

Service detail also exists as `ticvai/diagrams/lld/services/*.yaml` (16 services).

### Deploy

`git pull && sudo ./deploy/deploy.sh` on the box. PM2 keeps node on `:4173` and uvicorn on `:8787`;
nginx is placed by hand and the deploy script deliberately does not touch it.

---

## What is missing

| | |
|---|---|
| MCP server | nothing exists |
| ~~Routes `module`, `service`, `impl`~~ | **This row was wrong.** See the phase 2 note below — two of the three already existed and the third has nothing to point at |
| Artefact ↔ issue link table and API | nothing exists — see the revised decision 1 |
| Service tracker | nothing exists; `ticvai/docs/registers/conflicts.md` is the nearest habit |
| `.adam/` local cache and `/adam sync` | nothing exists |
| `/adam propose` | nothing exists |

---

## Decisions

### Settled 8 Sep

**How the MCP authenticates.** Email and password in the MCP's own environment
(`ADAM_EMAIL` / `ADAM_PASSWORD`); it logs in on start and refreshes the 14-day cookie when it
expires. Chosen over pasting a browser cookie (dies fortnightly, people resent re-pasting) and over
building personal access tokens first (right answer long-term, but real server work bolted onto the
front of phase 1). **The cost accepted:** a real password sits in a config file on each developer's
laptop. Revisit if the bridge leaves the team.

**How the MCP is built.** **Zero dependencies** — hand-written stdio JSON-RPC, roughly 120 lines,
rather than `@modelcontextprotocol/sdk`. Matches the codebase, which is raw `node:http` with no
framework, and a dependency-free folder is far easier to hand a developer than one needing an
`npm install`.

### 1. Task IDs — **REVISED, and the first draft had this wrong**

The original question was "is a task the same animal as a verdict, one table or two?" **Both answers
were wrong, because a PMS already exists.**

`ticvai/handoff/delivery-plan-vs-package.md` records the client delivery plan: **23 epics, 444
features, 2,173 tasks, six milestones, 7,552 person-days, and a Jira import of 2,640 issues.** That
file's entire subject is that *two* independent plans already run over the same work — the plan
sequences by milestone, the package by wave, neither references the other — and it is open as
**CF-124**. Minting task IDs in ADAM makes it three, on purpose, in a repo already carrying that
exact failure as a conflict.

**So ADAM does not own tasks. It owns the join nobody has.**

- **Task ID is the OpenProject work package id.** ADAM never mints one.
- **One link table:** `(project, target_kind, target_id, external_system, external_key, url,
  cached_status, cached_summary, synced_at)`. Artefact ↔ work package, many-to-many. A PMS can hold 2,640
  issues and cannot say *"this one is about screen BO-102, table `access.entitlement` and
  `AccessService`."* The package is the only thing that can, and that anchoring is the whole value of
  the bridge.
- **Milestones are read, not authored.** M1–M6 come from the plan. ADAM's contribution is the
  epic→contract mapping that `delivery-plan-vs-package.md` already recommends (E01→`catalogue`,
  E03→`access`, E04→`orders`+`finance`) — which is CF-124's actual remedy, and falls out of this
  table for free.
- **`verdict` stays exactly what it is.** A review finding on an artefact is not a work package and
  must not become one. The original decision dissolves: not "one table or two", but *review lives
  here, work lives in OpenProject, and a row may point at both.*

Phase 3 shrinks from tables + API + board commands to **one link table and a read-through client**.

### 1b. The PMS is OpenProject, and the TICVAI project in it is empty — **verified 8 Sep**

`https://pms.softlabsgroup.in` — *Softlabs Project Management System*, OpenProject **core 10.0.2**,
API v3 HAL+JSON. Probed with a read token; every finding below is from the live instance.

**Capability: everything the bridge needs is there.**

| need | how |
|---|---|
| Stable task IDs | work package `id`, `/api/v3/work_packages/{id}` |
| Service auth | API key over HTTP Basic as `apikey:<token>`, or OAuth2 |
| Filtered queries | `?filters=[…]`, including on custom fields |
| Milestones | Versions, **and** a built-in `Milestone` work package type |
| Epic → feature → task | WP parent/child plus `/api/v3/relations` |
| Write-back | `POST`/`PATCH` with `lockVersion` optimistic locking |
| Push instead of poll | admin-configurable webhooks |

**The type vocabulary already matches the delivery plan 1:1:**
`Task(1) Milestone(2) Phase(3) Feature(4) Epic(5) User story(6) Bug(7) Sub Task(10)` — against the
plan's 23 epics, 444 features, 2,173 tasks and six milestones.

**🔴 But project `ticvai` (id 153) holds 0 work packages and 0 versions.** It is a created shell. The
instance itself is live and used — 1,872 work packages across the other eight projects, 1,403 of them
in one — so this is not a dead server. **The plan has not been loaded.**

That changes the order of work. **There is nothing to link to yet.** Phase 3 is now two pieces, and
the first is not the bridge's:

1. **Load the plan into OpenProject** from `sources/client/TAIS_Product_Planning_and_Delivery_Plan.xlsx`
   — epics, features, tasks as parent/child; the six milestones as Versions or as Milestone-type work
   packages, which is an open choice. A scripted import against the API. **This writes ~2,600 rows
   into a live PMS and must not be run without explicit sign-off.**
2. **Then the link table**, which is unchanged by any of this.

**Custom fields on the instance are `Priority Number` (String), `Priority_No.` (Integer) and
`Priority_Num` (Float)** — three near-duplicates of one idea, and no artefact reference among them.
Adding one needs an admin. This is further reason the artefact↔issue join lives in ADAM and not in a
custom field: OpenProject knows nothing about the package's eleven checks, and a text field filtered
by substring matches `BO-10` inside `BO-102`.

**🔴 Core 10.0.2 shipped September 2019** — roughly seven years of unpatched Rails, internet-facing
behind Cloudflare, about to hold the delivery plan. Nothing above is blocked by it, and an upgrade
would move API details we are otherwise writing against. This belongs in the conflicts register.

### 1c. Where a developer's OpenProject key lives — **settled and built, 8 Sep**

Each developer needs their own OpenProject API key configured in ADAM, so that anything ADAM does in
the PMS is attributed to the real person rather than to one shared robot account. **Where that key is
stored is undecided**, and it is a schema decision, so it belongs with the others.

**Server-side, one encrypted token per account**, pasted once in the viewer's settings. Both the
browser board and the MCP then read through the same endpoint, so a developer configures it in one
place rather than two, and OpenProject attributes every change to the real person instead of to one
shared robot.

**The costs accepted.** A reusable third-party credential now sits at rest beside the password
hashes, so this needs an encryption key in the environment, a revoke path, and the key never
appearing in a payload once stored. Rejected: the developer's own MCP environment (free, but the
agent is then the only thing that can use it, and a browser board could never show "my tasks");
OAuth2 (the proper answer — 10.0.2 supports it — but it needs an OpenProject admin to register an
app, and it can replace this later without changing anything above it).

**Built as V-45.** `/settings.html`, plus `api/secrets.py` and an `account_secret` table.

What it turned out to need, beyond the obvious:

- **The token is verified against the live instance before it is stored.** A token that does not
  work is worse than none — it looks configured and fails later somewhere that reads as a different
  fault. `/api/v3/users/me` as the token, and the answer names who it turned out to be, so pasting
  the wrong one is caught immediately rather than when work starts being attributed oddly.
- **🔴 Cloudflare blocks `Python-urllib`.** The first verification attempt failed with a 403 and the
  page said "OpenProject did not accept that token" — and the token was fine. `pms.softlabsgroup.in`
  sits behind Cloudflare, which refuses urllib's default User-Agent outright with error 1010,
  *before OpenProject sees the request*. The same call from curl succeeds. Two fixes: send a real
  `User-Agent`, and tell an edge refusal apart from an auth rejection so the wrong thing is never
  blamed. **Anything else here that calls out to the PMS needs the same header.**
- **`account_secret` is its own table, not a column on `account`.** Every other secret in that store
  is a one-way hash; this one has to be usable later, so it is stored reversibly. Keeping it off the
  account row means sign-in, the roster, `/auth/me` and every JOIN cannot carry it out by accident.
- **The key is in `TICVAI_SECRET_KEY` and never in the database.** `deploy.sh` generates one into
  `/etc/ticvai/secret.key` at 0600 on first run and **never overwrites it** — regenerating would not
  lose the rows, it would leave them undecryptable, and the symptom is every developer's token
  failing at once with nothing in the logs. There is deliberately no default key: a default key is
  the one that ships.
- **Removing a token here does not revoke it there**, and the response says so in those words.
  "Removed" reading as "revoked" is how a live credential gets left lying about.

**Not a phase 1 concern** — phase 1 does not talk to OpenProject at all.

### 2. Who is a developer? — open

Run "current focus per developer" off the existing `account` rows, or a separate roster with git
identities so a commit can close a task?
*Recommended:* accounts, with a git email column added. A second roster is a second thing to keep in
step. **Note this now leans harder that way** — if task state lives in OpenProject, the only thing ADAM must
resolve is *which local person is which*, which is a column and not a roster.

### 3. One package or several? — open

`projects.json` is multi-project already. If the bridge will ever serve another package, the link
table needs a project column from day one.
*Recommended:* add it now, even if TICVAI is the only entry for a year.

---

## Build order

**Phase 1 — MCP over what exists. ✅ BUILT 8 Sep.** Read-only, no new server routes, no writes. One
new directory, `viewer/mcp/`, and nothing else touched:

| file | what |
|---|---|
| `server.mjs` | stdio JSON-RPC loop — `initialize`, `tools/list`, `tools/call` |
| `client.mjs` | login, cookie, layer fetch and ETag cache, 403 passthrough |
| `tools.mjs` | the five selectors and their JSON schemas |
| `README.md` | the `claude mcp add` line a developer runs |
| `mcp-check.mjs` | the harness, in the shape of `viewer/api/*-check.mjs` |

**Status: built and proven. 28 of 28 checks pass against live data** — 1,091 screens, 94 flows,
395 tables, 44 ADRs, 16 services, 32 modules. Zero dependencies.

```
viewer/start.ps1
ADAM_EMAIL=… ADAM_PASSWORD=… node viewer/mcp/mcp-check.mjs
```

The protocol half needs nothing running: handshake, version negotiation, `ping`, unknown-method
`-32601`, the tool listing, schema shape, and an unknown tool answering as `isError` rather than
crashing. The live half needs a viewer and an account.

**Running it live found three bugs the protocol checks could never have caught**, all in code that
read as correct — the dead-code table lookup, the impossible "did you mean" names, and `kinds`
describing the corpus rather than the result. All three are written up under the tools below. The
lesson is in the harness now: **a check that finds nothing to test fails rather than skips**, because
two of those three sat behind a benign-looking `skip` line.

The nine, and what each selects **out of a bulk payload** — the point of the revision above:

| tool | source |
|---|---|
| `adam_screen(id)` | `/api/journeys`.`screens` + `handoff/screen-index.json` (1,091 screens, keyed by id) |
| `adam_journey(id)` | `/api/journeys`.`flows` |
| `adam_contract(name)` | `/api/index` nodes, then `/api/detail?file=` for the held-back `properties` and `description` |
| `adam_table(name)` | `/api/backend`.`tables` + `.columns` |
| `adam_search(q)` | `/api/search` |
| `adam_decisions(id?, q?)` | `/api/decisions`.`adrs` + `.documents` |
| `adam_file(path)` | `/api/file`, windowed by line |
| `adam_service(name?)` | `/api/diagrams`.`services`, deepened by `diagrams/detail` |
| `adam_module(name?)` | `/api/backend`.`modules` + `.tables` |

**Nine, not five.** `adam_decisions` and `adam_file` came out of the audit's finding that the most
valuable thing an agent can read here is the decision it is about to contradict. `adam_service` and
`adam_module` are phase 2. **None of the four needed a server route**, which is the pattern: every
time this document said something was missing, it was already being served under another name.

### Three bugs that only running it could find

**`adam_table('entitlement')` never worked**, though the tool's own description promised the module
prefix was optional. `fold()` strips dots, so the prefix-stripping regex that ran after it was
searching a string with no dot left in it — dead code that always missed. It now matches the last
dot-segment, and **asks which** when a bare name is ambiguous across modules rather than returning
the wrong table's columns.

**The "did you mean" list offered names that exist nowhere.** A table record is
`{ module: 'access', name: 'access.entitlement' }` — **`name` already carries its schema** — so
joining the two printed `access.access.entitlement`, which a caller would paste straight back. Never
join those two fields.

**`kinds` described the corpus, not the result.** An agent reads that field as "what is in these
hits", asks for the first table in the list, and finds none — because every table was past the page
cap. It now counts hits per kind; the full vocabulary is offered only when nothing matched, which is
the one moment it helps.

### The size lesson, which the ceiling alone does not cover

`adam_module('access')` came back at **59 KB for eight tables**. The cause is a data shape worth
knowing before touching any of these payloads: **160 fields across the 395 tables are over 2 KB, and
every one of them is a `storageReason`** — the prose explaining why a table exists with no contract
schema behind it. The largest, `access.entitlement`, is **25,450 characters**. Three in one module
were the entire payload.

Listings now trim to ~300 characters on a sentence boundary and say they have; a single-table lookup
keeps the whole essay, because there the prose is the answer. Access went 59 KB → 3 KB, and the worst
of all 32 modules is 21 KB. **The 120 KB result ceiling did not catch this** — it prevents a wedged
session, not a tool quietly returning twenty times what it should. The harness now walks every module
and fails over 40 KB, because the module holding the essays is whichever one holds them this week.

**`adam_contract` answers in two steps.** `contracts/spine/access.yaml` is **756 KB**. The first
draft returned every schema with its properties merged in and defaulted that to on, which is one
tool result large enough to fill a context window and leave no room to act on it. So the default is
the map — operations with methods and paths, and the schema *names* — and a second call names the
one thing wanted in full. Every result is capped at 120 KB; over that the answer is replaced by its
own size and a suggestion, because truncated JSON does not parse and a model reads the surviving
half as the whole answer.

**Correction to an earlier draft of this table:** screen records come from **`/api/journeys`**, not
`/api/uiux`. `lib/journeys.mjs:429` returns `flows`, `screens`, `apps`, `platforms`, `wireframes`,
`vocabulary`, `operationUsage`. `/api/uiux` is about *design boards and frames* — how much of the
product is drawn — and holds no screen records at all. Reading `uiux` for a screen returns nothing
and looks like a missing screen.

Verify by starting the stack with `start.ps1` and driving the MCP over stdio from a small script —
the same shape as the existing `viewer/api/*-check.mjs` harnesses, which is how this repo already
tests.

**Phase 2 — ✅ BUILT 8 Sep, and it needed no server route at all.** The heading above said "the
three missing routes". **Two of the three were never missing**, and the third cannot be built yet.
This is the single largest correction in this document.

| planned route | what was actually there |
|---|---|
| `module` | **`/api/backend` has carried `modules` all along** — 32 of them, and *richer* than `handoff/modules.json`, which has 27 and lacks `writtenTables`, `migration` and `status`. Building a second source would have been a second answer to a question the package had already answered |
| `service` | **`/api/diagrams` carries 16 service summaries**, and `diagrams/detail?set=services&name=X` serves the whole LLD file. `DIAGRAM_SETS` in `lib/diagrams.mjs` has included `services` the entire time |
| `impl` | **Nothing to point at.** See below |

So phase 2 is two tools. `adam_service` lists all 16 or goes deep on one — the schemas it owns, why
it is its own service, how it scales, what happens when it is down, its operations by contract, and
the full operation list on request. It resolves `Tenancy` as well as `TenancyService`, because that
is how people say it. `adam_module` lists all 32 or returns one with its tables.

**`adam_impl` cannot be built yet, and the reason is not the one the first draft gave.** That draft
said there was no frontend source in the package. There is: `ticvai/repos/ticvai-frontend/` is a real
Nx monorepo with six apps — backoffice, employee, guest, pos, scanner, web-b2c — plus `packages/`.
**But every app is a single `export {};`.** Only `packages/offline-core` has code, about 700 lines of
it. There is no route file to resolve a screen against, so the tool would answer "not implemented"
for every input. The screen records already carry `app` and `route`, so this becomes a small piece of
work the day the apps grow routes — and not before.

**Also in phase 2 and not built:** `.adam/` and `/adam sync`. Deferred rather than dropped; the
cache is only worth its complexity once there is something slow enough to want it, and after the
stamp-keyed cache in `client.mjs` a tool call costs no HTTP after the first.

**Phase 3 — the join, not a coordination store. ✅ BUILT 8 Sep** as V-53.

`artefact_link` in the accounts store, `api/openproject.py`, four endpoints and four MCP tools.
Much smaller than the first draft assumed, because ADAM stores exactly one thing about work: which
artefact it is about.

- **Every PMS call is made as the caller**, with their own token from V-45. No service account, ever
  — a shared credential attributes the history to a robot, and the history is most of what a PMS is
  for.
- **A link is refused unless the work package resolves.** A link to a number nobody can open looks
  like coordination and is a dead end, and the board drawing it cannot tell.
- **`adam_link` is the only tool in the bridge that writes**, and all it writes is that row. It
  cannot change a status, an assignee or a work package.
- The `cached_*` columns are labelled a cache wherever they surface. OpenProject is the truth about
  status; a board reads live, and only artefact-side listings use the cache, where fanning out would
  be one API call per row.

**Verified against the live instance:** the board returns 36 real open items for the test account,
and a link to `#6046 "Data Analysis and Module Design"` round-trips both ways. **Those 36 are in the
company's other projects** — the TICVAI project itself is still empty, so a TICVAI board is empty
until the plan is loaded, and `/api/board/mine` says so in words rather than showing a blank.

**Still needed to make it useful:** loading the plan (1b), which nobody has signed off.

**Phase 4 — tracker and `/adam propose`.** Both small once phase 3's write path exists.
`propose` runs the eleven checks locally and **refuses to open a PR on a red check** — that refusal
is the entire reason package changes still go through git rather than an API.

---

## The local folder

Markdown, not JSON — the agent reads it better, `grep` works, a diff is legible. Gitignored.

```
.adam/
  manifest.json     what was fetched, when, and the package commit it came from
  screens/          BO-102.md · ADM-038.md
  journeys/         F06.md
  modules/          access.md
  services/         AccessService.md
  contracts/        access.md
  tables/           access.entitlement.md
  board/            mine.md · team.md · milestones.md
  tracker/          AccessService.md
```

Every cached file carries the package commit in its front matter, and `/adam sync` compares against
live `/api/summary` and names what moved rather than saying "done" — a cache that quietly serves last
week's screen is worse than no cache. `board/` and `tracker/` are **not** cached; they go stale in
minutes and are fetched per read — and after the revised decision 1 they are rendered from OpenProject plus
the link table rather than from anything ADAM owns, which is a second reason not to cache them.

---

## Constraints carried over

- **Write `viewer/` freely. Ask before touching `ticvai/`.** Never run `ticvai/tools/refresh.sh` —
  run the individual derivation tools instead.
- `viewer/api/*.db` holds real accounts, e-mail addresses and password hashes. It is gitignored and
  must never be committed or copied into a zip.
- Windows, Python 3.9, cp1252 console. Open files with an explicit `encoding='utf-8'`; several tools
  have been bitten by this.
- The MCP must authenticate as a real account and inherit `clientMayCall()` gating. An MCP that
  reads around the audience filter would hand a client account the decision layer. Inherit it by
  sending the cookie and surfacing the server's 403 — do not copy the rule into the MCP.
- `ADAM_EMAIL` / `ADAM_PASSWORD` are real credentials. They belong in the MCP client's own config,
  never in `viewer/`, never in git, and never in a zip.
- **ADAM mints no task IDs.** OpenProject owns them. Anything that starts to look like a second issue
  tracker is the CF-124 failure being recommitted.

---

## To start the next session

Phases 1 and 2 are done. What is in front of you:

> Read `viewer/HANDOFF-adam-bridge.md`. Phases 1 and 2 are built in `viewer/mcp/` — nine tools, 28
> checks passing. Build **V-45, the settings page**: per-account OpenProject key, encrypted at rest,
> plus the git identity and the `claude mcp add` line. It gates phase 3. Ask me decisions 2 and 3
> when you get there.

**Before writing any code, run the harness** — `viewer/start.ps1`, then `mcp-check.mjs` with
`ADAM_EMAIL` and `ADAM_PASSWORD`. It takes a minute and tells you whether the package still has the
shape this document claims. Four of this file's claims have been confidently wrong; three were caught
only by running something.

**Open before phase 3 proper:** V-45 (this), V-49 (`/adam propose` has no local checkout to run the
eleven checks against), decisions 2 and 3, and the empty TICVAI project in OpenProject — 1b — which
needs a load nobody has signed off.
