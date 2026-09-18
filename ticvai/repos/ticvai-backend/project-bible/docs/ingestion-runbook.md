# Ingestion runbook — client packs into the package

> **Read this before ingesting anything.** It is the order, not a summary of one. Every step exists
> because skipping it cost something, and the cost is named against each.
>
> **Owner:** Chinmay · **Last run:** 19 September 2026 · **Status:** authoritative

---

## The order

```
0  intake        zip -> sources/, dedupe, authority, platform
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
11 design        export the batches
12 checks        eighteen checkers
```

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
| Tool | `tools/index-packs.py` |
| Writes | `sources/packs-index.json` |

Hash every client document, group by content, record what its folder used to assert. **`sources/README.md` ranks folders by authority** — a file in `requirements/` is contracted scope and the identical file in `packs/` is reference material — so a document held twice is holding two claims that nothing keeps in sync.

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
tools/derive-id-register.py --apply          ids are issued, never reissued
tools/applied/wire-pack-boards-*.py          hubs off BO-100 / ADM-002 / CMS-001
tools/derive-board-flows.py --apply          idempotent on the hub, not the filename
tools/generate-screens-from-pack.py --module <x>    patterns, regions, gaps; --only for a repair
tools/derive-pack-linkage.py                 entity x verb -> operations
```

**None of this invents operations.** A generated screen declares `apis: []`. The 1,924 pack screens imply roughly three thousand endpoints against the ~1,032 that exist, and *authoring three thousand endpoints from a PDF is not derivation, it is fabricating an API surface.* The gap is written out as named operations instead.

## 10–12 — Refresh, design, checks

```
bash tools/refresh.sh
tools/export-design-batch.py
```

**`refresh.sh` does not run `derive-services.py --apply`, `generate-screens-from-pack.py`, or the one-off `applied/` tools.** Run those by hand.

**Baselines that must hold:**

| check | at |
|---|---|
| `check-package` | **9 errors** — 7 `release*` lineage, `p09-commercial`, `audit-2026-09-07` |
| `check-screens` · `check-flows` · `check-migrations` · `check-wireframes` | **PASS** |

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
