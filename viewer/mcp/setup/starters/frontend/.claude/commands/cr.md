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
   number if there is one. Then the intake:
   - `source`: `developer` (the default: a gap found while building) unless I say it came from
     meeting `minutes`, a client `answer`, a `design` or an `audit`; then `sourceRef` is the line that
     finds it again ("MoM 30 Sep, item 4"), and for minutes `clientSignoff` says who on the client's
     side agreed it and where. A developer gap's reference defaults to the ticket.
   - `triage` (`clarification`, `scope` or `defect`) and `when` (`now` or `later`), if you can tell.
   - `artefacts`: every other artefact id it touches, beyond the one it is about.
   - `contractImpact`: `none`, `additive` or `breaking`. A breaking one needs an `approver`.
   - `effortPoints`: the change in effort, signed, if it changes the estimate.
4. Show me the draft and stop. Run `adam_raise_change` only after I say yes.
5. If it blocks a ticket, offer to `adam_propose` that ticket **On hold** with "Blocked by CR-<n>".
