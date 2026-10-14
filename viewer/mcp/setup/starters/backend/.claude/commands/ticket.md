---
description: Pull an OpenProject ticket through ADAM, build it, test it, and propose the update
argument-hint: <ticket number>
---

Work ticket $ARGUMENTS, following "Working a ticket (ADAM)" in CLAUDE.md:

1. `adam_pull` ticket $ARGUMENTS with `dir` set to this folder. Read `.adam/work/$ARGUMENTS/README.md`
   and the linked files it lists. If nothing is linked, find the contract with `adam_search`, say
   what you found, and ask before linking it.
   **Read its Comments section too**, the newest last: a clarification or QA's reason for sending
   it back overrides the description where they differ - say so when it does.
2. **You are always on the latest release** (the README's `Release` line names it: r1, r2, …).
   Every pull is at it, so there is no release to choose and nothing to re-pin. If README.md has a
   section **What changed since your previous pull (rA -> rB)**, tell me in one line what changed
   (`spec-diff.md` has every diff) and build against the files as they are now. If a change is wrong
   for this ticket, raise a change request (`/cr`, source developer) and build the rest.
   **Read "Change requests on this ticket"** near the top of README.md: a settled decision overrides
   the description where they differ; an open request means that part waits - build the rest and
   say what waits on it.
3. If the ticket and its contract disagree, or the package contradicts itself, follow
   "When the package is wrong" in CLAUDE.md instead of guessing.
4. Build what the ticket and its contract describe, in the layers CLAUDE.md lists.
5. Add tests for the success case and each listed error. Run `dotnet test TICVAI-Backend.slnx` until it passes.
6. `adam_propose` the QA status (**Ready for QA** - `adam_propose` with only the ticket number lists the live statuses; use the one named for QA, and if there is none, stop and ask), 100%, and a 2-4 line comment that says what QA should check. Never **Closed**. If the build or the tests are not
   finished, propose **In progress** with an honest % done instead; if something outside this
   repository blocks it (an open change request, say), propose **On hold** and say what. Show me the proposal and stop.
   Do not run `adam_apply` until I say yes.
