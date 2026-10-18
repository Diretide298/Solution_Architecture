---
description: Work a ticket through ADAM - the one you name, or with no number the next one I can finish
argument-hint: [ticket number, or nothing to start the next one]
---

The ticket: "$ARGUMENTS".

**If that is empty, do not ask me for a number.** Run `adam_board` with `only: "workable"` and take its
`startHere`: the first ticket I can finish now, or its first open sub-task that is mine. Say in one line which
ticket it is and why, then work it as below. If there is no `startHere`, every ticket on my board is blocked: say
so in one line, with the CR that holds back each, and stop.

Work the ticket, following "Working a ticket (ADAM)" in CLAUDE.md:

1. `adam_pull` the ticket with `dir` set to this folder. Read `.adam/work/<ticket>/README.md`
   and the linked files it lists. If nothing is linked, find the screen or contract with `adam_search`, say
   what you found, and ask before linking it.
   **Read its Comments section too**, the newest last: a clarification or QA's reason for sending
   it back overrides the description where they differ - say so when it does.
   **If README.md lists Sub-tasks**, they are the work under this ticket, in the order it is done: say in one
   line which are still open, then pull the first open one that is mine (or nobody's) and work that, one at a
   time. Work this ticket itself only when none of its open sub-tasks is mine. A **Part of** line names
   the ticket this one belongs to; pull it only when you need the wider picture.
2. **You are always on the latest release** (the README's `Release` line names it: r1, r2, …).
   Every pull is at it, so there is no release to choose and nothing to re-pin. If README.md has a
   section **What changed since your previous pull (rA -> rB)**, tell me in one line what changed
   (`spec-diff.md` has every diff) and build against the files as they are now. If a change is wrong
   for this ticket, raise a change request (`/cr`, source developer) and build the rest.
   **Read "Change requests on this ticket"** near the top of README.md: a settled decision overrides
   the description where they differ; an open non-blocking request means that part waits - build the rest and
   say what waits on it. A blocking one is step 3.
3. **A blocker is always a change request.** If README.md has a **Blocked by** section, or the ticket and
   its contract disagree, the package contradicts itself, or it lacks storage or a rule the ticket needs:
   do not work around it and do not build a guess. Follow "When the package is wrong" in CLAUDE.md:
   raise a change request with `blocking: true` (`/cr`; I say yes before it is filed), propose this
   ticket **On hold** naming the CR (I say yes before it is applied), then find the next ticket I can
   finish: `adam_board` with `only: "workable"` lists, in board order, the tickets no open blocking CR
   affects. Propose the first one and say which CR holds back each ticket you skipped.
4. Build what the ticket and its contract describe, in the repository for the ticket's platform (the table
   in CLAUDE.md). If that repository is not cloned in this folder, or has no repository yet, stop and say so.
5. Add tests for the success case and each listed error. Run that repository's lint, typecheck and test
   commands inside its folder ("Git, build, test and lint" in CLAUDE.md) until they pass.
6. `adam_propose` the QA status (**Ready for QA** - `adam_propose` with only the ticket number lists the live statuses; use the one named for QA, and if there is none, stop and ask), 100%, and a 2-4 line comment that says what QA should check. Never **Closed**. If the build or the tests are not
   finished, propose **In progress** with an honest % done instead; if something outside this
   repository blocks it (an open change request, say), propose **On hold** and say what. Show me the proposal and stop.
   Do not run `adam_apply` until I say yes.
