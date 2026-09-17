---
description: Raise a change request in ADAM when the package is wrong, contradictory or missing something
argument-hint: <what is wrong, in a few words>
---

The package seems wrong: $ARGUMENTS

1. Find the artefact(s) involved with ADAM (`adam_contract`, `adam_table`, `adam_screen`,
   `adam_journey`, `adam_search`) and quote the passages that show the problem, with where each is.
2. `adam_changes` for those artefacts. If an open or accepted request already covers it, show me
   that one and stop.
3. `adam_draft_change` with the kind, the artefact, a one-line title, the problem, the quoted
   evidence, the options, your recommendation, whether it blocks the current ticket, and the ticket
   number if there is one.
4. Show me the draft and stop. Run `adam_raise_change` only after I say yes.
5. If it blocks a ticket, offer to `adam_propose` that ticket **On hold** with "Blocked by CR-<n>".
