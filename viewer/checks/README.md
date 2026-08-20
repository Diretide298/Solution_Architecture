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

`pages-check.mjs` is the cheap one to run after any edit to a module under
`public/`. `node --check` proves a file parses; it says nothing about whether the
names in it resolve. Three separate edits produced a file that parsed cleanly,
rendered its static HTML, and threw at module scope — leaving a page with a
header and nothing under it. A static version of this check was tried and pulled:
it could not tell a regex literal from a reference and reported eighteen things
that were fine. The browser either throws or it does not.

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
