# Ingesting a design pack — the audit, in order

**Written 26 August**, after three packs (F&B, POS, Retail), 160 frames and 64 screens. **Every
step below exists because something got past the one before it.**

---

## Before anything: run the suite and write the numbers down

```bash
bash tools/refresh.sh
```

**Record all nine warning totals, not PASS/FAIL.** A revert does not break the package, it
*un-fixes* it — `check-wireframes` went 13 → 32 on one and every checker still said PASS. **The
warning total is the only signal that failure mode produces.**

---

## 1 · Install the board and confirm the anchors

Drop the `.dc.html` into `wireframes/`.

**Every frame needs `id="<anchor>"` and every screen citing it needs `wireframe.board:
wireframes/<file>#<anchor>`.** `check-wireframes` tests both directions — a link to an anchor the
board lacks is a click that silently does nothing, **and a board nothing points at is 733 KB of
superseded content that opens by name and looks authoritative.**

**Two traps here, both hit:**

**`boardFrames` is a reference too.** Four packs read as orphans while 35 of their frames were
claimed through `boardFrames` — the join existed and the check read the other direction.

**`wireframe.status` describes the file, not the provenance.** P15 and P16 said `designed` while
pointing at boards this package generates. **`derivedFrom` is where the pack frame goes.**

---

## 2 · Map every operation the board names

Every button and panel on a frame implies an operation. **Three outcomes and all three are normal:**

| | |
|---|---|
| **Exists** | Nothing to do |
| **Aliased** | The client names the act, the contract names the artefact — `board-operation-aliases.json`, 358 entries |
| **Panel-mapped** | A read panel served by filtering an existing operation — `board-panel-map.json` |
| **Absent** | A real gap. Build it, or record why not |

**Zero unaccounted is the bar.** The F&B pack was 210 operations: 74 existing, 37 aliased, 99
panel-mapped, 0 absent.

**A read panel is not a new endpoint.** *Board panels are not endpoints* — several panels are often
one operation with filters, and treating each as an endpoint is how a contract doubles.

---

## 3 · Assign the frames to screens, by hand

**Three derivation attempts failed.** Matching on shared operations produced *Outlet Management →
Kitchen Operations Command Centre* on one shared operation.

**Assign by board purpose.** And expect concentration: **`BO-044` owns eighteen frames** — nine F&B
and nine Retail — because configuring an outlet and configuring a store are the same screen under a
different licence. **That is the module system working**, and it means "64 drawn" overstates the
coverage: a third of drawn frames land on six screens.

---

## 4 · Then run every checker, and read what moved

```bash
bash tools/refresh.sh
```

**Nine validators. What each one is actually for:**

**`check-screens`** — the biggest, and where a pack lands hardest. Operation existence, cold entry,
empty states, cross-module calls, **audience match** (a guest surface calling staff operations —
22 found), **offline claims** (prose against operation flags — 37 found), **empty regions that say
nothing about being empty**.

**`check-wireframes`** — anchors both ways, orphan boards, `status` against the file it points at.

**`check-flows`** — steps resolve, navigation exists, wave ordering, `crossesDevice` on handovers.

**`check-states`** — every status enum has a model, no unreachable states, no transition out of a
terminal one, **every transition names an operation**.

**`check-package`** — 34 rules. `$ref` resolution, duplicate YAML keys, derived-table writes,
currency scope, unbounded lists, orphan writes, diagram staleness, **relationship columns**.

**`check-config-scope`** — a path naming an outlet configures at that outlet, and **an operation the
naming rules do not reach reports itself** rather than being silently exempt.

**`check-frontend`, `check-backlog`, `check-traceability`** — app manifests, backlog integrity,
requirement coverage.

---

## 5 · Walk a flow through the new screens

**This is the step that finds what no checker can**, and it has never failed to find something:

| Flow | Found |
|---|---|
| F28 food safety | HACCP absent from 947 operations |
| F31 menu lifecycle | **A published menu reached no till** — no P04 screen polled the bundle |
| F32 till day | Readiness check ordered after the float |
| F33 offline | Two screens at wave 2 while offline trading is wave 1 |
| F58 ticket sale | **A till could author the catalogue** — 12 operations |
| F61 gate | A scanner could create access points; sign-in resolved no role |

**A screen with too many operations validates cleanly. Only a journey notices.**

---

## 6 · Run the link audit

```bash
python3 tools/audit-links.py --detail
```

**Nine directions, and a non-zero count is a link a reader can follow into nothing.** It runs inside
`refresh.sh` as the tenth check, but run it with `--detail` after a pack because that is when it
fires.

**`screen -> board anchor` is the one a pack breaks.** It checks two claims per screen — the board
file exists, and the anchor exists inside it — plus every `boardFrames` entry against every board on
disk.

