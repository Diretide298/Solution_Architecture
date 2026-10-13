---
description: Propose sending a finished ticket to QA in OpenProject, with a comment from the work and the tests
argument-hint: <ticket number>
---

Ticket $ARGUMENTS is finished.

1. In the folder of the repository the ticket changed, run its lint, typecheck and test commands (its
   README and `package.json` scripts; see "Git, build, test and lint" in CLAUDE.md) and note the results.
2. Look at `git diff` and `git status` in that repository's folder for what changed.
3. `adam_propose` ticket $ARGUMENTS: the QA status (**Ready for QA** - `adam_propose` with only the ticket number lists the live statuses; use the one named for QA, and if there is none, stop and ask), 100%, and a 2-4 line comment naming what was
   built, the test result, and what QA should check. **Never propose Closed**: closing is QA's call, not the maker's. If the tests fail, propose **In progress** instead and say what fails.
4. Show me the proposal and stop. Run `adam_apply` only after I say yes.
