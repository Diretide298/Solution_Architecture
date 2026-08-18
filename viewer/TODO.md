# Viewer — work index

**33 items — V-01 to V-33.**

Generated from `PLAN.md`, which holds the reasoning and the anchors. This is the
index: one line per item, so anything's state can be checked without reading it.

| State | Count |
|---|---|
| BLOCKED — needs your decision | **5** |
| IN FLIGHT — agents running | **2** |
| OPEN — security | **3** |
| OPEN — verified bugs | **3** |
| OPEN — missing views | **2** |
| OPEN — reviewer experience | **3** |
| OPEN — polish | **6** |
| DONE | **14** |

**Blocking: V-05.** No outside address can hold an account until the data server
is behind the session.

---

## Blocked — needs a decision from you — 5

| ID | Item | Why it is stuck |
|---|---|---|
| **V-01** | Commit + push everything | Asked four times. The set is now large: the promoted package, ten deleted manifests, the domain lens, the ADR and state-model parser fixes, the reviews dashboard, `/api/verdicts`, three harnesses, `PLAN.md`, this file |
| **V-02** | Split commit `d664719` | Needs a force-push to an already-pushed commit |
| **V-03** | Name the reviewer checklist criteria | I can build it; I cannot invent what it should ask |
| **V-04** | Change your password from `the-first-administrator` | Only you can. It is in a public repo |
| **V-25** | `tools/build-wireframes.py` and `tools/check-migrations.py` are at root and **not in your dump** — keep or delete? | A missing build tool reads like an export gap, not a decision |

## In flight — agents running — 2

| ID | Item | State |
|---|---|---|
| **V-27** | `tools/check-package.py` UTF-8 + `check-flows.py` warning→error and branch walk | check-flows done, check-package still running |
| **V-28** | The **Domains** lens page — `domains.html` / `.js` / `.css` | not yet written |

## Open — security — 3

| ID | Item |
|---|---|
| **V-05** | **Blocking.** Put `server.mjs` behind the session — every payload is open on 4173, and `/api/file` returns any `.yaml`/`.md`/`.json`/`.csv` in the tree |
| **V-06** | Role-filtered payloads and a gate on `/api/file`. **Unblocked.** ADR-0025 replaced the two guest markers with one `x-ticvai-audience` field across 776 operations — 96 name `guest`. There is now a single vocabulary to filter against |
| **V-07** | The `guest` role — invite-only, off-domain, read-only, enforced server-side |

## Open — verified bugs — 3

| ID | Item | Anchor |
|---|---|---|
| **V-10** | Backend › Data draws every schema amber — `module.written` reads a Modules-sheet column the workbook does not have. Count DDL per module instead; needs three states, not two | `public/app.js:4157` |
| **V-11** | The LINKS rail leaks the previous layer on every layer without a dispatch line — Contracts *and* Decisions. Clear before the dispatch, keep `pane-empty` | `public/app.js:5409` |
| **V-29** | Stale hardcoded counts in viewer prose — `decisions.mjs:5` "18 ADRs" (24), `app.js:171` "The 18 ADRs", `lineage.mjs:12` "654 operations" (776) | three files |

## Open — missing views — 2

| ID | Item |
|---|---|
| **V-30** | **No dashboard pages.** The package declares six — Platform, Cross-Tenant Health, Security & Compliance, Partner, Agent, My Account — across P01/P02/P04/P08/P09/P10/P12, and the viewer has no overview surface for any of them. Assumed to mean viewer-side; say if you meant the package's own screens |
| **V-31** | Domain lenses beyond AI — `finance`, `identity`, `access` are a one-line seed each once V-28 lands |

## Open — reviewer experience — 3

| ID | Item |
|---|---|
| **V-15** | Verdict dot per tree row, progress per group, `All / Untouched / Needs work / Mine` filter. The biggest single gap — 376 identical-looking rows |
| **V-16** | Keyboard navigation — `]` `[`, `n` for next unreviewed, `1` `2` `3` in a verdict form, `Ctrl+Enter` |
| **V-17** | Pin the verdict bar to the foot of the reader; rethink the LINKS rail |

