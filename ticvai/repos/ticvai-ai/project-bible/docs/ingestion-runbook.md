# Ingestion runbook — client packs into the package

> **Read this before ingesting anything.** It is the order, not a summary of one. Every step exists
> because skipping it cost something, and the cost is named against each.
>
> **Owner:** Chinmay · **Last run:** 19 September 2026 · **Status:** authoritative
>
> **A drop carries three kinds of document and only one of them used to be ingested.**
> Design books were parsed, MoMs were mined, and the specifications were filed and never
> opened — twelve technical chapters, the RFP, the hardware sheet and the seat manifest, with
> **zero citations anywhere in the package.** Step 0 now covers all three, and
> `tools/index-sources.py` is the ledger that says which have been read.

---

## The order

```
0  intake        zip -> sources/, all THREE categories, dedupe, authority, platform
1  parse         PDFs -> sources/workshop/pack.json          GATED
2  TRIAGE        every new screen vs every built one          <- decide compression HERE
3  placement     module -> platform, and what is not a screen
4  boards        one board per workshop board
5  ids           issue and register
6  wire          hubs off the platform home screens
7  flows         a flow per board
8  patterns      regions, components, gaps
9  linkage       entity x verb -> operations, and the gap doc
10 refresh       the whole derivation chain
11 design        export the batches                          <- ONE export, ONE queue
12 checks        eighteen checkers
```

## The precedence rule — which source wins

```
MoM  >  boards  >  specifications        and where all three are silent, the matrix
```

**Decided 19 September.** It replaced six coverage reports that disagreed with each other, and it
is the rule every step below resolves a conflict with. Full statement in
[source-precedence-19-september](active/source-precedence-19-september.md).

**The matrix is a real fallback, not a gesture**, and its route is two hops rather than one:

```
matrix row -> handoff/traceability.json -> contract operation -> generate-screens-from-contracts.py
```

`check-traceability.py` walks 3,184 rows with 2,647 `CONTRACTED`, so a row that is contracted
already names an operation that exists. **244 operations are reached by no screen** — that set *is*
the fallback, and it is bounded and countable. 136 rows (93 `GAP_CONTRACT`, 43
`CONTRACTED_PARTIAL`) cannot produce a screen by any route; they are contract work first.

## `P04` is final — never regenerate it

**The POS terminal is client-approved and is the fidelity reference every other build is measured
against.** No step in this runbook touches `screens/P04-point-of-sale.yaml`, and there is no
`P04-*` batch in `handoff/design-batches/` — the 10–14 September run already excluded it and every
run since must. Both generators take `--platform`; excluding it means never passing it.

**Steps 1 → 3 look like the whole job and are not.** On 19 September 814 screens were parsed,
placed and wired into `P08` and `P09` with step 2 skipped entirely. Nothing failed. The screens
were real, the counts reconciled, `check-screens` passed — and no board was collapsed, no screen
was folded into an existing one, and the archetype clusters that step 2 exists to catch went
straight into the package: **12 × "rule builder", 11 × "rule configuration", 9 × "policy
configuration", 9 × "command center"**.

---

## 0 — Intake

| | |
|---|---|
| Tools | `tools/index-packs.py` · **`tools/index-sources.py --write`** |
| Writes | `sources/packs-index.json` · **`sources/SOURCES-INDEX.md`** |

### A drop is three categories, and it is not ingested until all three are

| category | lands in | read by | how you know |
|---|---|---|---|
| **Design books** | `packs/`, `workshop/`, `boards/` | `parse-workshop-pack.py` | in `sources/workshop/pack.json` |
| **MoMs** | `mom/` | `mine-moms.py`, `build-mom-digest.py` | in `sources/mom-corpus.json` |
| **Specifications** | **`specifications/`** | **nothing, until 19 September** | cited outside `sources/` |

**On 19 September the third category had been filed and never opened** — the RFP, twelve technical
chapters, the hardware integration sheet and the seat manifest, **zero citations** anywhere in
`contracts/`, `screens/` or `docs/`, and no tool that so much as listed the folder. The MoM corpus
was simultaneously eight days stale: 22 of 27 mined, and the five missing were the five most
recent.

`tools/index-sources.py --write` reports all three with a read status that **cannot be faked** — a
document counts as read when something outside `sources/` names it. Writing the index does not make
anything read. Run it at intake and again at the end.

