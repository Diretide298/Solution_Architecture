---
description: Pull an OpenProject ticket through ADAM, build it, test it, and propose the update
argument-hint: <ticket number>
---

Work ticket $ARGUMENTS, following "Working a ticket (ADAM)" in CLAUDE.md:

1. `adam_pull` ticket $ARGUMENTS with `dir` set to this folder. Read `.adam/work/$ARGUMENTS/README.md`
   and the linked files it lists. If nothing is linked, find the contract with `adam_search`, say
   what you found, and ask before linking it.
2. Build what the ticket and its contract describe, in the layers CLAUDE.md lists.
3. Add tests for the success case and each listed error. Run `dotnet test TICVAI-Backend.slnx` until it passes.
4. `adam_propose` the done status, 100%, and a 2-4 line comment. Show me the proposal and stop.
   Do not run `adam_apply` until I say yes.