## Open — polish — 6

| ID | Item |
|---|---|
| **V-18** | Journey: a fade or chevron on the right edge. There is no Fit to fix — the sideways track is designed |
| **V-20** | Structure: the empty state draws a legend for a diagram that is not there |
| **V-21** | Unexplained tree counts, `status` as a chip, no breadcrumb, orphaned history notes, permanent sidebar note |
| **V-23** | The States zoom cap is a judgement, not a bug — `1.1` is deliberate and commented |
| **V-32** | ER: legibility floor, toolbar reserve, edge cardinality, fold in the hint text |
| **V-33** | **Package gap, not a viewer one — and not AI-specific.** `handoff/relationships.csv` states 514 relationships, and **143 of them name a column that no row on the Columns sheet defines** — `orders` 17, `identity` 16, `marketing` 16, `ai` 14. The two sheets are generated from different sources and were never reconciled. 76 of the 287 tables have no columns at all, which is why the AI schema draws thirteen empty boxes: all 13 are declared storage-only. Ask which sheet is authoritative |

## Housekeeping — 1

| ID | Item |
|---|---|
| **V-24** | Stop the demo API on 8788 and remove `demo.db` |

## Done — 14

| ID | Item |
|---|---|
| **V-D1** | Verdict submit button reads plain `Submit`. Harness 14/14 |
| **V-D2** | All 20 layer × view combinations screenshotted and reviewed |
| **V-D3** | `PLAN.md` — reviewer UX, every view, the guest role |
| **V-D4** | Seven findings root-caused and adversarially verified, 14 agents |
| **V-D5** | Four of my own screenshot readings corrected rather than deleted |
| **V-D6** | New-dump analysis — 8 agents, 55 raw findings → **21 verified contradictions** |
| **V-08** | The ten duplicate app manifests — your dump deleted them, I completed it at root. `frontend/` is 10 |
| **V-D7** | **ADR parser whole again** — emphasis stripped before the verdict, both heading forms, inline dates, `Addendum`/`History` counted. verdict null 6→0, date null 6→0, doubled titles 9→0, amended 3→5 |
| **V-D8** | **State-model enum anchors** — reads the package's declared `enumKind`/`enumSchema`/`enumProperty`, dotted string only as fallback. **31 false errors → 0**, leaving the one real one visible |
| **V-D9** | `lib/domains.mjs` + `/api/domains` + declared-tag plumbing across operations, states, events and ADRs |
| **V-09** | Graph arrowheads — painted the background colour because `fillStyle = strokeStyle` ran after `restore()` |
| **V-13** | Lead-in paragraphs ending in `:` losing their payload — both extractors |
| **V-26** | Root `README.md` back to 776 operations — restored by the 18 August re-extraction |
| **V-19/22** | Docked legends, routing legend above the fold, red retired from meaning "primary (write)" |

---

## The package promotion, 17 August

Your fixed dump landed in `viewer/` rather than the repo root, where nothing
reads it — `server.mjs` resolves `ROOT` to the parent of `viewer/`. Ten package
directories were promoted, then the ten superseded manifests deleted, because a
copy cannot carry a deletion.

**One casualty, mine — and it has since been undone.** The dump had also
overwritten `viewer/README.md` — the viewer's own documentation — with the
package README. I restored the viewer's copy from git *before* taking the
package README out of it, so the updated package README was lost and root kept
the old one at 753 operations. **The 18 August re-extraction restored it:** root
now reads 776. V-26 is closed by the dump, not by me.

## Integrity

- **Numbering:** V-01 to V-33; done items keep their original id or carry V-D
- **Reasoning** lives in `PLAN.md`; this file holds no argument, only state
- **Anchors** were checked against the source by a second reader. Re-verify any
  that is more than a few commits old — this package moves daily
