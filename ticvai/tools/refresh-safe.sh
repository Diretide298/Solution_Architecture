#!/usr/bin/env bash
# Run tools/refresh.sh in a throwaway git worktree, check it, and only then bring it home.
#
# **Council item C1 (1 October).** A refresh rewrites a few thousand files over about an hour.
# Run in the main tree, an interrupted or failing refresh leaves it half-derived -- the screens
# rewritten and the index not, the mirrors one run behind -- while designers and agents are
# reading it. So the refresh runs somewhere else:
#
#   1. refuse if ticvai/ holds uncommitted AUTHORED changes (listed), unless --include-working,
#      which copies them into the worktree. Uncommitted DERIVED files (a step writes them and no
#      step reads them first -- tools/refresh-manifest.py classify) are regenerated, not refused.
#   2. `git worktree add --detach` at HEAD, under the worktree dir (not inside the repository);
#      the gitignored inputs some tools read (_dump/, the large design files under sources/) are
#      copied in; every file's mtime is set to one instant so check-package's staleness rule
#      measures the refresh, not the order git checked files out in.
#   3. run refresh.sh there -- a copy generated from it by tools/refresh-manifest.py, identical
#      except that it cds into the worktree and leaves run-checks to step 4.
#   4. run every checker in run-checks.py and judge against tools/refresh-safe-baseline.json:
#      a gating checker may fail only with error lines the baseline already names. check-bindings
#      and the other REPORT_ONLY checkers never gate. No NEW failure = pass.
#   5. on pass only: copy the worktree's changes to ticvai/ in the main tree -- added, modified
#      and deleted files, never gitignored files, never repos/*/.git -- after checking that
#      nothing the refresh changed was also changed in the main tree meanwhile (conflict: nothing
#      is copied), and that no authored input moved under it (drift: nothing is copied unless
#      --allow-drift). Files the refresh rewrote identically get the worktree's mtime too.
#   6. always: the worktree is removed (trap on EXIT/INT/TERM, which also kills the running
#      step's process tree). A run killed so hard the trap never ran is removed by the next run.
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
#   bash tools/refresh-safe.sh --trace --no-merge --skip-checks --manifest-out handoff/refresh-manifest.json
#                                                      rebuild the manifest (refresh-manifest.py rebuild)
#   options: --wt-dir DIR (default $REFRESH_SAFE_WT, else $TMPDIR/ticvai-refresh-safe)
#            --allow-drift   merge even though authored inputs changed in the main tree meanwhile
#            --quiet         print step banners only, not every tool's output
#            --steps 1,5,9   run exactly these refresh steps (numbers from `refresh-manifest.py steps`)
#            --keep-worktree debugging only: leave the worktree (and the trace) for inspection;
#                            the next run removes it. Never merges.
#
# Exit codes: 0 pass (merged unless --no-merge) · 1 refresh or checks failed · 2 usage ·
#             3 uncommitted authored changes · 4 merge refused (conflict or drift) · 130 interrupted
# Logs of every run are kept in <wt-dir>/runs/<stamp>/ (refresh.log, checks.log, merge.log).
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
MANIFEST_OUT=""; CHANGED=(); STEPS_ARG=""; KEEP_WT=0
WT_BASE="${REFRESH_SAFE_WT:-${TMPDIR:-${TEMP:-/tmp}}/ticvai-refresh-safe}"
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
    --steps) shift; [ $# -gt 0 ] || die "--steps needs a list"; STEPS_ARG="$1" ;;
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

mkdir -p "$WT_BASE"
WT_BASE="$(mixed "$(cd "$WT_BASE" && pwd)")"
STAMP="$(date +%Y%m%d-%H%M%S)"
RUN="$WT_BASE/runs/$STAMP-$$"
mkdir -p "$RUN"
MAIN_MANIFEST="$PKG_MAIN/handoff/refresh-manifest.json"
HELPER="$RUN/helper.py"

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
def cmd_judge(pkg, baseline_path, log_path, tail_path=""):
    spec = importlib.util.spec_from_file_location("run_checks", os.path.join(pkg, "tools", "run-checks.py"))
    rc_mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(rc_mod)
    checks, report_only = list(rc_mod.CHECKS), dict(rc_mod.REPORT_ONLY)
    bdoc = json.load(open(baseline_path, encoding="utf-8"))
    base = bdoc.get("checkers", {})
    detail = [c for c in checks if c in base and c not in report_only]
    others = [c for c in checks if c not in detail]
    env = dict(os.environ, PYTHONIOENCODING="utf8")
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
    print("  running %d checker(s) through run-checks.py; %s alongside, in full, for the baseline"
          % (len(others), ", ".join(detail)))
    sys.stdout.flush()
    verdicts = {}
    p = subprocess.Popen([sys.executable, os.path.join(pkg, "tools", "run-checks.py"), "--no-gate", *others],
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

if __name__ == "__main__":
    cmd, args = sys.argv[1], sys.argv[2:]
    sys.exit(globals()["cmd_" + cmd](*args) or 0)
PYHELPER
helper() { "$PY" "$HELPER" "$@"; }

# ------------------------------------------------------------------------------------------------
# Leftovers from a run killed too hard for its trap (a closed terminal, kill -9).
PIDF=""
git -C "$REPO" worktree prune
while IFS= read -r _wt; do
  [ -n "$_wt" ] || continue
  _m="$(mixed "$_wt")"
  case "${_m,,}" in "${WT_BASE,,}"/w*) ;; *) continue ;; esac
  if [ -f "$_m.pid" ] && kill -0 "$(cat "$_m.pid")" 2>/dev/null; then
    echo "refresh-safe: another run is using $_m (pid $(cat "$_m.pid")); leaving it"
    continue
  fi
  echo "refresh-safe: removing a worktree left by an interrupted run: $_m"
  git -C "$REPO" worktree remove --force "$_m" 2>/dev/null || rm -rf "$_m"
  rm -f "$_m.pid"
