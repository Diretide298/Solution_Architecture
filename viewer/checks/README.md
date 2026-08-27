# Checks

Puppeteer harnesses run against a viewer that is already up. Both halves have to be
running and an account has to exist, because the viewer is behind a sign-in:

```
./start.ps1                       # frontend on 4173, accounts on 8787
node checks/paging-check.mjs
node checks/contract-trace-check.mjs
```

They sign in as `harness.admin@softlabsgroup.com`. Create that account once — through
`/admin.html` if you already have an administrator, or as the first account at the door
on an empty database.

| | what it holds still |
|---|---|
| `paging-check.mjs` | the boot payload is split and compressed, every held-back field comes back from `/api/detail`, and the long list is built a group and a page at a time without losing a row |
| `contract-trace-check.mjs` | a schema names the tables it is stored as, an operation names the tables it reaches, and an operation the lineage never resolved says so rather than reading as "touches nothing" |
| `signoff-check.mjs` | the overview counts against the whole population rather than what was judged, unreviewed artefacts sort first, and a row leads to the artefact — including the three kinds that had no deep link until it needed one |
| `pages-check.mjs` | every page loads, every layer renders every one of its modes, and **nothing anywhere logs a console error** |
| `landing-check.mjs` | the door sends people where it says — the lockup stays on the door rather than falling into a package, all 42 rail-panel links land on the layer *and* mode they name, Overview deselects, and sign out really ends the session |
| `tip-facts-check.mjs` | every count a tip states is the count the payload holds — the tips write `{operations}` and are measured against `/pkg/<project>/lineage`, `journeys` and `decisions` |
| `search-check.mjs` | search reaches the whole package and not only the contracts, every `file:line` it reports really is where that artefact is written, and a result opens the artefact's page *and* the source at that line |
| `subsearch-check.mjs` | every page that lists things can be narrowed, the count keeps its denominator, and a row drawn after the filter was typed is filtered too |
| `uiux-check.mjs` | the board list holds every board on disk, not only the ones a screen points at; each of the 58 board files and one frame out of each of the 54 with frames actually resolves; and the filters filter |

`pages-check.mjs` is the cheap one to run after any edit to a module under
`public/`. `node --check` proves a file parses; it says nothing about whether the
names in it resolve. Three separate edits produced a file that parsed cleanly,
rendered its static HTML, and threw at module scope — leaving a page with a
header and nothing under it. A static version of this check was tried and pulled:
it could not tell a regex literal from a reference and reported eighteen things
that were fine. The browser either throws or it does not.

`tip-facts-check.mjs` exists because nothing failed when the numbers were wrong.
The tips stated **654 operations against a live 1,023, 22 services against 16, 18
ADRs against 30**, and "318 of the 654 resolve to no table" against a lineage in
which nothing is unresolved — every page rendered, every check passed, and the
viewer told its readers the wrong size of the thing they were reviewing. The
counts are read off the payload at hover now; this is what holds that true.

It drives the panel with a dispatched `mouseover` rather than a real hover,
because most tipped controls sit in a toolbar belonging to a view that is not
open: `hover()` cannot reach them, fails silently, and leaves the previous tip's
text in the panel — which reads as a pass for every element after the first. It
also walks every layer, since a mode button exists only while its own layer does.

It runs against a gated viewer as the others do, or against a throwaway
`TICVAI_NO_GATE=1` instance with no account at all.

`uiux-check.mjs` exists for the reason the page does. `buildWireframes`
describes only the boards a screen already points at, because its job is
putting a frame on a screen's page — so **23 of the 58 boards were reachable
from nowhere in the viewer**, including every Inventory board and a hand-built
index of 255 frame links, every one of which resolves. Nothing failed while
that was true; the boards were simply absent, and absent and non-existent look
identical. So the first thing this holds is that the number of cards equals the
number of files on disk, and the second is that every one of those files and a
frame out of each of them answers 200 — a catalogue whose entries 404 is worse
than no catalogue, because it says the board is there.

**Point every harness at a throwaway pair rather than 4173/8787.** The two
environment variables are not the same thing and the difference is easy to get
backwards: `TICVAI_API` is where the *page* is told to look, and on a
workstation that has to be the **viewer's** origin, because the viewer serves
the package and forwards `/api/auth` to the accounts service. Setting it to the
accounts port instead gets a CORS failure on sign-in, or — worse, because it
looks like it worked — a signed-in page whose every package read 404s.

```
TICVAI_VIEWER=http://127.0.0.1:4620 TICVAI_API=http://127.0.0.1:4620 \
  node checks/uiux-check.mjs
```

`signoff-check.mjs` **records one real verdict per kind** — six of them now that
state models and schemas are reviewable — against real artefacts, because checking
the join against a fake population would check nothing.

Point the service at a scratch store before running it —

```
TICVAI_DB=/tmp/scratch.db python -m uvicorn api.main:app --port 8787
```

— or undo it afterwards with `python -m api.cli forget harness.admin@softlabsgroup.com --yes`.
Do one or the other. Left alone, the first thing the sign-off page shows is four
things already approved by nobody in particular.

Both check on a **cold tab** — one navigation, no visiting another layer first. The parts
these views read arrive after the layer is already drawn, which is exactly where a block
like this fails quietly.

`api/api-check.mjs`, `api/extras-check.mjs`, `api/gate-check.mjs` and `api/ui-auth-check.mjs`
cover the accounts service and the sign-in gate, and run the same way.

`api/logout-all-check.mjs` covers signing out everywhere — both the reviewer doing it
to themselves and an admin doing it to somebody else. It is the one harness that needs
**no browser**: it holds five cookie jars at once, because the claim is a counting one
(that account's sessions, all of them, nobody else's) and a session is only observable
by whether its cookie still answers. It enrols two throwaway reviewers, so give it a
scratch store like the rest.

`search-check.mjs` verifies the lines rather than trusting them. The palette
searched `index.nodes` and nothing else — **1,979 contract nodes out of 3,199
things in the package** — so a reviewer typing `POS-006` got "No match", which
reads as *not in this package* and meant *not a contract*. Widening it is easy;
the part worth holding is that a reported `screens/P04-point-of-sale.yaml:949`
is really line 949. **A file:line nobody checks is the worst kind of precision:
it gets believed.** So this fetches the file and reads the line, for a sample of
every kind, and separately fetches one file of every extension search points at
— which is how `.sql` turned out to be refused by `/api/file` until the
migrations became a search destination.

`subsearch-check.mjs` types a string nothing can contain and requires that
nothing is left showing. A filter that matches everything is indistinguishable
from one that does nothing, so matching *nothing* is the only assertion that
separates them — and it is what caught two `.stuck-row`s in a third container on
`domains.html`, out of 237 rows. Two rows left standing under a filter that
matched nothing read as two rows that did match.
