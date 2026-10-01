#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""What every step of `refresh.sh` reads and writes, so a change can run only what it reaches.

**Built by tracing a real refresh, not by reading the tools** (1 October, council items C13 and
C15). A refresh takes about an hour; a change to one screen file does not need most of it. To run
only the steps downstream of a change, something has to know which step reads what -- and a list
typed from the source code is the same mistake as a count kept by hand next to the thing it
counts. So the list is measured:

  * **writes** -- every file each step opened for writing, renamed onto or deleted (an
    interpreter hook, below), unioned with what a git snapshot of the tree says changed across
    the step. The snapshot catches a writer the hook cannot see.
  * **reads** -- every file each step opened for reading and every directory it listed, recorded
    by the same hook, plus the step's own tool source and the local modules it imports. Then the
    tool's source is read for path literals (`ROOT / "handoff" / "x.json"`, `"screens/"`); a
    literal the trace never saw is added as a read anyway and lowers the step's confidence,
    because it is a branch the traced run did not take.

**Confidence**, per step:

    high     traced, the snapshot agrees with the hook, no path literal the trace missed
    medium   the source names package paths the traced run did not read (added as reads), or
             the tool shells out (git, a subprocess) where the hook cannot follow a read
    low      no trace at all for the step, or the snapshot saw changes the hook did not

