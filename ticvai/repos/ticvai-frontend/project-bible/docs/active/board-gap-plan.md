# Closing the board gap — one board per pattern, not one per screen

**The gap is 591 screens and about 22 boards.** Those are not two estimates of the same thing: the
screens on the five affected platforms come from a generator applying a small vocabulary, so a
board drawn once serves dozens of them.

`board-plan.json` beside this file is the machine-readable version — 37 boards, each carrying the
full list of screens it covers, ready to join against Claude Design's `board-data.js`.

**Regenerate both with the snippet at the end.** Nothing here was typed by hand.

---

## Where the gap is

| Platform | Screens | Boards drawn | Gap |
|---|---:|---:|---:|
| **P09** platform admin console | 318 | 37 | **281** |
| **P08** venue back office | 363 | 143 | **220** |
| P13 white label CMS | 60 | 20 | 40 |
| P10 partner reseller portal | 51 | 21 | 30 |
| P12 support agent console | 28 | 8 | 20 |
| Ten other platforms | 271 | 271 | **0** |
| | **1,091** | **500** | **591** |

**Two platforms are 85% of it.** Every guest-facing platform — P01, P02, P05, P06 — is complete.

---

## Why 591 screens is not 591 boards

| | Screens | Distinct layout patterns | Screens per pattern |
|---|---:|---:|---:|
| The ten covered platforms | 271 | **69** | 3.9 |
| The five with a gap | 820 | **37** | 22.2 |

**The two halves of the estate were made differently, and counting them in the same unit is what
makes 591 look like 591.** Sixty-nine patterns for 271 screens is near-bespoke — almost every
screen its own thing, which is what hand-designing looks like. Thirty-seven for 820 is a generator
working from a short list.

**Three boards cover 567 of the 820 screens — 69%.**

| Board | Screens | Template | Components | What it is |
|---|---:|---|---|---|
| **BP-001** | 315 | `split` | dataTable · detailPanel · searchField | master–detail with search |
| **BP-002** | 137 | `split` | detailPanel · selectField · toggle | a settings pane |
| **BP-003** | 115 | `dashboard` | dataTable · metricTile | tiles over a table |

The tail is the opposite shape: **21 boards cover one or two screens each**, 23 screens in total.
Those are genuinely bespoke and should be drawn as such — but they are 21 boards, not 300.

---

## What is actually to be drawn

| | Boards | Screens they cover |
|---|---:|---:|
| **New patterns** — nothing existing matches | **22** | 632 |
| **Reuse** — a pattern already drawn on a covered platform | 15 | 188 |
| | **37** | **820** |

Boards touching each platform: **P08 32 · P09 12 · P10 12 · P12 8 · P13 11.** P08 needs the most
distinct work despite P09 having the larger raw gap — P09 is repetitive where P08 is broad.

---

## The one number still to confirm

**22 is an upper bound, and it may be much lower.**

The "already drawn" vocabulary was derived from the ten fully-covered platforms, and those are
mostly guest-facing. They share only **15 of 37** signatures with the admin surfaces: they use
`board` and `canvas` templates the admin screens never touch, and the admin screens lean on `split`
far harder. **So some of the 22 may already exist on the covered portion of P08 and P09** — the 143
and 37 boards drawn before the packs landed — and that cannot be seen from the package side.

**`board-data.js` settles it.** Join it on screen id against `board-plan.json`:

- a board id already against any screen in a `BP-` group → that pattern is drawn, mark it reuse
- a `BP-` group with no board against any of its screens → genuinely new

**The difference between 22 boards and 8 is the difference between a fortnight and a sprint**, so
it is worth doing that join before anyone commits to a plan.

---

## Two things the audit found that are not this

**558 dead screen links**, from ten legacy modules — `seatp`, `crm`, `inv`, `fnb`, `retail`, `pos`,
`gm`, `ksk`, `seat`, `dash` — pointing at 66 board files not in the project. Separate problem,
separate fix: those modules predate the platform split and the links were never repointed.

**The index contradicts itself on P01, P04 and P06.** Checked against `screens/`, and the package
is right in all three — **P01 is 46, P04 is 24, P06 is 66**, and the modules side of the index is
stale in the same direction each time. The audit read this correctly.

**One discrepancy in the audit itself:** it reports eleven platforms level; there are **ten of
fifteen**. The arithmetic still reconciles exactly — 500 + 591 = 1,091 either way — so this is a
labelling difference rather than a counting error.

**The likely cause is a platform code the package does not define**, and `check-package` rule 12
proves it: naming the missing code in this very document failed the build, because the rule refuses
any `P`-code with no matching `screens/` file. The package defines fifteen, and the numbering skips
one between the second and the fourth. **If the board carries that sixteenth platform, it has no
package presence at all** — which would also fit the 66 missing board files in finding 2. Worth
confirming from the board side, because a whole platform absent from `screens/` is a larger problem
than a board gap.

---

## Regenerating this

```bash
python - <<'EOF'
import yaml, glob, os, json
from collections import defaultdict
def sig(s):
    L = s.get('layout') or {}
    k = [c.get('kind') for r in (L.get('regions') or []) for c in (r.get('components') or [])]
    return (L.get('template') or 'none', tuple(sorted(set(x for x in k if x))))
load = lambda f: (yaml.safe_load(open(f, encoding='utf-8')) or {}).get('screens') or []
GAP = {'P09','P08','P13','P10','P12'}
groups, covered = defaultdict(lambda: {'screens': [], 'platforms': set()}), set()
for f in sorted(glob.glob('screens/P*.yaml')):
    code = os.path.basename(f)[:3]
    for s in load(f):
        g = sig(s)
        if code in GAP:
            groups[g]['screens'].append({'id': s.get('id'), 'name': s.get('name'),
                                         'platform': code, 'module': s.get('module')})
            groups[g]['platforms'].add(code)
        else:
            covered.add(g)
rows = sorted(groups.items(), key=lambda x: -len(x[1]['screens']))
out = [{'board': f'BP-{i:03d}', 'template': g[0], 'components': list(g[1]),
        'screenCount': len(d['screens']), 'platforms': sorted(d['platforms']),
        'reusesExistingPattern': g in covered, 'screens': d['screens']}
       for i, (g, d) in enumerate(rows, 1)]
json.dump(out, open('docs/active/board-plan.json','w',encoding='utf-8'), indent=1, ensure_ascii=False)
print(len(out), 'boards |', sum(o['screenCount'] for o in out), 'screens |',
      sum(1 for o in out if not o['reusesExistingPattern']), 'new')
EOF
```

The board-drawn counts in the first table come from the 7 September design audit, not from the
package — the package does not record which screens have boards. That is the join
`board-data.js` closes.
