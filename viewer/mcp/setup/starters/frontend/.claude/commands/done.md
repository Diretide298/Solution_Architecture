---
description: Propose closing a ticket in OpenProject, with a comment from the work and the tests
argument-hint: <ticket number>
---

Ticket $ARGUMENTS is finished.

1. Run `pnpm lint`, `pnpm typecheck` and `pnpm test` and note the results.
2. Look at `git diff` and `git status` for what changed.
3. `adam_propose` ticket $ARGUMENTS: the done status, 100%, and a 2-4 line comment naming what was
   built and the test result.
4. Show me the proposal and stop. Run `adam_apply` only after I say yes.
