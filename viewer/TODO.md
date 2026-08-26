# Viewer — work index

**Rewritten 26 August from the source, not from the previous index.**

Every open row below was checked against the code or the package on the day it
was written. Ten did not survive that: four described work already finished, two
quoted counts that had grown by 40-80%, and **every line-number anchor in the
file pointed at unrelated code** — `app.js:4157` had become 5172, `5409` had
become 9683, and V-29's three anchors matched nothing at all.

So the rules changed with the rewrite:

**No line numbers.** A function name survives an edit; a line number is wrong by
the next one, and it is worse than nothing because it reads as precision.

**No counts that live somewhere else.** If a number can be derived, say where
from and let the reader run it. Quoting it here is the same bug the viewer's own
tooltips had — see V-29, which was exactly this, one level down.

**Ids resolve here and nowhere else.** The old header called this file
*generated from `PLAN.md`*. There is no generator, and `PLAN.md` contains no
V-numbers — it is organised by prose sections. The two cannot be
cross-referenced, so read `PLAN.md` for reasoning and treat these ids as local
labels.

| State | Count |
|---|---|
| BLOCKED — needs your decision | **3** |
| OPEN — with the package side | **3** |
| OPEN — reviewer experience | **3** |
| OPEN — correctness | **2** |
| OPEN — polish | **5** |
| DONE | **27** |

**Nothing is blocking.**

---

## Blocked — needs a decision from you — 3

| ID | Item | Why it is stuck |
|---|---|---|
| **V-03** | Name the reviewer checklist criteria | I can build it; I cannot invent what it should ask. Gates the wording half of V-15 |
| **V-04** | Change the first administrator's password | Only you can. It was committed to a public repo. **Separately**: `harness.admin@softlabsgroup.com` / `a-long-enough-passphrase` is now public in `checks/*.mjs`. It does *not* authenticate against the live instance, so it is inert — but do not create that account there |
| **V-24** | Stop the second accounts API on 8788 | `python -m uvicorn api.main:app --port 8788`, pid 13208, started 11:43 on 26 August. A **full second copy of the accounts API** — same routes, same 401 on a bogus login — and its command line sets no `TICVAI_DB`, so it defaults to the real `api/ticvai.db`. `demo.db` no longer exists, so that half of the old row is already done. Stopping a process is denied to me: `Stop-Process -Id 13208 -Force` |

## Open — with the package side — 3

Raised from the viewer, fixed in the package. Listed here so they are not lost.

| ID | Item |
|---|---|
| **V-36** | **The workbook's `Scaling` sheet lost every contract row.** Commit `d200412` carried 25 contracts and 776 routed operations; the 26 August dump has one row reading `TOTAL 0 0 0 0`. Backend › Routing therefore draws nothing, and `pages-check` is 52/1 because of it. The routing data itself is intact — the lineage still carries the replica/primary/analytical split — so this is the sheet's generator, not the source. **No package validator reads this sheet**, which is why all ten still pass |
| **V-27** | **The UTF-8 stdout guard is missing from 27 of 33 tools**, not the single file the old row named. The failure lands *after* the work: output is written, then the summary line dies on `UnicodeEncodeError` and a correct run exits 1. It only shows on a cp1252 console, so a piped or CI run never sees it. `derive-wireframes.py` and the two tools added on 26 August carry the guard; nothing was retrofitted. Ready-to-run, dry-run first: `scratchpad/apply-utf8-guard.py` |
| **V-30 / V-33** | Dashboards, and `relationships.csv` columns — **taken by the package side.** Both rows were stale here: six dashboards is eight, and 143-of-514 is 185-of-914 |

## Open — reviewer experience — 3

| ID | Item |
|---|---|
| **V-15** | Verdict dot per tree row, progress per group, `All / Untouched / Needs work / Mine` filter. **The biggest single gap** — the tree draws every reviewable artefact as an identical row, so a reviewer cannot see their own progress. Only the checklist wording waits on V-03; the dots and the filter do not |
| **V-16** | Keyboard navigation for the review loop — `]` `[`, `n` for next unreviewed, `1` `2` `3` in a verdict form, `Ctrl+Enter`. Cheap once V-15 gives a row a state to show. Arrow-key panning and `+`/`-` on the diagrams already landed |
| **V-17** | Pin the verdict bar to the foot of the reader. The LINKS rail half of this row is partly answered by V-11 — re-scope before starting |

## Open — correctness — 2

| ID | Item |
|---|---|
| **V-37** | **Eight harnesses hardcode `4173`/`8787`** and ignore `TICVAI_VIEWER`/`TICVAI_API`: `ai-tables`, `contract-trace`, `lens`, `scroll`, `signoff`, `tree-fold`, `verdict-submit`, `_shot`. They can only run against the instance backed by the real account database. **`signoff-check` is the one that matters** — its own README says it records real verdicts. `pages-check`, `paging-check`, `links-rail-check` and `tip-facts-check` are parameterised and are the pattern to copy |
| **V-38** | `paging-check` fails 2 against the current package — *"the reader shows prose the index no longer carries — proposeTranslations"*, and the Lineage view drawing no group to page through. Both surfaced once the harness could run at all. Neither is diagnosed |

## Open — polish — 5

