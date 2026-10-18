# Release runbook: how a change becomes a release

> **For:** Chinmay (lead) and anyone running a release. **Decided 1 October 2026** (LLM Council, `docs/active/council/council-report-2026-10-01.html`).
> **The rule:** OpenProject holds who, when, state and order. The package, served by ADAM at a release tag, holds what. ADAM's propose-then-confirm CR flow is the only way a change gets in.

## Cadence
Releases go out **Tuesday and Friday**. CRs confirmed by **Monday or Thursday at noon** make the next release. Anything later waits for the one after.

## 1. Intake: every change is a CR
Minutes, client answers, design returns, developer gaps and audit findings each become a CR in ADAM, and each CR records:
- **Source:** minutes, answer, design, developer or audit, with the line or reference it came from.
- **Approver.** A change from minutes needs the **client's sign-off** before it is confirmed.
- **Triage:** clarification, scope or defect; now or later.
- **The artefact ids it touches:** operations, tables, screens, services.
- **Contract impact:** none, additive or breaking. A breaking change is listed in `docs/active/breaking-changes.yaml` with its approver.
- **Effort change,** in points.

If a CR contradicts a registered decision (the Decisions Register or an ADR), it goes back to the lead. It is not applied.

## 2. Edit: agents on branches
The rule for agent edits:
- One CR, one branch (`cr/<id>-<slug>`).
- An AI agent or a person edits **authored sources only**: contracts, screens, flows, states, events, ADRs, docs, the team and plan inputs. Never derived files.
- The lead reviews the diff and merges it into `change-process`, or into `main` after `r1`.
- No agent commits on the release branch directly. No agent runs a full refresh in the main tree.

## 3. Refresh: safe, then scoped
- `bash tools/refresh-safe.sh`: refreshes in a throwaway worktree. It merges into the main tree **only if every check passes** (no new failures against the baseline). A failed or interrupted run keeps its worktree for `--resume` (which never merges); any other run removes it. One run at a time (a release lock), and nothing merges if HEAD moved during the run (STALE BASE). How to run it, read a failure and resume: `docs/active/refresh-runbook.md`.
- **Policy (council of 3 October, CHG-RSPD-001):** scoped runs and single checkers while iterating; the full gate only at the Tuesday and Friday releases with the CRs batched; never a gate with more than two agents running.
- `bash tools/refresh-safe.sh --changed <paths>`: runs only the steps downstream of the changed files (from `handoff/refresh-manifest.json`). Use it between releases. **A full `refresh-safe.sh` run is required before tagging.**

## 4. Gates (in the checks)
- **Keys:** a pushed key is never renamed (`check-key-stability`).
- **Migrations:** the baseline migrations are frozen at `r1`; table changes come out as new forward migrations (`check-migration-freeze`); anything destructive goes to `handoff/migration-review.md` for a person.
- **Contracts:** a breaking change must be listed in `breaking-changes.yaml` (`check-contract-compat` against `r1`).
- **Audit classes:** every root-issue class from the audit has its check (`docs/active/root-classes.md`).
- **Ticket links:** every Block A feature and task links something ADAM pulls, and every link ADAM loads resolves to
  an operation, table (or declared read view), screen, ADR, tracked file or service the package has
  (`check-ticket-links`; CHG-GRD-001). It reads `handoff/service-docs/adam-links.json`, which a rebuild does not
  write: run `python3 tools/adam-links.py` after the full refresh and before the release gate, so it checks the
  links this release will load.
- **Approved UI:** no visible change to a client-approved screen without the client's approval recorded in
  `docs/active/approved-ui-changes.yaml` (`check-approved-ui` against `handoff/approved-ui.json`; CHG-GRD-002).

### The rehearsal pull: the last gate step before the tag (CHG-GRD-003, CHG-RHS-001)
The checks read the package; the rehearsal reads what a developer will get. It runs after the full gate is green
and before anything is tagged or pushed (Block A audit plan, step 11a; lead, 14 October 2026: "before pushing r6
can we simulate the results in the pulls?"). Tag `r<N>-rc` locally first and never push it. Then, from `ticvai/`:

    python3 tools/rehearse/prepare.py snapshot --out <work>/op-snapshot.json      (reads OpenProject; writes nothing)
    bash tools/rehearse/rehearse.sh r<N>-rc --base <last live pull> --op-snapshot <work>/op-snapshot.json

The last live pull is the previous release's live re-pull (section 7), its `direct/` folder. The one command:
1. Clones the repository into its work folder at `r<N>-rc` (no remote; the mirrors as ADAM's release export keeps
   them) and tags the candidate `r<N>` in that clone only.
2. Runs a local ADAM on the candidate with the stand-in OpenProject (`tools/rehearse/stand-in-openproject.mjs`)
   loaded from `r<N>`'s bundle (`handoff/service-docs/op-release.json`, or built at the candidate when the committed
   one is older), applied with the apply's rules (`tools/rehearse/simulate.py`) to OpenProject as the snapshot shows
   it, so every ticket reads as it will after the apply. Tickets the release creates get stand-in ids (990001 and up)
   in `op-created-r<N>.json`, the file the apply writes.
