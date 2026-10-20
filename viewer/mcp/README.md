# ADAM context bridge — MCP server

Nineteen tools for a developer's local Claude: **nine read the package**, **four are
about the work scheduled against it** in OpenProject, **three are for working a ticket**:
pulling it to local files, and changing its status once the developer has agreed, and **three
are for change requests**: raising, after the developer has agreed, that the package itself is
wrong, contradictory or short of something. Phases 1 to 3 of
`viewer/HANDOFF-adam-bridge.md`.

## What a developer runs

**The easy way is now the plugin.** Two lines in Claude Code, and nothing to download or unzip:

```
/plugin marketplace add Diretide298/Solution_Architecture
/plugin install adam@adam
```

Claude Code prompts for the four values in `userConfig` — the ADAM address, the developer's e-mail
and password, and optionally a package — and substitutes them into the server's `env`. The password
is declared `sensitive`, so it goes to the OS credential store rather than `settings.json`; the
`claude mcp add` registration the zip writes keeps it in plain text, where `claude mcp get` prints
it.

The manifests are `.claude-plugin/plugin.json` here and `.claude-plugin/marketplace.json` at the
repository root, whose entry's relative source (`./viewer/mcp`) is this directory — so the plugin is
the connector, not a copy of it, and there is no second place for the tools to drift.

The plugin also ships `hooks/hooks.json`, which wires the usage hooks that fill the Agents page.
Those were previously a block of JSON in `hooks/README.md` for somebody to paste into their
settings by hand, which meant they were mostly not installed. Since 13 October 2026 the zip's
setup and `/update-adam` put them into `~/.claude/settings.json` too, and `adam-hook.mjs` sits
beside `client.mjs` so both installs have one layout — `hooks/README.md` says how, and
`hooks-check.mjs` walks it end to end.

**A plugin install updates through the marketplace** (`/plugin update adam@adam`), never through
`update.mjs`: Claude Code replaces the whole plugin directory on update, so anything the updater
wrote there would work until it was silently reverted. `update.mjs` refuses outright when it finds
a manifest beside it, and `server.mjs` prints the marketplace command instead of the updater's.
Both are guarded by `plugin-check.mjs`:

```
node viewer/mcp/plugin-check.mjs
```

which also checks what `claude plugin validate` cannot — that the file the manifest launches
exists, that every `${user_config.*}` the server reads was declared, and that the marketplace entry
resolves to this directory.

### The zip, still

**The zip remains the first install for anyone not on the plugin**, and nothing has to move today.
Build it once, hand it out:

```powershell
powershell -ExecutionPolicy Bypass -File viewer\mcp\setup\build-zip.ps1
```

That writes `adam-connector-setup.zip` (about 220 KB, gitignored) at the repository root, and nothing
personal — the same file works for everyone. It opens to `adam-setup\`: `setup.cmd`,
`uninstall.cmd` and a README on top, and `adam-connector\` beside them with the connector files,
`setup.ps1` and `starters\` — a backend and a frontend skeleton (`setup/starters/backend`,
`setup/starters/frontend`) and the coding standards (`setup/starters/docs`, copied from
`ticvai-docs/setup`). A developer unzips it into their work folder and double-clicks `setup.cmd`,
which:

1. checks for Node.js 22+ and Claude Code,
2. asks for their ADAM email and password (hidden),
3. **signs in to ADAM with them before changing anything** — a wrong password stops here,
4. lists the ADAM projects that account can open (`/api/projects`) and asks for one by number,
5. asks **backend or frontend**,
6. offers `<work folder>\<project>-<role>` — beside `adam-setup`, or inside the folder it was run
   from in a terminal — and **creates it from the starter**: the skeleton with TICVAI renamed to
   the project (`Greenleaf Demo` → `GreenleafDemo`, `ticvai` → `greenleaf-demo`), `CLAUDE.md`,
   `.claude\` (permissions with `adam_apply` always asking, and `/ticket`, `/board`, `/done`), the
   role's standards in `project-bible\setup\` (not renamed), and a git repository with the
   starter as its first commit. **Frontend** (13 Oct 2026: one repository per app) is different: a new
   folder is a workspace with ADAM's files only (`CLAUDE.md`, `.claude\`, `project-bible\setup\`),
   setup prints one clone command per app repository, and the developer clones inside it and opens
   Claude Code in the workspace (`-UseStarter` brings back the old Nx starter). A folder that already
   has files keeps every one of them and gets ADAM's own where they are missing, nothing committed;
   in a repository, what was added goes into `.git\info\exclude`, so it never reaches the team's
   repository (`setup-check.mjs` checks both orders),
7. copies the connector to `%USERPROFILE%\.adam\connector` (without the starters: the installed
   copy can reconnect and remove, not create),
8. registers it with `claude mcp add -s local` for that folder only — or `-s user` for
   `-Folder all` — with `ADAM_PROJECT` and `ADAM_WORKDIR` set, reads it back, and removes any
   every-folder registration an older setup left, so no other session can use ADAM,
9. optionally runs `mcp-check.mjs` against the live site, and prints the `claude mcp remove`
   line for each registration it holds.

The starters are checked, not assumed: the backend builds and passes `dotnet test` on .NET 10,
renamed or not, and the frontend passes `pnpm install`, `lint`, `typecheck` and `test`.

**One registration per folder, and two spellings of each.** Claude Code files a `local`
registration under the folder it was run in, *as spelled*: VS Code starts it in `c:\work\repo`
and a terminal in `C:\work\repo`, and `~/.claude.json` keeps those as two different projects.
So setup registers both. It cannot use `Set-Location` for that — PowerShell rewrites the drive
letter to upper case — and starts Claude Code with `ProcessStartInfo.WorkingDirectory` instead.
It also starts npm's `bin\claude.exe` directly rather than `claude.cmd`, so Command Prompt never
sees the password: any character works, including `"`, `&`, `%` and a trailing `\`.

