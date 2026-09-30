---
description: Pull an OpenProject ticket through ADAM, build it, test it, and propose the update
argument-hint: <ticket number>
---

Work ticket $ARGUMENTS, following "Working a ticket (ADAM)" in CLAUDE.md:

1. `adam_pull` ticket $ARGUMENTS with `dir` set to this folder. Read `.adam/work/$ARGUMENTS/README.md`
   and the linked files it lists. If nothing is linked, find the screen or contract with `adam_search`, say
   what you found, and ask before linking it.
   **Read its Comments section too**, the newest last: a clarification or QA's reason for sending
   it back overrides the description where they differ - say so when it does.
2. **Check which release you are on.** The README's `Release` line names the release tag ADAM
   serves (r1, r2, …); your first pull pinned this ticket to it. If README.md has a section
   **Spec changed since you pulled at rA (now rB)**, stop and show it to me before building. The
   linked files are still the release you are pinned to, and `spec-diff.md` has every diff.
   - **Re-pin required** means a breaking contract change on an operation this ticket produces or
     consumes: the producer and the consumer have to build against the same release. Say that it
     is required, then run `adam_repin` with `breaking: true` and `dir` set to this folder, and read
     the new README.md. Do not build against the old release.
   - Otherwise it is my choice: take the change (`adam_repin` with `dir`, which pulls the ticket again
     at the new release), or keep building against the pinned release and raise a change request
     (`/cr`, source developer) if the change is wrong for this ticket. Ask me; do not choose.
3. If the ticket and its contract disagree, or the package contradicts itself, follow
   "When the package is wrong" in CLAUDE.md instead of guessing.
4. Build what the ticket and its contract describe, in the app and packages CLAUDE.md lists.
5. Add tests for the success case and each listed error. Run `pnpm lint`, `pnpm typecheck` and `pnpm test` until they pass.
6. `adam_propose` the QA status (**Ready for QA** - `adam_propose` with only the ticket number lists the live statuses; use the one named for QA, and if there is none, stop and ask), 100%, and a 2-4 line comment that says what QA should check. Never **Closed**. If the build or the tests are not
   finished, propose **In progress** with an honest % done instead; if something outside this
   repository blocks it (an open change request, say), propose **On hold** and say what. Show me the proposal and stop.
   Do not run `adam_apply` until I say yes.
