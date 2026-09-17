---
description: Pull an OpenProject ticket through ADAM, build it, test it, and propose the update
argument-hint: <ticket number>
---

Work ticket $ARGUMENTS, following "Working a ticket (ADAM)" in CLAUDE.md:

1. `adam_pull` ticket $ARGUMENTS with `dir` set to this folder. Read `.adam/work/$ARGUMENTS/README.md`
   and the linked files it lists. If nothing is linked, find the screen or contract with `adam_search`, say
   what you found, and ask before linking it.
2. If the ticket and its contract disagree, or the package contradicts itself, follow
   "When the package is wrong" in CLAUDE.md instead of guessing.
3. Build what the ticket and its contract describe, in the app and packages CLAUDE.md lists.
4. Add tests for the success case and each listed error. Run `pnpm lint`, `pnpm typecheck` and `pnpm test` until they pass.
5. `adam_propose` **Closed**, 100%, and a 2-4 line comment. If the build or the tests are not
   finished, propose **In progress** with an honest % done instead; if something outside this
   repository blocks it (an open change request, say), propose **On hold** and say what. Show me the proposal and stop.
   Do not run `adam_apply` until I say yes.
