#!/usr/bin/env bash
# Run tools/refresh.sh in a throwaway git worktree, check it, and only then bring it home.
#
# **Council item C1 (1 October).** A refresh rewrites a few thousand files (38 minutes traced on
# 1 October, then about 16 minutes of checks, check-package alongside).
# Run in the main tree, an interrupted or failing refresh leaves it half-derived -- the screens
# rewritten and the index not, the mirrors one run behind -- while designers and agents are
# reading it. So the refresh runs somewhere else:
#
#   1. refuse if ticvai/ holds uncommitted AUTHORED changes (listed), unless --include-working,
#      which copies them into the worktree. Uncommitted DERIVED files (a step writes them and does
#      not edit them in place; the mirrors -- tools/refresh-manifest.py classify) are regenerated,
#      not refused. With no manifest, everything uncommitted counts as authored.
#   2. `git worktree add --detach` at HEAD, under the worktree dir (not inside the repository);
#      the gitignored inputs some tools read (_dump/, the large design files under sources/) are
#      copied in; every file's mtime is set to one instant so check-package's staleness rule
#      measures the refresh, not the order git checked files out in.
#   3. run refresh.sh there -- a copy generated from it by tools/refresh-manifest.py, identical
#      except that it cds into the worktree, leaves run-checks to step 4, and captures the verdict
#      of refresh.sh's closing tools/ coverage block instead of exiting on it.
#   4. run every checker in run-checks.py and judge against tools/refresh-safe-baseline.json:
#      a gating checker may fail only with error lines the baseline already names (check-package:
#      the two build-readiness-21-september.md errors; check-authored-inputs: the seven stale
#      inputs); the tools/ coverage block only on the tools the baseline lists. check-bindings and
#      the other REPORT_ONLY checkers never gate. No NEW failure = pass.
#   5. on pass only: copy the worktree's changes to ticvai/ in the main tree -- added, modified
#      and deleted files, never gitignored files, never repos/*/.git -- after checking that
#      nothing the refresh changed was also changed in the main tree meanwhile (conflict: nothing
#      is copied), and that no authored input moved under it (drift: nothing is copied unless
#      --allow-drift). Files the refresh rewrote identically get the worktree's mtime too.
#   6. always: the worktree is removed (trap on EXIT/INT/TERM/HUP, which also kills the running
#      step's process tree). A run killed so hard the trap never ran is removed by the next run.
#      Stop a run with Ctrl-C or `kill -TERM <pid>`: a run started in the background BY A SCRIPT
#      has SIGINT ignored from birth (a bash rule for asynchronous commands), so only TERM reaches
#      it there.
#
# **--changed PATH... runs only the steps downstream of PATH** (council item C15), using
# handoff/refresh-manifest.json (C13): a step runs when it reads something changed, and what it
# writes is changed for every step after it. Checks still run in full.
#
#     ****************************************************************************************
#     **  A SCOPED RUN IS NOT A RELEASE. A FULL RUN (no --changed) IS REQUIRED BEFORE A      **
#     **  RELEASE TAG. The manifest is measured from one traced run: a branch that run did   **
#     **  not take, or a step whose confidence is low, can be missed by --changed.           **
#     ****************************************************************************************
#
# **--changed assumes HEAD's derived files are a full refresh of HEAD's inputs.** Where commits
# since the last full refresh changed inputs (a contract committed without a refresh), pass
# --since <that commit> so those paths count as changed too -- otherwise the checks fail on the
# unrefreshed inputs (seen 1 October: a screen-scoped run on a HEAD holding four new, never-
# refreshed contract operations failed check-package and eight other gates, and did not merge).
#
# Most of the refresh is downstream of the screens: a change to one screen file still reaches 43
# of the 61 steps (about 90% of the traced time). The saving is real for contracts-only, docs,
# handoff and tool changes; for screens it is small.
#
# Usage (from anywhere; paths in --changed are relative to ticvai/, the repo, or absolute):
#
#   bash tools/refresh-safe.sh                         full refresh, check, merge on pass
#   bash tools/refresh-safe.sh --include-working       ...carrying uncommitted authored edits
#   bash tools/refresh-safe.sh --ignore-untracked      ...leaving untracked files (other people's
#                                                      drafts) out: they neither block nor get merged over
#   bash tools/refresh-safe.sh --head-only --no-merge  refresh exactly the committed HEAD, whatever the
#                                                      main tree holds (a release check). A merge after it
#                                                      is still refused on any conflict or drift.
#   bash tools/refresh-safe.sh --changed screens/P08-venue-back-office.yaml
#   bash tools/refresh-safe.sh --no-merge              run and judge, never touch the main tree
#   bash tools/refresh-safe.sh --trace --head-only --no-merge --skip-checks --manifest-out handoff/refresh-manifest.json
#                                                      rebuild the manifest (= refresh-manifest.py rebuild)
#   options: --wt-dir DIR (default $REFRESH_SAFE_WT, else $TMPDIR/ticvai-refresh-safe)
#            --allow-drift   merge even though authored inputs changed in the main tree meanwhile
#            --quiet         print step banners only, not every tool's output
#            --steps 1,5,9   run exactly these refresh steps (numbers from `refresh-manifest.py steps`)
#            --since REF     with --changed: also treat every ticvai/ path that differs between REF
#                            and HEAD as changed (REF = the last commit whose outputs were fully refreshed)
#            --keep-worktree debugging only: leave the worktree (and the trace) for inspection;
#                            the next run removes it. Never merges.
#            --jobs N        checkers run N at a time (default 4; 1 = the original sequential loop).
#                            The table, the verdict and every checker's output are the same either way.
#            --resume        after a failed run: reuse its worktree and skip the steps it completed.
#                            Refused (and a fresh run started instead) if HEAD or any step's script
#                            changed since. A resumed run never merges: it is for iterating, and a
#                            release gate is always a fresh run (docs/active/refresh-runbook.md).
#
# **Speed-up of 4 October (council of 3 October 23:30, CHG-RSPD-001):**
#   * every refresh step's exit code and expected outputs are checked; a failure prints
#     `FAILED at step N <name>` and stops the run, and the judge refuses a PASS unless the refresh
#     printed `== refresh completed: all N selected steps of T` -- a silent death cannot pass;
#   * per-step timings in <run>/steps.tsv (step, name, start, seconds, exit, status), the ten
#     slowest and the time of each phase printed at the end (<run>/phases.tsv);
#   * a failed run keeps its worktree for --resume (state in <run>/state.tsv, validity in
#     <wt-dir>/resume.json: HEAD and the fingerprint of every step's script);
#   * one run at a time: a release lock in the repository's git directory
#     (ticvai-refresh-safe.lock: pid, start, HEAD), a stale one (holder gone) is removed; and before
#     merging, HEAD must still be the commit the run started from, or it is a STALE BASE;
#   * the checks run --jobs at a time, per-check output kept in <run>/checks/<name>.txt.
#
# Exit codes: 0 pass (merged unless --no-merge) · 1 refresh or checks failed · 2 usage ·
#             3 uncommitted authored changes · 4 merge refused (conflict or drift) ·
#             5 STALE BASE (HEAD moved during the run; nothing merged) ·
#             6 another run holds the release lock · 130 interrupted
# Logs of every run are kept in <wt-dir>/runs/<stamp>/ (refresh.log, steps.tsv, checks.log,
# checks/, merge.log, phases.tsv).
#
# **The whole script is one brace group**, so bash parses all of it before running any of it. Bash
# reads a script as it goes; a `git pull` that changed this file during an hour-long run would
# otherwise have the running copy resume at a byte offset in the new text.
{
set -euo pipefail
export PYTHONIOENCODING=utf-8

die() { echo "refresh-safe: $*" >&2; exit 2; }

SELF_DIR="$(cd "$(dirname "$0")" && pwd)"
PKG_MAIN="$(cd "$SELF_DIR/.." && pwd)"
REPO="$(git -C "$PKG_MAIN" rev-parse --show-toplevel)"
PKG_REL="$(git -C "$PKG_MAIN" rev-parse --show-prefix)"; PKG_REL="${PKG_REL%/}"
[ -n "$PKG_REL" ] || die "tools/ must sit inside a package directory of the repository"

# Windows tools want C:/... ; cygpath -l also undoes 8.3 short names (CHINMA~1.PAR).
mixed() { if command -v cygpath >/dev/null 2>&1; then cygpath -m -l "$1" 2>/dev/null || cygpath -m "$1"; else printf '%s\n' "$1"; fi; }

# The same interpreter rule as refresh.sh: python3 may be the Microsoft Store stub.
PY=""
for _c in python3 python py; do
  if command -v "$_c" >/dev/null 2>&1 && "$_c" -c 'import sys; sys.exit(0)' >/dev/null 2>&1; then
    PY="$(command -v "$_c")"; break
  fi
done
[ -n "$PY" ] || die "no working Python found"

INCLUDE_WORKING=0; IGNORE_UNTRACKED=0; HEAD_ONLY=0; MERGE=1; TRACE=0; SKIP_CHECKS=0; ALLOW_DRIFT=0; QUIET=0
MANIFEST_OUT=""; CHANGED=(); STEPS_ARG=""; KEEP_WT=0; SINCE=""; RESUME=0; JOBS=4
WT_BASE="${REFRESH_SAFE_WT:-${TMPDIR:-${TEMP:-/tmp}}/ticvai-refresh-safe}"
T_RUN0=$(date +%s)
while [ $# -gt 0 ]; do
  case "$1" in
    --include-working) INCLUDE_WORKING=1 ;;
    --ignore-untracked) IGNORE_UNTRACKED=1 ;;
    --head-only) HEAD_ONLY=1 ;;
    --changed) shift
      while [ $# -gt 0 ] && [ "${1#--}" = "$1" ]; do CHANGED+=("$1"); shift; done
      [ ${#CHANGED[@]} -gt 0 ] || die "--changed needs at least one path"
      continue ;;
    --no-merge|--dry-run) MERGE=0 ;;
    --trace) TRACE=1 ;;
    --skip-checks) SKIP_CHECKS=1 ;;
    --manifest-out) shift; [ $# -gt 0 ] || die "--manifest-out needs a path"; MANIFEST_OUT="$1" ;;
    --allow-drift) ALLOW_DRIFT=1 ;;
    --wt-dir) shift; [ $# -gt 0 ] || die "--wt-dir needs a directory"; WT_BASE="$1" ;;
    --quiet) QUIET=1 ;;
    --keep-worktree) KEEP_WT=1 ;;
    --since) shift; [ $# -gt 0 ] || die "--since needs a commit"; SINCE="$1" ;;
    --steps) shift; [ $# -gt 0 ] || die "--steps needs a list"; STEPS_ARG="$1" ;;
    --resume) RESUME=1 ;;
    --jobs) shift; [ $# -gt 0 ] || die "--jobs needs a number"; JOBS="$1"
      case "$JOBS" in ''|*[!0-9]*|0) die "--jobs needs a whole number of at least 1" ;; esac ;;
    -h|--help) sed -n '2,/^{$/p' "$0" | sed '$d; s/^# \{0,1\}//'; exit 0 ;;
    *) die "unknown option: $1 (see --help)" ;;
  esac
  shift
