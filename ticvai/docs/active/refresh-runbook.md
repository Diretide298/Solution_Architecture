# The refresh gate: how to run it, read it, and keep it fast

> **Owner:** Chinmay. **Decided:** council of 3 October 2026, 23:30 (refresh speed-up; TODO "Refresh speed-up").
> **Change:** `changes/entries/CHG-RSPD-001-refresh-speed-up.yaml`. **Tools:** `tools/refresh-safe.sh`,
> `tools/refresh-manifest.py` (emits the run), `tools/run-checks.py` (the checks).
> The release steps around it are in `docs/active/release-runbook.md`.

`bash tools/refresh-safe.sh` is the only way a refresh reaches the main tree. It copies the package into a
throwaway worktree, runs the 65 derive steps of `tools/refresh.sh`, runs the 68 checkers, judges them against
`tools/refresh-safe-baseline.json` and merges the derived output only on PASS. Everything below is about
making a failure cheap and the gate trustworthy. None of it changes what a step or a checker produces.

## 1. Policy

1. **While iterating, run scoped.** Use `--changed <paths>` (with `--since <last fully refreshed commit>` when
   commits since then changed inputs), and rerun only the checker that failed:
   `python3 tools/<checker>.py` or `python3 tools/run-checks.py <checker>`. A scoped run is not a release.
2. **The full gate runs at the Tuesday and Friday releases, with the CRs batched.** One full run per release,
   not one per CR. A full gate is always a fresh run; `--resume` is for iterating and never merges.
3. **Never start a gate while more than two agents are running.** On 3 October a run died at step 37 under
   the load of five to eight agents; the same step passed alone. The release lock stops two gates
   overlapping; it cannot see agents, so this one is on whoever starts the run.
4. **No content-hash cache before Sprint 2.** The manifest behind `--changed` is measured from one traced run;
   a cache keyed on it would pass stale output as a full gate. It is considered only once the manifest
   rebuilds itself and three cold runs match cached runs byte for byte.

## 2. Running it

| Command | What it does |
|---|---|
| `bash tools/refresh-safe.sh` | Full run: refresh, check, merge on PASS |
| `bash tools/refresh-safe.sh --no-merge` | Full run, judged, the main tree untouched |
| `bash tools/refresh-safe.sh --changed <paths>` | Only the steps downstream of the paths; checks in full |
| `bash tools/refresh-safe.sh --resume` | After a failed run: skip the steps it completed (never merges) |
| `bash tools/refresh-safe.sh --jobs 1` | The checks one at a time (the original loop); default is 4 |
| `bash tools/refresh-safe.sh --quiet` | Print step banners, failures and the verdict only |

Exit codes: 0 pass · 1 refresh or checks failed · 2 usage · 3 uncommitted authored changes · 4 merge refused
(conflict or drift) · 5 STALE BASE · 6 another run holds the release lock · 130 interrupted.

Every run keeps its logs in `<wt-dir>/runs/<stamp>-<pid>/` (default `<wt-dir>` is
`%TEMP%\ticvai-refresh-safe`):

| File | Holds |
|---|---|
| `refresh.log` | Every step's output, its banner, a `FAILED at step N` line, and the completion marker |
| `steps.tsv` | One row per step: step, name, start, seconds, exit, status (`ok`, `FAILED`, `resumed`) |
| `state.tsv` | The steps completed, for `--resume` |
| `plan.json` | The steps selected and each step's expected outputs |
| `checks.log`, `checks/<name>.txt` | The checks: the table, and each checker's full output |
| `phases.tsv` | Seconds per phase: setup, derive, checks, merge, total |
| `merge.log` | What was (or would be) merged |

At the end of every run, passed or failed, it prints the ten slowest steps and the time of each phase.

## 3. When it fails

**A derive step fails.** The run stops at once with one line naming it:

```
FAILED at step 37 python3 tools/build-service-docs.py -- exit 1 after 12.3s (step 37 of 65)
```

A step also fails when it exits 0 but leaves an expected output missing, empty or unreadable (a JSON file
that does not parse, an `.xlsx` that is not a zip). The expected outputs are the files the traced manifest
(`handoff/refresh-manifest.json`) says the step writes and that existed before the run. A refresh whose
process is killed outright prints no FAILED line; refresh-safe then says so (`no FAILED line: the refresh
process itself was killed`) and names the last step that started.

**A silent death can never pass.** The emitted script prints `== refresh completed: all N selected steps of T`
as its last line, only when every selected step completed. Both refresh-safe and the judge refuse a run
whose log lacks it.

**Resume instead of starting over.** A failed or interrupted run keeps its worktree. Fix the cause (a flake,
load, a file lock), then:

