# What a package is, and where it goes

The viewer used to live inside the one package it could read, and "where is the
package" was answered by `..`. It reads several now, each registered by path, so
a package is a thing with a name and a shape rather than a folder that happens to
be one level up.

This is the shape. Anything that generates a dump should produce it.

---

## The layout

Three things at the same level, none inside another:

```
adrov/
├── viewer/                 the reading server and the pages — its own repo
│   ├── server.mjs
│   ├── projects.json       ← which packages, and where
│   ├── lib/
│   ├── public/
│   └── api/                the accounts service (FastAPI + SQLite)
│
├── ticvai/                 one delivery package — its own repo
│   ├── contracts/
│   ├── screens/
│   └── …                   see **What a package contains** below
│
└── some-other-project/     another one, identical in shape
    └── …
```

The viewer does not have to be beside the packages, and the packages do not have
to be beside each other — `root` in the registry can be an absolute path on
another disk. The layout above is the one that reads clearly; the code only cares
about the registry.

## The registry

`viewer/projects.json`. One entry per package. Read once at startup, so adding a
project is a restart.

```json
{
  "default": "ticvai",
  "projects": [
    {
      "id": "ticvai",
      "name": "TICVAI",
      "root": "../ticvai",
      "contracts": "contracts",
      "active": true,
      "note": "The venue platform delivery package."
    }
  ]
}
```

| field | |
|---|---|
| `id` | the first segment of every read — `/pkg/ticvai/index`. Lowercase letters, digits and hyphens; no dots or slashes. `projects`, `api`, `pkg` and `health` are reserved. |
| `name` | what a person calls it. Shown on the door. |
| `root` | resolved against the **viewer directory**, so `..` is the folder the viewer sits in and `../ticvai` is a sibling. Absolute paths work. |
| `contracts` | the folder inside it holding the OpenAPI files. Defaults to `contracts`. This is what the old `--dir` flag used to say, and it is a property of a package rather than of the process. |
| `active` | `false` hides it without deleting the entry. |
| `default` | which project answers the pre-project `/api/*` routes. |

A broken entry is reported at startup and skipped. The other packages still
serve — a viewer that refuses to start because one of four disks was not mounted
is a viewer that cannot tell you which one.

## The addresses

```
/pkg/<project>/index                every payload route
/pkg/<project>/wireframes/<file>    a board, served whole
/pkg/<project>/frame?board=…&anchor=…   one frame lifted out of a board
/pkg/<project>/designs/<file>       an exported design board
/pkg/projects                       the registry — what there is
/api/…                              the accounts service: auth, invites, verdicts
```

The package reads are **not** under `/api/`. That prefix is shared with the
accounts service, which is why nginx had to name each package route explicitly —
and why `summary` and `diagrams` fell through to a service with no code for them
and 404ed while the landing page drew zeroes. `/pkg/` belongs to one process, so
the front door is one rule with no list in it.

`/api/*` still answers, against the default project, until every client has
moved. It is the last thing in the deployment kept in step by hand.

---

## What a package contains

Every folder is optional. A package with only `contracts/` serves every route —
the rest come back empty, and the Audit says what is missing rather than the
server failing. Verified: a package containing one `contracts/widgets.yaml` and
nothing else answers all fifteen routes.

| folder | read by | what it holds |
|---|---|---|
| `contracts/` | the index, the tooltips, the diagrams | the OpenAPI files. **The only folder worth calling required** — it is the join every other layer resolves against. |
| `screens/` | frontend, wireframes, boards | `P##-name.yaml`, one per platform: the platform block, then `screens[]` with `layout`, `apis`, `wireframe.board`. |
| `flows/` | frontend, tooltips | one job a person came to do, traced across screens. |
| `frontend/` | frontend | the app manifests — runtime, platforms, packages. |
| `states/` | lifecycles | one state model per file: which moves between statuses are legal. |
| `events/` | lifecycles | what goes through the outbox when something happens. |
| `backend/` | DB | the versioned SQL. |
| `handoff/` | DB, lineage, boards, tooltips | the pre-computed joins: `screen-index.json`, `api-data-lineage.json`, `tooltips.json`, `relationships.csv`, `domain-markers.json`, the schema workbook. |
| `diagrams/` | architecture | `README.yaml`, `hld/00-platform.yaml` … `04-lifecycles.yaml`, and `lld/<set>/<name>.yaml`. |
| `docs/` | decisions, tooltips, DB | `docs/architecture/` (the ADRs), `docs/registers/`, `docs/active/`. |
| `wireframes/` | frontend | the drawn boards, `*.dc.html`, with an `id="<screen-id>"` per frame. |
| `designs/` | frontend | exported UI/UX boards. The folder name comes from the boards reader, so a rename does not need a code change. |
| `UIUX_html/` | boards | an alternative home for the same. |

Each package is watched independently. A change under one rebuilds that package
and tells only its readers to reload.

### Two conventions that carry weight

**Board anchors are the join between a drawing and a definition.** A screen says
`wireframe.board: wireframes/<file>#<anchor>`, and the board carries
`id="<anchor>"` on that frame. A link to an anchor that is not in the board is a
click that silently does nothing, which is worse than no link — `tools/check-wireframes.py`
checks both directions.

**Where a package ships two boards for one platform, the screens must point at
the drawn one.** A generated board is named after the platform; a drawn pack is
named after the app. `wireframe.status` says which: `designed` or `generated`.

---

## Permissions

Access is per project. The tables are created and backfilled at boot by
`viewer/api/db.py` — additive and idempotent, so a live store needs no dump and
no restore.

```
project          id · name · active · created_at
account_project  account_id · project_id · role     (PK: account_id, project_id)
verdict          + project_id      DEFAULT 'ticvai'
invite           + project_id      DEFAULT 'ticvai'
```

- **A missing row is no access.** There is no "everyone may read everything"
  default to forget to turn off, so a newly registered project is invisible until
  somebody is granted it.
- **`account_project.role` decides a package read** — reviewer or client. The
  same person can be a reviewer on one package and a client on another.
- **`account.role` keeps only `admin`**, which was never per-project: who may
  invite, reset and manage. An admin reads every active project, because they are
  the person who registers projects and issues grants.
- Existing rows migrate by default value: every verdict that exists was written
  about TICVAI, because there was nothing else to write about. The one backfill
  is a single `INSERT` giving every account the access it already has.

`session` is untouched. A session is a person, not a project — otherwise a second
tab on a second package would need a second login, which is the thing a
multi-project viewer exists to allow.

---

## Running it

```bash
cd viewer && node server.mjs --port 4173
```

Startup prints one line per package: its id, its root, and how many folders are
being watched. A package that fails to build says so with its own id in the
message.

`--dir` is accepted and ignored — it said which folder held the contracts, which
is now `contracts` in the registry, per package.

### Deployment

nginx needs one rule for the reads:

```nginx
location /pkg/ { proxy_pass http://127.0.0.1:4173; }
```

`deploy.sh` checks for it. While the old `/api/*` names are still listed, it
checks those against `server.mjs` too and refuses a deploy where they disagree.