A developer on two projects or roles runs setup once for each. Setup keeps a ledger of what it
registered in `registrations.txt` beside the installed connector, with copies of `setup.ps1`,
`setup.cmd` and `uninstall.cmd`; `setup.ps1 -RemoveFolder <path>` removes one folder (both
spellings), and `uninstall.cmd` removes every registration and the files. A session opened on
a subfolder of a registered folder does not see ADAM — Claude Code matches the folder exactly.
The scripts are kept to plain ASCII on purpose — PowerShell 5.1 reads a
BOM-less script in the ANSI code page — and `build-zip.ps1` refuses to build if that slips.

## Updating an installed connector

**The zip is for the first install. After that the connector updates itself**, which is the
difference between a change landing here and a change reaching anybody: handing out a new zip and
asking eleven people to re-run setup is a distribution step that does not happen.

A developer runs `/update-adam`, or the command it wraps:

```
node "%USERPROFILE%\.adam\connector\update.mjs"
```

It asks the viewer for `/connector/version`, compares, and replaces the files only if they differ,
keeping what it replaced in `backup-<build>` beside the connector. The new code runs on the next
Claude Code start — the connector cannot replace the files it is running from.

Nobody has to remember to check: `server.mjs` asks on every start and says one line, with the
command in it, only when there is something to say. It is best-effort and silent about failure, so
a developer who is offline gets a connector that works and no noise.

**The build is a hash of the shipped files, not a version number.** Nothing to bump and nothing to
forget; two people are on the same build exactly when they are running the same code. `version.mjs`
holds the list, and `setup.ps1` and `build-zip.ps1` copy the same seven — if those three ever
disagree, every install computes a build the server never offers and updating silently fixes
nothing, so `mcp-check.mjs` compares the three lists and fails when they drift.

**The updater says which files it can take** (`/connector/version?accept=…`, the same on
`/connector/bundle`), and the viewer answers with those files and the hash of exactly those. An
updater from before 13 October 2026 sends no list and refuses a bundle naming a file it does not
know, so it is answered with the six it does know (`BEFORE_HOOKS` in `version.mjs`): it updates
cleanly to the new updater, and the next run of that one brings `adam-hook.mjs`. `latest` in the
version answer is the whole connector's build, which is what the fleet list compares against.

What `update.mjs` will not do: fetch from any address but the configured one, write any path that
is not already part of the connector, or run anything it downloads. It writes text files and tells
you to restart. The one other file it touches is `~/.claude/settings.json`, once, to add the usage
hooks — with its own code, keeping a backup, never against a file it cannot parse, and never again
after somebody has taken them out (`hooks/README.md`).

