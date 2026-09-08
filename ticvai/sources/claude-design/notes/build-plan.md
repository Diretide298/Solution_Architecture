# Build plan

**8 September 2026.** Supersedes the 7 September plan, which ordered Phase 4 → 1 → 2 → 3.
Phases 1 and 2 are drawn, Phase 4 is drawn but not applied to the source. What follows is
what is left.

Where we are: **655 screens on board files that open** — 292 from the original pass, 363
assembled on P08. The pattern gap is closed: 43 patterns, every one with a frame. 362 of
P08's 363 screens are routed to the frame they reuse; BO-235 waits on its re-signature.

---

## Done

**Phase 1 — the 17 leftover screens.** `Queue and Resources Board.dc.html` carries the queue
cluster drawn as integration rather than implementation, and the three resource screens with
the written gap naming what the other screens would be. `Stray Screens Board.dc.html` carries
the eight one-offs. Pattern gap closed, 44 → 43.

**Phase 2 — P08.** `P08 Assembly Board.dc.html`, 363 screens in five module sections, each
routed by `frameKey` (file + anchor) held separately from its display label so stored mislabel
markers cannot drift from rendered flags. The parse corrected the inventory the plan was
written from: **Access & Venue is 175, not 114; Orders & Money is 59, not 15; the BP-010 fold
is 20 screens, not 17.** Half of P08 runs on BP-001. 127 screens carry generated empty states.

**Phase 4, board side.** `Vocabulary Corrections.dc.html` carries the reasoning and the patch
blocks. Three corrections came out of the parse: 17 mislabelled frames, not 19; BO-020 does
declare a layout; `scanTarget` appears on five screens, of which three are correct — back
office reports *about* scans, not scanners.

---

## Phase A — Land Phase 4 on the source

The only phase half-done, and the reason every count above is still a board-side assertion
the repo cannot confirm. Patch blocks and order are in `notes/phase4-patch.md`; the repo-facing
version with exact patches is `notes/atlas-handoff.md`.

**The decision is answered, pending your sign-off.** `publishGate`'s `requiredWhen` fires on
**45 screens**, not eight: 34 real gates, none of which declares the component, and 11 where
`release` means *let go of a hold*. Recommendation: **ship it warning**, key `requiredWhen` off the
declared operation rather than the screen's subject, and declare it on **BO-153 and BO-094 only** —
the two screens with a real publish operation. Working in `notes/ops-review-2026-09-08.md` §5.

**Phase A gained a step.** Six of the seven screens the patch adds `publishGate` to — BO-173,
BO-193, BO-213, BO-223, BO-343, ADM-227 — declare a single `list…` and no publish operation. The
list was read off their titles. They join BO-233 and CMS-033 as contract gaps: nine screens, not
two.

Then five files, vocabulary first so the screen edits validate:

1. `_components.yaml` — add `publishGate`, add `emptyNoEvents`
2. `P08-venue-back-office.yaml` — BP-010 fold (20 screens), three venue-map layouts, six
   `publishGate`, three audit-trail state swaps, BO-235 re-signature
3. `P09-platform-admin-console.yaml` — three re-signatures, ADM-227 gate, four `emptyNoEvents`
4. `P12-support-agent-console.yaml` — SUP-011
5. `P13-white-label-cms.yaml` — CMS-044 re-signature, three `emptyNoEvents`

**Then regenerate** `pattern-data.js` and the derived frame inventory. The boards already read
43 patterns and BP-001 at 331, so a correct regeneration moves no number on the index. If a
number moves, one of the edits did not land.

**Then close BO-235** on the assembly board — P08 goes 363 of 363.

---

## Phase B — Operations review, re-run · done 8 September

`notes/ops-review-2026-09-08.md`. All 1,091 screens in 15 platform files, parsed from
`apis[].operationId` as declared.

**The cell block holds and grew: eight screens, not six** — ADM-003 and ADM-029 carry the full
seven too. All eight can decommission a cell, including the WAF policy view, the backup status
page and the archival job monitor. But it is **not a pattern**: only ADM-013 declares the seven
and nothing else, and across all 318 screens there is exactly one other identical repeated
operation set (ADM-022 / ADM-023, the seven release operations, one a `form` and one a
`wizard`). It is a base stamped onto anything infrastructure-shaped — an eight-screen defect,
fixed by removing `decommissionCell` and `cancelDecommission` from the six screens that only
observe.

**The reviewed 37 and the unreviewed 281 are different populations.** P09's declarations are 110
catalogue and 100 promotions; the first review reached almost none of that. Its findings should
not be read as a sample.

**P08 has its own version, previously unrecorded.** Five repeated identical operation sets across
14 screens, in the modules where money is counted: BO-039/040/041/042 each declare the full
thirteen-operation shift block, BO-022/026/047 each declare the full fourteen-operation order
block including refunds, BO-029/059/061 each declare the nine report operations. Four screens can
each close a shift.

**BO-092, BO-093 and BO-094 still have no `template` key** — Phase A's item 2.4 confirmed
unapplied from the source side.

---

## Phase C — The two CI checks

Once the source is clean, these are what stop the generator default from quietly rebuilding
the defects Phase A just fixed:

1. A screen whose only operation is `list…` cannot claim a verb in its title.
2. An unauthored layout fails rather than defaults.

**Check one is sized and can ship today.** 360 of 1,091 screens declare exactly one operation and
it is `list` + the screen's own title camel-cased: P09 55%, P08 38%, P10 37%, P13 35%, P12 29% —
and **zero across the other ten platforms**. The stamp is a property of five files, not of the
package, so ship it *enforcing* on P01, P02, P04–P07, P11, P14–P16 immediately and warning on the
five until re-signature. A check that can only warn everywhere is a check nobody fixes.

The default outlived the whole pass: all 23 BP-006 screens carried one stamped layout and the
same generator wrote the other 793. Operation names are the titles camel-cased, so the API and
the layout agreeing means nothing.

---

## Parked, and why

- **The 96 command centres** — one decision. Drawing them before it is answered is the single
  largest way to waste effort on this project.
- **`seatp` and `crm`** — 250 screens drawn, no package counterpart. Raised as a package gap
  in `notes/decisions-2026-09-07.md`. Not ours to draw over.
- **Two contract gaps** — BO-233 is a shift handover whose only operation is
  `listShiftHandoverSummary`; CMS-033 manages withdrawals with only
  `listConsentEvidenceWithdrawal`. The screens their titles promise cannot be built from what
  they declare. Missing operations, not layout defects — raise against the contracts.
- **`graphFinding`** — BO-094 carries two findings (unreachable point, step-only route) with no
  component to declare them. Does not answer `CF-146`; raise separately.
- **`Marketing Board 1.dc.html`** — referenced by `board-data.js`, never built. Build or drop
  the reference.
