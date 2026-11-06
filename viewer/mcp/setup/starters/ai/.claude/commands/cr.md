---
description: Raise a change request in ADAM when the package is wrong, contradictory or missing something
argument-hint: <what is wrong, in a few words>
---

The package seems wrong: $ARGUMENTS

1. **Hand it to the `adam-cr` agent** with the ticket number and what you found, in a few lines. It finds
   the artefacts, quotes the evidence and drafts the change request in its own context, so none of that
   research fills this session, and it hands back the draft, its code, and any request already open or
   recently settled on the same artefacts. If a settled one already decides this, tell me, follow its
   decision and file nothing; if an open one covers it, show me that one and stop. Go to step 4.
2. No `adam_changes` search first: `adam_draft_change` reports both of those itself.
3. Only if this workspace has no `adam-cr` agent: find the artefact(s) with ADAM (`adam_contract`,
   `adam_table`, `adam_screen`, `adam_journey`, `adam_search`), quote the passages that show the problem,
   and `adam_draft_change` yourself with the kind, the artefact, a one-line title, the problem, the quoted
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
5. If it blocks a ticket (`blocking: true` - a blocker is always a change request, never a workaround),
   `adam_propose` that ticket **On hold** with "Blocked by CR-<n>" and show me; apply only after I say yes.
   Then find the next ticket I can finish: `adam_board` with `only: "workable"`, the first in board order,
   saying which CR holds back each ticket skipped.
6. When it is settled, ADAM tells the ticket it came from: a comment for the agent while the ticket is
   open (the next `/ticket` also lists it under "Change requests on this ticket"), or a child task for
   the change when that ticket is closed. You are always on the latest release: nothing to re-pin.
