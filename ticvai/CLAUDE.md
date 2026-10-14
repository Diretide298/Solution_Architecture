# TICVAI package: rules for every change (binding from Monday 5 October 2026)

These rules bind every person and every AI agent who changes this package. They are not advice. They come
from the council of 2 October (its final report, `docs/active/council/council-report-2026-10-02-opus.html`); the detail is in
`docs/active/release-runbook.md` ("Rules from 5 October") and `changes/README.md`. If a rule blocks you,
stop and ask the lead (Chinmay). Do not work around it.

## Every change is logged and comes in through ADAM
1. Every change to an authored input (`contracts/`, `screens/`, `flows/`, `states/`, `events/`, `docs/adr/`,
   `docs/registers/`, `sources/mom/`, `docs/active/team.json`, the plan inputs,
   `handoff/design-inputs/mom-design-inputs.yaml`) is **one entry file** in `changes/entries/`
   (`CHG-<BATCH>-<nnn>-<slug>.yaml`), **plus an ADAM CR** recording the source, the approver and the triage
   (`blocker`, `fix-forward` or `defer`).
2. The entry records the **decision** (what, by whom, when) and **why**, citing its source (MoM, DI, R-root,
   ADR, council, finding, commit). The commit message names the id: `... (CHG-WIR-004)`.
3. A change taken from minutes needs **client sign-off**. Sign-offs are batched weekly; silence for 5 working
   days after the batch is sent counts as accepted. Until then, record `client_signoff: pending`.
4. **No change without a prevention:** a check (`tools/check-*.py`, registered in `tools/run-checks.py`), a
   generator rule or a template field that would catch it next time. The only alternative is
   `prevention: none` with a reason the lead approves. An entry closes only when its prevention exists.
5. Run `python3 tools/check-changelog.py` before you hand work back. It gates.

## Tickets
6. **Developers and agents always build against the latest release.** Every ADAM pull serves the release
   ADAM serves now and moves the ticket to it; nobody chooses or asks between releases, and `/ticket` says
   what changed since the ticket's previous pull (CHG-ADM-001; Chinmay, 14 October 2026: "we always want
   agents to pull the latest"). **A started ticket's OpenProject text is never rewritten.**
7. **A settled CR reaches its ticket** (CHG-ADM-002). A ticket that is not closed gets a comment written for
   the AI agent that pulls it (and `/ticket` lists the CR, its decision and its release); a closed ticket gets
   a **child task** for the change, created before the CR is marked Done. A CR's work is one child task of
   the ticket it was raised from; migration work it causes is a child task of the affected MIG-* ticket,
   assigned to the migration owner (`docs/active/team.json` `migrations.owner`). An unstarted ticket picks the
   fix up at the next tag, through its pointer body. Never edit OpenProject text to carry a spec change.

## Releases and the plan
8. Releases go out on **Tuesday and Friday** only. No spec edits on the day before a release.
9. A plan change is a change of kind `plan`. It ships only at a release, after a **24-hour cooling-off**,
   is never announced before it is committed, and is **never reversed within 48 hours**.
10. **Derive before check.** Refresh only through `bash tools/refresh-safe.sh`, never `refresh.sh` in the main
    tree. Never edit derived files by hand.

## Agents
11. Work in **your own git worktree** on your own branch. Make checkpoint commits as you go. Never leave
    partial work in the main checkout. When you share a tree, write only your own files.
12. **Every source you cite is inside git.** Copy a minute or a document into `sources/` before citing it.
    Never cite `audit/` or a scratchpad: git ignores them.

## Audits and AI capacity
13. **Checks first.** Run the checks before any AI audit. Spend AI only where a check cannot see: new
    classes of issue, sampled at **20 screens per app**. Each new class gets a check, which then runs across
    every block.
14. The weekly AI budget is **Block A 50%, Block B 25%, Blocks C and D 15%, finding new kinds of issue 10%**.
15. The binding counts only fall (`check-binding-ratchet`). Allowlist entries expire within 14 days.

## The lead's rhythm
16. After each release, a canary pulls **5 tickets** through ADAM as a developer would.
17. Triage gets a **daily 30-minute slot**. A CR waits for it, and is not decided ad hoc.

## Blockers (developers and their agents)
18. **A blocker is always a CR, then the next workable ticket** (CHG-ADM-004; Chinmay, 14 October 2026: "if
    there is blocker we log it as CR always. and than scour for next tasks that can be completed and if
    existing blockers effect it"). When the package blocks a ticket (a contradiction, missing storage, an
    undefined rule), the agent raises a CR with `blocking: true` and proposes the ticket **On hold** naming
    it; it never works around the blocker and never builds a guess. Then it takes the next ticket it can
    finish: `adam_board` with `only: "workable"` lists, in board order, the tickets no open blocking CR
    affects (by the ticket's links, and the tables its operations read or write). Nothing is filed or
    changed in OpenProject until the person says yes.