done < <(git -C "$REPO" worktree list --porcelain | sed -n 's/^worktree //p')
for _d in "$WT_BASE"/w*; do
  [ -d "$_d" ] || continue
  if [ -f "$_d.pid" ] && kill -0 "$(cat "$_d.pid")" 2>/dev/null; then continue; fi
  echo "refresh-safe: removing a leftover directory: $_d"; rm -rf "$_d" "$_d.pid"
done
git -C "$REPO" worktree prune

# ------------------------------------------------------------------------------------------------
echo "refresh-safe: $(git -C "$REPO" rev-parse --short HEAD) on $(git -C "$REPO" rev-parse --abbrev-ref HEAD) · run log $RUN"
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
if [ ${#CHANGED[@]} -gt 0 ]; then
  echo "2. scoped run: steps downstream of ${CHANGED[*]}"
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

# ------------------------------------------------------------------------------------------------
WT="$WT_BASE/w$$"
PIDF="$WT.pid"
CHILD=""; TAILP=""; MERGED=0; FINISHED=0
kill_tree() {
  local p="$1" w
  if [ -r "/proc/$p/winpid" ] && command -v taskkill >/dev/null 2>&1; then
    w="$(cat "/proc/$p/winpid")"; taskkill //F //T //PID "$w" >/dev/null 2>&1 || true
  fi
  pkill -TERM -P "$p" 2>/dev/null || true
  kill -TERM "$p" 2>/dev/null || true
}
on_exit() {
  local rc=$?
  set +e
  trap - INT TERM HUP
  if [ -n "$CHILD" ] && kill -0 "$CHILD" 2>/dev/null; then
    echo "refresh-safe: stopping the refresh (pid $CHILD) and everything it started"
    kill_tree "$CHILD"; wait "$CHILD" 2>/dev/null
  fi
  [ -z "$TAILP" ] || kill "$TAILP" 2>/dev/null
  if [ "$KEEP_WT" = 1 ]; then
    echo "refresh-safe: --keep-worktree: left $WT (the next run removes it)"
  elif [ -d "$WT" ] || git -C "$REPO" worktree list --porcelain | grep -qi "^worktree $WT\$"; then
    echo "refresh-safe: removing the worktree $WT"
    git -C "$REPO" worktree remove --force "$WT" >/dev/null 2>&1 || { rm -rf "$WT"; git -C "$REPO" worktree prune; }
    [ ! -d "$WT" ] || { sleep 2; rm -rf "$WT"; git -C "$REPO" worktree prune; }
  fi
  rm -f "$PIDF"
  [ "$KEEP_WT" = 1 ] || rm -rf "$RUN/trace/objects" "$RUN/trace/index" 2>/dev/null
  if [ "$MERGED" = 1 ]; then
    echo "refresh-safe: done -- merged into $PKG_MAIN (not committed)"
  else
    echo "refresh-safe: the main tree was not touched (exit $rc; logs in $RUN)"
  fi
  exit $rc
}
trap on_exit EXIT
trap 'echo; echo "refresh-safe: INTERRUPTED"; exit 130' INT TERM HUP
echo $$ > "$PIDF"

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

# ------------------------------------------------------------------------------------------------
if [ "$STEPS" != "none" ]; then
  echo "4. refresh in the worktree ($( [ "$STEPS" = all ] && echo "all steps" || echo "steps $STEPS"))$( [ "$TRACE" = 1 ] && echo ", traced")"
  EMIT=(emit --refresh "$WPKG/tools/refresh.sh" --steps "$STEPS" --out "$RUN/run.sh")
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
  export REFRESH_TICVAI="$WPKG" REFRESH_TAIL_OUT="$RUN/tail.log"
  T_START=$(date +%s)
  bash "$RUN/run.sh" > "$RUN/refresh.log" 2>&1 &
  CHILD=$!
  if [ "$QUIET" = 1 ]; then
    tail -n +1 -f --pid="$CHILD" "$RUN/refresh.log" 2>/dev/null | grep --line-buffered '^== refresh step' &
  else
    tail -n +1 -f --pid="$CHILD" "$RUN/refresh.log" 2>/dev/null &
  fi
  TAILP=$!
  set +e; wait "$CHILD"; RRC=$?; set -e
  CHILD=""
  sleep 1; kill "$TAILP" 2>/dev/null || true; TAILP=""
  echo "  refresh finished rc=$RRC in $(( ($(date +%s) - T_START) / 60 )) min"
  if [ "$RRC" != 0 ]; then
    echo "refresh-safe: FAIL -- refresh.sh stopped (rc=$RRC); last lines of $RUN/refresh.log:" >&2
    tail -n 15 "$RUN/refresh.log" >&2
    exit 1
  fi
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
echo "5. checks, judged against tools/refresh-safe-baseline.json"
set +e
( cd "$WPKG" && helper judge "$WPKG" "$SELF_DIR/refresh-safe-baseline.json" "$RUN/checks.log" "$RUN/tail.log" )
JRC=$?
set -e
[ "$JRC" = 0 ] || { echo "refresh-safe: FAIL -- checks (full output in $RUN/checks.log)" >&2; exit 1; }

echo "6. merge"
trap '' INT HUP   # a copy half-done is worse than a copy finished: no interrupting it
set +e
helper merge "$REPO" "$WT" "$PKG_REL" "$BASE_TREE" "$T0" "$SELF_DIR" "$MAIN_MANIFEST" "$MERGE" "$ALLOW_DRIFT" "$RUN/merge.log" "$IGNORE_UNTRACKED"
MRC=$?
set -e
trap 'echo; echo "refresh-safe: INTERRUPTED"; exit 130' INT TERM HUP
[ "$MRC" = 0 ] || exit 4
[ "$MERGE" = 1 ] && MERGED=1
[ "$STEPS" = all ] || echo "  scoped run -- a full run is still required before a release tag"
exit 0
}