### Where things live now

```
sources/mom/               rank 1   minutes
sources/requirements/      rank 2   the matrix
sources/specifications/    rank 2   rfp/ ; and reference/ planning/ handover/
sources/packs/ workshop/ boards/    rank 3   the design books
sources/designs/ diagrams/ rank 3   directional
sources/legacy/            RETIRED  Ch01-Ch09 - a proposal WE wrote, never scope
```

**`sources/legacy/` is the trap this section exists to prevent.** Those chapters answer the RFP
domain for domain, so a coverage check run against them measures our screens against *our own
reply* and reports that the proposal is self-consistent. They are a useful checklist and they are
never scope.

**`specifications/handover/`** holds `Dev01`–`Dev03`. They produce **no screens** — nothing in
`screens/` should cite them and no coverage check should count them. They are the shape of what the
RFP's IP clause obliges us to hand over.

### Read the specifications, do not just file them

| tool | reads | rank |
|---|---|---|
| `tools/check-rfp-coverage.py` | the RFP | **2 — scope** |
| `tools/check-spec-coverage.py` | `legacy/Ch03` | 3 — ours |

**Both are review queues, not verdicts**, and both had to be built twice. A pooled-text match calls
`Emirates ID Reader` delivered on the word *reader* from an unrelated gaming screen; a strict
all-words match calls `Audit Trail & Logging` missing when the screen is called *Governance Audit
Trail & Compliance Evidence*. **The rule that works is the capability's rarest word, matched against
one name rather than the pool.**

**A PDF watermark corrupts capability names silently.** The RFP carries a rotated `CONFIDENTIAL` on
every page and pdfplumber splices its letters into words one at a time — `CrCedit`, `WCishlist`,
`ManOagement`. Left in, `Credit Memo Management` becomes a capability nothing can ever match. An
uppercase letter with lowercase on both sides is never legitimate in prose; that is the repair.

### Traps, all paid for

- **`Table Added` in a client changelog means added *this round*,** not *everything they have that we lack*. Reading it the second way produced a wrong correction within the hour.
- **Never deduplicate by filename.** Four PDFs in `requirements/` were byte-different truncations of the real pack at 3% of the size — a name-based pass would have kept the broken one. Compare hashes, and check the file *parses* before trusting either copy.
- **A hash-set check does not prove nothing was lost.** Comparing the set of hashes in the drop against the set on disk passes while a *path* disappears, because the same bytes still exist elsewhere. Five files went missing under exactly that check on 19 September. **Verify by path.**
- **`--apply` scope.** Only `reference`, `workshop` and `board` class documents centralise. `mom`, `requirement`, `design` and `rfp` never move.

**Check for duplicates here, before parsing.** The 18 September scan found **30 byte-identical sets** across five folders, 17 packs duplicated into `workshop/` alone.

**Traps, all paid for:**

- **`Table Added` in a client changelog means added *this round*,** not *everything they have that we lack*. Reading it the second way produced a wrong correction within the hour.
- **Never deduplicate by filename.** Four PDFs in `requirements/` were byte-different truncations of the real pack at 3% of the size — a name-based pass would have kept the broken one. Compare hashes, and check the file *parses* before trusting either copy.
- **`--apply` scope.** Only `reference`, `workshop` and `board` class documents centralise. `mom`, `requirement`, `design` and `rfp` never move.

## 1 — Parse

| | |
|---|---|
| Tool | `tools/parse-workshop-pack.py --check --apply` |
| Reads | `sources/workshop/*.pdf`, or `--from sources/packs --only <name>` |
| Writes | `sources/workshop/pack.json` |

**Count the boards and screens from the document's own headings first**, then set the gate from that — not from the parser's output. `--check` fails unless the parse reconciles.

**Compare on `(pack, board, number, title)`, never `(pack, number)`.**

**Two pack families, two vocabularies.** The workshop books put `Purpose` alone on a line; the `sources/packs/` books write `Purpose: …` inline. A parser that knows only the first reports every screen with an empty body and looks like it worked — `ACCREDITATION.pdf` first came back as **131 screens with 131 empty specifications**.

**The quality gate is not optional.** A title with no purpose and no sections is a line from a contents list, not a screen. Dropping them is the difference between **814 screens and 1,024 numbers**.

