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

## 5. Tag
Once everything is green:
1. Commit.
2. `git tag r<N>` on the package **and** the six mirror repos.
3. Push both remotes.
4. Rebuild the setup zip from a clean HEAD.

## 6. Distribute
- **OpenProject:** on the server, run `op-release-server.sh r<N>`: dry run, then `APPLY=1`. That one script:
  - creates new tickets and writes pointer bodies;
  - syncs assignee and week;
  - sets build order and links;
  - retires tickets that left the plan;
  - runs a health check.
- **ADAM:** on the box, run `git pull` and deploy. ADAM serves `r<N>`, and `/ticket` shows each developer what changed since their pin.
- **Client:** send the release note, `python tools/release-notes.py r<N-1> r<N>`: what their answers changed, and what is waiting on them.

## 7. Re-audit, every release
- Every check is green.
- Pull a **sample of 20 to 30 tickets** through ADAM at the new tag, across every developer's board.
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

**R3. Triage.** Every CR is triaged `blocker` (fixed in the next release, even on started tickets, as a
delta), `fix-forward` (into unstarted tickets at the next tag) or `defer` (logged, open). The lead triages
in a **daily 30-minute slot**.

**R4. Client sign-off.** A minutes-sourced change carries `client_signoff`. Sign-offs go to the client as
one batch a week (contract decisions and open questions included). Silence for 5 working days after the
batch is sent is acceptance, recorded as `by: "silence (5 working days)"` with the date.

**R5. Started tickets.** A ticket past "New" is frozen. A fix to it is a comment plus a linked delta
ticket, and ADAM keeps serving the developer's start tag until they re-pin. Unstarted tickets get the fix at
the next tag through their pointer bodies.

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

**R12. Canary.** After each release, one AI session pulls **5 tickets** through ADAM at the new tag, as a
developer would. A problem it finds is a CR. This comes before the wider §7 sample.
