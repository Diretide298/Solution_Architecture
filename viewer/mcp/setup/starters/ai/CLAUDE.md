# TICVAI AI engine

Python 3.12 and FastAPI, in the `ticvai-ai` repository: the AI engine (retrieval on Qdrant, the model gateway,
evaluations). This workspace is for an AI engineer; ADAM setup made it with the `ai` role (r8 cause
FOUNDATION-AI-C29, 20 October 2026). The code is the team's `ticvai-ai` repository, cloned here when you have access.

```
pip install -e '.[dev,qdrant]'
ruff check src tests
mypy src
pytest
pytest tests/evals --strict-markers     # the eval regression gate: no capability ships without a baseline
```

## Coding standards

Loaded into every session, so every ticket is built to them:

@project-bible/setup/naming-and-style.md
@project-bible/setup/llm-conventions.md
@project-bible/setup/quality-gates.md

Read these when the work calls for them, not before:

| Read | When |
|---|---|
| `project-bible/setup/api-conventions.md` | adding or changing an endpoint, an error or paging |
| `project-bible/setup/backend-patterns.md` | the platform's rules the AI endpoints share (tenancy, idempotency, events) |
| `project-bible/setup/git-and-mrs.md` | before a commit or a merge request |
| `project-bible/setup/data-and-storage.md` | touching tables, vectors or snapshots |
| `project-bible/setup/config-and-secrets.md` | adding a setting, a key or a token (Key Vault, never source) |
| `project-bible/setup/dependencies.md` | adding a package |
| `project-bible/setup/adding-things.md` | adding a module, a permission or an integration |

In one session, a document already read does not need reading again.

## Hard rules

- Every request is scoped to the caller's tenant and venue; the one retrieval client takes no scope parameter
  and always adds the venue filter (ADR-0049).
- `ticvai-ai` never reads the Qdrant admin key: it uses the tenant's token, which the workers host issues (ADR-0049).
- No secrets, keys or tokens in source; they come from Key Vault.
- No personal data in logs or prompts beyond what the contract allows; Presidio runs before anything leaves the UAE.
- A contract comes first: build what the ADAM contract says - status codes, error codes, field names.

<!-- ADAM:start working-a-ticket -->
## Working a ticket (ADAM)

ADAM is connected for this folder. It holds the contracts, tables and screens; OpenProject holds the tickets.

No ticket named? Do not ask for a number: `adam_board` with `only: "workable"` gives `startHere`, the first ticket
you can finish or its first open sub-task of yours. Start that one.

1. `adam_pull` the ticket with `dir` set to this folder. Read `.adam/work/<ticket>/README.md`,
   then only the linked files it lists. Ask ADAM (`adam_contract`, `adam_table`, `adam_search`)
   rather than guessing a name or a shape.
   **Read its Comments section too**, the newest last: a clarification or QA's reason for sending
   it back overrides the description where they differ - say so when it does.
   **Sub-tasks** in README.md are the work under the ticket, in order: pull the first open one of yours and work
   that, one at a time; work the ticket itself only when none of its open sub-tasks is yours. **Part of** names
   the ticket it belongs to.
   **You are always on the latest release.** ADAM serves the package at its latest release tag
   (r1, r2, …) and every pull is at it; there is no release to choose and nothing to re-pin. If
   README.md says **What changed since your previous pull (rA -> rB)**, tell the person in one line
   (`spec-diff.md` has the diffs) and build against the files as they are now.
   **Read "Change requests on this ticket" too**, near the top of README.md: follow a settled
   decision where it differs from the description, and wait on the part an open non-blocking request
   covers; a blocking one is "When the package is wrong", step 4.
2. Build exactly what the ticket and its linked artefacts describe. Nothing outside the ticket.
3. Add tests for the success case and each error the contract lists. `ruff`, `mypy` and `pytest` must pass.
4. `adam_propose` the ticket: **Ready for QA**, 100% (see the statuses below; never Closed), and a 2-4 line comment on what was built and
   that the tests pass. Show the proposal and **wait for a yes** before `adam_apply`.

