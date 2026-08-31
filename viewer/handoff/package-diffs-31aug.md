# Two diffs for the package side — 31 August 2026

Written by Claude Code, which writes `atlas/viewer` only. **Apply these yourself**, then run
`tools/refresh.sh` and check the ten validators actually print.

Both come out of the audit of the 31 August dump. They are independent: either can go alone.

---

## 1. The rename left its old files behind

`docs/active/renames-26-august.md` says, in bold, **"All nine validators pass."** They do not, and
they did not run — see §3 for why. Run by hand they report six errors, and **every one of them is a
file the rename added a replacement for and did not delete.**

| Still on disk | The replacement that was added |
|---|---|
| `states/redemption-right.yaml` | `states/cross-region-entitlement.yaml` |
| `diagrams/lld/lifecycles/redemption-right.yaml` | `diagrams/lld/lifecycles/cross-region-entitlement.yaml` |
| `diagrams/lld/services/CrossCellService.yaml` | `diagrams/lld/services/CrossRegionService.yaml` |
| `diagrams/lld/services/ControlService.yaml` | `diagrams/lld/services/PlatformService.yaml` |

The old state model still names things the rename moved out from under it:

```
check-states.py
  FAIL  redemption-right.yaml: enum cross-cell.RedemptionRight.status not found in the contracts
  FAIL  redemption-right.yaml: transition active->exhausted names unknown operation 'consumeRedemptionRight'
  FAIL  redemption-right.yaml: transition active->revoked names unknown operation 'revokeRedemptionRight'
```

`RedemptionRight`, `consumeRedemptionRight` and `revokeRedemptionRight` appear nowhere in
`contracts/` any more. The new twin, `cross-region-entitlement.yaml`, names
`CrossRegionEntitlement.status` and `consumeCrossRegionEntitlement` and passes cleanly.

And the two service files:

```
check-package.py
  FAIL  diagrams/lld/ has ['ControlService', 'CrossCellService'] which is not a service
        — a renamed or removed service left a file behind
  FAIL  3 diagram file(s) are older than what they are derived from
        (first: diagrams/lld/lifecycles/redemption-right.yaml) — run tools/derive-diagrams.py
```

### The change

```sh
git rm ticvai/states/redemption-right.yaml
git rm ticvai/diagrams/lld/lifecycles/redemption-right.yaml
git rm ticvai/diagrams/lld/services/CrossCellService.yaml
git rm ticvai/diagrams/lld/services/ControlService.yaml
```

**Check the metric afterwards.** `build-status.py` currently fails on
`metric 'State models' reports 124 of 122`. The numerator counts state models on disk and there are
two twins in there; removing `redemption-right.yaml` should take it to 123, and if the denominator
is 122 for a reason then one more pair is doing the same thing. Worth reading before assuming this
diff fixes it — see §3.

---

## 2. `build-schema-workbook.py` reads from `/home/claude`

Three globs point at a machine the workbook is not being built on. They match nothing, and nothing
fails — the tool carries on with empty sets and writes a workbook that looks complete.

| Line | Path | What it silently produces |
|---|---|---|
| 50 | `/home/claude/ticvai/ticvai-backend/src/Ticvai.Migrations/Scripts/V*.sql` | **0 of 379** tables marked `Written` |
| 53 | `/home/claude/ticvai/ticvai-contracts/openapi` | Scaling sheet with **0 contract rows** — header, then `TOTAL 0 0 0 0` |
| 171 | `/home/claude/ticvai-pkg/handoff/service-decomposition.json` | **321 of 379** tables given "Foreign writers" — with no service map every writer looks foreign |

That 321 is the same 321 the previous dump's audit reported. It was diagnosed then and the globs are
still here.

The empty Scaling sheet is what the viewer's DB → Routing view reports as
*"The workbook's Scaling sheet is empty — it carries its header and no contract rows, so nothing here
is routed. The sheet is generated, so this is upstream of the viewer."* That sentence is correct and
this is the upstream.

