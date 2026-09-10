# Handoff — TICVAI wireframe boards

**8 September 2026.** Everything drawn and everything found, as of today.

```
handoff/
  HANDOFF.md      this file
  boards/         23 boards + their data files. Open any .dc.html in a browser.
  notes/          the written record — plan, patches, reviews
  screens/        the source YAMLs, copied as-is from atlas/ticvai/screens (unpatched)
```

Boards are self-contained HTML — no build step, no server. Keep `boards/` intact: each board
loads `support.js` and its data file from the same folder.

---

## Read these first

| File | What it is |
|---|---|
| `notes/build-plan.md` | Current state and what is left. Start here. |
| `notes/atlas-handoff.md` | The repo-facing file — the YAML edits with exact patches, for `atlas/ticvai/`. |
| `notes/ops-review-2026-09-08.md` | Operations review across all 1,091 screens. Answers the `publishGate` decision. |
| `notes/phase4-patch.md` | Per-file apply checklist for the YAML edits. |

Also in `notes/`: `audit-2026-09-07.md`, `decisions-2026-09-07.md`, `p09-ops.md` (superseded by
the 8 September re-run), `p10-ops.md`.

---

## Tracking and management boards

| Board | What it tracks |
|---|---|
| `TICVAI Board Index.dc.html` | Top-level ledger — drawn vs left, per module and platform, superseded frames, pattern rollup. |
| `P08 Assembly Board.dc.html` | All 363 P08 screens in five module sections, each routed to the frame it reuses. 362 routed; BO-235 pending. |
| `Pattern Boards.dc.html` | The 43 layout patterns behind the generated screens, with frame coverage. |
| `Stray Screens Board.dc.html` | Screens outside any module set, or whose declared home does not hold up. |
| `Queue and Resources Board.dc.html` | The queue cluster drawn as integration, and the three resource screens with the written gap. |
| `Vocabulary Corrections.dc.html` | The component-vocabulary defects and their patch blocks, with reasoning. |

## Screen boards

Guest App · Guest Web · TICVAI Web · Venue POS · Venue Scanner · Venue CMS · Venue Analytics ·
Venue Support · Venue Staff App 1–3 · Partner Web · Developer Portal · Kitchen Display ·
Accreditation · Dashboards Board 2.

## Data

`board-data.js` · `p08-data.js` · `pattern-data.js` — the boards read these; edit the data, not
the markup. `support.js` is the runtime and is generated; do not hand-edit.

---

## Where the numbers stand

- **655 screens on boards that open** — 292 from the first pass, 363 assembled on P08.
- **43 patterns, every one with a frame.** The pattern gap is closed.
- **1,091 screens across 15 platform files** in the package.
- **362 of 363** P08 screens routed to a frame.

## What is outstanding

1. **The five YAML edits** in `notes/atlas-handoff.md` §2 — not applied to `screens/` or to the repo.
2. **The `publishGate` decision** — recommendation is warn, operation-keyed, BO-153 and BO-094
   only. `notes/ops-review-2026-09-08.md` §5.
3. **Regenerate** `pattern-data.js` and the frame inventory after the edits. If any number on the
   index moves, an edit did not land.
4. **Two CI checks** — check one can ship enforcing on ten of the fifteen platforms today.
5. **Nine contract gaps** — BO-233, CMS-033 and the six title-only publish screens.
6. `board-data.js` references `Marketing Board 1.dc.html`, which was never built.

## Known caveats

- `BO-006 Parking Configuration` is deliberately undrawn — its own open question asks whether
  parking is barrier integration, space counting or pre-booking. Three different screens.
- The 96 command centres are parked on one decision.
- `seatp` and `crm` — 250 screens drawn, no package counterpart. A package gap, recorded in
  `notes/decisions-2026-09-07.md`.
- `screens/` is a read-only copy taken 8 September. The repo is the source of truth.