**A partial run must merge.** `--only X --apply` writes the whole file; without merging it replaces every other pack and prints a success line.

## 2 — TRIAGE · the step that gets skipped

| | |
|---|---|
| Tool | `tools/check-screen-redundancy.py --pack` |
| Writes | `docs/active/workshop-pack-triage.md` |

Scores every parsed screen against every built one and sorts them **check first / check / no near match**. Last full run: 590 screens → **26 check first, 58 check, 506 clear**.

**It is a review queue, not a verdict.** Operations decide whether two screens are the same, and a screen parsed from a PDF has none — so the scores rank a shortlist for a person and settle nothing alone.

**Compression is decided here and recorded in three places, all read by step 3:**

| mechanism | what it means | precedent |
|---|---|---|
| `BOARD_PLACEMENT: None` | a whole board is not drawn as screens | Unified BI boards 5–8 — *"a domain is a filter on an analytics screen, not a copy of it"*, **26 board screens became nine** |
| `COLLAPSED` | a pack screen folds into an existing screen | `ADM-321` → `ADM-241`, `ANL-011` → `ANL-001` |
| `SCREEN_PLACEMENT` | one screen of a board goes elsewhere | Subscription 6.10 hands the customer to board 7 |

**Record, never silently drop.** A collapsed screen that only prose remembers comes back on the next run — which is exactly how `ADM-321` and `ANL-011` returned, and why `COLLAPSED` is a table in the tool rather than a sentence in a document.

### Match on exact title too — the score understates a real duplicate

`Approval SLA & Workload Monitor` scored **0.38** against a built screen of precisely that name, because a short title shares few terms however identical it is. TF-IDF ranks a shortlist; it does not find the certainties.

The 19 September run: **0 pairs scored ≥ 0.40, and 16 collided on an exact title.** Ten of the sixteen were one board — F&B board 2, already built in full as `EMP-051`–`EMP-060`, same titles in the same order. **A whole board can already exist and the score will never say so.**

### The score says two screens are alike. It does not say which should survive.

**This is the finding that cost the most to see, and nothing in the tooling carries it.** Of the 38 pairs scoring 0.25–0.40 on 19 September, **none should be collapsed**, and eight say the opposite of what they look like.

Eight pointed at screens sourced from `Game_and_Ride_Module.pdf`, six of which have **zero components and zero operations**. `BO-417 Top-Up Configuration` is one line of purpose and nothing else. The pack screen matched against it — `Top-Up Rule Configuration` — is backed by:

- **MoM §4.5** (27 Aug, rank 1), which names nine distinct funding screens and calls the recurring schedule *"distinct from auto-reload"*
- **Matrix 4.3.28–4.3.35** (rank 2) — a `Wallet` sub-domain of 33 requirements
- the pack's own board 2, which is those nine screens one for one

**Collapsing on the score would have folded the MoM-backed, matrix-traceable screen into an empty stub from an unrelated pack.**

The cause is structural: **an earlier pack described a domain incidentally, and its screens were built first.** Game & Ride board 3 is titled *Wallet & Credit* and restates the wallet module in gaming terms; all 19 wallet screens on P08 came from it, before the wallet module itself was ever parsed.

**So before collapsing anything, read both sides:**

| ask | why |
|---|---|
| **What is the built screen's `source.pack`?** | A screen from a pack about something else is a weaker claim on the domain than a screen from the pack about it |
| **How much of it exists** — components, operations? | Zero components is an unbuilt stub, not a screen that covers the ground |
| **What do the MoMs say?** | Rank 1. A workshop dedicated to the domain outranks a paragraph in a workshop about its neighbour |
| **What does the matrix say?** | Rank 2. A sub-domain with its own requirement block is the contracted shape |

**Where the pack is the better source, the collapse runs the other way** — and that is a decision for a person, not a table.

A further trap: `COLLAPSED` is keyed **`(pack, number, page)`**, not `(pack, board, number)`. A wrong-shaped key does not fail. It never matches, the collapse silently does not happen, and the count comes out short — ten short, on 19 September, caught only by checking the number rather than the exit code.

## 3 — Placement

| | |
|---|---|
| Tool | `tools/derive-pack-screens.py --apply` |
| Writes | `screens/P*.yaml`, `docs/active/workshop-contract-gap.md` |