**The workspace's own files follow it** (CHG-ADM-006). Setup adds only what a folder lacks, so a workspace made
before a change used to keep its old `/ticket`, `/board` and `CLAUDE.md` for good. Now `/update-adam`, run in the
workspace folder, and a re-run of setup replace ADAM's five command files there
(`.claude/commands/ticket|board|cr|done|update-adam.md`, the old ones kept in `.adam/backup-workspace-*`), reading
them from the viewer's `/connector/workspace?role=` (the same starters the zip carries) or, for setup, from the
unzipped starters. `CLAUDE.md` is the team's: only the part between `<!-- ADAM:start name -->` and
`<!-- ADAM:end name -->` is replaced; a section of a `CLAUDE.md` made before the markers is left exactly as it is, with one
line saying which section to replace and the new text in `.adam/new-claude-sections.md`. Missing files are not
created here (setup adds them and keeps them out of git). Two exceptions, for the backend's [DB] check (20 October
2026): ADAM's script `.claude/scripts/db-ticket.mjs` is added or refreshed (kept out of git through
`.git/info/exclude`, as setup does), and a section a CLAUDE.md never had, `<!-- ADAM:start db-ticket -->`, is added
whole with its markers after "Working a ticket (ADAM)" (or at the end of a CLAUDE.md without markers), so nobody
copies it by hand. The project's `.claude/settings.json` is not touched, so an existing folder lacks the permission
line for the script: Claude asks once before running it (allow it for the folder), or add
`"Bash(node .claude/scripts/db-ticket.mjs:*)"` to `permissions.allow` by hand. The first `/update-adam` on an older connector brings the
new updater and cannot use it yet, so run `/update-adam` a second time. `mcp/workspace-check.mjs` holds all of it.

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
| `adam_board` | none, or `only` (`workable` / `blocked`), `subtasks`, `limit` | what is open and assigned to you, what each item touches, and which open blocking CRs affect it (`blocked`; `firstWorkable`) |
| `adam_team` | none, or `person` (a name, first name or part of one), `days`, `limit` | **read-only**: everybody's in-progress tickets with in progress / awaiting QA / stalled / open / finished-in-14-days counts; or one teammate's open tickets (in progress first) and what they finished lately (closed or moved to Ready for QA, with status and date). Read with your own OpenProject token, so it shows only what you could see there; refused to client accounts |
| `adam_work` | `key` | one work package, live, plus the artefacts it touches |
| `adam_links` | `kind`, `id` | what work is scheduled against one artefact |
| `adam_link` | `kind`, `id`, `key` — or `remove` + `linkId` | **writes**: records that a work package is about an artefact |
| `adam_pull` | `key` (or nothing, for the whole board), `dir`, `limit` | **writes local files**: `.adam/work/<key>/` and `.adam/board.md`; always at the latest release ADAM serves; when the release moved since the ticket's previous pull, README.md says what changed and `spec-diff.md` has the diffs; README.md lists the change requests raised from the ticket |
| `adam_repin` | `key`, `dir`, `breaking`, `note` | **not needed** (every pull is at the latest release); kept for older instructions: moves the ticket to the latest release and pulls again. Changes nothing in OpenProject |
| `adam_propose` | `key`, and `status` / `percentDone` / `comment` | the change that would be made, and a one-use code. **Changes nothing** |
| `adam_apply` | `key`, `proposal`, `dir` | **changes OpenProject**, as you, with that code — after you said yes |
| `adam_changes` | none, or `id`, `status`, `kind` + `target`, `ticket`; or `from` / `to` release tags | the project's change requests; one in full; or the release notes between two tags |
| `adam_draft_change` | `kind`, `target`, `title`, `problem`, `evidence`, `options`, `recommendation`, `blocking`, `ticket`, and the intake: `source` (default developer), `sourceRef`, `approver`, `triage`, `when`, `artefacts`, `contractImpact`, `effortPoints`, `clientSignoff` | a draft and a `draft` code, plus open requests already on that artefact — **files nothing** |
| `adam_raise_change` | `draft` | **files the change request in ADAM** (CR-007) — after you said yes |

