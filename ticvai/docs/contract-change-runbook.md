# Contract change runbook — what a contract edit sets off

> **Read this before editing anything in `contracts/`.** It is the order and the blast radius, not
> a summary of them. Every step exists because skipping it cost something, and the cost is named
> against each.
>
> **Owner:** Chinmay · **Written:** 19 September 2026 · **Status:** authoritative
>
> **A contract is the top of everything derived, and a wrong one does not announce itself.** It
> produces a screen layer that cannot bind and a gap list proposing operations that already
> exist — three steps from the cause, in a tool that had no part in it. On 19 September a
> duplicate `/resource-bookings:` key silently replaced the original path object, took
> `bookResource` with it, and surfaced as *"operation does not exist"* in a checker that runs
> twenty minutes later.

---

## The rule

**`contracts/` is edited by hand. Nothing below it is.** Thirty-two files, 1,981 operations. Every
number, table, diagram, workbook, screen binding and register in the package is computed from
them, and the computation is `tools/refresh.sh`.

**The corollary is the part that gets skipped: an edit is not finished when the YAML is valid.**
It is finished when the refresh has run to the end and the checkers pass. Between those two
moments the package is internally inconsistent and nothing should be published from it.

---

## The blast radius, in four rings

A contract edit reaches further than it looks. The rings below are ordered by how far the change
has to travel before it becomes visible, and **ring 4 is the one that has never been automatic.**

### Ring 1 — the data layer (automatic, ~4 min)

`derive-lineage` runs first because **twenty-plus tools read `handoff/api-data-lineage.json` as
authoritative**. Until it runs, a new operation is invisible to `check-package`, `check-screens`,
`derive-relationships`, both workbooks and the viewer — and `check-package` fails the package for
the gap, correctly, with nothing in the pipeline able to close it.

```
derive-lineage --apply      api-data-lineage.json     <- first, always
derive-schema               merges into handoff/      <- merges, never rebuilds
derive-relationships        relationship-graph.json
derive-ddl --apply          backend/*.sql + schema-reference.json
derive-burst-scope          derive-sizing             derive-table-notes
derive-schema-roots         derive-write-decisions
```

**`derive-lineage --apply` adds and never updates.** An entry that exists is left exactly as it
is, because the original entries carry judgements a derivation cannot reproduce. This is correct
and it is also a trap: on 19 September a *new* contract had no neighbours to infer a `service`
from, 133 operations landed with `service: null`, and `derive-diagrams` crashed on them. The
refresh was re-run twice before it was noticed that `--apply` could not repair what it had
already written. **A new contract needs its service named in `NEW_CONTRACT_SERVICE` before the
first refresh, not after.**

### Ring 2 — presentation and screens (automatic, ~6 min)

Diagrams, both workbooks, the board-panel map, then the screens block — which **fills blanks
only**. Tools that assert content were removed from the chain on 9 September because they
silently reverted hand edits.

The ordering inside this ring is load-bearing and each constraint was learned:

- `derive-board-flows` runs **before** `derive-transitions-from-flows`, so a board flow written
  this run becomes an edge this run rather than waiting a full rebuild.
- `derive-entrystate-params` runs **before** `derive-carries-from-entrystate`, which reads it.
- `index-boards` and `derive-id-register` run **before** `check-screens`, because a stale register
  fails the package for a screen that is perfectly fine.
- **Mirrors are last.** They copy `handoff/`, and `build-status` and `sync-counts` write
  `handoff/`. For a week every run finished with the mirrors one file behind and `check-package`
  reported six out-of-sync mirrors on a package that was otherwise clean.

### Ring 3 — registers, status and mirrors (automatic, ~3 min)

`build-backlog-index`, `build-cluster-index`, `build-cf-index`, `index-packs`, platform, audience,
status, guest parity, `sync-counts`, then the six repo mirrors.

### Ring 4 — the authored inputs no tool rebuilds (MANUAL)

**This is the discovery, and it is the reason this file exists.**

Nine files sit in `handoff/` and `wireframes/` looking exactly like derived artefacts. They are
read by the pipeline and by the viewer. **Nothing in `tools/` writes any of them.** A contract
change invalidates them and the refresh cannot say so, because from the refresh's point of view
they are inputs.

