# The change log: every change, its decision, why, and what stops it coming back

> **Owner:** Chinmay. **Decided:** council of 2 October 2026 (`docs/active/council-2-october.md`).
> **Binding from Monday 5 October 2026** for every person and every AI agent (`ticvai/CLAUDE.md`).
> **Checked by:** `tools/check-changelog.py` (gating, in `run-checks.py`). **Schema:** `changes/schema.yaml`.

Chinmay, 2 October: *"All the changes and fixes: log them, also the decision and why."*

Every change to an authored package input (contracts, screens, flows, ADRs, registers, the team
and plan inputs, the meeting design inputs, the minutes) is **one entry file** here, and the
commit that makes the change names the entry's id in its message. An entry is not a note: it
**closes only when it ships a prevention** (a check, a generator rule or a template field) that
would have caught the problem, or a reason no prevention is possible that the lead approved.

## Where entries go

```
changes/
  schema.yaml                         the rules check-changelog applies
  entries/CHG-<BATCH>-<nnn>-<slug>.yaml   one file per change (what you write)
  CHANGELOG.md                        the index, generated: python3 tools/build-changelog-index.py
```

- **One file per entry**, so parallel branches never conflict. The file name is the id, a dash and
  a short lowercase slug: `CHG-FIN-003-guest-selects-currency.yaml`.
- **Ids are allocated per batch.** A batch is one branch or one agent run, with its own code of 2 to
  6 capital letters: `CHG-SEED-` (the seed of 2 October), `CHG-FIN-` (finance decisions), `CHG-WIR-`
  (wiring fixes), `CHG-GST-` (guest fixes). Number from `001` with no gaps inside the batch. Ask the
  lead for a new code; never reuse another branch's.
- **Do not commit `CHANGELOG.md` from a branch.** It is regenerated at the refresh; editing it on
  two branches is exactly the merge conflict the directory avoids.

## The fields

| Field | Required | What it holds |
|---|---|---|
| `id` | yes | `CHG-<BATCH>-<nnn>`, pattern `^CHG-[A-Z]{2,6}-\d{3}$`; matches the file name |
| `date` | yes | the day the change was made, `YYYY-MM-DD` |
| `source` | yes | `mom` · `cr` · `audit` · `client-review` · `plan` · `design-input` · `developer` |
| `kind` | yes | `spec` · `contract` · `plan` · `design-input` · `process` |
| `summary` | yes | one sentence: what changed |
| `decision` | yes | `what` was decided, `by` whom, on what `date` |
| `why` | yes | the reason, **citing its source** so a reader can open it: a MoM (`sources/mom/...`), a design input (`DI-...`), an audit root (`R123`), an ADR (`ADR-0060`), the council, an audit fix (`F1`-`F8`), a client return (`POSV2-3`), a CR, a finding, a commit or another `CHG-` id. The check refuses a `why` with no citation |
| `keys_touched` | yes | lists of the keys it changes: `screens`, `operations`, `tables`, `schemas`, `flows`, `tickets`, `files`, `other`. At least one key unless the kind is `process` or `plan` |
| `root_class` | yes | the audit class it belongs to (`audit/ticvai/ROOT-CLASSES.md` id, e.g. `CR-3`) or `new: <name>` for a new class (`change-rules.md` CR-7: a new class gets a guard) |
| `tickets` | yes | `started: [...]` and `unstarted: [...]` OpenProject keys or ids it affects |
| `release_tag` | yes | the tag that carries it (`r3`), or `pending` until it is tagged |
| `decision_owner` | yes | who owns the decision (the lead, or the client for a minutes-sourced change) |
| `client_signoff` | when `source: mom` | `{by: <name>, date: YYYY-MM-DD}` or `pending`. Batched weekly; silence for 5 working days after the batch is acceptance (`by: "silence (5 working days)"`) |
| `adam_cr` | from 5 Oct | the ADAM change-request id the change came in through |
| `triage` | from 5 Oct | `blocker` · `fix-forward` · `defer` |
| `prevention` | yes | `type`: `check` · `generator-rule` · `template-field` · `none`; `ref`: the path (and `::symbol`) of the check, rule or field; with `none`, a `reason` and `approved_by` (the lead) |
| `status` | yes | `open` or `closed` |
| `closed_by_commit` | when closed | the commit that merged the fix |
| `proposed` | plan changes, from 5 Oct | when the plan change was proposed, `YYYY-MM-DD[THH:MM]`; the decision comes at least 24 hours later |
| `reverses` | when it does | the id of the change this one reverses; that one must have been decided at least 48 hours before |
| `notes` | no | anything else a reader needs |