Reads and writes are stored as `path`, `dir/*` (the directory's direct children) or `dir/**`
(the subtree). Collapsing is always wider, never narrower: a scoped run may run a step it did not
need, and must never skip one it did.

    python3 tools/refresh-manifest.py rebuild [--wt-dir DIR] [--include-working]
        trace a full refresh of HEAD in a throwaway worktree (refresh-safe.sh --trace
        --head-only) and write handoff/refresh-manifest.json. About 40 minutes; nothing else in
        the main tree is touched. Rebuild whenever refresh.sh gains, loses or reorders a step
        (`select` refuses a manifest traced against a different step list).
    python3 tools/refresh-manifest.py steps               the steps parsed from refresh.sh
    python3 tools/refresh-manifest.py select PATH...      the steps a change to PATH reaches
    python3 tools/refresh-manifest.py classify PATH...    derived-only vs authored, per path

`emit` and `build` are the halves refresh-safe.sh calls; they are not meant to be run by hand.
**A scoped run is a convenience, not a release.** A full refresh is required before a tag.
"""
import argparse
import ast
import fnmatch
import hashlib
import json
import os
import re
import subprocess
import sys
import time
from collections import defaultdict

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REFRESH = os.path.join(ROOT, "tools", "refresh.sh")
MANIFEST = os.path.join(ROOT, "handoff", "refresh-manifest.json")

# A directory is recorded as `dir/*` when one step reads (or writes) at least COLLAPSE_AT of its
# files and they are most of it (COLLAPSE_SHARE), or at least COLLAPSE_ALWAYS of them. Sixteen
# platform files in a handoff/ of three hundred stay sixteen paths; a screens/ read in full is
# `screens/*`.
COLLAPSE_AT, COLLAPSE_SHARE, COLLAPSE_ALWAYS = 12, 0.6, 200
# A list longer than this is widened, deepest crowded directory first, into `dir/**` entries --
# the mirror steps touch nine thousand paths, and a scoped run needs the shape, not the census.
GLOB_BUDGET = 80
# Copies, whatever reads them: derive-mirrors and sync-project-bible compare each copy before
# overwriting it, which the trace records as a read, but "project-bible/ is a copy, not a source".
DERIVED_ROOTS = ("repos/*/project-bible/**", "repos/ticvai-docs/**")


# ---------------------------------------------------------------------------------------------
# Parsing refresh.sh into steps
# ---------------------------------------------------------------------------------------------

CD_LINE = 'cd "$(dirname "$0")/.."'


def parse_refresh(path=REFRESH):
    """refresh.sh -> {"preamble": [lines], "items": [...]}.

    An item is `step` (one derive/build command, a heredoc, or a for-loop block), `checks` (the
    run-checks line -- the caller runs the checks itself), `report` (the transition-coverage
    line), `tail` (the tools/ coverage block at the end) or `text` (comments, blanks, echoes).
    """
    with open(path, encoding="utf-8") as fh:
        lines = fh.read().split("\n")
    try:
        cd_at = next(i for i, l in enumerate(lines) if l.strip() == CD_LINE)
    except StopIteration:
        raise SystemExit("refresh.sh has no `%s` line; the parser needs updating" % CD_LINE)
    preamble = lines[:cd_at]
    items, i, n = [], cd_at + 1, 0
    while i < len(lines):
        l = lines[i]
        s = l.strip()
        if s.startswith("_EXCLUDED="):
            items.append({"kind": "tail", "text": "\n".join(lines[i:])})
            break
        if re.match(r"^python3 - <<'?(\w+)'?\s*$", s):
            tag = re.match(r"^python3 - <<'?(\w+)'?", s).group(1)
            j = i + 1
            while j < len(lines) and lines[j].strip() != tag:
                j += 1
            block = lines[i:j + 1]
            n += 1
            body = "\n".join(block)
            m = re.search(r"open\('([^']+)', *'w'", body)
            label = "inline python -> %s" % m.group(1) if m else "inline python"
            items.append({"kind": "step", "index": n, "command": label, "text": body,
                          "tools": []})
            i = j + 1
            continue
        if re.match(r"^for .*; do\s*$", s):
            j = i + 1
            while j < len(lines) and lines[j].strip() != "done":
                j += 1
            block = lines[i:j + 1]
            n += 1
            body = "\n".join(block)
            tools = re.findall(r"tools/([\w.-]+\.py)", body)
            items.append({"kind": "step", "index": n, "command": " ; ".join(
                x.strip() for x in block[1:-1] if x.strip()), "text": body,
                "tools": ["tools/" + t for t in dict.fromkeys(tools)]})
            i = j + 1
            continue
        if s.startswith("python3 tools/run-checks.py"):
            items.append({"kind": "checks", "text": l})
            i += 1
            continue
        if s.startswith("printf") and "audit-transitions" in s:
            items.append({"kind": "report", "text": l})
            i += 1
            continue
        if s.startswith("python3 "):
            n += 1
            cmd = re.sub(r"\s+#.*$", "", s)
            tools = re.findall(r"tools/([\w.-]+\.py)", cmd)
            items.append({"kind": "step", "index": n, "command": cmd, "text": l,
                          "tools": ["tools/" + t for t in tools]})
            i += 1
            continue
        items.append({"kind": "text", "text": l})
        i += 1
    return {"preamble": preamble, "items": items}


def steps_of(parsed):
    return [it for it in parsed["items"] if it["kind"] == "step"]


# ---------------------------------------------------------------------------------------------
# Emitting a runnable script: all steps or a selection, with or without the trace hooks
# ---------------------------------------------------------------------------------------------

HOOK = r'''
# Generated by tools/refresh-manifest.py for a trace run. Records, per process, every file opened
# for reading or writing, every directory listed, and every rename or delete, then writes them to
# $REFRESH_TRACE_DIR at exit. The wrappers are callable objects rather than functions because
# pathlib (3.9) binds os.open/os.scandir as class attributes, and a function there would become
# a bound method.
import os, sys, io, builtins, json, atexit, shutil
_OUT = os.environ.get("REFRESH_TRACE_DIR")
if _OUT:
    _STEP = os.environ.get("REFRESH_TRACE_STEP", "x")
    _R, _W, _L, _D = set(), set(), set(), set()
    _open0, _osopen0 = builtins.open, os.open

    def _p(f):
        try:
            if isinstance(f, int):
                return None
            return os.path.abspath(os.fsdecode(os.fspath(f)))
        except Exception:
            return None

    class _Open:
        def __call__(self, file, mode="r", *a, **k):
            fh = _open0(file, mode, *a, **k)
            p = _p(file)
            if p:
                if any(c in mode for c in "wax"):
                    _W.add(p)
                elif "+" in mode:
                    _W.add(p); _R.add(p)
                else:
                    _R.add(p)
            return fh

    class _OsOpen:
        def __call__(self, path, flags, *a, **k):
            fd = _osopen0(path, flags, *a, **k)
            p = _p(path)
            if p:
                if flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC | os.O_APPEND):
                    _W.add(p)
                else:
                    _R.add(p)
            return fd

    class _List:
        def __init__(self, fn):
            self.fn = fn
        def __call__(self, path=".", *a, **k):
            r = self.fn(path, *a, **k)
            p = _p(path)
            if p:
                _L.add(p)
            return r

    class _Move:
        def __init__(self, fn):
            self.fn = fn
        def __call__(self, src, dst, *a, **k):
            r = self.fn(src, dst, *a, **k)
            ps, pd = _p(src), _p(dst)
            if ps: _D.add(ps)
            if pd: _W.add(pd)
            return r

    class _Del:
        def __init__(self, fn, tree=False):
            self.fn, self.tree = fn, tree
        def __call__(self, path, *a, **k):
            p = _p(path)
            r = self.fn(path, *a, **k)
            if p:
                _D.add(p + (os.sep + "**" if self.tree else ""))
            return r

    builtins.open = io.open = _Open()
    os.open = _OsOpen()
    os.listdir, os.scandir = _List(os.listdir), _List(os.scandir)
    os.rename, os.replace = _Move(os.rename), _Move(os.replace)
    os.remove, os.unlink = _Del(os.remove), _Del(os.unlink)
    shutil.rmtree = _Del(shutil.rmtree, tree=True)

    def _dump():
        try:
            f = os.path.join(_OUT, "step-%s-%d.json" % (_STEP, os.getpid()))
            with _open0(f, "w", encoding="utf-8") as fh:
                json.dump({"step": _STEP, "argv": sys.argv, "cwd": os.getcwd(),
                           "reads": sorted(_R), "writes": sorted(_W), "lists": sorted(_L),
                           "deletes": sorted(_D)}, fh)
        except Exception:
            pass
    atexit.register(_dump)
'''

SNAP = r'''
# --- trace hooks (refresh-manifest.py) -------------------------------------------------------
__snap() {
  # The tree after a step, in a private index and object store: the worktree's own index and the
  # main repository's objects are never written.
  GIT_INDEX_FILE="$REFRESH_TRACE_DIR/index" GIT_OBJECT_DIRECTORY="$REFRESH_TRACE_DIR/objects" \
  GIT_ALTERNATE_OBJECT_DIRECTORIES="$REFRESH_TRACE_ALT" git add -A -- . >/dev/null 2>&1
  GIT_INDEX_FILE="$REFRESH_TRACE_DIR/index" GIT_OBJECT_DIRECTORY="$REFRESH_TRACE_DIR/objects" \
  GIT_ALTERNATE_OBJECT_DIRECTORIES="$REFRESH_TRACE_ALT" git write-tree > "$REFRESH_TRACE_DIR/tree-$1"
  date +%s > "$REFRESH_TRACE_DIR/time-$1"
}
export PYTHONPATH="$REFRESH_TRACE_DIR/hook${PYTHONPATH:+;$PYTHONPATH}"
__snap 0
'''


def emit(parsed, selected, trace, total=None):
    """The script text. `selected` is a set of step indexes (None = all)."""
    steps = steps_of(parsed)
    total = total or len(steps)
    out = ["#!/usr/bin/env bash",
           "# GENERATED by tools/refresh-manifest.py from tools/refresh.sh -- do not edit, do not keep.",
           "# Steps: %s" % ("all" if selected is None else ",".join(map(str, sorted(selected))))]
    out += parsed["preamble"]
    out.append('cd "${REFRESH_TICVAI:?REFRESH_TICVAI must name the ticvai/ directory to refresh}"')
    if trace:
        out.append(SNAP)
    for it in parsed["items"]:
        k = it["kind"]
        if k == "step":
            n = it["index"]
            if selected is not None and n not in selected:
                out.append(": # skipped step %d: %s" % (n, it["command"].replace("\n", " ")[:120]))
                continue
            out.append('echo "== refresh step %d/%d: %s"' % (
                n, total, it["command"].replace('"', "'").replace("$", "")[:110]))
            if trace:
                out.append("export REFRESH_TRACE_STEP=%d" % n)
            out.append(it["text"])
            if trace:
                out.append("__snap %d" % n)
        elif k == "checks":
            if trace:
                out.append("export REFRESH_TRACE_STEP=post")
            out.append(": # run-checks: run and judged by refresh-safe.sh after this script")
        elif k == "report":
            if trace:
                out.append("export REFRESH_TRACE_STEP=post")
            out.append(it["text"] + " || true")
        elif k == "tail":
            # The tools/ coverage block. It fails at the 1 October baseline (tools refresh.sh
            # neither runs nor excuses) and nobody saw, because refresh.sh stops at run-checks
            # first. Its verdict is captured and judged against the baseline like any checker.
            if trace:
                out.append("export REFRESH_TRACE_STEP=post")
            out.append("(\n%s\n) 2>&1 | tee \"${REFRESH_TAIL_OUT:-/dev/null}\" || true"
                       % it["text"].rstrip())
        else:
            out.append(it["text"])
    return "\n".join(out) + "\n"


# ---------------------------------------------------------------------------------------------
# Building the manifest from a trace
# ---------------------------------------------------------------------------------------------

_BASES = {}


def _rel(p, base):
    """Absolute path -> path relative to base with forward slashes, or None if outside.

    Windows hands out two spellings of one directory (`CHINMA~1.PAR` and `Chinmay.Parab`), and a
    traced process reports whichever it was given, so both spellings of the base are tried."""
    if base not in _BASES:
        forms = {os.path.normcase(os.path.abspath(base))}
        try:
            forms.add(os.path.normcase(os.path.realpath(base)))
        except OSError:
            pass
        _BASES[base] = sorted(forms, key=len, reverse=True)
    q = os.path.normcase(os.path.abspath(p))
    for b in _BASES[base]:
        if q == b:
            return ""
        if q.startswith(b.rstrip("\\/") + os.sep):
            # keep the original spelling's case for the relative part
            return os.path.abspath(p)[len(b.rstrip("\\/")) + 1:].replace("\\", "/")
    return None


def _is_noise(rel):
    parts = rel.split("/")
    return "__pycache__" in parts or rel.endswith((".pyc", ".pyo")) or "/.git/" in "/" + rel + "/"


_SUBDIRS = {}
_NFILES = {}


def _nfiles(full):
    if full not in _NFILES:
        try:
            _NFILES[full] = sum(1 for e in os.scandir(full) if e.is_file())
        except OSError:
            _NFILES[full] = 0
    return _NFILES[full]


def _subdirs(full):
    if full not in _SUBDIRS:
        try:
            _SUBDIRS[full] = [e.name for e in os.scandir(full) if e.is_dir()
                              and e.name not in ("__pycache__", ".git")]
        except OSError:
            _SUBDIRS[full] = None
    return _SUBDIRS[full]


def _ancestors(p):
    while p:
        p = p.rsplit("/", 1)[0] if "/" in p else ""
        yield p


def collapse(files, dirs, pkg, at=COLLAPSE_AT):
    """Exact files + listed dirs -> sorted globs (`path`, `dir/*`, `dir/**`). Always widens."""
    dirset = set(dirs)
    by_parent = defaultdict(list)
    for f in files:
        by_parent[_parent(f)].append(f)
    for parent, fs in by_parent.items():
        n = len(fs)
        if n >= COLLAPSE_ALWAYS or n >= at and                 n >= COLLAPSE_SHARE * _nfiles(os.path.join(pkg, parent) if parent else pkg):
            dirset.add(parent)
    # A listed directory whose every subdirectory (at trace time) is also covered is a subtree.
    memo, tree = {}, set()

    def covered(d):
        if d in memo:
            return memo[d]
        memo[d] = False                                    # recursion guard
        if d not in dirset:
            return False
        subs = _subdirs(os.path.join(pkg, d) if d else pkg)
        if subs is None:
            return False
        ok = all([covered((d + "/" if d else "") + x) for x in subs])
        if ok and subs:
            tree.add(d)
        memo[d] = ok
        return ok

    for d in sorted(dirset, key=lambda x: x.count("/"), reverse=True):
        covered(d)
    globs = set()
    for d in dirset:
        if any(x in tree for x in _ancestors(d)):
            continue
        globs.add(((d + "/**") if d else "**") if d in tree else ((d + "/*") if d else "*"))
    for f in files:
        if _parent(f) in dirset or any(x in tree for x in _ancestors(f)):
            continue
        globs.add(f)
    return budget(globs)


def budget(globs, limit=GLOB_BUDGET):
    """Widen a long list: the deepest directory holding 10+ entries becomes `dir/**`, repeatedly."""
    globs = set(globs)
    while len(globs) > limit:
        under = defaultdict(int)
        for g in globs:
            k, p = _kind(g)
            for a in _ancestors(p if k == "file" else p + "/x"):
                if a:
                    under[a] += 1
        cands = [a for a, c in under.items() if c >= 10] or                 [max(under, key=lambda a: under[a])] if under else []
        if not cands:
            break
        a = max(cands, key=lambda a: (a.count("/"), under[a]))
        globs = {g for g in globs if not _under(_kind(g)[1], a)} | {a + "/**"}
    return sorted(globs)


class GlobSet:
    """A set of manifest globs that answers "does any of these overlap X" without a pairwise
    scan -- derive-mirrors alone reads and writes tens of thousands of paths."""

    def __init__(self, globs):
        self.files, self.dirs, self.trees = set(), set(), set()
        for g in globs:
            k, p = _kind(g.lower())
            (self.files if k == "file" else self.dirs if k == "dir" else self.trees).add(p)
        self.file_parents = {_parent(f) for f in self.files}
        self.tree_parents = {_parent(t) for t in self.trees if t}
        self.all_sorted = sorted(self.files | self.dirs | self.trees)

    def _any_under(self, t):
        if t == "":
            return bool(self.all_sorted)
        import bisect
        i = bisect.bisect_left(self.all_sorted, t)
        while i < len(self.all_sorted):
            x = self.all_sorted[i]
            if x == t or x.startswith(t + "/"):
                return True
            if x > t + "/￿":
                break
            i += 1
        return False

    def hits(self, g):
        k, p = _kind(g.lower())
        if any(a in self.trees for a in _ancestors(p)) or p in self.trees:
            return True
        if k == "file":
            return p in self.files or _parent(p) in self.dirs
        if k == "dir":
            return p in self.dirs or p in self.file_parents or p in self.tree_parents
        # a subtree: anything inside it, or a listing of the directory that holds it
        return self._any_under(p) or (p != "" and _parent(p) in self.dirs)

    def overlaps(self, globs):
        return any(self.hits(g) for g in globs)


def _kind(p):
    if p.endswith("/**") or p == "**":
        return "tree", p[:-3] if p != "**" else ""
    if p.endswith("/*") or p == "*":
        return "dir", p[:-2] if p != "*" else ""
    return "file", p


def _parent(p):
    return p.rsplit("/", 1)[0] if "/" in p else ""


def _under(p, d):
    return d == "" or p == d or p.startswith(d + "/")


def match(a, b):
    """Do two manifest globs overlap? Case-insensitive, because the package lives on Windows."""
    ka, pa = _kind(a.lower())
    kb, pb = _kind(b.lower())
    if ka == "file" and kb == "file":
        return pa == pb or fnmatch.fnmatchcase(pa, pb) or fnmatch.fnmatchcase(pb, pa)
    if ka != "file" and kb == "file":
        ka, pa, kb, pb = kb, pb, ka, pa
    if ka == "file":
        if kb == "dir":
            return _parent(pa) == pb
        return _under(pa, pb)
    if ka == "dir" and kb == "dir":
        return pa == pb
    if ka == "tree" and kb == "tree":
        return _under(pa, pb) or _under(pb, pa)
    if ka == "tree":
        ka, pa, kb, pb = kb, pb, ka, pa
    # dir vs tree: the listed directory is inside the subtree, or the subtree's root is one of
    # the directory's entries (created or removed, it changes the listing)
    return _under(pa, pb) or _parent(pb) == pa


def local_imports(tool_path, pkg):
    """tools/*.py a tool imports or loads by path -- a change to them changes the step."""
    out = set()
    try:
        src = open(tool_path, encoding="utf-8").read()
    except Exception:
        return out
    here = os.path.join(pkg, "tools")
    for m in re.finditer(r"^\s*(?:from|import)\s+([A-Za-z_][\w]*)", src, re.M):
        if os.path.isfile(os.path.join(here, m.group(1) + ".py")):
            out.add("tools/%s.py" % m.group(1))
    for line in src.split("\n"):
        if line.lstrip().startswith("#"):
            continue
        if "spec_from_file_location" not in line and \
                not re.search(r'"tools"\s*/\s*"[\w.-]+\.py"', line):
            continue
        for name in re.findall(r"([\w.-]+\.py)", line):
            if os.path.isfile(os.path.join(here, name)):
                out.add("tools/" + name)
    return out


_COP = {}


def static_io(tool_path, pkg):
    """(reads, writes, unresolved-write count, shells out) from check-output-paths' AST scan,
    which follows module constants (`H = ROOT / "handoff"`) -- the same resolution the package
    already trusts for its own output-path check. Directories become subtrees."""
    if pkg not in _COP:
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "check_output_paths", os.path.join(pkg, "tools", "check-output-paths.py"))
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        _COP[pkg] = mod
    try:
        w, r, dyn = _COP[pkg].scan(tool_path)
    except Exception:
        return set(), set(), 1, True
    tops = {e.name for e in os.scandir(pkg)}

    def keep(p):
        p = p.replace("\\", "/").strip("/")
        if not p or p.split("/")[0] not in tops or " " in p:
            return None
        if "*" in p:
            return _parent(p) + "/*"
        full = os.path.join(pkg, p)
        if os.path.isdir(full):
            return p + "/**"
        return p
    reads = {k for k in map(keep, r) if k}
    writes = {k for k in map(keep, w) if k}
    try:
        src = open(tool_path, encoding="utf-8").read()
    except OSError:
        src = ""
    shells = bool(re.search(r"\bsubprocess\b|os\.system\(", src))
    return reads, writes, dyn.get("write", 0), shells