**156 broke on 31 August and all 156 were case drift**: `boardFrames` held `POS-2A` where the board
anchored on `pos-2b`. **`check-wireframes` did not see them** because it only reads
`wireframe.board`, not `boardFrames`, and the frames had been recorded from a pack that uppercased
its labels.

**The audit also reports reach, which is not integrity.** A link that resolves is not the same as a
link that exists: `screens with no board` counts screens nobody has pointed anywhere, and
`screens drawn` separates a client drawing from a generated one.

---

## 7 · Regenerate and diff the counts

`refresh.sh` writes `handoff/status.json` — eleven counts. **A count that moved when you did not
expect it to is the signal.**

---

# The audits added since the packs landed

**Each one is a join nothing was checking.** That is the pattern: **the package validated each
artefact against its own schema and each reference against its target, and never one artefact's
claim against another artefact's fact.**

| Audit | What it compares | Found |
|---|---|---|
| **Platform audience** | Screen's platform audience vs. operation's declared audience | 22 — a guest login calling staff MFA |
| **Offline claim** | A screen's offline *prose* vs. its operations' *flags* | 37 claiming they keep working with nothing offline-capable |
| **Unbounded list** | `list*` operations vs. the size of the table behind them | 27 over `orders`, `marketing`, `access`, `ledger` |
| **Orphan write** | Tables written vs. tables read, parent-aware | 21 features that half-exist |
| **`$ref` resolution** | Every reference vs. its target, both files | 11 broken by one edit, found by a person |
| **Currency scope** | Stored currency vs. what the region already decides | 4 tables storing a fact that cannot differ |
| **Relationship column** | `col` vs. the table's actual columns | 185 holding an operation name |
| **Config scope path** | `x-ticvai-config-scope` vs. the path's own parameters | 4 saying `venue` on `/outlets/{outletId}` |
| **Naming-gate escape** | Operations carrying a tag the rules never examine | 24 unexamined, including two cited as correct |
| **Diagram staleness** | Diagram mtime vs. its source | Fails a package where `refresh.sh` was not run |
| **Board orphan** | Boards on disk vs. anything pointing at them | P15 and P16 shipped correctly anchored and unreachable |
| **`status` vs. board** | `wireframe.status` vs. the file it points at | 20 claiming a client drew a generated board |
| **Duplicate YAML key** | A key defined twice — **YAML keeps the last silently** | 80 in one file, twice, from a `safe_dump` round-trip |
| **Empty region** | A declared region with nothing in it *and no note* | 2, both correct, both now saying so |
| **Cross-surface parity** | Two guest surfaces sharing a screen name vs. the operations each calls | 13 — `Loyalty & Rewards` shared **zero of nine** |
| **Placeholder group** | `module` against a list of placeholder words | **124** reading `TODO`, including 59 of 63 on P02 |
| **Unrecognised board** | Files in `wireframes/` vs. what the manifest accounts for | 17 — a consumer counted **811 frames against a real 359** |
| **Anchor collision** | An anchor appearing on more than one board | 22 — Claude Design adopted our screen ids as frame ids |
| **`boardFrames` resolution** | Every claimed frame vs. every board on disk | 156 stale, all case drift `check-wireframes` could not see |

---

## What the manifest is for

**`wireframes/manifest.json` has three categories and a consumer can act on each:**

**`generated`** — boards this package writes. **`refresh.sh` deletes any it no longer generates**,
which is what stops a rename leaving a ghost. **`P08 Staff Web Back Office.dc.html` outlived its
replacement by six days** at 733 KB against 383 KB, opening by name with nothing to say it was
superseded.

**`clientPacks`** — drawn boards, matched by a known pack prefix. **Never touched by any tool here**:
the generator did not write them and has no business removing somebody else's work.

**`unrecognised`** — everything else. **This is the category that did not exist and needed to.** A
board from another product and a board superseded by a rename both used to answer *not generated*,
which is the same answer for a file that belongs and a file that does not.

**Count from the manifest, not from the folder.** A folder is what a copy-based transfer has
accumulated; the manifest is what the package can account for.

---

## Two things worth knowing before you add another

**A check that measures the easy thing next to the real thing passes vacuously.** A patcher asserted
insertions and not insertions *in the right place*, and passed a broken edit. A hover harness
couldn't reach controls in a closed view, left the previous tip in the panel, and read every element
after the first as a pass. **Both were caught by a second measurement disagreeing, never by the
check itself.**

**A tool copied out of the package tests an empty package.** Every path here is anchored on the
script's own location, so a copy in `/tmp` resolves `ROOT` to `/`, finds no `wireframes/`, prints
*no wireframes directory* and returns zero. **I lost several rounds to probes that were silent
because they were correct about the wrong folder.**

**A number typed once is correct once.** `platform-P01.md` said 35 against a live 46. The viewer said
654 operations against 1,023, in 25 places. `platform-deployment.md` had twelve rows against fifteen
platforms. **All three are now derived, and that is the only fix that holds.**