### The closing rule

`status: closed` passes `check-changelog` only when:

- `closed_by_commit` names a commit git knows;
- **type `check`:** `prevention.ref` is `tools/<name>.py`, the file exists, and `tools/run-checks.py`
  runs it. A check nobody runs prevents nothing;
- **type `generator-rule` or `template-field`:** `prevention.ref` is `<path>` or `<path>::<symbol>`,
  the path exists, and the symbol appears in it;
- **type `none`:** `prevention.reason` says why no check, rule or field can catch it, and
  `prevention.approved_by` names the lead who accepted that.

The council's stricter form (the prevention fails on the commit before the fix and passes after
it) is asked of the author and the reviewer: run the new check on the parent commit and say so in
`notes`. The tool cannot replay history on every run.

### The plan-change rule

On 1 October the plan was reversed several times in one day (Block A 35 to 40 days, Sprint 5 to 4, the
pace, the block cuts). So from 5 October a commit that touches a plan input (`docs/active/team.json`,
`docs/active/block-a-extra-tasks.json`, `tools/sprint_plan.py`) names a change of kind `plan`, and that
entry records `proposed`, is decided at least 24 hours later, names its release when closed, and may
reverse (`reverses`) only a change decided at least 48 hours earlier. Plan changes ship only in a Tue/Fri
release and are not announced before they are committed.

### The commit rule

`python3 tools/check-changelog.py --since [REF]` (default: the latest `r*` tag) reads every
non-merge commit in `REF..HEAD`. A commit that touches an authored input (`contracts/`,
`screens/`, `flows/`, `states/`, `events/`, `docs/adr/`, `docs/registers/`, `sources/mom/`,
`docs/active/team.json`, `handoff/design-inputs/mom-design-inputs.yaml`, and the plan inputs
`docs/active/block-a-extra-tasks.json` and `tools/sprint_plan.py`) must name an existing entry id in its message,
for example `TICVAI guest storefront reads its theme without a session (CHG-GST-001)`. A release
refresh commit by the lead may carry `CHG-exempt: <reason>` instead; every exemption is printed.
Commits dated before 5 October 2026 are grandfathered. Without `--since` the tool validates the
entry files only.

## A filled example

`changes/entries/CHG-SEED-006-till-cart-audience.yaml` (one of the seed entries):

```yaml
id: CHG-SEED-006
date: '2026-10-01'
source: client-review
kind: contract
summary: The till's cart operations (addCartLine, getCart) and getGuestMenu declare the staff audience, because POS screens call them.
decision:
  what: Add staff to x-ticvai-audience on the cart operations the till calls and on getGuestMenu (POS-021 reads it at the till).
  by: Chinmay
  date: '2026-10-01'
why: >-
  POS v2 follow-up (POSV2 decisions of 1 October, commits 5726cc36 and 0d59727e): a fix exposed that
  operations bound on staff screens declared only the guest audience, so a staff caller would be refused
  or served guest-shaped data. Same root as the process-agent finding on guest screens binding staff
  operations (council of 2 October: typed audience property).
keys_touched:
  operations: [getGuestMenu, getCart, addCartLine]
  screens: [POS-002, POS-010, POS-021, POS-023, POS-030]
root_class: 'new: audience-mismatch'
tickets:
  started: []
  unstarted: []
release_tag: r2
decision_owner: Chinmay
prevention:
  type: check
  ref: tools/check-audience-match.py
status: closed
closed_by_commit: 0d59727e
notes: check-audience-match is report-only until the guest fixes land; the lead flips it to gating.
```

## How an agent or a person logs a change

1. Get a batch code from the lead (or use the one in your brief) and take the next number.
2. Make the change in your own worktree, authored files only (`docs/active/release-runbook.md` §2).
3. Write the entry file. `decision` and `why` are not optional: a fix without its reason is the one
   somebody reverses next week.
4. Write or name the prevention. If you add a check, register it in `tools/run-checks.py`.
5. Commit with the id in the message: `... (CHG-WIR-004)`.
6. Run `python3 tools/check-changelog.py` before you hand the branch back.
