# TICVAI package: rules for every change (binding from Monday 5 October 2026)

These rules bind every person and every AI agent who changes this package. They are not advice. They come
from the council of 2 October (`docs/active/council-2-october.md`); the detail is in
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
6. **A started ticket is never rewritten.** A fix to one is a comment plus a linked delta ticket, and ADAM
   keeps serving the developer the release tag they started on.
7. An unstarted ticket picks the fix up at the next tag, through its pointer body. Never edit OpenProject
   text to carry a spec change.

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
