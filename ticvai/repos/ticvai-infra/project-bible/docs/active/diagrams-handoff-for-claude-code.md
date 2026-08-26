# Handoff — the diagrams folder and the Architecture layer

**24 August 2026.** Read this before touching `diagrams/`, `tools/derive-diagrams.py`, or the
viewer's Architecture layer.

---

## What changed

**`diagrams/` is new and it is entirely derived.** Five high-level files, 172 low-level files, and
an index. `tools/derive-diagrams.py` writes all of them and is wired into `refresh.sh`.

```
diagrams/
  README.yaml                  the map of the map — start here
  hld/
    00-platform.yaml           actors, surfaces, services, stores, externals, regions
    01-hierarchy.yaml          eight scope levels, counted from the contracts
    02-services.yaml           sixteen services, five tiers, 34 cross-service write edges
    03-contracts.yaml          28 contracts, spine and satellite, events between them
    04-lifecycles.yaml         113 state models, 29 events
  lld/
    services/                  16 — schemas, tables, operations by contract, screens, flows
    platforms/                 15 — screens with modules, offline states, entry params, coverage
    contracts/                 28 — every operation with verb, path, scope, permission, reads, writes
    lifecycles/                113 — the full state model, transitions and guards
```

**Every node carries a `ref` at the file below it.** `hld/00-platform.yaml` is the entry point.

---

## The rule that matters most

**Nothing in `diagrams/` is hand-authored, and nothing should be.**

A hand-maintained diagram in a package with nine validators is **the one artefact that goes stale
silently** — no check fails when it is wrong. That is how the mirrors drifted 503 files and how the
services workbook reported 371 tables against 379, and both were found by a person rather than by a
check.

**`check-package` now refuses a diagram older than `handoff/service-decomposition.json`**, and
refuses an LLD file naming a service that no longer exists. It compares mtime rather than content
deliberately: the point is to catch a package where `refresh.sh` was not run.

**If a diagram is wrong, fix the deriver or fix the source. Never fix the file.**

---

## What to do in the viewer

The **Architecture** layer is built and shows services. **Extend it to read the whole folder.**

**Suggested modes**, matching what the files now hold:

| Mode | Reads |
|---|---|
| Overview | `hld/00-platform.yaml` |
| Hierarchy | `hld/01-hierarchy.yaml` |
| Services | `hld/02-services.yaml` → `lld/services/*` |
| Contracts | `hld/03-contracts.yaml` → `lld/contracts/*` |
| Lifecycles | `hld/04-lifecycles.yaml` → `lld/lifecycles/*` |
| Deploy | `hld/02-services.yaml` `deployOrder` |

**`lib/structure.mjs` already renders these as-is** — it turns any YAML into a node tree with a
source line on every node, which is what lets a click on a table node open the schema reference at
the right place. **No new renderer is needed; a lib module that reads the folder is.**

---

## Two naming decisions to make

**The `domain` layer should be renamed `Lifecycles`.** *Domain* names a methodology rather than a
subject, and every other layer names a thing a reader recognises — Frontend, Contracts, DB,
Decisions. **It does not hold the domain either**; the domain is spread across all five layers.
It holds lifecycles: a state model is one within an entity, an event is one crossing between two.

**`hld/04-lifecycles.yaml` carries that argument in a `naming` field**, so the file explains itself
if the rename is not made.

**Do not add HLD/LLD files for the DB layer.** It already has both and they are computed — Galaxy is
the schema overview, the drill-down is the table detail. **A YAML restating a live view is a file
that can disagree with it**, which is the failure this folder exists to avoid.

---

## Related changes in the same pass

**`shift` moved from TenancyService to OrderService.** It owns no tables — which is true, and the
conclusion drawn from it was wrong. **A service with no data belongs where its data is**, and a
shift's data is entirely in `orders`. All 43 of Tenancy's cross-service touches into `orders` were
the `shift` contract; moving it took Tenancy's cross-service writes from 23 to 2.

**`diagrams` was added to `MIRRORED` in `tools/derive-mirrors.py`.** It was in the root package and
in no mirror — the same shape of defect that left 96 orphaned wireframe files in six repos, arriving
from the other direction.

**Two workbook columns now join services to tables.** `Tables` gained `Service` and
`Foreign writers`; `Where used` gained `Owner service` and `Also written by`. Before this, a reader
could ask which service owned an *operation* and not which owned a *table* — and the second is the
question you ask before writing DDL.

---

## Figures worth not restating from memory

**304 of 379 tables anchor on `platform.scope_node`**, and 71 reference it directly. I reported
"289 of 378" for several days from an earlier count. **The hierarchy diagram now derives it**, so it
cannot drift again.

**32 tables have a foreign writer** — a contract outside the owning service. **22 tables have two or
more writing contracts.** Both figures are correct and they count different things; the first is the
one that matters for a service boundary.

**Build is 0%.** 379 tables specified, none written. **No diagram in this folder changes that**, and
`hld/00-platform.yaml` says so in its own `honestly` field.
