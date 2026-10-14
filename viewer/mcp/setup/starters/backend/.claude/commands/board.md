---
description: What is on my board — my open tickets and the module each one is from
---

Run `adam_board`. Show me `rows` as a markdown table using its `columns`, in the order they
come back, and nothing else. That order is the order the work is finished in (what I have
started, then the plan's build order), so never re-sort it.

Do not list the subtasks and do not summarise them: the `subtasks` column gives the count, and
they are only worth reading when I ask. If I do ask, run `adam_board` again with
`subtasks: true` and show them under their ticket.

If `columns` includes `release`, it is the release tag each ticket was last pulled at. I am always on
the latest release: `r1 -> r2` means the last pull was at r1 and the next `/ticket <n>` is at r2 and
says what changed; say that in one line under the table. Blank means not pulled yet, which is not a
problem.

End with the first ticket in that order that is not blocked, and why, in one sentence.