| ID | Item |
|---|---|
| **V-18** | Journey: a fade or chevron on the right edge. There is no Fit to add — the sideways track is deliberate |
| **V-20** | Structure: the empty state draws a legend for a diagram that is not there |
| **V-21** | Unexplained tree counts, `status` as a chip, no breadcrumb, orphaned history notes, permanent sidebar note |
| **V-31** | Domain lenses beyond AI — `finance`, `identity`, `access`. `domains.html`/`.js`/`.css` and `lib/domains.mjs` all exist and render, so this is a seed each rather than a build |
| **V-32** | ER: legibility floor, toolbar reserve, edge cardinality, fold in the hint text |

**Dropped rather than done.** `V-23` was never a bug — the States zoom cap of `1.1` is deliberate and commented. `V-25` asked whether two root tools should be kept or deleted; both now live in `ticvai/tools/`, so the question answered itself. `V-02` wanted a commit split that a fresh history made moot.

## Done — 27

| ID | Item |
|---|---|
| **V-01** | Commit and push everything. `atlas` initialised, 6,917 files, **no database staged** — `.gitignore` excludes `api/*.db` and it was verified before the push, not after. Both remotes force-pushed to `d200412` |
| **V-28** | The Domains lens page — `domains.html`, `.js`, `.css`, all present and rendering. **The row was stale, not the work** |
| **V-39** | Backend › Routing now says *which* emptiness it is. A missing sheet and a present-but-empty sheet read identically before, and the old message sent a reader looking for a sheet that was there. `lib/backend.mjs` exports `scalingSheet` |
| **V-D10** | `checks/tip-facts-check.mjs` and `checks/links-rail-check.mjs` — new. The second fails 2 on the pre-fix code, which is the only reason to trust it |
| **V-D11** | `checks/paging-check.mjs` — could only ever run against the live pair; now honours the environment, opens the project the registry names instead of the bare door, and reports an empty Lineage view rather than throwing from inside puppeteer |
| **V-29** | Stale hardcoded counts in viewer prose. Bigger than the three files named: **25 sites across 8 files**, and four separate figures — 654 operations (live **1,023**), 22 services (**16**), 18 ADRs (**30**), "318 of the 654 resolve to no table" against a lineage where **nothing is unresolved**, and Waves' "347 screens / twelve platforms / 192 name no operation" (**492 / 15 / 14**). Fixed as a class, not a list: tips write `{operations}` and `public/tips.js` substitutes at hover, so the count comes off the payload. `checks/tip-facts-check.mjs` holds it — 14 passed. `pages-check` still 53/53 |
| **V-11** | The LINKS rail leaked the previous layer. The earlier fix moved the clear ahead of the dispatch and gave each layer its own empty sentence, but left the half that carries content: `state.selectedId` is written only by `select()`, which only resolves contract artefacts, so the tail of the dispatch put **the last contract's REFERENCED BY / REFERENCES on the Decisions layer**. Reproduced in a browser, then scoped the read to Contracts rather than clearing the selection — the reader keeps their place. The theme toggle had the same leak through a second door and now re-renders through the dispatch. `checks/links-rail-check.mjs` holds it — 13 passed, and it fails 2 on the old code |
| **V-10** | Backend › Data drew every schema amber. **Already fixed before this session; the row was stale** — the anchor read `app.js:4157` and the code is at 5172. It counts `table.ddl` per module instead of reading `module.written` off a Status column the workbook does not have, and it draws three states. Verified against the package: **1 written (pii 4/4), 7 part-written, 23 with nothing** — not all amber |
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
| **V-05** | **The gate.** `lib/session.mjs` — every payload and every page behind the session, the sign-in page the one exception. `/api/index` 401s without a cookie |
| **V-06** | **Role-filtered reads.** `lib/audience.mjs` — a client reads everything except the Decisions layer. `/api/decisions` 403s, and so does `/api/file` for anything that layer serves, which is the leak that matters: an ADR is a `.md` |
| **V-07** | **The `client` role.** Off-domain by invite only, 3-day links, read-only enforced by `require_writer`. Named `client` not `guest` — the package already uses `guest` for a venue visitor. `checks/client-check.mjs` — 32 checks |
| **V-34** | **Deploy.** `deploy/` — setup.sh, three units, a backup timer, nginx on one origin. Both processes on loopback |
| **V-35** | **Decisions › Gaps read the audit three times.** `artefact-audit.md` carries the original finding, a dated position after the work and the blocked remainder; every table was read and every row pushed, so each class appeared twice — red from the first, green from the second. 27 rows → 15, 12 open → 3, and the blocked three are now a state of their own rather than dropped |
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

- **Numbering:** V-01 to V-39; done items keep their original id or carry V-D.
  Ids are local to this file — `PLAN.md` has none, so there is nothing to look
  an id up in
- **Reasoning** lives in `PLAN.md`, by prose section rather than by id. This
  file holds state, not argument
- **Anchors** are function and file names, never line numbers. The previous
  edition anchored by line and **every one of them had drifted** — which is how
  a row survived three sessions telling a reader to fix something already fixed
- **Counts** are not quoted here unless the row says where to derive them. Two
  rows in the previous edition had grown 40-80% while still stating the old
  figure. The rule the viewer's tooltips now follow applies to its work index
  too: a number written into a sentence has no reason to change when the thing
  it describes does
- **Re-verify anything more than a few commits old.** This package moves daily,
  and that warning was in the previous edition as well — it was correct, and it
  was not enough on its own
