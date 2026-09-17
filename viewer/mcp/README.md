# ADAM context bridge — MCP server

Sixteen tools for a developer's local Claude: **nine read the TICVAI package**, **four are
about the work scheduled against it** in OpenProject, and **three are for working a ticket**:
pulling it to local files, and changing its status once the developer has agreed. Phases 1 to 3 of
`viewer/HANDOFF-adam-bridge.md`.

## What a developer runs

**The easy way is the setup zip.** Build it once, hand it out:

```powershell
powershell -ExecutionPolicy Bypass -File viewer\mcp\setup\build-zip.ps1
```

That writes `adam-connector-setup.zip` (about 33 KB, gitignored) at the repository root. It holds the
connector files, `setup.cmd`, `uninstall.cmd`, `setup.ps1` and a README, and nothing personal — the
same file works for everyone. A developer unzips it and runs `setup.cmd` **from the code folder**
whose Claude Code sessions should use ADAM (`cd C:\work\repo; C:\Downloads\adam-connector\setup.cmd`),
which:

1. checks for Node.js 22+ and Claude Code,
2. asks for their ADAM email and password (hidden),
3. **signs in to ADAM with them before changing anything** — a wrong password stops here,
4. lists the ADAM projects that account can open (`/api/projects`) and asks for one by number,
5. asks for the folder, offering the one it was started from (Enter takes it; `all` means every
   folder; double-clicked, there is no default and a path must be pasted),
6. copies the connector to `%USERPROFILE%\.adam\connector`,
7. registers it with `claude mcp add -s local` for that folder only — or `-s user` for `all` —
   with `ADAM_PROJECT` and `ADAM_WORKDIR` set, reads it back, and removes any every-folder
   registration an older setup left, so no other session can use ADAM,
8. optionally runs `mcp-check.mjs` against the live site, and prints the `claude mcp remove`
   line for each registration it holds.

**One registration per folder, and two spellings of each.** Claude Code files a `local`
registration under the folder it was run in, *as spelled*: VS Code starts it in `c:\work\repo`
and a terminal in `C:\work\repo`, and `~/.claude.json` keeps those as two different projects.
So setup registers both. It cannot use `Set-Location` for that — PowerShell rewrites the drive
letter to upper case — and starts Claude Code with `ProcessStartInfo.WorkingDirectory` instead.
It also starts npm's `bin\claude.exe` directly rather than `claude.cmd`, so Command Prompt never
sees the password: any character works, including `"`, `&`, `%` and a trailing `\`.

A developer on two packages runs setup from each checkout. Setup keeps a ledger of what it
registered in `registrations.txt` beside the installed connector, with copies of `setup.ps1`,
`setup.cmd` and `uninstall.cmd`; `setup.ps1 -RemoveFolder <path>` removes one folder (both
spellings), and `uninstall.cmd` removes every registration and the files. A session opened on
a subfolder of a registered folder does not see ADAM — Claude Code matches the folder exactly. Rebuild the zip whenever anything in `viewer/mcp` changes; the README inside is stamped with
the commit it was built from. The scripts are kept to plain ASCII on purpose — PowerShell 5.1 reads a
BOM-less script in the ANSI code page — and `build-zip.ps1` refuses to build if that slips.

**By hand**, for Git Bash or a machine where the zip is not an option:

A viewer must be reachable — the MCP reads through it and has no other source. **Most developers
should point at the deployed one and run nothing locally:**

```bash
claude mcp add -s user adam -e ADAM_VIEWER_URL=https://adam.ainfinite.ai -e ADAM_PROJECT=ticvai -e ADAM_EMAIL=you@softlabsgroup.com -e 'ADAM_PASSWORD=YOUR_PASSWORD' '--' node C:/path/to/adam/viewer/mcp/server.mjs
```

**Every `-e` goes before the `--`.** Everything after `--` is passed to node as arguments, and
`server.mjs` never reads its arguments. This line was first published the other way round, which
registers a server with an empty environment that then cannot sign in — `claude mcp get adam`
shows it at once: the credentials appear under `Args:` instead of `Environment:`.

**And keep the quotes on `'--'`.** In PowerShell, `claude` is npm's `claude.ps1` wrapper, and
PowerShell silently drops a bare `--` passed to a script; the command then fails with
`missing required argument 'commandOrUrl'`. Quoted, it gets through, and bash simply removes the
quotes — so this one line works in PowerShell and Git Bash alike. Not in Command Prompt (`cmd.exe`),
which does not treat single quotes as quotes.

One line, because `\` is not a line continuation in PowerShell. The password is single-quoted, which
both bash and PowerShell treat literally. `-s user` makes the bridge available in every project you
open; without it, it only appears when Claude runs in the directory you added it from.

The password ends up in plain text in Claude's own settings file (`~/.claude.json`), readable by
anything running as you. Use a password for ADAM that you use nowhere else, and one **without quote
characters**: Windows PowerShell 5.1 splits the argument at a `"` inside it, and the command fails
with the same `missing required argument` error. Tested 17 September.