```
bash tools/refresh-safe.sh --resume
```

It skips the completed steps, reruns the rest and the checks, and reports what would be merged. It is
refused, and a fresh run starts instead, when HEAD is not the commit the failed run started on or any step's
script changed: the step's text, its tool, the modules the tool imports, `refresh.sh` or the emitter. A fix
to an input or a tool is therefore a fresh run, as it must be. Any run without `--resume` removes the kept
worktree.

**A checker fails.** Its full output is in `checks/<name>.txt`. Rerun it alone in the kept worktree, fix the
cause, and run `--resume` (which skips every step and reruns the checks) or a scoped run.

## 4. One run at a time

**The release lock.** A run takes `ticvai-refresh-safe.lock` in the repository's common git directory
(`D:\Chinmay\adam\.git`), shared by the main checkout and every worktree. It records the pid, the Windows
pid, the start time, HEAD, the tree and the run. A second run exits 6 and prints the holder. A lock whose
holder is no longer running is stale and is removed by the next run. Remove it by hand only when you are
certain its run is gone.

**STALE BASE.** The verdict is for the commit the run started from. Before merging, refresh-safe checks that
HEAD is still that commit; if anything was committed meanwhile it prints `STALE BASE`, merges nothing and exits
5. Run again on the new HEAD.

## 5. The checks in parallel

`run-checks.py --jobs 4` runs four checkers at a time and prints each row only after every row above it, so
the table, the exit code and each checker's output are the same as `--jobs 1`. Proven on 4 October on one
derived tree: the per-check outputs of both runs are identical, and the tables differ only in the seconds
column. check-package and check-authored-inputs still run alongside, as before.

**Checkers that must run alone (`SERIAL` in `run-checks.py`): none today.** All 68 were read on 4 October.
Every file write is behind a flag `run-checks.py` never passes: `--write`, `--csv`, `--json`, `--fix`,
`--bless`, `--freeze`, `--update-baseline`. check-contract-compat's one unflagged write goes to a fresh
temporary directory per process. The git calls only read. **A checker that starts writing a file another
checker reads must be added to `SERIAL` in the same change.** A `SERIAL` checker waits for everything before
it to finish and runs before anything after it starts.

## 6. Where the time goes (4 October)

| | Before | After |
|---|---|---|
| Derive (65 steps) | 47.9 min | see CHG-RSPD-001 |
| Checks | 33.4 min (sequential) | see CHG-RSPD-001 |
| check-screens alone | 676 s | about 36 s |

check-screens spent 99.7% of its time in PyYAML, parsing the same 16 screens files and 35 contracts about
twenty times. Each file is now parsed once per run and every rule gets its own fresh copy, so the output is
byte-identical. The faster libyaml loader was not adopted: it is a different parser, and the gate's results
must not move.

## 7. Defender exclusions (Chinmay, as administrator)

Real-time scanning inspects every file the refresh writes: a 30,000-file worktree copy, six mirrors, and
about 120 Python and Git Bash process starts per run. Excluding the refresh paths and the tools is a cheap win
that does not change what the gate checks, and the council named it as a possible cause of the step-37 death.
Nothing here was changed by an agent; run these in **PowerShell as Administrator**:

```powershell
# Folders: the refresh worktrees and logs, the package checkout, and the agents' worktrees
Add-MpPreference -ExclusionPath "C:\Users\Chinmay.Parab\AppData\Local\Temp\ticvai-refresh-safe"
Add-MpPreference -ExclusionPath "D:\Chinmay\adam"
Add-MpPreference -ExclusionPath "D:\wt"

# Processes: the interpreter and the shells the refresh runs (files they open are not scanned)
Add-MpPreference -ExclusionProcess "C:\Users\Chinmay.Parab\AppData\Local\Programs\Python\Python39\python.exe"
Add-MpPreference -ExclusionProcess "C:\Program Files\Git\usr\bin\bash.exe"
Add-MpPreference -ExclusionProcess "C:\Program Files\Git\bin\bash.exe"
Add-MpPreference -ExclusionProcess "C:\Program Files\Git\mingw64\bin\git.exe"

# Check
Get-MpPreference | Select-Object -ExpandProperty ExclusionPath
Get-MpPreference | Select-Object -ExpandProperty ExclusionProcess
```

The process exclusions are the broader of the two: anything those programs open is skipped, wherever it is.
If that is more than you want, run only the three folder lines; they cover what the refresh writes. To undo
any line, run it again with `Remove-MpPreference` in place of `Add-MpPreference`. If you run refresh-safe with
`--wt-dir` or `REFRESH_SAFE_WT` somewhere else, exclude that folder instead of the first one.