The file already has the machinery to do this properly: `_ROOT` and `_pkg()` are defined at the top
and used on line 33. These three lines just do not use them.

### The change

```diff
--- a/ticvai/tools/build-schema-workbook.py
+++ b/ticvai/tools/build-schema-workbook.py
@@
-for f in glob.glob('/home/claude/ticvai/ticvai-backend/src/Ticvai.Migrations/Scripts/V*.sql'):
+# The migrations that ship *in the package*, not a checkout on whoever's machine
+# built this last. The absolute path below matched nothing anywhere else and the
+# glob returned empty rather than failing, so every table came out `Written: no`.
+for f in sorted(glob.glob(str(_ROOT / 'backend' / 'V*.sql'))):
     s=open(f).read(); m=re.search(r"^-- =+\n-- ROLLBACK",s,re.M)
     written.update(re.findall(r'CREATE TABLE (?:IF NOT EXISTS )?([\w.]+)', s[:m.start() if m else len(s)]))
-C='/home/claude/ticvai/ticvai-contracts/openapi'
+# Same again. Empty here means the Scaling sheet ships with its header and a
+# TOTAL row of zeros, which reads as "nothing is routed" rather than as "this
+# tool could not find the contracts".
+C=str(_ROOT / 'contracts')
 routing=defaultdict(lambda: defaultdict(int))
 for f in glob.glob(f'{C}/spine/*.yaml')+glob.glob(f'{C}/satellite/*.yaml'):
@@
 try:
-    _D = json.load(open('/home/claude/ticvai-pkg/handoff/service-decomposition.json',
-                        encoding='utf-8'))['services']
+    # `_pkg` resolves against the package's own handoff/, which is where this
+    # file actually is. The absolute path found nothing, the bare `except`
+    # swallowed it, and `_D = {}` meant no schema had an owner — so every writer
+    # of every table looked foreign, and 321 of 379 tables were labelled as
+    # written by somebody else.
+    _D = json.load(open(_pkg('service-decomposition.json'), encoding='utf-8'))['services']
 except Exception:
     _D = {}
```

`_ROOT` is `parents[1]` of `tools/`, so `_ROOT / 'backend'` and `_ROOT / 'contracts'` are the
package's own folders — both present, with 6 migrations and `contracts/spine` + `contracts/satellite`
respectively.

### Worth doing at the same time

The bare `except Exception: _D = {}` on line 174 is what let this run for two dumps without anyone
noticing. A tool that cannot find its inputs should say so:

```python
except Exception as e:
    raise SystemExit(f'build-schema-workbook: no service decomposition ({e})')
```

The same globs are in `build-review-responses.py` (line 29), `build-services-workbook.py` (line 18),
`build-status.py` (line 44) and `derive-domain.py` (lines 64, 326). The last two already have a
fallback chain and are fine; the first two do not.

---

## 3. The reason none of this was caught

`tools/refresh.sh` is `set -euo pipefail`. Line 59 is `python3 tools/build-status.py`, and it exits
1:

```
metric 'State models' reports 124 of 122 — the numerator and denominator are counting
different sets, and every figure derived from it is wrong
```

So the script stops there. **Everything after line 59 never runs** — `derive-overview.py`,
`derive-mirrors.py`, `build-status.py --domain ai`, `sync-counts.py`, and the loop at the bottom that
runs all ten validators.

That is why `check-package.py` reports six mirrors out of sync with the root: `derive-mirrors.py` is
line 63. It is a symptom of the abort, not a separate problem, and not the `repos/` policy question —
that one is still parked.

It is also why the renames document could say "All nine validators pass" in good faith. The line that
would have printed their output is below the line that stopped.

**Last dump this metric read 123 of 122. This dump it reads 124 of 122** — the new state model moved
the numerator and the denominator stayed. So the dump deepened the failure that hides its own errors.

Fixing §1 probably takes the numerator to 123. That is still not 122, and the remaining one is worth
finding rather than working around: the message is right that every figure derived from a metric
whose two halves count different sets is wrong.