Working on the viewer itself? Run `./start.ps1` and drop `ADAM_VIEWER_URL` for the local default.

| variable | default | what |
|---|---|---|
| `ADAM_EMAIL` | — | your viewer account. Required. |
| `ADAM_PASSWORD` | — | its password. Required. |
| `ADAM_VIEWER_URL` | `http://127.0.0.1:4173` | where the viewer is. `https://adam.ainfinite.ai` is the deployed one. |
| `ADAM_PROJECT` | the account's default package | which package to read. Setup sets it. It also decides which OpenProject project the work tools read — see below. |

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
| `adam_pull` | `key` (or nothing, for the whole board), `dir`, `limit` | **writes local files**: `.adam/work/<key>/` and `.adam/board.md` |
| `adam_propose` | `key`, and `status` / `percentDone` / `comment` | the change that would be made, and a one-use code. **Changes nothing** |
| `adam_apply` | `key`, `proposal`, `dir` | **changes OpenProject**, as you, with that code — after you said yes |

Start with `adam_search` when you have a name but not a kind. A miss returns candidate spellings
rather than an empty result — a wrong id is usually a wrong spelling of a right one.

**The four work tools read one OpenProject project, chosen per ADAM project.** An admin picks it
on the admin page under Projects (`PUT /api/pms/projects/{id}`); TICVAI reads `ticvai`
(OpenProject project 153), filled in by the migration. The board filters on it, and a work
package or a new link from any other OpenProject project is refused with the project it is
actually in. A package with nothing chosen answers 428 and says who can fix it. The connector
sends `project_id` with every one of these calls, from `ADAM_PROJECT`.

**The four work tools read OpenProject as *you*.** They need a token stored on your settings page —
without one they say so and name the page, rather than failing. There is no service account,
deliberately: a shared credential attributes every change to a robot, and the history is most of what
a PMS is for.

**`adam_pull` keeps the conversation small.** A ticket, its description and milestone, and
one JSON file per linked artefact (plus the ADR's own text) go to `.adam/work/<key>/` in the
folder Claude is working in — `dir` from the call, else `ADAM_WORKDIR` (setup sets it for a
folder registration), else the server's own folder. Claude then reads `README.md` and opens
only the files it needs. `.adam/` writes its own `.gitignore` of `*`. Pulling again replaces
everything except `notes.md` (the developer's) and `log.md` (applied changes). It refuses a
drive root and a folder that does not exist.

**Changing OpenProject takes two calls and a yes in between.** `adam_propose` reads the work
package, works out the change (status by name, % done, a comment) and stores it in
`wp_proposal` under a one-use code valid for 15 minutes — nothing is sent. Claude shows the
person the change. `adam_apply` with the code sends it as that person, with their token, and
only if the work package's `lockVersion` is still the one they were shown; otherwise it is
refused and nothing changes. A code works once, for that person and that ticket only. Claude
Code's own permission prompt stands in front of `adam_apply` as well — do not "always allow"
it. Assignees, dates and the work packages themselves remain OpenProject's alone.

**`adam_link` writes one row and nothing else** — that a work package
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

45 checks with a credential stored, 34 without. The live half pulls into a temporary folder,
proposes a comment it never applies, and tries a made-up code — nothing in OpenProject changes. The handshake and tool-listing ones need nothing running. The live calls need the viewer
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

A background sync of `.adam/`. Pulling is on request, so the files say when they were pulled
rather than pretending to be current. (The `/adam propose` in `viewer/HANDOFF-adam-bridge.md` is a
different thing — a change to the *package* — and is still open as V-49.)

Anything that changes a work package without the person agreeing first, or that changes its
assignee or dates, or creates work packages. Status, assignee, dates and the work packages themselves are
OpenProject's, and a second system writing them is the failure `delivery-plan-vs-package.md` already
has open as CF-124: two independent plans over the same work, neither referencing the other.

**`adam_impl` is not here and cannot be yet.** It was meant to start from the file you have open and
return the screen behind it. `ticvai/repos/ticvai-frontend/` is a real Nx monorepo with six apps and
**every one of them is `export {};`** — only `packages/offline-core` has code. There is no route file
to resolve against, so the tool would answer "not implemented" for every input. The screen records
already carry `app` and `route`, so this becomes small the day the apps grow routes.