3. Loads the ticket links the way production does, never by its own setup: `tools/op-created-merge.py` with those
   ids, `tools/adam-links.py`, then `viewer/api/load_links.py --prune` (dry run, then `--apply`) into the
   rehearsal's database. On r6 the rehearsal's setup loaded them and passed, while the live ADAM had none (P-22).
4. Pulls every ticket of the block being delivered (Block A: every feature and task) with the shipped connector,
   the same `adam_pull` a developer runs (`tools/rehearse/pull-direct.mjs`, `ADAM_URL` set to the local ADAM).
5. Compares ticket by ticket with the last live pull, and keeps the difference: it is the developer impact list
   (`rehearsal-summary.md` and `rehearsal-report.json` in the work folder).
6. Checks the people as well as the links: no open ticket keeps someone who left (the bundle's `successors`) as
   assignee or Accountable, started tickets included, read from the stand-in's OpenProject state, because a pull does
   not carry Accountable. On r6 the rehearsal checked assignees only, and 158 Ready for QA tickets kept Tanmay
   Dukhande as Accountable (P-25). Without the snapshot this criterion is not judged and the rehearsal does not pass.

**It passes only with all five at zero:** 0 pull errors; release `r<N>` on every ticket (`release.current`); 0
tickets with nothing linked (`linked: 0`, features and tasks alike); 0 dead links (`notFound: 0`); 0 open tickets
with someone who left as assignee or Accountable. Anything else is fixed in `r<N>` and the rehearsal runs again; the
tag waits. On r5 the pull found 123 features and 29 tasks with nothing linked and 55 tickets with links ADAM could not
find, after the release was out; this step finds them while they are still the package's to fix. It touches nothing
live: the clone has no remote, ADAM's database is a scratch one, OpenProject's token is removed from every step, and
it refuses the ports 4173, 8787 and 8798 (a local ADAM another session may be running).

## 5. Tag
Once everything is green, the rehearsal pull included (section 4):
1. Commit.
2. `git tag r<N>` on the package **and** the six mirror repos.
3. Push the branch **and the tag by name** to both remotes: `git push origin main r<N>`, then
   `git push github main r<N>`; the same push of its branch and `r<N>` in each of the six mirror repos. A bare
   `git push` sends no tag, and ADAM's server knows only the tags it fetched: r5 was tagged and never pushed, so
   ADAM served r4 for a day after OpenProject said r5 (PROCESS-LOG P-20, 14 October 2026; CHG-GTE-006).
4. `python3 tools/check-adam-latest-release.py --remotes`: it fails if the newest `r<N>` here is missing from
   `origin` or `github`.
5. Rebuild the setup zip from a clean HEAD.

## 6. Distribute
- **OpenProject:** on the server, run `op-release-server.sh dry-run r<N>`, then `op-release-server.sh apply r<N>`.
  That one script:
  - turns OpenProject's notifications off for the whole instance first (OpenProject 10 has no per-run switch; the
    list is saved in `.release-out/notified_events.json`) and leaves them off for the steps below (P-23);
  - creates new tickets and writes pointer bodies;
  - syncs assignee and week; a started ticket keeps its owners except a field held by someone who left, which goes
    to the plan's person or the successor (P-25);
  - sets build order and links;
  - retires tickets that left the plan, and removes the build-order links of the ones it rejects (P-24);
  - runs a health check. Every health line must be zero apart from tickets the plan does not know; anything else is
    fixed before the next step.
  A manual fix after the apply names its tickets and people from the bundle (`op-release.json`: `responsible`,
  `assignee`, `parent`), never from a list written by hand: r6's sheet named the wrong Accountable for two migration
  families (P-26). Server scripts run on the container's Ruby (2.6 on OpenProject 10): nothing newer than 2.6.
- **New ticket ids:** copy `.release-out/op-created-r<N>.json` to the workstation, then
  `python3 tools/op-created-merge.py <file>`, `python3 tools/adam-links.py` (with `TICVAI_OP_TOKEN`), and commit and
  push `pms-map.json` and `adam-links.json`.
