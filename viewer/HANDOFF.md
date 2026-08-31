# Handoff

Written 25 Aug 2026, at the end of the session that split this repository out of
the delivery package. Everything below is either waiting on you or waiting to be
built. Read it, then say which.

```
Desktop/adam/
├── viewer/     this repo — server.mjs at the root, deploy/ inside
└── ticvai/     the delivery package — its own repo, no viewer in it
```

`Desktop/ticvai` is the pre-split repository. It still exists and is untouched
apart from one commit. Nothing has been deleted anywhere.

---

## Waiting on you

**1 · Neither new repo has a remote.** Nothing is pushed.

```bash
cd ~/Desktop/adam/viewer && git remote add origin <url> && git push -u origin main
cd ~/Desktop/adam/ticvai && git remote add origin <url> && git push -u origin main
```

**2 · Decide about `repos/` before the first push.** `adam/ticvai/repos/` is
5,762 files of generated `project-bible` mirrors, already 14 files out of date —
`tools/check-package.py` fails on exactly that and did so before the split too.
If `tools/derive-mirrors.py` still makes them they do not belong in a repository
at all. Removing them after the first push is a history rewrite; removing them
now is a delete.

**3 · The nginx config still has to be installed and reloaded.** This is the
`/api/summary` 404 you reported as "still same" — the file in this repo has been
right for a while and the server has never been given it.

```bash
sudo cp deploy/nginx/adamapi.ainfinite.ai /etc/nginx/sites-available/
sudo rm -f /etc/nginx/sites-enabled/asterapi.ainfinite.ai
sudo ln -sf /etc/nginx/sites-available/adamapi.ainfinite.ai /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx
```

It now carries `location /pkg/`, which is one rule covering every route of every
project — so this is the last time a new route needs an nginx change.

**4 · Deploying runs the database migration.** `project`, `account_project`,
`verdict.project_id` and `invite.project_id` are created and backfilled at boot
by `api/db.py`. Additive and idempotent: no dump, no restore, no data step.
Tested on a copy of the live store, run twice — 15 verdicts all landed on
`ticvai`, 3 accounts kept the access they had, 148 sessions and 5 mentions
untouched.

It is reversible until the first verdict is filed against a *second* project.
After that, older code keeps the rows but stops being able to tell which project
they were about.

**5 · The deployed layout changed.** `deploy.sh` now copies this repo into
`$APP_DIR/viewer/` rather than `$APP_DIR/`, and the package must be checked out
beside it:

```
/srv/ticvai/
├── viewer/     this repo
└── ticvai/     the package repo
```

so `"root": "../ticvai"` in `projects.json` means the same thing on the server as
it does here. `deploy.sh` refuses to finish if a registered package is not on
disk, naming it — a viewer without its packages starts, answers every route and
counts zero, which is the shape of the bug that had the landing page drawing
zeroes for weeks.

**6 · `openpyxl` is missing on the serving interpreter.** CSV decision upload
works; `.xlsx` fails at request time.

```bash
"C:/ProgramData/miniconda3/python.exe" -m pip install openpyxl   # then restart 8787
```

**7 · A fresh clone needs `npm install`.** `node_modules` is gitignored, so the
split left it behind. It was copied in by hand to test.

---

## Waiting to be built

**Animated diagrams.** Direction agreed, nothing written. Two pieces, the second
built on the first:

1. An `<animateMotion>` dot travelling the existing `<path>` on the SVG diagrams,
   on the same hover trigger, *alongside* the current dash rather than replacing
   it — the dash says "this path is live", the dot says which way.
2. A trace on the Overview: click a box, the dot walks its path column by column
   with a delay per hop, and what it reached stays lit and counted.

Three things the research settled, worth not rediscovering:

- The Figma technique in the inspiration images is a masked dashed line looped
  with Smart Animate. Its web equivalent is `stroke-dasharray` + `stroke-dashoffset`,
  which `dia-flow` in `public/styles.css` already does. That half is built.
- **SMIL ignores `prefers-reduced-motion`.** `<animateMotion>` keeps running
  whatever the media query says, so the dots have to be removed from the DOM
  rather than styled off. Every other animation in this viewer honours the
  setting; this one would quietly not.
- A visible pause/play belongs on any diagram that moves on its own.

**Nothing grants a project through the UI.** `account_project` is enforced —
a missing row is 403 and the project is not listed — but rows can only be made
by hand. Admins read every active project, so this is invisible until the first
non-admin needs a second package.

**The `/api/*` alias.** Every package route answers at both `/pkg/<project>/x`
and `/api/x`, the second against the default project. The client uses `/pkg/`
everywhere now, so the alias is only there for anything outside this repo that
still calls the old paths. When it goes, the per-route nginx regex and the drift
check in `deploy.sh` go with it.

---

## Things that will bite

**`public/` is served from disk — a reload is enough.** `server.mjs`, `lib/*.mjs`
and `api/*.py` are read at startup: those need a restart.

**Never touch `api/ticvai.db`.** Do not create, delete or modify any account or
verdict in it. Test against a copy, or a spare port with the gate off:

```bash
TICVAI_NO_GATE=1 node server.mjs --port 4619
```

**Do not kill or restart anything on 4173 or 8787.** Those are started by hand
and stay that way. Throwaway instances go on 4619+.

**Route names live in two files while the alias lasts** — `server.mjs` owns them,
`deploy/nginx/adamapi.ainfinite.ai` forwards them, and `deploy.sh` greps both
and dies when they disagree. `location /pkg/` satisfies the check on its own.

**The package's own checkers pass with warnings, and the warnings matter.** From
`adam/ticvai`: `check-wireframes` PASS/13, `check-screens` PASS/657,
`check-traceability` PASS/0, `check-package` FAILS on the six stale mirrors.
`check-wireframes` prints only the first 20 warnings — a warning that "appears"
may just have become visible.

---

## Shape of the thing, briefly

```
/pkg/<project>/index               every payload route
/pkg/<project>/wireframes/<file>   a board
/pkg/<project>/frame?board=&anchor= one frame out of a board
/pkg/projects                      the registry
/api/…                             the accounts service — auth, invites, verdicts
```

`projects.json` is the only place a package path appears. `PACKAGES.md` in this
repo is the full description of what a package contains — hand that to whatever
generates the dump.

Server state is a record per project in a `Map`; a rebuild publishes every part
in one statement, so a request mid-rebuild can never get a new index against an
old backend.