| file | last written | what it feeds | what a contract change breaks in it |
|---|---|---|---|
| **`handoff/service-decomposition.json`** | **24 Aug** | `check-package`, `derive-diagrams`, `derive-burst-scope`, both workbooks | its own note reads *"How **28** contracts and **378** tables become 16 deployable services"*. There are now **32 contracts and 556 tables**. `rental` and `accreditation` do not appear in it at all |
| `handoff/contract-backlog.json` | 3 Sep | rendered to `docs/registers/contract-backlog.md` | the backlog still lists operations that now exist |
| `handoff/backlog-clusters.json` | 3 Sep | rendered to `docs/registers/clusters.md` | clusters formed before 346 operations were added |
| `handoff/traceability.json` | 3 Sep | `build-status`, `check-traceability` | one verdict per matrix row; rows answered by new operations still read as unanswered |
| `handoff/api-list.md` | 3 Sep | viewer `lib/consumers.mjs` | which app consumes which API — new operations have no consumer |
| `handoff/artefact-audit.md` | 3 Sep | viewer `lib/decisions.mjs` | classifies the handoff tables; new artefacts unclassified |
| `handoff/schema-viewer-notes.md` | 3 Sep | viewer `lib/relationships.mjs` | the prose explaining the schema the viewer draws |
| `handoff/rag-index-sources.md` | 3 Sep | `check-package` | what the RAG index was built from |
| **`docs/**/*.md`** | **continuously** | the reasoning — ADRs, briefs, audits, the registers | **a rename falsifies every sentence naming the old table.** On 20 September sixteen tables were renamed and 48 names across 21 documents went stale, including ADR-0018's own justification for the scope walk, *"`org_unit` is an `ltree`"* — in the ADR the rename was argued from. **Guarded since: `check-doc-tables.py`**, which reads the renames `derive-schema-history.py` declares and fails on a document still using the old name. A quotation is left alone |
| `wireframes/LINKAGE.md` | **25 Aug** | viewer `lib/wireframes.mjs`, `lib/lineage.mjs` | the chain from board to screen to operation, drawn in one line |

**`service-decomposition.json` is the one that matters most and the one that can least be
automated.** Assigning a contract to a deployable service is a deployment decision, not a contract
fact — the same reason `derive-lineage` is additive-only. It needs a person. But everything that
draws the service topology reads it, so a contract absent from it is absent from the diagrams, the
burst scope and both workbooks, **while every checker passes.**

---

## The protocol

### Before the edit

1. **Check the matrix and the MoMs before the contract.** A stated product rule may contradict the
   requirement matrix. Source precedence is **MoM > boards > specifications**, and the matrix where
   all three are silent.
2. **Check whether the operation already exists.** On 19 September a gap list proposed ~1,300
   operations and ~260 were real. `python3 tools/find-capability.py <term>` before authoring.
3. **Scope before authoring.** `tools/scope-pack-to-contracts.py` scores unserved screens against
   every operation in every contract. **Nine of nineteen packs turned out to be joins, not gaps** —
   Marketing CRM needed 17 new operations to serve 107 screens.

### Making the edit

4. **Never hand-append to a contract. Use `tools/splice-contract.py`.** It exists because of the
   two failures it now refuses:
   - a **duplicate path key**, which YAML resolves silently by keeping the last one — taking every
     operation on the original object with it;
   - **paths appended inside `components:`** when `securitySchemes:` happened to come first, which
     made 13 operations vanish from `paths` while every `$ref` still resolved and the tool
     reported *clean*.

   It now splits the file into three regions and verifies each expected `operationId` is present in
   the parsed `paths` afterwards.
5. **Check the operation exists before wiring a screen to it.** Four wiring runs invented ten
   operation names between them — `getDemandPricing`, `createPage`, `listSites`, `publishSite` and
   six more. A pre-apply existence check against all contracts catches every one.
6. **Check whether your target screen is a `source.sameAs` twin.** `sameAs` means **twin, not
   superseded**: ten fields must stay byte-identical and **only the master may be edited**. This
   was tripped three times in one day — 53 bulk-wiring errors, then `SGN-005`, then `EMP-088`.
   **No wiring script checks this yet.** Until one does, check by hand and let
   `tools/applied/apply-*.py` copy master to twin.
7. **A new contract needs its service before the first refresh** — see ring 1.
8. **ADR changes are confirmed with the owner every time.** No exceptions.

### After the edit

9. **Run `bash tools/refresh.sh` and let it finish.** It is idempotent and takes roughly 12–15
   minutes. **Stopping it midway is the worst outcome available**: the data layer moves and the
   screen index, status and mirrors do not, so `handoff/screen-index.json` ends up older than the
   lineage it describes while every file on disk looks current.
10. **Read the checker block at the end.** Twenty-four checks, all non-fatal so one failure cannot
    hide the twenty-three below it. The baseline is `check-screens` PASS and `check-package` 9.
11. **Re-check ring 4 by hand.** Nothing else will.
12. **Only then commit**, and scope the commit to the work actually done.

---

## What this cost on 19 September

The run that produced this file added 346 operations and four contracts, and the refresh was run
**in the middle of the repair phase rather than after it**. Three commits then edited contracts and
screens — `promotions.yaml` lost 104 lines, `marketing-crm.yaml` gained 8 operations, three screens
changed — all after the last derive.

`check-screens` reported PASS and it was telling the truth: the checkers read the screens directly.
**The derived layer underneath them was thirty-five minutes stale, and nothing in the package said
so.** Step 9 is that lesson, and the coverage guard now at the foot of `refresh.sh` is the other
half of it — eleven tools existed that the script never ran, four of their outputs between 10 and
25 days stale, under a comment claiming every checking tool was already in the list.

**A tool that exists and never runs is worse than one that does not exist**, because its output is
on disk with a date nobody reads.