def git_changed(worktree, trace_dir, a, b):
    env = dict(os.environ, GIT_OBJECT_DIRECTORY=os.path.join(trace_dir, "objects"),
               GIT_ALTERNATE_OBJECT_DIRECTORIES=open(os.path.join(trace_dir, "alt"),
                                                     encoding="utf-8").read().strip())
    p = subprocess.run(["git", "-C", worktree, "diff-tree", "-r", "--no-renames", "--name-only",
                        "-z", a, b], capture_output=True, env=env)
    if p.returncode != 0:
        return None
    return [x for x in p.stdout.decode("utf-8", "replace").split("\0") if x]


def build(trace_dir, pkg, commit, out_path, parsed):
    pkg = os.path.abspath(pkg)
    worktree = os.path.dirname(pkg)
    pkg_prefix = _rel(pkg, worktree) + "/"
    steps = steps_of(parsed)
    traces = defaultdict(list)
    for f in os.listdir(trace_dir):
        m = re.match(r"step-(\d+)-\d+\.json$", f)
        if m:
            with open(os.path.join(trace_dir, f), encoding="utf-8") as fh:
                traces[int(m.group(1))].append(json.load(fh))
    trees = {}
    times = {}
    for f in os.listdir(trace_dir):
        m = re.match(r"(tree|time)-(\d+)$", f)
        if m:
            v = open(os.path.join(trace_dir, f), encoding="utf-8").read().strip()
            (trees if m.group(1) == "tree" else times)[int(m.group(2))] = v

    rows, prev = [], 0
    for st in steps:
        n = st["index"]
        reads, writes, lists, dels, external = set(), set(), set(), set(), set()
        for t in traces.get(n, []):
            for key, bucket in (("reads", reads), ("writes", writes), ("lists", lists),
                                ("deletes", dels)):
                for p in t[key]:
                    tree_del = p.endswith(os.sep + "**")
                    p0 = p[:-3] if tree_del else p
                    r = _rel(p0, pkg)
                    if r is None:
                        rr = _rel(p0, worktree)
                        if rr is not None and key != "lists":
                            external.add(rr)
                        continue
                    if _is_noise(r):
                        continue
                    bucket.add(r + ("/**" if tree_del else ""))
        changed = None
        if n in trees and prev in trees:
            ch = git_changed(worktree, trace_dir, trees[prev], trees[n])
            if ch is not None:
                changed = {c[len(pkg_prefix):] for c in ch if c.startswith(pkg_prefix)}
        if n in trees:
            prev = n
        # a file both opened for writing and later deleted (a temp file) is not an output
        tmp = {w for w in writes if w in dels and not os.path.exists(os.path.join(pkg, w))}
        writes -= tmp
        untraced = sorted((changed or set()) - writes - {d for d in dels if "*" not in d})
        writes |= set(changed or ())
        deleted = sorted(d for d in dels if d not in tmp)
        # the tool's own source and what it imports
        src_reads = set()
        s_reads, s_writes, dyn_w, shells = set(), set(), 0, False
        for tool in st["tools"]:
            src_reads.add(tool)
            src_reads |= local_imports(os.path.join(pkg, tool), pkg)
            r_, w_, d_, sh_ = static_io(os.path.join(pkg, tool), pkg)
            s_reads |= r_
            s_writes |= w_
            dyn_w += d_
            shells = shells or sh_
        if not st["tools"]:
            # inline python: its literals straight from the script text
            for m in re.finditer(r"open\('([^']+)'(, *'w')?", st["text"]):
                c = m.group(1)
                (s_writes if m.group(2) else s_reads).add(c)
            for m in re.finditer(r"glob\('([^']+)'\)", st["text"]):
                s_reads.add(_parent(m.group(1)) + "/*")
        traced_r = collapse(reads, lists, pkg)
        traced_w = collapse(writes, set(), pkg)
        # A resolved path the trace never saw is a branch the traced run did not take: a write
        # made only when there is something to add, a fallback file. Added -- wider is safe --
        # and it costs confidence.
        seen_rw, seen_w = GlobSet(traced_r + traced_w), GlobSet(traced_w)
        static_only_r = sorted(x for x in s_reads - s_writes if not seen_rw.hits(x))
        static_only_w = sorted(x for x in s_writes if not seen_w.hits(x))
        static_only = static_only_r + ["(write) " + x for x in static_only_w]
        read_globs = sorted(set(collapse(reads | src_reads, lists, pkg)) | set(static_only_r))
        write_globs = sorted(set(traced_w) | set(static_only_w))
        wg = GlobSet(write_globs)
        write_globs += [d for d in deleted if not wg.hits(d)]
        external = {e for e in external if not _is_noise(e)}
        # files this step opened AND wrote: an in-place edit or an additive register, whose old
        # content survives the step -- the mark of an authored file (classify, below)
        self_reads = collapse({w for w in writes if w in reads}, set(), pkg)
        assumed = False
        if not writes and dyn_w and not static_only_w and traces.get(n):
            # It writes through paths built at run time and had nothing to do when traced. Assume
            # it may rewrite anything it reads (outside tools/): wider, so never a skipped step.
            write_globs = sorted(g for g in read_globs if not g.startswith("tools/"))
            self_reads = list(write_globs)
            assumed = True
        why = []
        if not traces.get(n):
            conf = "low"
            why.append("no trace recorded for this step")
        elif untraced:
            conf = "low"
            why.append("%d file(s) changed that the hook did not see written" % len(untraced))
        elif assumed:
            conf = "low"
            why.append("writes through a path built at run time and wrote nothing when traced; "
                       "its writes are assumed to be everything it reads")
        elif static_only or shells or external:
            conf = "medium"
            if static_only_r:
                why.append("%d path(s) the source names that the traced run did not read "
                           "(added as reads)" % len(static_only_r))
            if static_only_w:
                why.append("%d path(s) the source writes that the traced run did not "
                           "(added as writes)" % len(static_only_w))
            if shells:
                why.append("shells out (git or a subprocess); reads there are not traced")
            if external:
                why.append("reads outside ticvai/: %s" % ", ".join(sorted(external)[:4]))
        else:
            conf = "high"
        dur = None
        earlier = [k for k in times if k < n]
        if n in times and earlier:
            try:
                dur = int(times[n]) - int(times[max(earlier)])
            except ValueError:
                pass
        rows.append({
            "step": n,
            "command": st["command"],
            "tools": st["tools"],
            "reads": sorted(set(read_globs)),
            "writes": sorted(set(write_globs)),
            "self_reads": sorted(set(self_reads)),
            "changed_in_trace": len(changed or ()),
            "confidence": conf,
            "why": why,
            "static_only": static_only,
            "untraced_changes": untraced[:50],
            "external_reads": sorted(external),
            "seconds": dur,
            "processes": len(traces.get(n, [])),
        })

    # feedback: a step reading what a later step writes (the previous run's output)
    wsets = {r["step"]: GlobSet(r["writes"]) for r in rows}
    for r in rows:
        r["reads_output_of_later_steps"] = [
            later["step"] for later in rows
            if later["step"] > r["step"] and wsets[later["step"]].overlaps(r["reads"])]

    doc = {
        "generated_by": "tools/refresh-manifest.py",
        "note": ("What each step of tools/refresh.sh reads and writes, measured by tracing a full "
                 "refresh in a throwaway worktree. Used by `refresh-safe.sh --changed` to run only "
                 "the steps downstream of a change. A scoped run is not a release: a full "
                 "refresh is required before a release tag. Rebuild with "
                 "`python3 tools/refresh-manifest.py rebuild` whenever refresh.sh changes."),
        "traced_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "commit": commit,
        "refresh_sh_sha1": hashlib.sha1(open(os.path.join(pkg, "tools", "refresh.sh"), "rb")
                                        .read()).hexdigest(),
        "steps_signature": signature(parsed),
        "python": sys.version.split()[0],
        "glob_forms": {"path": "one file", "dir/*": "the directory's direct children, and "
                       "listing it", "dir/**": "the subtree"},
        "summary": {
            "steps": len(rows),
            "confidence": {c: sum(1 for r in rows if r["confidence"] == c)
                           for c in ("high", "medium", "low")},
            "steps_reading_later_outputs": sum(1 for r in rows if r["reads_output_of_later_steps"]),
            "traced_seconds": sum(r["seconds"] or 0 for r in rows),
        },
        "derived_roots": list(DERIVED_ROOTS),
        "post": ["tools/run-checks.py (every checker; judged by refresh-safe.sh against "
                 "tools/refresh-safe-baseline.json)",
                 "audit-transitions coverage line", "tools/ coverage block"],
        "steps": rows,
    }
    with open(out_path, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(doc, fh, indent=1, ensure_ascii=False)
        fh.write("\n")
    return doc


def signature(parsed):
    return hashlib.sha1("\n".join(s["command"] for s in steps_of(parsed))
                        .encode("utf-8")).hexdigest()


# ---------------------------------------------------------------------------------------------
# Using the manifest
# ---------------------------------------------------------------------------------------------

def norm_changed(paths, pkg=ROOT):
    """User paths (absolute, repo-relative `ticvai/...`, or package-relative) -> manifest globs."""
    pkg = os.path.abspath(pkg)
    out = []
    for p in paths:
        q = p.replace("\\", "/").rstrip("/")
        a = os.path.abspath(q) if (os.path.isabs(q) or re.match(r"^[A-Za-z]:/", q)) else None
        if a is None:
            if q.startswith("ticvai/"):
                q = q[len("ticvai/"):]
            a = os.path.join(pkg, q)
        r = _rel(a, pkg)
        if r is None:
            raise SystemExit("not inside ticvai/: %s" % p)
        if r == "" or os.path.isdir(a):
            out.append((r + "/**") if r else "**")
        else:
            out.append(r)
    return out


def select(manifest, changed):
    """Steps a change reaches, in refresh order: a step runs when it reads something changed, and
    what it writes is then changed for every step after it. One pass, like a full refresh."""
    live = list(changed)
    picked, why = [], {}
    for r in manifest["steps"]:
        rs = GlobSet(r["reads"])
        c = next((c for c in live if rs.hits(c)), None)
        if c is not None:
            g = next((g for g in r["reads"] if match(c, g)), "?")
            picked.append(r["step"])
            why[r["step"]] = (c, g)
            live.extend(r["writes"])
    return picked, why


def classify(manifest, paths):
    """`derived`: a step writes it and no step that writes it opened it first -- so its old
    content does not survive a refresh, and a refresh from HEAD regenerates it (the mirrors are
    derived by rule, DERIVED_ROOTS). `authored`: nothing writes it (docs, sources, anything
    unknown), or a writer edits it in place or adds to it (screens, contracts, the lineage, the
    id register), so an uncommitted edit would change what the refresh produces.

    A derived file an EARLIER step reads (the previous run's screen-index, read by
    derive-relationships) is still derived: a refresh from HEAD reads HEAD's copy, which is what a
    refresh of the committed package means."""
    roots = [r.lower()[:-3] + "/*" if r.endswith("/**") else r.lower()
             for r in manifest.get("derived_roots") or DERIVED_ROOTS]
    sets = [(GlobSet(r["writes"]), GlobSet(r.get("self_reads") or [])) for r in manifest["steps"]]
    out = {}
    for p in paths:
        if any(fnmatch.fnmatch(p.lower(), r) for r in roots):     # fnmatch's * crosses "/"
            out[p] = "derived"
            continue
        writers = [sr for w, sr in sets if w.hits(p)]
        if not writers or any(sr.hits(p) for sr in writers):
            out[p] = "authored"
        else:
            out[p] = "derived"
    return out


def load_manifest(path=MANIFEST):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd")
    sub.add_parser("steps")
    e = sub.add_parser("emit")
    e.add_argument("--refresh", default=REFRESH)
    e.add_argument("--steps", default="all")
    e.add_argument("--trace", action="store_true")
    e.add_argument("--out", required=True)
    e.add_argument("--hook-dir")
    b = sub.add_parser("build")
    b.add_argument("--trace-dir", required=True)
    b.add_argument("--pkg", required=True)
    b.add_argument("--commit", default="")
    b.add_argument("--out", required=True)
    s = sub.add_parser("select")
    s.add_argument("paths", nargs="+")
    s.add_argument("--manifest", default=MANIFEST)
    s.add_argument("--refresh", default=REFRESH)
    s.add_argument("--csv", action="store_true", help="print only the comma-separated step list")
    c = sub.add_parser("classify")
    c.add_argument("paths", nargs="*")
    c.add_argument("--manifest", default=MANIFEST)
    c.add_argument("--stdin0", action="store_true", help="paths NUL-separated on stdin")
    r = sub.add_parser("rebuild")
    r.add_argument("--wt-dir")
    r.add_argument("--include-working", action="store_true")
    a = ap.parse_args()

    if a.cmd == "steps":
        for st in steps_of(parse_refresh()):
            print("%3d  %s" % (st["index"], st["command"]))
        return 0

    if a.cmd == "emit":
        parsed = parse_refresh(a.refresh)
        sel = None if a.steps == "all" else {int(x) for x in a.steps.split(",") if x.strip()}
        with open(a.out, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(emit(parsed, sel, a.trace))
        if a.trace:
            os.makedirs(a.hook_dir, exist_ok=True)
            with open(os.path.join(a.hook_dir, "sitecustomize.py"), "w", encoding="utf-8",
                      newline="\n") as fh:
                fh.write(HOOK)
        return 0

    if a.cmd == "build":
        parsed = parse_refresh(os.path.join(a.pkg, "tools", "refresh.sh"))
        doc = build(a.trace_dir, a.pkg, a.commit, a.out, parsed)
        sm = doc["summary"]
        print("refresh-manifest: %d steps · confidence high %d / medium %d / low %d · "
              "%d step(s) read a later step's output"
              % (sm["steps"], sm["confidence"]["high"], sm["confidence"]["medium"],
                 sm["confidence"]["low"], sm["steps_reading_later_outputs"]))
        return 0

    if a.cmd == "select":
        m = load_manifest(a.manifest)
        parsed = parse_refresh(a.refresh)
        if m.get("steps_signature") != signature(parsed):
            print("refresh-manifest.json was traced against a different refresh.sh step list; "
                  "rebuild it (python3 tools/refresh-manifest.py rebuild) or run a full refresh",
                  file=sys.stderr)
            return 3
        changed = norm_changed(a.paths)
        if any(match(c, "tools/refresh.sh") for c in changed if not c.endswith("**")) or \
                "**" in changed:
            print("refresh.sh itself (or the whole package) changed: that is a full run",
                  file=sys.stderr)
            return 4
        picked, why = select(m, changed)
        if a.csv:
            print(",".join(map(str, picked)))
            return 0
        by = {r["step"]: r for r in m["steps"]}
        print("changed: %s" % ", ".join(changed))
        print("%d of %d steps reached:" % (len(picked), len(m["steps"])))
        for n in picked:
            c, g = why[n]
            print("  %3d  %-60s  [%s]  via %s ~ %s"
                  % (n, by[n]["command"][:60], by[n]["confidence"], c, g))
        return 0

    if a.cmd == "classify":
        paths = list(a.paths)
        if a.stdin0:
            paths += [p for p in sys.stdin.buffer.read().decode("utf-8").split("\0") if p]
        try:
            m = load_manifest(a.manifest)
        except (OSError, ValueError):
            m = None
        for p in paths:
            q = p[len("ticvai/"):] if p.startswith("ticvai/") else p
            kind = classify(m, [q])[q] if m else "authored"
            print("%s\t%s" % (kind, p))
        return 0

    if a.cmd == "rebuild":
        cmd = ["bash", os.path.join(ROOT, "tools", "refresh-safe.sh"), "--trace", "--no-merge",
               "--skip-checks", "--manifest-out", MANIFEST]
        if a.wt_dir:
            cmd += ["--wt-dir", a.wt_dir]
        # HEAD unless told otherwise: the shape of the pipeline is what is being measured, and
        # somebody's half-made edit in the main tree is not part of it
        cmd.append("--include-working" if a.include_working else "--head-only")
        return subprocess.call(cmd)

    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