Each module needs `(platform, licensed module, nav section)` in `PLACEMENT`. **`ModuleKey` in `subscription.yaml` is the licensed-module vocabulary** — one list for what a tenant buys and what a screen belongs to.

**Placement is a product decision and is argued in a comment, not just written.** A module can split by board, and two of the 9 September books do.

**Cross-check it.** `sources/packs-index.json` derives platforms independently from the contracts — `pack → operation citation → x-ticvai-consumed-by → platform`. It agrees with all 23 hand placements including the splits, so where it fires it is evidence. It cannot fire for a pack nothing has been drafted from.

**It adds, it does not rebuild.** A pack entry a screen already claims is skipped.

## 4–9 — Boards, ids, wire, flows, patterns, linkage

```
tools/derive-pack-boards.py                  one board per workshop board
tools/derive-id-register.py --apply          ids are issued, never reissued
tools/applied/wire-pack-boards-<date>.py     hubs off BO-100 / ADM-002 / CMS-001
tools/derive-board-flows.py --apply          idempotent on the hub, not the filename
tools/generate-screens-from-pack.py --module <x>    patterns, regions, gaps; --only for a repair
tools/derive-pack-linkage.py                 entity x verb -> operations
```

**Wiring gets a dated sibling, never a re-run.** An `applied/` tool records what was done on a day.
Re-running an older one over a different screen set promotes different hubs and writes edges nobody
decided — and the 11 September tool's collapse path is a one-off that already ran.

**Do not name the packs in a literal.** The 11 September sibling listed its four packs by hand; on
19 September there were 36, and a hand-written list is exactly what silently omits one. **Select
every pack that still holds a screen with no `entryFrom`** — self-limiting, and idempotent anyway.

**19 September, for scale:** 798 screens placed, 798 wired, 86 flows written and 109 skipped. `P08`
went 614 → 1,182 and `P09` 446 → 676, taking the package to **2,427 screens**. Screens with no
`entryFrom` fell from 851 to 90.

**None of this invents operations.** A generated screen declares `apis: []`. The 1,924 pack screens imply roughly three thousand endpoints against the ~1,032 that exist, and *authoring three thousand endpoints from a PDF is not derivation, it is fabricating an API surface.* The gap is written out as named operations instead.

### 9b — Before authoring anything, scope the pack

**The gap list is not a work list.** On 19 September it proposed ~1,300 operations; roughly 260
were actually needed. The rest existed already, usually under a better name.

```
tools/check-contract-split.py                 is an unused half a missing join, or drift?
tools/scope-pack-to-contracts.py <pack>       per board: join, author, or mixed
```

**The recurring shape is not a missing domain — it is an operation acting without the rule that
governs it.** `mergeGuests` merged and nothing said which records were duplicates. `createSeatBlock`
took seats out of sale and nothing said when they come back. `registerDevice` created a row and
nothing turned it into a device you could trust. Look for the rule before authoring the verb.

**A pack with fewer than five wired screens has no reliable contract attribution.** `audit-contracts`
assigns a pack to whichever contract its wired screens name most, so one stray reference decides.
That is how `orders` came to show 178 unserved screens it did not own — Wallet's 99 and Payment's 79,
one reference each.

**Check every operation you are about to reference actually exists**, before applying:

```
python - <<'PY'
import io, glob, re
have = set()
for f in glob.glob('contracts/*/*.yaml'):
    have |= set(re.findall(r'^\s*operationId:\s*(\S+)', io.open(f, encoding='utf8').read(), re.M))
src = io.open('tools/applied/<your-wiring>.py', encoding='utf8').read()
print(sorted(set(re.findall(r"\('(\w+)',\s*(?:[A-Z]|')", src)) - have))
PY
```

Ten invented references were caught this way across four wiring runs on 19 September — every one a
plausible guess at a name in a contract nobody had opened.

### 9c — Adding to a contract

```
tools/splice-contract.py <contract.yaml> <paths.yaml> <schemas.yaml>
```

**Never append paths by hand, and never by "everything before `schemas:`".** Two failures, both
silent, both on 19 September:

- A duplicate path key produces valid YAML in which the later mapping **replaces** the earlier one.
  Splicing `/resource-bookings:` when it already existed took `bookResource` with it. The checker
  then reported *"screen WEB-031 calls 'bookResource', which does not exist"* — three steps from the
  cause.
- `schemas:` is not always the first key under `components:`. `approvals.yaml` opens with
  `securitySchemes:`, so appending before `schemas:` appends *inside* `components:`. Thirteen
  operations vanished from `paths`, every reference still resolved, and the tool reported **clean**.

The splice now refuses on a collision and **verifies each new `operationId` is present in the parsed
`paths`** — presence in the document, not the file looking plausible. Same principle as the intake
trap: verify by path.

> **The blast radius of a contract edit is its own runbook:**
> [`docs/contract-change-runbook.md`](contract-change-runbook.md). It carries the four rings a
> change travels through and, in ring 4, **the nine authored files that look derived, are read by
> the pipeline and the viewer, and that no tool in `tools/` rebuilds** — chief among them
> `handoff/service-decomposition.json`, still describing 28 contracts and 378 tables when there
> are now 32 and 556.

## 10–12 — Refresh, design, checks

```
bash tools/refresh.sh
tools/export-design-batch.py
```

**`refresh.sh` does not run `derive-services.py --apply`, `generate-screens-from-pack.py`, or the one-off `applied/` tools.** Run those by hand.

### One export, one queue — and it comes after generation

**`QUEUE.md` is a numbered running order** — *"never skip, never reorder, never choose your own"* —
and batches are ~10 screens each. **Cutting batches before the screen set is final means re-cutting
them.** Placing 798 screens after a batch export would have added ~82 new batches to `P08` and
`P09`, forced the 28 existing ones to be re-cut because their membership changed, and renumbered
the queue underneath whatever had already been built.

Placement does **not** cause double *generation* — `derive-pack-screens.py` adds rather than
rebuilds, and the generators take `--only`. **It is the queue that only wants cutting once.**

**Baselines that must hold:**

| check | at |
|---|---|
| `check-package` | **9 errors** — 7 `release*` lineage, `p09-commercial`, `audit-2026-09-07` |
| `check-screens` · `check-flows` · `check-migrations` · `check-wireframes` | **PASS** |

**Two rules `check-package` enforces that catch a careless edit every time:**

- **An ADR citing an amended ADR must say so within one line of the citation**, and the match is
  **case-sensitive on the lowercase word**. A `**Amends:**` header does not satisfy it. This is
  CF-97's rule — ADR-0001 once read *"Accepted — split rule superseded by ADR-0014"*, a reader took
  the first word, and built a cross-tenant isolation defect on it.
- **Mirrors drift the moment a root file changes.** Six `repos/*/project-bible` copies go stale
  together; `tools/derive-mirrors.py` puts them back. Six of the errors on any run straight after
  an edit are this and nothing else.

**A YAML description is a quoted scalar.** Writing `The RFP's` into one breaks the file — the
apostrophe has to be doubled. `check-screens` catches it as a parser error, not as a content
problem, so read the traceback rather than the summary line.

Anything above the baseline is ours and gets fixed before the next cluster.

---

## Environment

| | |
|---|---|
| Python | `/c/Users/Chinmay.Parab/AppData/Local/Programs/Python/Python39/python.exe` — **`python3` is the Microsoft Store stub and exits 0** |
| Encoding | `PYTHONIOENCODING=utf8`, and `io.open(..., encoding='utf8')` for JSON |
| Not available | LibreOffice · pandoc · `pdftoppm` · `grep -P` |
| Binaries | `.gitattributes` marks them; without it `core.autocrlf` rewrites PDFs on checkout |

## Screen ids

`^[A-Z]{2,3}-[0-9]{3,4}$` — widened to four digits on 19 September when P08 passed 999.

**Splitting a platform does not fix the ceiling.** The over-999 ids are spread by allocation order, not by module: when P08 hit 1,198, 102 of the 199 failures sat in `Orders & Money` and 97 in `Access & Venue`, so moving one group out left the other failing. **The ceiling is the pattern; a split is a navigation decision that stands on its own.**

Four tools repeat the digit count — `check-screens`, `check-board-flows`, `check-wireframes`, `derive-board-flows`. Widen all of them together, or a checker silently reads `BO-1042` as `BO-104`.