done
[ "$KEEP_WT" = 0 ] || MERGE=0
[ "$HEAD_ONLY" = 0 ] || [ "$INCLUDE_WORKING" = 0 ] || die "--head-only and --include-working contradict"
[ "$SKIP_CHECKS" = 0 ] || [ "$MERGE" = 0 ] || die "--skip-checks needs --no-merge: nothing unchecked is merged"
[ "$TRACE" = 0 ] || [ ${#CHANGED[@]} -eq 0 ] || die "--trace is a full run; it cannot be scoped with --changed"
if [ -n "$MANIFEST_OUT" ]; then
  [ "$TRACE" = 1 ] || die "--manifest-out needs --trace"
  case "$MANIFEST_OUT" in /*|[A-Za-z]:*) ;; *) MANIFEST_OUT="$PKG_MAIN/$MANIFEST_OUT" ;; esac
fi
if [ "$RESUME" = 1 ]; then
  # A resumed run repeats the failed run's selection on the failed run's worktree; scoping it again
  # would mix two runs' state.
  [ ${#CHANGED[@]} -eq 0 ] && [ -z "$STEPS_ARG" ] && [ -z "$SINCE" ] && [ "$TRACE" = 0 ] \
    && [ "$INCLUDE_WORKING" = 0 ] && [ "$HEAD_ONLY" = 0 ] && [ "$SKIP_CHECKS" = 0 ] \
    || die "--resume reuses the failed run's options; it combines only with --jobs, --quiet, --wt-dir, --no-merge, --keep-worktree"
fi

mkdir -p "$WT_BASE"
WT_BASE="$(mixed "$(cd "$WT_BASE" && pwd)")"
STAMP="$(date +%Y%m%d-%H%M%S)"
RUN="$WT_BASE/runs/$STAMP-$$"
mkdir -p "$RUN"
MAIN_MANIFEST="$PKG_MAIN/handoff/refresh-manifest.json"
HELPER="$RUN/helper.py"
RESUME_FILE="$WT_BASE/resume.json"

# ------------------------------------------------------------------------------------------------
# **The release lock: one refresh-safe at a time** (council of 3 October 23:30, CHG-RSPD-001). Two
# gates overlapping on a machine shared with agents is how a step dies under load, and two merges
# from two runs is how a PASS approves a base that no longer exists. The lock is a directory (mkdir
# is atomic) in the repository's common git directory, so every worktree of the repository shares
# it. It records who holds it; a lock whose holder is no longer running is stale and is removed.
LOCK_DIR="$(mixed "$(git -C "$REPO" rev-parse --path-format=absolute --git-common-dir)")/ticvai-refresh-safe.lock"
LOCKED=0
lock_alive() {
  local pid wpid
  pid="$(sed -n 's/^pid=//p' "$1" 2>/dev/null | head -1)"
  wpid="$(sed -n 's/^winpid=//p' "$1" 2>/dev/null | head -1)"
  if [ -n "$pid" ] && kill -0 "$pid" 2>/dev/null; then return 0; fi
  # a holder started from another shell runtime is invisible to kill -0; Windows still sees it
  if [ -n "$wpid" ] && command -v tasklist >/dev/null 2>&1 \
     && tasklist //FI "PID eq $wpid" //NH 2>/dev/null | grep -qi 'bash'; then return 0; fi
  return 1
}
take_lock() {
  local i
  for i in 1 2 3; do
    if mkdir "$LOCK_DIR" 2>/dev/null; then
      { echo "pid=$$"
        echo "winpid=$(cat "/proc/$$/winpid" 2>/dev/null || true)"
        echo "started=$(date '+%Y-%m-%d %H:%M:%S %z')"
        echo "head=$(git -C "$REPO" rev-parse HEAD)"
        echo "tree=$PKG_MAIN"
        echo "run=$RUN"
      } > "$LOCK_DIR/info"
      LOCKED=1
      return 0
    fi
    if [ ! -f "$LOCK_DIR/info" ]; then
      # another run between its mkdir and its info file -- or one killed exactly there
      sleep 2
      if [ ! -f "$LOCK_DIR/info" ] && [ -n "$(find "$LOCK_DIR" -maxdepth 0 -mmin +1 2>/dev/null)" ]; then
        echo "refresh-safe: removing a stale release lock with no holder recorded: $LOCK_DIR"
        rm -rf "$LOCK_DIR"
      fi
      continue
    fi
    if lock_alive "$LOCK_DIR/info"; then
      echo "refresh-safe: REFUSED -- another refresh-safe run holds the release lock ($LOCK_DIR):" >&2
      sed 's/^/    /' "$LOCK_DIR/info" >&2
      echo "  One gate at a time (docs/active/refresh-runbook.md). Wait for it or stop it; if you are" >&2
      echo "  certain it is gone, remove the directory above. The main tree was not touched." >&2
      exit 6
    fi
    echo "refresh-safe: removing a stale release lock (its holder is no longer running):"
    sed 's/^/    /' "$LOCK_DIR/info"
    rm -rf "$LOCK_DIR"
  done
  echo "refresh-safe: could not take the release lock $LOCK_DIR" >&2
  exit 6
}
release_lock() {
  if [ "$LOCKED" = 1 ] && grep -qx "pid=$$" "$LOCK_DIR/info" 2>/dev/null; then rm -rf "$LOCK_DIR"; fi
  LOCKED=0
}
take_lock
trap 'release_lock' EXIT
trap 'echo; echo "refresh-safe: INTERRUPTED"; exit 130' INT TERM HUP
HEAD0="$(git -C "$REPO" rev-parse HEAD)"
fmt_s() { printf '%dm%02ds' $(( $1 / 60 )) $(( $1 % 60 )); }

# ------------------------------------------------------------------------------------------------
# The Python half: status, include, hydrate, normalise, judge, merge. Written per run so the
# script stays one file; it imports tools/refresh-manifest.py from the MAIN tree.
cat > "$HELPER" <<'PYHELPER'
import hashlib, importlib.util, json, os, re, shutil, subprocess, sys, threading, time

def git(repo, *args, inp=None, env=None):
    p = subprocess.run(["git", "-C", repo, "-c", "core.quotepath=off", *args], input=inp,
                       capture_output=True, env=env)
    if p.returncode != 0:
        sys.stderr.write(p.stderr.decode("utf-8", "replace"))
        raise SystemExit("git %s failed" % " ".join(args[:3]))
    return p.stdout

def z(b):
    return [x for x in b.decode("utf-8", "surrogateescape").split("\0") if x]

def manifest_mod(tools_dir):
    spec = importlib.util.spec_from_file_location("refresh_manifest",
                                                  os.path.join(tools_dir, "refresh-manifest.py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m

def load_manifest(path):
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, ValueError):
        return None

def status_entries(repo, pkg_rel):
    """(XY, path) for everything uncommitted under pkg_rel, renames split into add + delete."""
    out = []
    for e in z(git(repo, "status", "--porcelain=v1", "-z", "--no-renames",
                   "--untracked-files=all", "--", pkg_rel)):
        xy, path = e[:2], e[3:]
        if re.search(r"(^|/)repos/[^/]+/\.git(/|$)", path):
            continue
        out.append((xy, path))
    return out

def classify(tools_dir, manifest_path, pkg_rel, paths):
    m = load_manifest(manifest_path)
    if not m:
        return {p: "authored" for p in paths}
    mod = manifest_mod(tools_dir)
    rel = {p: p[len(pkg_rel) + 1:] for p in paths}
    c = mod.classify(m, list(rel.values()))
    return {p: c[rel[p]] for p in paths}

def cmd_status(repo, pkg_rel, tools_dir, manifest_path, out_authored, out_derived, ignore_untracked="0"):
    ents = status_entries(repo, pkg_rel)
    if ignore_untracked == "1":
        skipped = [p for xy, p in ents if xy == "??"]
        ents = [(xy, p) for xy, p in ents if xy != "??"]
        if skipped:
            print("  --ignore-untracked: %d untracked file(s) left out of the run and never merged over" % len(skipped))
    cls = classify(tools_dir, manifest_path, pkg_rel, [p for _, p in ents])
    auth = [(xy, p) for xy, p in ents if cls[p] == "authored"]
    der = [(xy, p) for xy, p in ents if cls[p] == "derived"]
    with open(out_authored, "w", encoding="utf-8") as fh:
        fh.write("".join("%s\t%s\n" % (xy, p) for xy, p in auth))
    with open(out_derived, "w", encoding="utf-8") as fh:
        fh.write("".join("%s\t%s\n" % (xy, p) for xy, p in der))
    if not load_manifest(manifest_path):
        print("  (no handoff/refresh-manifest.json: every uncommitted change counts as authored)")
    if der:
        print("  %d uncommitted DERIVED file(s) in the main tree; the refresh regenerates them:" % len(der))
        for xy, p in der[:10]:
            print("    %s %s" % (xy, p))
        if len(der) > 10:
            print("    ... %d more" % (len(der) - 10))
    if auth:
        print("  %d uncommitted AUTHORED change(s) under %s/:" % (len(auth), pkg_rel))
        for xy, p in auth[:60]:
            print("    %s %s" % (xy, p))
        if len(auth) > 60:
            print("    ... %d more" % (len(auth) - 60))
    return 0

def cmd_include(repo, wt, authored_list):
    n_cp = n_rm = 0
    for line in open(authored_list, encoding="utf-8"):
        line = line.rstrip("\n")
        if not line:
            continue
        xy, p = line.split("\t", 1)
        src, dst = os.path.join(repo, p), os.path.join(wt, p)
        if os.path.lexists(src) and os.path.isfile(src):
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy2(src, dst)
            n_cp += 1
        elif os.path.lexists(dst):
            os.remove(dst)
            n_rm += 1
    print("  --include-working: %d file(s) copied into the worktree, %d removed" % (n_cp, n_rm))

HYDRATE_SKIP = re.compile(r"(^|/)(__pycache__|bin|obj|\.venv|node_modules)(/|$)|\.(pyc|pyo|log)$"
                          r"|^[^/]+/Updating old wireframes/|^[^/]+/repos/")

def cmd_hydrate(repo, wt, pkg_rel):
    """Gitignored files some tools read (audit-links reads _dump/; index-packs hashes sources/).
    The worktree has only what git tracks, so without these the checks would see less than the
    main tree does. Mirrors under repos/ are outputs and are not copied."""
    files = z(git(repo, "ls-files", "--others", "--ignored", "--exclude-standard", "-z", "--", pkg_rel))
    n = size = 0
    for p in files:
        if HYDRATE_SKIP.search(p):
            continue
        src, dst = os.path.join(repo, p), os.path.join(wt, p)
        if not os.path.isfile(src) or os.path.exists(dst):
            continue
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(src, dst)
        n += 1
        size += os.path.getsize(src)
    print("  hydrated %d gitignored input file(s), %.1f MB" % (n, size / 1e6))

def cmd_normalise(pkg, t0):
    t0 = float(t0)
    n = 0
    for dp, dns, fns in os.walk(pkg):
        dns[:] = [d for d in dns if d != ".git"]
        for f in fns:
            try:
                os.utime(os.path.join(dp, f), (t0, t0))
                n += 1
            except OSError:
                pass
    print("  %d file(s) set to one mtime" % n)

# ---------------------------------------------------------------------------------------------
def cmd_judge(pkg, baseline_path, log_path, tail_path="", jobs="1", out_dir="", refresh_log="", plan_path=""):
    spec = importlib.util.spec_from_file_location("run_checks", os.path.join(pkg, "tools", "run-checks.py"))
    rc_mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(rc_mod)
    checks, report_only = list(rc_mod.CHECKS), dict(rc_mod.REPORT_ONLY)
    bdoc = json.load(open(baseline_path, encoding="utf-8"))
    base = bdoc.get("checkers", {})
    detail = [c for c in checks if c in base and c not in report_only]
    others = [c for c in checks if c not in detail]
    env = dict(os.environ, PYTHONIOENCODING="utf8", PYTHONUNBUFFERED="1")
    log = open(log_path, "w", encoding="utf-8")
    lock = threading.Lock()
    results = {}

    def run_detail(c):
        t = time.time()
        p = subprocess.run([sys.executable, os.path.join(pkg, "tools", c + ".py")], cwd=pkg, env=env,
                           capture_output=True, text=True, encoding="utf-8", errors="replace")
        out = (p.stdout or "") + (p.stderr or "")
        with lock:
            log.write("\n===== %s rc=%d (%.0fs)\n%s" % (c, p.returncode, time.time() - t, out))
            log.flush()
        results[c] = (p.returncode, out, time.time() - t)

    threads = [threading.Thread(target=run_detail, args=(c,)) for c in detail]
    for th in threads:
        th.start()
    print("  running %d checker(s) through run-checks.py, %s at a time; %s alongside, in full, for the baseline"
          % (len(others), jobs, ", ".join(detail)))
    sys.stdout.flush()
    verdicts = {}
    extra = ["--jobs", str(jobs)] + (["--out-dir", out_dir] if out_dir else [])
    p = subprocess.Popen([sys.executable, os.path.join(pkg, "tools", "run-checks.py"), "--no-gate", *extra, *others],
                         cwd=pkg, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         text=True, encoding="utf-8", errors="replace")
    for line in p.stdout:
        with lock:
            log.write(line)
        sys.stdout.write(line)
        sys.stdout.flush()
        m = re.match(r"^\s+(\S+)\s+(ok  |FAIL|rpt |MISSING)", line)
        if m:
            verdicts[m.group(1)] = m.group(2).strip()
    p.wait()
    for th in threads:
        th.join()

    new, known_hit, notes = [], set(), []
    for c in others:
        v = verdicts.get(c)
        if v is None:
            new.append("%s: no verdict from run-checks.py" % c)
        elif v in ("FAIL", "MISSING"):
            new.append("%s: %s (not in the baseline)" % (c, v))
    for c in detail:
        rc, out, secs = results[c]
        errs = [m.group(2).strip() for m in re.finditer(r"^\s*(FAIL|STALE|ISSUE)\s+(.*\S)\s*$", out, re.M)
                if not m.group(2).startswith("-")]
        pats = base[c].get("known", [])
        unknown = [e for e in errs if not any(re.search(pt, e) for pt in pats)]
        for e in errs:
            for pt in pats:
                if re.search(pt, e):
                    known_hit.add((c, pt))
        last = [l for l in out.splitlines() if l.strip()][-1:] or [""]
        mark = "ok  " if rc == 0 else ("base" if not unknown and errs else "FAIL")
        print("  %-26s %s rc=%-3d %5.1fs  %s" % (c, mark, rc, secs, last[0].strip()[:96]))
        if rc != 0 and not errs:
            new.append("%s: rc=%d with no FAIL/STALE/ISSUE line to compare" % (c, rc))
        for e in unknown:
            new.append("%s: %s" % (c, e))
        gone = [pt for pt in pats if (c, pt) not in known_hit]
        if gone:
            notes.append("%s: %d baseline failure(s) no longer reported -- remove them from "
                         "tools/refresh-safe-baseline.json" % (c, len(gone)))
    # refresh.sh's own tools/ coverage block, captured by the generated script
    if tail_path and os.path.exists(tail_path):
        txt = open(tail_path, encoding="utf-8", errors="replace").read()
        m = re.search(r"neither runs nor excuses:(.*)", txt)
        names = m.group(1).split() if m else []
        known = set(bdoc.get("refresh_tools_coverage", {}).get("known_unexcused", []))
        fresh = [n for n in names if n not in known]
        gone = sorted(known - set(names))
        print("  %-26s %s  %d tool(s) neither run nor excused, %d in the baseline"
              % ("refresh.sh tools/ cover", "ok  " if not names else ("base" if not fresh else "FAIL"),
                 len(names), len(names) - len(fresh)))
        for n in fresh:
            new.append("refresh.sh tools/ coverage: %s is neither run nor excused" % n)
        if gone:
            notes.append("refresh.sh tools/ coverage: %d baseline name(s) now run or excused -- remove "
                         "them from tools/refresh-safe-baseline.json" % len(gone))
    else:
        print("  %-26s --    not run (no refresh step ran)" % "refresh.sh tools/ cover")
    # **No PASS without the refresh saying it finished** (CHG-RSPD-001). On 3 October a run died at
    # step 37 with no line after the step's banner; whatever stops the derive phase, a log without
    # the marker is a failure here, not a shorter run.
    if plan_path:
        plan = json.load(open(plan_path, encoding="utf-8"))
        marker = "== refresh completed: all %d selected steps of %d" % (len(plan["selected"]), plan["total"])
        txt = open(refresh_log, encoding="utf-8", errors="replace").read() if os.path.exists(refresh_log) else ""
        if any(l.rstrip() == marker for l in txt.splitlines()):
            print("  %-26s ok    %s" % ("refresh.sh steps", marker[3:]))
        else:
            print("  %-26s FAIL  no '%s' line in the refresh log" % ("refresh.sh steps", marker))
            new.append("refresh: the derive phase never reported completing all %d selected steps"
                       % len(plan["selected"]))
    rpt = [c for c in others if verdicts.get(c) == "rpt"]
    print()
    print("  baseline: %s" % ", ".join("%s (%d known)" % (c, len(base[c].get("known", []))) for c in detail))
    if rpt:
        print("  report-only, non-zero (never gates): %s" % ", ".join(rpt))
    for n in notes:
        print("  note: %s" % n)
    if new:
        print("  JUDGEMENT: FAIL -- %d new failure(s) against the baseline:" % len(new))
        for e in new[:40]:
            print("    NEW  %s" % e[:220])
        if len(new) > 40:
            print("    ... %d more in %s" % (len(new) - 40, log_path))
        return 1
    print("  JUDGEMENT: PASS -- no failure outside tools/refresh-safe-baseline.json")
    return 0

# ---------------------------------------------------------------------------------------------
def hashes(repo, paths):
    """git's hash of each working-tree file (filters applied), or None where it does not exist."""
    out, have = {}, [p for p in paths if os.path.isfile(os.path.join(repo, p))]
    for p in paths:
        out[p] = None
    for i in range(0, len(have), 2000):
        chunk = have[i:i + 2000]
        res = git(repo, "hash-object", "--stdin-paths", inp="\n".join(chunk).encode("utf-8")).decode().split()
        out.update(dict(zip(chunk, res)))
    return out

def cmd_merge(repo, wt, pkg_rel, base_tree, t0, tools_dir, manifest_path, apply, allow_drift, log_path,
              ignore_untracked="0"):
    apply, allow_drift, t0 = apply == "1", allow_drift == "1", float(t0)
    log = open(log_path, "w", encoding="utf-8")
    base = {}
    for e in z(git(repo, "ls-tree", "-r", "-z", base_tree, "--", pkg_rel)):
        meta, path = e.split("\t", 1)
        base[path] = meta.split()[2]
    # 1. what the refresh changed, against the staged base in the worktree's index
    changes = {}
    for xy, p in status_entries(wt, pkg_rel):
        if xy == "??":
            changes[p] = "A"
        elif xy[1] == "D":
            changes[p] = "D"
        elif xy[1] != " ":
            changes[p] = "M" if p in base else "A"
    # 2. what the main tree changed since the base was taken
    cand = set(z(git(repo, "diff", "--name-only", "-z", "--no-renames", base_tree, "--", pkg_rel)))
    untracked = set(z(git(repo, "ls-files", "--others", "--exclude-standard", "-z", "--", pkg_rel)))
    cand |= untracked
    if ignore_untracked == "1":
        cand -= untracked
    cand |= set(changes)
    cand = {p for p in cand if not re.search(r"(^|/)repos/[^/]+/\.git(/|$)", p)}
    now = hashes(repo, sorted(cand))
    moved = sorted(p for p in cand if now[p] != base.get(p))
    cls = classify(tools_dir, manifest_path, pkg_rel, moved)
    conflict = [p for p in moved if p in changes and cls[p] == "authored"]
    overwrite = [p for p in moved if p in changes and cls[p] == "derived"]
    drift = [p for p in moved if p not in changes and cls[p] == "authored"]
    # a derived file edited in the main tree that this run regenerated to its committed content:
    # the run's output wins, as it would have in a main-tree refresh
    restore = [p for p in moved if p not in changes and cls[p] == "derived"]
    for p in moved:
        log.write("main-moved\t%s\t%s\n" % (cls[p], p))
    if conflict:
        print("  MERGE REFUSED: %d file(s) changed by the refresh were ALSO changed in the main "
              "tree during the run:" % len(conflict))
        for p in conflict[:30]:
            print("    %s" % p)
        return 4
    if drift and not allow_drift:
        print("  MERGE REFUSED: %d authored input(s) changed in the main tree during the run, so the "
              "refresh was computed from something the main tree no longer holds:" % len(drift))
        for p in drift[:30]:
            print("    %s" % p)
        print("  run again (or pass --allow-drift to merge anyway)")
        return 4
    # 3. files rewritten identically: their mtime still moves, as it would in a main-tree refresh
    touch = []
    for dp, dns, fns in os.walk(os.path.join(wt, pkg_rel)):
        dns[:] = [d for d in dns if d not in (".git", "__pycache__")]
        for f in fns:
            full = os.path.join(dp, f)
            rel = os.path.relpath(full, wt).replace("\\", "/")
            if rel in base and rel not in changes and rel not in moved:
                try:
                    if os.stat(full).st_mtime > t0 + 1:
                        touch.append(rel)
                except OSError:
                    pass
    counts = {"A": 0, "M": 0, "D": 0}
    tops = {}
    for p, k in sorted(changes.items()):
        counts[k] += 1
        top = "/".join(p.split("/")[1:2]) or p
        tops.setdefault(top, {"A": 0, "M": 0, "D": 0})[k] += 1
        log.write("%s\t%s\n" % (k, p))
    verb = "merged into the main tree" if apply else "WOULD be merged (--no-merge: main tree untouched)"
    print("  %d added, %d modified, %d deleted under %s/ -- %s"
          % (counts["A"], counts["M"], counts["D"], pkg_rel, verb))
    for top, c in sorted(tops.items(), key=lambda kv: -sum(kv[1].values()))[:15]:
        print("    %-34s +%d ~%d -%d" % (top, c["A"], c["M"], c["D"]))
    if overwrite or restore:
        print("  %d uncommitted derived file(s) in the main tree replaced by this run's output"
              % (len(overwrite) + len(restore)))
    if drift:
        print("  --allow-drift: %d authored input(s) moved in the main tree during the run" % len(drift))
    print("  %d file(s) rewritten identically (mtime carried over)" % len(touch))
    if not apply:
        return 0
    for p in restore:
        changes[p] = "M" if os.path.isfile(os.path.join(wt, p)) else "D"
    for p, k in sorted(changes.items()):
        src, dst = os.path.join(wt, p), os.path.join(repo, p)
        if k == "D":
            if os.path.lexists(dst):
                os.remove(dst)
                d = os.path.dirname(dst)
                while os.path.normcase(d) != os.path.normcase(os.path.join(repo, pkg_rel)):
                    try:
                        os.rmdir(d)
                    except OSError:
                        break
                    d = os.path.dirname(d)
        else:
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy2(src, dst)
    for p in touch:
        st = os.stat(os.path.join(wt, p))
        try:
            os.utime(os.path.join(repo, p), (st.st_atime, st.st_mtime))
        except OSError:
            pass
    print("  full list: %s" % log_path)
    return 0

# ---------------------------------------------------------------------------------------------
# --resume (CHG-RSPD-001): what a failed run leaves, and whether it may still be trusted
def cmd_resume_write(path, run, wt, wpkg, head, base_tree, t0, steps, fp_path):
    doc = {"run": run, "wt": wt, "wpkg": wpkg, "head": head, "base_tree": base_tree, "t0": t0,
           "steps": steps, "fingerprint": json.load(open(fp_path, encoding="utf-8")),
           "written": time.strftime("%Y-%m-%d %H:%M:%S")}
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(doc, fh, indent=1)
    return 0

def cmd_resume_check(path, head_now, fp_path):
    """Shell assignments for the run to resume (exit 0), or the reasons it may not be (exit 1)."""
    import shlex
    try:
        d = json.load(open(path, encoding="utf-8"))
    except (OSError, ValueError) as e:
        print("the resume record %s cannot be read (%s)" % (path, e))
        return 1
    now = json.load(open(fp_path, encoding="utf-8"))
    old = d.get("fingerprint") or {}
    why = []
    if d.get("head") != head_now:
        why.append("HEAD moved: the failed run started on %s, HEAD is now %s"
                   % ((d.get("head") or "?")[:10], head_now[:10]))
    if old.get("frame") != now.get("frame"):
        why.append("tools/refresh.sh or tools/refresh-manifest.py changed since the state was written")
    os_, ns_ = old.get("steps") or {}, now.get("steps") or {}
    changed = sorted((n for n in set(os_) | set(ns_) if os_.get(n) != ns_.get(n)), key=int)
    if changed:
        why.append("the script of step(s) %s changed since the state was written" % ", ".join(changed))
    if not os.path.isdir(d.get("wpkg") or ""):
        why.append("its worktree %s is gone" % d.get("wt"))
    state = os.path.join(d.get("run") or "", "state.tsv")
    if why:
        for w in why:
            print(w)
        return 1
    done = sum(1 for l in open(state, encoding="utf-8") if l.strip()) if os.path.exists(state) else 0
    for k, v in (("R_RUN", d["run"]), ("R_WT", d["wt"]), ("R_WPKG", d["wpkg"]), ("R_HEAD", d["head"]),
                 ("R_BASE_TREE", d["base_tree"]), ("R_T0", d["t0"]), ("R_STEPS", d["steps"]),
                 ("R_STATE", state), ("R_DONE", str(done))):
        print("%s=%s" % (k, shlex.quote(str(v))))
    return 0

def cmd_timings(steps_tsv, top="10"):
    """The slowest steps of this run, from the per-step log the refresh writes."""
    if not os.path.exists(steps_tsv):
        return 0
    rows = []
    for l in open(steps_tsv, encoding="utf-8", errors="replace").read().splitlines()[1:]:
        f = l.split("\t")
        if len(f) >= 6 and f[5] != "resumed":
            try:
                rows.append((float(f[3]), f[0], f[1], f[4], f[5]))
            except ValueError:
                pass
    if not rows:
        return 0
    total = sum(r[0] for r in rows)
    print("  %d slowest of %d timed step(s) (derive steps sum %.1f min; %s):"
          % (min(int(top), len(rows)), len(rows), total / 60, steps_tsv))
    for s, n, name, rc, st in sorted(rows, key=lambda r: -r[0])[:int(top)]:
        print("    %7.1fs  step %-3s %s%s" % (s, n, name[:80], "" if st == "ok" else "  [%s, exit %s]" % (st, rc)))
    return 0

if __name__ == "__main__":
    cmd, args = sys.argv[1], sys.argv[2:]
    sys.exit(globals()["cmd_" + cmd](*args) or 0)
PYHELPER
helper() { "$PY" "$HELPER" "$@"; }

# ------------------------------------------------------------------------------------------------
# **--resume is decided before the leftovers are cleared** (CHG-RSPD-001), because the worktree a
# valid resume needs is one of them. Valid means: HEAD is the commit the failed run started from,
# and every step's script (the step's text, its tool, the modules the tool imports, refresh.sh and
# the emitter) hashes as it did then. Anything else is refused and the run starts over.
RESUMING=0; R_WT=""; RESUMABLE=0
"$PY" "$SELF_DIR/refresh-manifest.py" fingerprint --pkg "$PKG_MAIN" > "$RUN/fingerprint.json"
if [ "$RESUME" = 1 ]; then
  if [ ! -f "$RESUME_FILE" ]; then
    echo "refresh-safe: --resume: no failed run to resume under $WT_BASE -- starting a fresh run"
  elif helper resume_check "$RESUME_FILE" "$HEAD0" "$RUN/fingerprint.json" > "$RUN/resume.env"; then
    . "$RUN/resume.env"
    RESUMING=1
    MERGE=0
  else
    echo "refresh-safe: --resume REFUSED -- the failed run's state no longer describes this tree:"
    sed 's/^/    /' "$RUN/resume.env"
    echo "  starting over with a fresh run"
    rm -f "$RESUME_FILE"
  fi
elif [ -f "$RESUME_FILE" ]; then
  echo "refresh-safe: a fresh run: the state kept for --resume is discarded ($RESUME_FILE)"
  rm -f "$RESUME_FILE"
fi

# ------------------------------------------------------------------------------------------------
# Leftovers from a run killed too hard for its trap (a closed terminal, kill -9), and the worktree a
# failed run kept for --resume when this run is not resuming it.
PIDF=""
git -C "$REPO" worktree prune
while IFS= read -r _wt; do
  [ -n "$_wt" ] || continue
  _m="$(mixed "$_wt")"
  case "${_m,,}" in "${WT_BASE,,}"/w*) ;; *) continue ;; esac
  if [ "$RESUMING" = 1 ] && [ "${_m,,}" = "${R_WT,,}" ]; then continue; fi
  if [ -f "$_m.pid" ] && kill -0 "$(cat "$_m.pid")" 2>/dev/null; then
    echo "refresh-safe: another run is using $_m (pid $(cat "$_m.pid")); leaving it"
    continue
  fi
  echo "refresh-safe: removing a worktree left by an earlier run: $_m"
  git -C "$REPO" worktree remove --force "$_m" 2>/dev/null || rm -rf "$_m" 2>/dev/null \
    || echo "refresh-safe: could not remove $_m yet (a process still holds a file in it); the next run tries again"
  rm -f "$_m.pid"
done < <(git -C "$REPO" worktree list --porcelain | sed -n 's/^worktree //p')
for _d in "$WT_BASE"/w*; do
  [ -d "$_d" ] || continue
  if [ "$RESUMING" = 1 ] && [ "${_d,,}" = "${R_WT,,}" ]; then continue; fi
  if [ -f "$_d.pid" ] && kill -0 "$(cat "$_d.pid")" 2>/dev/null; then continue; fi
  echo "refresh-safe: removing a leftover directory: $_d"
  rm -rf "$_d" "$_d.pid" 2>/dev/null || echo "refresh-safe: could not remove $_d yet; the next run tries again"
done
git -C "$REPO" worktree prune

# ------------------------------------------------------------------------------------------------
echo "refresh-safe: $(git -C "$REPO" rev-parse --short HEAD) on $(git -C "$REPO" rev-parse --abbrev-ref HEAD) · run log $RUN"
if [ "$RESUMING" = 1 ]; then
  echo "1-3. resuming $R_RUN: its worktree $R_WT at ${R_HEAD:0:10}, $R_DONE step(s) completed there"
  echo "  HEAD and every step's script are unchanged since. A resumed run never merges: the release"
  echo "  gate is a fresh run."
  STEPS="$R_STEPS"
else
echo "1. uncommitted changes under $PKG_REL/"
helper status "$REPO" "$PKG_REL" "$SELF_DIR" "$MAIN_MANIFEST" "$RUN/authored.txt" "$RUN/derived.txt" "$IGNORE_UNTRACKED"
if [ -s "$RUN/authored.txt" ] && [ "$HEAD_ONLY" = 1 ]; then
  echo "  --head-only: the run uses HEAD; none of these is carried, and a merge would be refused if"
  echo "  the refresh touches any of them (conflict) or they are inputs it read (drift)"
  : > "$RUN/authored.txt"
elif [ -s "$RUN/authored.txt" ] && [ "$INCLUDE_WORKING" = 0 ]; then
  echo
  echo "refresh-safe: REFUSED -- uncommitted authored changes (above). Commit them, stash them, or"
  echo "  pass --include-working to copy them into the worktree. The main tree was not touched."
  exit 3
fi
[ -s "$RUN/authored.txt" ] || [ "$HEAD_ONLY" = 1 ] || echo "  none authored"

STEPS="${STEPS_ARG:-all}"
[ -z "$STEPS_ARG" ] || [ ${#CHANGED[@]} -eq 0 ] || die "--steps and --changed do not combine"
[ -z "$SINCE" ] || [ ${#CHANGED[@]} -gt 0 ] || die "--since goes with --changed"
if [ ${#CHANGED[@]} -gt 0 ]; then
  echo "2. scoped run: steps downstream of ${CHANGED[*]}"
  if [ -n "$SINCE" ]; then
    git -C "$REPO" rev-parse --verify --quiet "$SINCE^{commit}" >/dev/null || die "--since: no such commit: $SINCE"
    mapfile -t _since < <(git -C "$REPO" -c core.quotepath=off diff --name-only --no-renames "$SINCE" HEAD -- "$PKG_REL")
    echo "  --since $SINCE: ${#_since[@]} path(s) under $PKG_REL/ changed between it and HEAD, added"
    CHANGED+=("${_since[@]}")
  else
    echo "  (assumes HEAD's outputs are a full refresh of its inputs; if commits since then changed"
    echo "   inputs, pass --since <last fully refreshed commit> or run in full)"
  fi
  [ -f "$MAIN_MANIFEST" ] || { echo "refresh-safe: no $MAIN_MANIFEST -- build it (python3 tools/refresh-manifest.py rebuild) or run in full" >&2; exit 2; }
  set +e
  ( cd "$PKG_MAIN" && "$PY" tools/refresh-manifest.py select "${CHANGED[@]}" ) | sed 's/^/  /'
  _sel_rc=${PIPESTATUS[0]}
  STEPS="$(cd "$PKG_MAIN" && "$PY" tools/refresh-manifest.py select --csv "${CHANGED[@]}" 2>/dev/null)"
  set -e
  [ "$_sel_rc" = 0 ] || { echo "refresh-safe: cannot scope this change (above); run without --changed" >&2; exit 2; }
  if [ -z "$STEPS" ]; then
    echo "  no refresh step reads these paths: only the checks run"
    STEPS="none"
  fi
  echo "  A SCOPED RUN IS NOT A RELEASE: a full run is required before a release tag."
fi
fi

# ------------------------------------------------------------------------------------------------
if [ "$RESUMING" = 1 ]; then WT="$R_WT"; else WT="$WT_BASE/w$$"; fi
PIDF="$WT.pid"
CHILD=""; TAILP=""; MERGED=0; FINISHED=0
T_DERIVE0=""; T_DERIVE1=""; T_CHECKS0=""; T_CHECKS1=""; T_MERGE0=""
kill_tree() {
  local p="$1" w
  if [ -r "/proc/$p/winpid" ] && command -v taskkill >/dev/null 2>&1; then
    w="$(cat "/proc/$p/winpid")"; taskkill //F //T //PID "$w" >/dev/null 2>&1 || true
  fi
  pkill -TERM -P "$p" 2>/dev/null || true
  kill -TERM "$p" 2>/dev/null || true
}
_ph() { if [ -n "$1" ]; then fmt_s $(( ${2:-$T_END} - $1 )); else printf -- '-'; fi; }
on_exit() {
  local rc=$? keep=0
  set +e
  trap - INT TERM HUP
  if [ -n "$CHILD" ] && kill -0 "$CHILD" 2>/dev/null; then
    echo "refresh-safe: stopping the refresh (pid $CHILD) and everything it started"
    kill_tree "$CHILD"; wait "$CHILD" 2>/dev/null
  fi
  [ -z "$TAILP" ] || kill "$TAILP" 2>/dev/null
  T_END=$(date +%s)
  # A run that failed (or was interrupted) keeps its worktree for --resume; a pass, a merge refusal
  # or a stale base has nothing to resume.
  if [ "$RESUMABLE" = 1 ] && { [ "$rc" = 1 ] || [ "$rc" = 130 ]; }; then keep=1; fi
  if [ "$KEEP_WT" = 1 ]; then
    echo "refresh-safe: --keep-worktree: left $WT (the next run removes it)"
  elif [ "$keep" = 1 ]; then
    echo "refresh-safe: kept the worktree $WT for --resume:"
    echo "  bash tools/refresh-safe.sh --resume   skips the $( [ -f "$RUN/state.tsv" ] && grep -c . "$RUN/state.tsv" || true) completed step(s), never merges;"
    echo "  any other run removes it. Resume is refused if HEAD or a step's script changes."
  elif [ -d "$WT" ] || git -C "$REPO" worktree list --porcelain | grep -qi "^worktree $WT\$"; then
    echo "refresh-safe: removing the worktree $WT"
    git -C "$REPO" worktree remove --force "$WT" >/dev/null 2>&1 || { rm -rf "$WT"; git -C "$REPO" worktree prune; }
    [ ! -d "$WT" ] || { sleep 2; rm -rf "$WT"; git -C "$REPO" worktree prune; }
  fi
  if [ "$RESUMABLE" = 1 ] && [ "$keep" != 1 ] && { [ "$KEEP_WT" != 1 ] || [ "$rc" = 0 ]; }; then
    rm -f "$RESUME_FILE"
  fi
  rm -f "$PIDF"
  [ "$KEEP_WT" = 1 ] || rm -rf "$RUN/trace/objects" "$RUN/trace/index" 2>/dev/null
  # **Where the time went** (CHG-RSPD-001): the ten slowest steps and every phase, at the end.
  helper timings "$RUN/steps.tsv" 10
  printf 'phase\tseconds\nsetup\t%s\nderive\t%s\nchecks\t%s\nmerge\t%s\ntotal\t%s\n' \
    "$(( ${T_DERIVE0:-${T_CHECKS0:-$T_END}} - T_RUN0 ))" \
    "$( [ -n "$T_DERIVE0" ] && echo $(( ${T_DERIVE1:-$T_END} - T_DERIVE0 )) || echo 0)" \
    "$( [ -n "$T_CHECKS0" ] && echo $(( ${T_CHECKS1:-$T_END} - T_CHECKS0 )) || echo 0)" \
    "$( [ -n "$T_MERGE0" ] && echo $(( T_END - T_MERGE0 )) || echo 0)" \
    "$(( T_END - T_RUN0 ))" > "$RUN/phases.tsv"
  echo "refresh-safe: times -- setup $(_ph "$T_RUN0" "${T_DERIVE0:-${T_CHECKS0:-$T_END}}") · derive $(_ph "$T_DERIVE0" "$T_DERIVE1")" \
       "· checks $(_ph "$T_CHECKS0" "$T_CHECKS1") · merge $(_ph "$T_MERGE0") · total $(_ph "$T_RUN0")"
  if [ "$MERGED" = 1 ]; then
    echo "refresh-safe: done -- merged into $PKG_MAIN (not committed)"
  else
    echo "refresh-safe: the main tree was not touched (exit $rc; logs in $RUN)"
  fi
  release_lock
  exit $rc
}
trap on_exit EXIT
trap 'echo; echo "refresh-safe: INTERRUPTED"; exit 130' INT TERM HUP
echo $$ > "$PIDF"

if [ "$RESUMING" = 1 ]; then
  WPKG="$R_WPKG"; BASE_TREE="$R_BASE_TREE"; T0="$R_T0"
  if [ -f "$R_STATE" ]; then cp "$R_STATE" "$RUN/state.tsv"; else : > "$RUN/state.tsv"; fi
  helper resume_write "$RESUME_FILE" "$RUN" "$WT" "$WPKG" "$HEAD0" "$BASE_TREE" "$T0" "$STEPS" "$RUN/fingerprint.json"
  RESUMABLE=1
else
  echo "3. worktree $WT at $(git -C "$REPO" rev-parse --short HEAD)"
  git -C "$REPO" -c core.longpaths=true worktree add --detach --quiet "$WT" HEAD
  WPKG="$WT/$PKG_REL"
  if [ "$INCLUDE_WORKING" = 1 ] && [ -s "$RUN/authored.txt" ]; then
    helper include "$REPO" "$WT" "$RUN/authored.txt"
  fi
  helper hydrate "$REPO" "$WT" "$PKG_REL"
  T0=$(( $(date +%s) - 60 ))
  helper normalise "$WPKG" "$T0"
  git -C "$WT" add -A -- "$PKG_REL"
  BASE_TREE="$(git -C "$WT" write-tree)"
  echo "  base tree $BASE_TREE (HEAD$( [ "$INCLUDE_WORKING" = 1 ] && [ -s "$RUN/authored.txt" ] && echo " + included working changes"))"
  : > "$RUN/state.tsv"
  # A traced run measures the pipeline; its trace cannot be stitched from two runs, so it is not resumable.
  if [ "$TRACE" = 0 ]; then
    helper resume_write "$RESUME_FILE" "$RUN" "$WT" "$WPKG" "$HEAD0" "$BASE_TREE" "$T0" "$STEPS" "$RUN/fingerprint.json"
    RESUMABLE=1
  fi
fi

# ------------------------------------------------------------------------------------------------
if [ "$STEPS" != "none" ]; then
  T_DERIVE0=$(date +%s)
  echo "4. refresh in the worktree ($( [ "$STEPS" = all ] && echo "all steps" || echo "steps $STEPS"))$( [ "$TRACE" = 1 ] && echo ", traced")$( [ "$RESUMING" = 1 ] && echo ", resumed")"
  EMIT=(emit --refresh "$WPKG/tools/refresh.sh" --steps "$STEPS" --out "$RUN/run.sh"
        --manifest "$WPKG/handoff/refresh-manifest.json" --plan-out "$RUN/plan.json")
  if [ "$TRACE" = 1 ]; then
    TD="$RUN/trace"
    mkdir -p "$TD/objects"
    EMIT+=(--trace --hook-dir "$TD/hook")
    cp "$(git -C "$WT" rev-parse --path-format=absolute --git-path index)" "$TD/index"
    ALT="$(mixed "$(git -C "$REPO" rev-parse --path-format=absolute --git-common-dir)")/objects"
    printf '%s\n' "$ALT" > "$TD/alt"
    export REFRESH_TRACE_DIR="$TD" REFRESH_TRACE_ALT="$ALT"
  fi
  "$PY" "$SELF_DIR/refresh-manifest.py" "${EMIT[@]}"
  export REFRESH_TICVAI="$WPKG" REFRESH_TAIL_OUT="$RUN/tail.log" REFRESH_STEP_LOG="$RUN/steps.tsv" \
         REFRESH_STATE="$RUN/state.tsv" REFRESH_RESUME="$RESUMING"
  bash "$RUN/run.sh" > "$RUN/refresh.log" 2>&1 &
  CHILD=$!
  if [ "$QUIET" = 1 ]; then
    tail -n +1 -f --pid="$CHILD" "$RUN/refresh.log" 2>/dev/null | grep -E --line-buffered '^(== refresh|FAILED)' &
  else
    tail -n +1 -f --pid="$CHILD" "$RUN/refresh.log" 2>/dev/null &
  fi
  TAILP=$!
  set +e; wait "$CHILD"; RRC=$?; set -e
  CHILD=""
  sleep 1; kill "$TAILP" 2>/dev/null || true; TAILP=""
  T_DERIVE1=$(date +%s)
  echo "  refresh finished rc=$RRC in $(fmt_s $(( T_DERIVE1 - T_DERIVE0 )))"
  if [ "$RRC" != 0 ]; then
    echo "refresh-safe: FAIL -- the refresh stopped (rc=$RRC):" >&2
    if grep -q '^FAILED' "$RUN/refresh.log"; then
      grep '^FAILED' "$RUN/refresh.log" | tail -1 | sed 's/^/  /' >&2
    else
      echo "  no FAILED line: the refresh process itself was killed (last step started: $(grep '^== refresh step' "$RUN/refresh.log" | tail -1))" >&2
    fi
    echo "  last lines of $RUN/refresh.log:" >&2
    tail -n 15 "$RUN/refresh.log" >&2
    exit 1
  fi
  # **No marker, no pass** -- checked here and again by the judge.
  MARK="$("$PY" -c 'import json, sys; p = json.load(open(sys.argv[1], encoding="utf-8")); print("== refresh completed: all %d selected steps of %d" % (len(p["selected"]), p["total"]))' "$RUN/plan.json")"
  if ! grep -qxF "$MARK" "$RUN/refresh.log"; then
    echo "refresh-safe: FAIL -- the refresh exited 0 but never printed '$MARK'" >&2
    tail -n 15 "$RUN/refresh.log" >&2
    exit 1
  fi
  echo "  ${MARK#== }"
  if [ "$TRACE" = 1 ]; then
    echo "  building the step manifest from the trace"
    "$PY" "$SELF_DIR/refresh-manifest.py" build --trace-dir "$TD" --pkg "$WPKG" \
      --commit "$(git -C "$REPO" rev-parse HEAD)" --out "$RUN/refresh-manifest.json"
    if [ -n "$MANIFEST_OUT" ]; then
      cp "$RUN/refresh-manifest.json" "$MANIFEST_OUT"
      echo "  manifest written to $MANIFEST_OUT"
    fi
  fi
fi

# ------------------------------------------------------------------------------------------------
if [ "$SKIP_CHECKS" = 1 ]; then
  echo "5. checks skipped (--skip-checks); nothing is merged"
  exit 0
fi
T_CHECKS0=$(date +%s)
echo "5. checks, $JOBS at a time, judged against tools/refresh-safe-baseline.json"
set +e
( cd "$WPKG" && helper judge "$WPKG" "$SELF_DIR/refresh-safe-baseline.json" "$RUN/checks.log" "$RUN/tail.log" \
    "$JOBS" "$RUN/checks" "$RUN/refresh.log" "$( [ "$STEPS" != none ] && echo "$RUN/plan.json")" )
JRC=$?
set -e
T_CHECKS1=$(date +%s)
[ "$JRC" = 0 ] || { echo "refresh-safe: FAIL -- checks (full output in $RUN/checks.log and $RUN/checks/)" >&2; exit 1; }

T_MERGE0=$(date +%s)
echo "6. merge"
# **STALE BASE** (CHG-RSPD-001): the verdict is for the commit the run started from. If HEAD moved
# meanwhile, a merge would put that commit's derived output on top of a different one.
HEAD_NOW="$(git -C "$REPO" rev-parse HEAD)"
if [ "$HEAD_NOW" != "$HEAD0" ]; then
  if [ "$MERGE" = 1 ]; then
    echo "refresh-safe: STALE BASE -- HEAD moved from ${HEAD0:0:10} to ${HEAD_NOW:0:10} during the run." >&2
    echo "  This PASS is for ${HEAD0:0:10}; nothing is merged. Run again on the new HEAD." >&2
    exit 5
  fi
  echo "  STALE BASE (no merge requested): HEAD moved from ${HEAD0:0:10} to ${HEAD_NOW:0:10}; this verdict is for ${HEAD0:0:10}"
fi
trap '' INT HUP   # a copy half-done is worse than a copy finished: no interrupting it
set +e
helper merge "$REPO" "$WT" "$PKG_REL" "$BASE_TREE" "$T0" "$SELF_DIR" "$MAIN_MANIFEST" "$MERGE" "$ALLOW_DRIFT" "$RUN/merge.log" "$IGNORE_UNTRACKED"
MRC=$?
set -e
trap 'echo; echo "refresh-safe: INTERRUPTED"; exit 130' INT TERM HUP
[ "$MRC" = 0 ] || exit 4
[ "$MERGE" = 1 ] && MERGED=1
[ "$STEPS" = all ] || echo "  scoped run -- a full run is still required before a release tag"
[ "$RESUMING" = 0 ] || echo "  resumed run -- never merged; the release gate is a fresh run"
exit 0
}
