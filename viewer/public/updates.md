Newest first. Each entry says what changed and, where there is one, what you have to do about it.

Most changes need nothing from you: the pages are served from one place, so a reload is the whole
upgrade. The exception is the **connector** — the part that runs on your own machine — which only
changes when you run `/update-adam` in Claude Code and restart it.

## 24 September 2026

### ADAM says when there is something new here

A **What's new** chip appears in the top bar when these notes have changed, and
disappears once you have opened them. It is driven by a hash of this page rather than a date, so
fixing a typo does not call everybody back and a rebuild that changes no words does not either.

Before this, the only way to reach this page was a link inside the account drawer — which is a link
nobody finds.

### The mascot is in ADAM

Thirty frames of it, from neutral through working to total collapse. They arrived with an index
badge burnt into every corner and a faint wash over the background that showed up as a pale
rectangle on any dark panel; both are gone, and the frames are now part of ADAM rather than a zip
somebody has to be sent.

Only one is used so far — the one at the top of this page. The plan is that its expression tracks
the **delivery's** state, never a person's: a sad robot next to somebody's name is a performance
review, not a status light.

### The package downloads as a spreadsheet

**Document → Download .xlsx.** The same section picker that builds the document now also writes a
workbook: services, tables and their columns, screens, operations, contracts, journeys, state models
and transitions, events, modules, decisions, registers and wireframe boards — sixteen sheets.

It is deliberately flat. The document nests a table under its module because that is how a package
reads; a spreadsheet is for sorting, filtering and pasting a column into an estimate, so every row
stands alone and repeats the name of what it belongs to. Counts stay numbers so they add up. Ids and
version strings stay text so Excel does not turn `1.10` into a date.

**Wireframes is spreadsheet-only** and the picker says so on the control — there is no sensible way
to put 228 boards into a prose document.

### "What is on my board" answers with a table

Ask Claude what is on your board and you get one table: ticket, task, the epic or module it came out
of, status, due date. Subtasks are still fetched and counted, and shown only if you ask for them —
they were the bulk of what made the old answer unreadable.

### The connector updates itself

Handing eleven people a zip and asking them to re-run setup is a distribution step that does not
happen, so it no longer has to. When ADAM is serving a newer connector than the one on your machine,
Claude Code says so in one line on startup, with the command in it. You run:

```
/update-adam
```

Then **restart Claude Code** — the connector cannot replace the files it is currently running from,
so the new build is the next session's.

A **build** is a hash of the connector's own files rather than a version number: there is nothing to
bump and nothing to forget, and two people are on the same build exactly when they are running the
same code. **Settings → Claude connector → Builds** shows which build each install reported and
whether it matches what ADAM is serving.

**The zip is for the first install and nothing after it.** `setup.cmd` is not something you run
again for an update — `/update-adam` is, and setup now installs that command for every folder rather
than only for projects it created, so it is there whichever repository you are in.

The one exception is a connector installed before any of this existed: it has no updater to run, so
`/update-adam` will not find one. Those installs need `setup.cmd` once more. After that, never
again.

## 23 September 2026

### The delivery as bars you can drag

A timeline of the main modules rather than a list of every task, with the bars draggable by pointer
or arrow keys. Dragging changes nothing anybody else can see: it is your own sketch, held separately
from the plan, and the two are allowed to disagree for as long as it takes to think. When you are
happy, ADAM shows exactly what it is about to change and only then writes it to OpenProject.

### The owner role is now called System Architect

A rename and nothing more — the same permissions, the same access, the same everything. If a screen
said "owner" before, it says System Architect now.

### Ask the package anything, on your own key

A question box over the whole package, using whichever provider you already pay for. The key is
yours, kept encrypted, and never shown back to you after you save it.

### The package as one document

Pick the sections you want and ADAM assembles them into a single document to hand over, with the
diagrams drawn again at the size they are printed rather than scaled up from a screenshot.

### Hours from the tickets, rates from here

Costing reads the hours off the tickets and the rates from ADAM, and says plainly when a total is a
floor rather than an estimate.

### A diagram remembers how somebody arranged it

Move the boxes and the arrangement is kept. If the underlying package changes enough that the saved
layout no longer matches it, the diagram says it has come adrift rather than quietly drawing
something wrong.

### Two fixes worth naming

- ADAM would not start on any store with real history in it — an index named a column that the
  migration had not added yet. Fresh installs never saw it; every real one did.
- The avatar page is gone.
