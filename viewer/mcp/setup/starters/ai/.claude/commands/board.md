---
description: What is on my board — my open tickets and the module each one is from
---

Run `adam_board`. Show me `rows` as a markdown table using its `columns`, in the order they
come back, and nothing else. That order is the order the work is finished in (what I have
started, then the plan's build order), so never re-sort it.

Do not list the subtasks and do not summarise them: the `subtasks` column gives the count, and
they are only worth reading when I ask. If I do ask, run `adam_board` again with
`subtasks: true` and show them under their ticket.

If `subtaskNote` is present, say it in one line under the table: the sub-task counts could not be read, which is
not the same as none.

If `columns` includes `release`, it is the release tag each ticket was last pulled at. I am always on
the latest release: `r1 -> r2` means the last pull was at r1 and the next `/ticket <n>` is at r2 and
says what changed; say that in one line under the table. Blank means not pulled yet, which is not a
problem.

The `blocked` column names the open blocking change requests that affect a ticket; blank means it can be
finished now. End with `firstWorkable`, the first ticket in that order that no blocking CR affects, and
why, in one sentence, and say in one line which CR holds back each ticket above it. If I hit a blocker
on a ticket, it is a change request (`/cr`, blocking), the ticket goes On hold, and we move to that next
workable one - never a workaround.

`startHere` is where `/ticket` with no number starts: the first ticket I can finish, or its first open sub-task of
mine.