- **OpenProject, a release that creates nothing** (a change-request release): from any workstation,
  `python3 tools/op-release-api.py --from r<N-1> --to r<N>` (dry run), then `--apply`, with `TICVAI_OP_TOKEN`
  set. It applies only the tickets that differ between the two bundles, over the REST API, with the same rules
  (New tickets set, started ones commented, no mail; a started ticket's text is never rewritten). It refuses, naming the server path, when the release creates
  tickets, changes links or retires tickets.
- **Change requests:** settle them and tell their tickets with ADAM's `viewer/api/settle_changes.py
  decisions.json` (dry run, then `--apply`), or on ADAM's Changes page, which tells the ticket the same way
  (CHG-ADM-002): a ticket that is not closed gets one comment for the AI agent that pulls it; a closed one
  gets a child task for the change, created before the CR is marked Done. Never two tickets or two identical
  comments per CR. Migration work a CR causes is a child task of the affected MIG-* ticket for the migration
  owner, filed by the lead. If ADAM cannot create a child task (its apply answers 502 behind the proxy), make it
  on the OpenProject server with `tools/op-create.rb`, subject `[CR-nnn] ...`, under the CR's ticket, then record
  it in ADAM with `settle_changes.py --link-existing` (or `POST /api/changes/<n>/ticket/link`, admin) (CHG-ADM-003).
- **Notifications back on:** once the CRs are settled and the child tasks are filed, on the OpenProject server:
  `op-release-server.sh notify-on`. It refuses unless the restored list matches the saved one. Then send the team
  and developer messages, so they reach people with the tickets already in their final state.
- **ADAM:** on the box, run `git pull` and deploy. ADAM serves `r<N>`, and every developer and agent is always
  on the latest release: their next `/ticket` is at `r<N>` and shows what changed since their previous pull.
- **ADAM's ticket links:** ADAM reads them from its own database, not from the release (P-22). After the new ids are
  pushed, on the box: `git pull`, then as the service user
  `python3 viewer/api/load_links.py ticvai/handoff/service-docs/adam-links.json --email <lead> --prune --db <ADAM db>`
  (dry run), then the same with `--apply`. Without it every ticket the release linked pulls with "What this
  touches (0)".
- **Client:** send the release note, `python tools/release-notes.py r<N-1> r<N>`: what their answers changed, and what is waiting on them.
- **Last, one pull through ADAM:** once ADAM is deployed, run one `adam_pull` of any ticket. Its release must say
  `r<N>`. If it names an older release, ADAM has not fetched the tag (on the box: `git fetch --tags`, then
  deploy) and the release is not out yet (PROCESS-LOG P-20; CHG-GTE-006).

## 7. Re-audit, every release
- Every check is green.
- Pull a **sample of 20 to 30 tickets** through ADAM at the new tag, across every developer's board. After a release
  with a rehearsal, pull the whole rehearsal list on the live ADAM instead, the tickets the release created by their
  real ids and not the rehearsal's stand-in ids, and compare: it must match the rehearsal. From `ticvai/`, with
  `ADAM_URL`, `ADAM_EMAIL` and `ADAM_PASSWORD` set (the audit account; it reads tickets and records that account's own pull marks on live ADAM, nothing else):
  `bash tools/rehearse/rehearse.sh live-repull r<N> --rehearsal <work> --created <op-created-r<N>.json>`. Its
  `live/direct/` folder is the next rehearsal's last live pull.
- A new root issue gets a check before it counts as closed.

## 8. Configuration promotion after go-live
A package release moves the specification; a tenant's **configuration** moves between its environments by
[ADR-0070](../adr/0070-configuration-moves-as-a-versioned-package.md) (Chinmay, 2 October, DEC-168; CHG-DOC-011):
never copy, merge or reverse-migrate a production database. The schema goes forward only, expand then contract
(`check-migration-freeze` after r1). Configuration goes as a versioned package with stable keys: a diff against
production, approval by someone other than its author, an idempotent upsert by key and an audit record; rollback
re-applies the previous package. Secrets and environment settings never travel in a package.

## Rules from 5 October (council of 2 October)
Source: the council's final reports, `docs/active/council/council-report-2026-10-02-opus.html` and `docs/active/council/council-report-2026-10-02.html`. The short form every agent loads is `ticvai/CLAUDE.md`. These
rules add to sections 1 to 7; they do not replace them.

**R1. Every change is a change-log entry, with its decision and why.** One file per change in
`changes/entries/` (`changes/README.md`), plus the ADAM CR from §1. The entry records the decision (what,
who, when), why (citing the MoM, DI, R-root, ADR, council, finding or commit), the keys touched, the
started and unstarted tickets, the release tag and a prevention. The commit names the id. Gate:
`check-changelog`. At a release, run `python3 tools/check-changelog.py --since r<N-1>`: every commit that
touched an authored input since the last tag must name an entry. A release refresh commit may instead carry
`CHG-exempt: <reason>`, and the tool prints every exemption.

**R2. No change closes without a prevention.** The prevention is a check registered in `run-checks.py`, a
generator rule or a template field, and it must fail on the commit before the fix (the author runs it there
and says so). `prevention: none` needs a reason and the lead's approval. A new root class gets its check
before its fix merges (`change-rules.md` CR-7).

**R3. Triage.** Every CR is triaged `blocker` (fixed in the next release, even on started tickets: a comment
for the agent, or a child task when the ticket is closed, R5), `fix-forward` (into unstarted tickets at the next tag) or `defer` (logged, open). The lead triages
in a **daily 30-minute slot**.

**R4. Client sign-off.** A minutes-sourced change carries `client_signoff`. Sign-offs go to the client as
one batch a week (contract decisions and open questions included). Silence for 5 working days after the
batch is sent is acceptance, recorded as `by: "silence (5 working days)"` with the date.

**R5. Started tickets, and always the latest release** (replaced 14 October 2026, CHG-ADM-001 and
CHG-ADM-002). A ticket past "New" is frozen: its OpenProject text is never rewritten. Developers and agents
always build against the latest release: every ADAM pull serves the release ADAM serves now and moves the
ticket to it (the pin moves by itself, logged `auto`), and `/ticket` says what changed since the ticket's
previous pull. Nobody chooses or asks between releases. A fix to a started ticket reaches it when its CR is
settled: a ticket that is not closed gets a comment written for the AI agent that pulls it (and the pull's
README.md lists the CR, its decision and its release under "Change requests on this ticket"); a closed
ticket gets a **child task** for the change, created before the CR is marked Done. A CR's work is one child
task of the ticket it was raised from; migration work it causes is a child task of the affected MIG-*
ticket, assigned to the migration owner (`docs/active/team.json` `migrations.owner`). Unstarted tickets get
the fix at the next tag through their pointer bodies.

**R6. The release window.** Releases go out on Tuesday and Friday. No spec edits on Monday or Thursday after
the noon CR cut-off. Edits wait for the next window.

**R7. Plan changes.** A plan change is an entry of kind `plan`: proposed, decided no sooner than 24 hours
later, shipped only at a release, never announced before it is committed, and never reversed within 48
hours. Gate: `check-changelog` (the plan-change rule and the plan-file commit rule).

**R8. Agents.** Every agent works in its own git worktree on its own branch (`cr/<id>-<slug>` or a batch
branch), makes checkpoint commits, and never leaves partial work in the main checkout. When agents share a
tree, each writes only its own files. Every source an agent cites is inside git. `refresh-safe.sh` already
refuses a release over uncommitted authored changes.

**R9. Audit order and AI budget.** Checks first: every known root class is a deterministic check, run over
all 16 apps in block order A, B, C, D. AI is spent only where checks cannot see, on new classes, sampled at
20 screens per app and widened only where a new class appears. Each new class gets a check. The weekly AI
budget is **Block A 50%, Block B 25%, Blocks C and D 15%, discovery of new kinds of issue 10%**. Agent output
lands in the next release tag, never straight into one already served.

**R10. The ratchet.** `check-binding-ratchet` holds the design-handoff generator's three counts (unbound
controls, forms calling undefined operations, bound fields missing from the contracts) per app and block to
`checks/baseline.json`. Any count that rises fails the run. After a fix lowers a count, the lead runs
`--update-baseline` in a reviewed commit. An exception goes in `checks/allowlist.yaml` with a reason, an
approver and an expiry no more than 14 days out. **Re-record the baseline at r2 on main.**

**R11. Typed properties.** `check-audience-match`, `check-preauth-session` and `check-subject` hold every
screen against three operation properties: its audience, whether it needs a session, and whether it acts on
the caller or a named customer. `check-audience-match` also reports an operation whose declared audience
includes guests while its security admits no guest. They are report-only until the guest fixes and the POS loyalty swap land.
The lead then records each baseline (`--update-baseline`) and takes the check out of `REPORT_ONLY`.
**`check-audience-match` gates since 14 October 2026** (CHG-SWP-002): the guest fixes had landed (no guest-screen
finding on r6), its baseline is recorded, and it also holds every app's feature ticket to the app's audience
(AM-TICKET-OP, after #27741 listed the staff-only `searchGuests` on the guest app). `check-preauth-session` and
`check-subject` stay report-only until the POS loyalty swap.

**R12. Canary.** After each release, one AI session pulls **5 tickets** through ADAM at the new tag, as a
developer would. A problem it finds is a CR. This comes before the wider §7 sample.
