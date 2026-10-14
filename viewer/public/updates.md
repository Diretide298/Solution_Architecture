Newest first. Each entry says what changed and, where there is one, what you have to do about it.

Most changes need nothing from you: the pages are served from one place, so a reload is the whole
upgrade. The exception is the **connector** — the part that runs on your own machine — which only
changes when you run `/update-adam` in Claude Code and restart it. The top of this page says whether
any of your machines is behind.

## 14 October 2026

### The pages are rebuilt the way Tasks is

Tasks was rebuilt first, and the other pages now work the same way. Each opens on one sentence
answering the question it is opened for, with the figures it rests on underneath as a line of type
rather than a row of boxes, one chart, and what to do next. One section shows at a time, picked from
the list on the left. One filter covers the whole page, says in a sentence what it is showing, and
is kept in the address, so a link you send opens on what you were looking at. A person's name leads
to their page on Tasks.

- **The menu** is grouped by when you reach for it: Every day, The package, Administration. The names are short, a count is a badge beside the name, and the page you are on is marked.
- **Change requests**, **My work**, **Agent activity**, **People and projects** and **Audit** are rebuilt this way.
- **Reviews** now holds what has been signed off as well as the review activity: one page instead of two that showed the same verdicts.
- **Costing** has a budget, set on the page, and says how the spend compares with it.
- **Domain lenses** is now **AI capabilities: who can use them**. It opens on how many AI operations no screen reaches, and the table under it can be searched. The flash sale lens has gone from it; the deployment map covers the flash sale.
- **Ask about the package** opens on the question box with questions drawn from this package, names the sources under each answer as links, and sets the provider key in **Settings → AI answers**.

### A blocker is always a change request

When something stops a ticket, it is raised as a change request, the ticket goes On hold, and the
agent takes the next ticket that nothing blocks. **My work** and the connector's board say which
tickets an open blocking request affects, so a held ticket says why.

### You are always on the latest release

Pulling a ticket always pulls it at the release ADAM serves; nothing asks which release, and the
ticket's README says what changed since your last pull. When a change request is settled, the ticket
it came from is told: an open ticket gets one comment for the agent that pulls it, a closed one gets
a child task. A child task somebody made by hand in OpenProject can be linked to its request rather
than made twice.

## 13 October 2026

### Tasks counts Tasks, and shows each day and each person

- **Count: Tasks or Tickets.** Every number on the Tasks page used to mix features, tasks and sub-tasks. It now counts OpenProject Tasks by default, with a switch for every ticket; every count says which unit it is in.
- **One person.** Select a name and the page is everything about that developer: their sprint, what they hold, what waits for QA, what they finished and the testing gate. The address names them, so it is a link you can send.
- **Finished each day** and **Daily expected**: who finished how many on each working day of the sprint, and what each person's sprint asks of them per day.

### Pages open faster

The Tasks page took over half a minute to open, most of it waiting for OpenProject to be read
again. ADAM now keeps the last read, re-reads in the background, and answers at once; Tasks says
when the numbers were read and Refresh redraws when a new read lands. Scripts are kept by your
browser between visits.

### Setup, for frontend developers and for agent activity

- Setup on a new frontend folder makes a workspace you clone your app's repository into, and setup on a folder that already has code adds ADAM's missing files without touching yours.
- Setup and `/update-adam` now install the usage hooks for a zip install too, so your sessions reach **Agent activity**. Before this only a plugin install had them, and the team installs from the zip, so the page stayed empty.

## 12 October 2026

### Tasks is the whole team's delivery dashboard

The Tasks page opens on the current sprint: who has finished what, who is late, what waits for QA,
and who is held on the testing gate. In progress, waiting for QA and stalled are told apart, and a
move to QA counts as finished. Every member of the delivery team can open it; a client account still
cannot.

Through the connector, developers can see each other's work too (`adam_team`).

### Change requests settle in a batch

An administrator can settle a batch of change requests from a file on a workstation; each settled
request leaves one comment on the OpenProject ticket it came from.

## 7 October 2026

### /update-adam finds your ADAM

`/update-adam` used to look for ADAM on your own machine and fail for everybody. It now finds it
where the connector does, and says where it looked.

## 6 October 2026

### Setup clones the team's repository

For a TICVAI backend developer, setup clones the team's repository. It asks for your GitLab
username first, because a private project answers "not found" to a clone that has not said who
it is.

## 5 October 2026

### Tasks reads the whole project

The Tasks page, Costing, the plan and My work read only the newest 2,000 tickets, which were almost
all sub-tasks. They now read every ticket in the project.

## 1 October 2026

### Releases, and what changed since you pulled

ADAM serves each package at its newest release. Pulling a ticket records the release you pulled it
at, and when a newer one is served the pull says what changed in the parts that ticket touches.
A change request now carries where it came from, who approved it, its effect on the contracts and
its size, and the Change requests page shows them.

Every ticket shows its build order again, read from the Priority_No. field.

## 30 September 2026

### The connector copes with a dropped connection and a long board

A read that loses its connection is tried again, and when it still fails it says why. The board
shows the first 30 tickets in build order and says how many follow, instead of an answer too large
to send.

## 28 September 2026

### Tasks is a dashboard, not a long scroll

The Tasks page was one 26,000-pixel scroll. It is now a dashboard, with throughput as a chart.

### The connector installs as a Claude Code plugin

Two lines in Claude Code instead of a zip, a `setup.cmd` and a walkthrough:

```
/plugin marketplace add Diretide298/Solution_Architecture
/plugin install adam@adam
```

Claude Code then **asks you** for the ADAM address, your e-mail and your password, and puts the
password in your operating system's credential store rather than in a settings file. The old
registration kept it in plain text where `claude mcp get` would print it.

The plugin carries the connector, and also the **usage hooks** — the ones that fill the Agent
activity page (in the menu, under Every day). Those were a block of JSON in a README that people were asked to paste into
`settings.json` by hand, which is to say they were mostly not installed at all. Installing the
plugin installs them.

**Updates come from the marketplace**, so `/update-adam` is not the command for a plugin install —
`/plugin update adam@adam` is, and the connector says so on startup rather than sending you to an
updater that would write files the marketplace owns on its next update. **Settings → Claude
connector → Builds** now shows which of the two installs each machine is on, so retiring the zip is
something you can watch happen rather than guess at.

**The zip still works and still needs `setup.cmd` for a first install.** Nothing has to move today.

### Adam is on the landing and home pages

The mascot now stands beside the lockup on the landing page, next to each section heading, and in
the corner of the home page's graph. Twenty poses came out of the delivered sheet — reading,
thinking, sleepy, error, and the rest — cleaned the same way the first set was: the sheet arrives
with a faint wash over the background that shows up as a pale rectangle on any dark panel.

These are stills, not video. The clips the corner dock plays are keyed out of a dark render at
runtime, and both of these pages have a light theme — the key leaves a haze that is invisible on the
viewer's dark panel and would not be here. The dock is unchanged.

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

- ADAM would not start on any store with real history in it — an index named a column that the migration had not added yet. Fresh installs never saw it; every real one did.
- The avatar page is gone.