To see a teammate's work, ask ("what is Hrushikant working on?", "what's everyone doing?"):
`adam_team` answers, read-only, with their open and in-progress tickets and what they finished lately.

<!-- ADAM:end working-a-ticket -->

## Ticket kinds

"Working a ticket" above is the [AI] path: an AI engine task or a contract-backed AI operation. The other kinds differ in
what "built" and "tested" mean:

| Ticket | Built means | Tested means | Propose |
|---|---|---|---|
| **[AI]** (`AI-*`, `SVC-AI-*`) | the engine work or the operations the ticket names, as its description and contract say | a test for the success case and each listed error; `ruff`, `mypy` and `pytest` pass | Ready for QA |
| **[DevOps]** (`SETUP-*`) | the pipeline, environment or seed the description names, in the repository it names | it runs once end to end; say in the comment what QA can re-run | Ready for QA |
| **[Onboarding]** | nothing to build: the step is done when the connector answers in this folder | `adam_board` returns your board | Ready for QA with that as evidence |

A setup ticket links no contract or screen; that is normal, not a gap.

## Searching pulled files

`.adam/` is git-ignored, so **Grep skips it unless told not to**: search pulled files with
`--no-ignore` (or read them directly). Read works as usual.

## When the package is wrong

If the contract, table, screen or journey you are building from contradicts itself, is wrong, or
lacks something the ticket needs, **do not settle it in code** - not even with a sensible guess.

1. `adam_changes` for the artefact: somebody may have raised it already. If so, name that CR.
2. Otherwise `adam_draft_change`: quote the conflicting passages in `evidence`, list the `options`,
   say which you would pick in `recommendation`, set `blocking` and the `ticket`. The intake goes
   with it: `source` is `developer` (the reference defaults to the ticket) unless the person says
   it came from minutes, a client answer, a design or an audit - then `sourceRef`, and for minutes
   `clientSignoff`; `triage` and `when` if known; other `artefacts` it touches; `contractImpact`
   (none, additive, breaking - breaking needs an `approver`); `effortPoints` if the estimate moves.
3. Show the draft and **wait for a yes** before `adam_raise_change`.
4. **A blocker is always a change request** (CHG-ADM-004): set `blocking: true`, and once it is filed,
   propose the ticket **On hold** with "Blocked by CR-<n>" (applied only after a yes). Never work around
   it and never build a guess. Then find the next ticket you can finish: `adam_board` with
   `only: "workable"` lists, in board order, the tickets no open blocking CR affects (a ticket's
   `blocked` column and the "Blocked by" section of its README.md name the CRs). Propose the first one,
   and say which CR holds back each ticket you skipped.

Before building against an artefact, check `adam_changes` for an accepted request on it: the
package may be about to change.

## Ticket statuses (OpenProject)

| Status | Use it when |
|---|---|
| **New** | Not started. Never set it yourself. |
| **In progress** | Work has started but is not finished - a build that stopped part-way, or tests still failing. |
| **Ready for QA** | Done on your side: built as the ticket and its contract describe, and the tests pass. **This is where finished work goes.** Say in the comment what QA should check. |
| **Closed** | Set by QA after testing. **Never propose it yourself**, even when everything passes: the person who built it is not the person who says it works. |
| **On hold** | Blocked on something outside this repository - a missing contract, an unanswered question, an open change request. Say what in the comment. |
| **Rejected** | Only when the person says the ticket will not be done. Never on your own. |

Pair the status with % done: In progress 10-90, Ready for QA 100, On hold unchanged.
If the live statuses have no QA status, stop and ask rather than choosing Closed.
These are the statuses on pms.softlabsgroup.in. `adam_propose` with only a ticket number lists
the live ones; if they differ from this table, use those.

`.adam/` is a local copy and is git-ignored. Never commit it.
