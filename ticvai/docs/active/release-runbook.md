# Release runbook: how a change becomes a release

> **For:** Chinmay (lead) and anyone running a release. **Decided 1 October 2026** (LLM Council, `audit/ticvai/council/`).
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
- `bash tools/refresh-safe.sh`: refreshes in a throwaway worktree. It merges into the main tree **only if every check passes** (no new failures against the baseline). An interrupted run is deleted.
- `bash tools/refresh-safe.sh --changed <paths>`: runs only the steps downstream of the changed files (from `handoff/refresh-manifest.json`). Use it between releases. **A full `refresh-safe.sh` run is required before tagging.**

## 4. Gates (in the checks)
- **Keys:** a pushed key is never renamed (`check-key-stability`).
- **Migrations:** the baseline migrations are frozen at `r1`; table changes come out as new forward migrations (`check-migration-freeze`); anything destructive goes to `handoff/migration-review.md` for a person.
- **Contracts:** a breaking change must be listed in `breaking-changes.yaml` (`check-contract-compat` against `r1`).
- **Audit classes:** every root-issue class from the audit has its check (`audit/ticvai/ROOT-CLASSES.md`).

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