**Change requests.** When the package contradicts itself, is wrong, or lacks what a ticket needs,
Claude does not settle it in code: it checks `adam_changes` for one already open on that artefact,
drafts one with the conflicting passages quoted and the options listed, shows it, and files it only
after a yes (a one-use code, 30 minutes). A blocking one can put the ticket On hold with "Blocked by
CR-007". They are internal — a client account neither reads nor files them — and are settled on
ADAM's **Changes** page (`/changes.html`) by an admin or a reviewer on the project, never by the
person who raised it unless they are an admin: open → accepted or rejected (a rejection needs a
reason) → done, with what fixed it. The page exports what it shows as CSV.

**Releases (C2, C9; always the latest from 14 October, CHG-ADM-001).** ADAM serves the package at
its newest release tag (`r1`, `r2`, … in the package repository; `viewer/lib/releases.mjs`), not at
whatever the working tree holds, and **every pull is at that release**: you are always on the latest
release, and nobody chooses between releases. The first `adam_pull` of a ticket records the tag in force
as its pin; a later pull, once ADAM serves a newer tag, moves the pin to it (the service does it, logged
`auto`, so an older connector is moved too), compares every artefact the ticket is linked to between the
previous pull's tag and the latest, and says in README.md what changed, with the diffs in `spec-diff.md`.
The linked files are always the latest release. A breaking contract change listed in
`docs/active/breaking-changes.yaml` is called out for a ticket that produces the operation or consumes
it, so code written before the pull can be checked. `adam_board` shows `r1 -> r2` for a ticket last
pulled at an older release; its next pull is at the latest. `adam_repin` is kept for older instructions
and is never needed.

**Change requests reach the ticket (CHG-ADM-002).** When a request is settled (accepted, done or
rejected), the ticket it was raised from is told: an open ticket gets one comment written for the agent
that pulls it (what was decided, which release carries it, what to do now); a closed ticket gets a child
task for the change (one per request, at most; filed before the request is marked Done). `adam_pull` lists every
request raised from the ticket near the top of README.md, under "Change requests on this ticket", with
its decision and release: follow the settled ones, wait on the open ones.

**A blocker is always a change request, then the next workable ticket (CHG-ADM-004).** When the package
blocks a ticket (a contradiction, missing storage, an undefined rule), the agent raises a CR with
`blocking: true` (draft, the person says yes, file), proposes the ticket On hold naming the CR (applied only
after a yes), and never works around it or builds a guess. Then it looks for the next ticket it can finish:
the service works out, for every ticket on the board, which open blocking CRs affect it (raised from it, or
naming one of its linked artefacts, or a table one of its operations reads or writes by the lineage of the
release served; an accepted CR blocks until a served release carries it), so `adam_board` with
`only: "workable"` is a lookup. The pull's README.md has a "Blocked by" section above "Change requests on
this ticket".

**Change request intake (C8).** A draft carries where the change came from (`source`: minutes,
answer, design, developer, audit, and `sourceRef`, the line that finds it again — a developer's
defaults to the ticket), who approved it, its triage class (clarification, scope, defect) and when
(now, later), every artefact it touches, its contract impact (none, additive, breaking), the change
in effort in points, and the client's sign-off — required when the source is minutes. A breaking
impact needs an approver. The request also records the release the person raising it was on.

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
one JSON file per linked artefact go to `.adam/work/<key>/` in the
folder Claude is working in — `dir` from the call, else `ADAM_WORKDIR` (setup sets it for a
folder registration), else the server's own folder. Claude then reads `README.md` and opens
only the files it needs. Linked decisions are listed, not pulled; `adam_decisions` answers
them when a build needs one. `.adam/` writes its own `.gitignore` of `*`. Pulling again replaces
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

```bash
node viewer/mcp/db-ticket-check.mjs              # add --package for the whole DDL (about 4 minutes)
```

A [DB] ticket's quick check (20 October 2026). `adam_pull` writes `expected-schema.json` into a
[DB] ticket's folder: the tables' end state as parsed by `tools.mjs`, and the package statements
that make them. The backend starter's `.claude/scripts/db-ticket.mjs` applies only the ticket's file
to a template copy of the previous state, applies it again (which must succeed and change nothing),
applies the package statements to a second copy, and compares the two databases whole, in
PostgreSQL's own words. This checks the statement picking, the compare, the pull (against a stand-in
ADAM serving `ticvai/`) and, with Docker, the script on a developer folder made from the real DDL,
including the files that must fail. `--package` requires the statements tickets are given to make
exactly the database the whole package makes, tenant and control.

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
