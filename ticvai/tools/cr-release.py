#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The light change-request release: a merged class fix reaches developers in minutes (CHG-LCR-001).

Self-tests run first, every time; `self-test` runs only them.

    python3 tools/cr-release.py self-test
"""
from __future__ import annotations

import argparse
import json
import os
import posixpath
import re
import subprocess
import sys
import time
from pathlib import Path

PKG = Path(__file__).resolve().parents[1]           # ticvai/
REPO = PKG.parent                                   # the repository: ticvai/, viewer/, audit/ (gitignored)
LINKS = "ticvai/handoff/service-docs/adam-links.json"
PMS_MAP = "ticvai/handoff/service-docs/pms-map.json"
SCHEMA_REF = "ticvai/handoff/schema-reference.json"
REMOTES = ("origin", "github")
RELEASE_TAG = re.compile(r"^r([1-9]\d*)$")
METHODS = ("get", "put", "post", "delete", "options", "head", "patch", "trace")
ADR_FILE = re.compile(r"^docs/adr/(\d{4})-[^/]+\.md$")
# The statuses a ticket can be in, as OpenProject names them. Started: anything else but Rejected (lane D ruling 2:
# "a task or sub-task in any status except New, On hold, Rejected").
NOT_STARTED = {"New", "On hold"}
FINISHED = {"Ready for QA", "Closed", "Done", "Resolved"}
SKIPPED = {"Rejected"}
# Every backend task links its service, so one changed operation would name the whole service: service links are
# never used to select tickets (an operation, table or screen link does that).
IMPACT_KINDS = ("operation", "table", "screen", "file", "adr")


# ---------------------------------------------------------------------------------------------------------------------
# Release numbering
# ---------------------------------------------------------------------------------------------------------------------

def release_numbers(tags):
    """The numbers of the release tags (`r<N>` only: `r6-rc`, `r06` and the like are not releases), sorted."""
    return sorted({int(m.group(1)) for m in (RELEASE_TAG.match(str(t).strip()) for t in tags) if m})


def next_release(local_tags, remote_tags=()):
    """The tag the next release takes: one past the highest release tag here or on a remote."""
    nums = release_numbers(list(local_tags) + list(remote_tags))
    return f"r{(nums[-1] if nums else 0) + 1}"


# ---------------------------------------------------------------------------------------------------------------------
# What changed between two releases, artefact by artefact (pure: the caller reads the files from git)
# ---------------------------------------------------------------------------------------------------------------------

def _str_keys(x):
    if isinstance(x, dict):
        return {str(k): _str_keys(v) for k, v in x.items()}
    if isinstance(x, list):
        return [_str_keys(v) for v in x]
    return x


def _canon(x) -> str:
    """One text per value, to compare two releases' copies. YAML reads `200:` as a number beside `default:`, so keys
    are made text first (json cannot sort mixed keys)."""
    return json.dumps(_str_keys(x), sort_keys=True, default=str)


def _refs(obj, path):
    """Every `$ref` inside obj, as (contract file, section, name); a relative file is resolved against `path`."""
    out = set()
    stack = [obj]
    while stack:
        o = stack.pop()
        if isinstance(o, dict):
            for k, v in o.items():
                if k == "$ref" and isinstance(v, str) and "#/components/" in v:
                    f, _, ptr = v.partition("#")
                    target = posixpath.normpath(posixpath.join(posixpath.dirname(path), f)) if f else path
                    parts = ptr.strip("/").split("/")
                    if len(parts) >= 3:
                        out.add((target, parts[1], parts[2]))
                else:
                    stack.append(v)
        elif isinstance(o, list):
            stack.extend(o)
    return out


def _operations(doc, path):
    """'<contract stem>#<operationId>' -> what defines it: the operation and its path's shared parameters."""
    stem = posixpath.splitext(posixpath.basename(path))[0]
    out = {}
    paths = (doc or {}).get("paths") if isinstance(doc, dict) else None
    for route, item in (paths or {}).items():
        if not isinstance(item, dict):
            continue
        shared = {k: v for k, v in item.items() if k not in METHODS}
        for method in METHODS:
            op = item.get(method)
            if isinstance(op, dict) and op.get("operationId"):
                out[f"{stem}#{op['operationId']}"] = {"route": route, "method": method, "op": op, "shared": shared}
    return out


def _components(doc, path):
    comps = (doc or {}).get("components") if isinstance(doc, dict) else None
    return {(path, sec, name): body for sec, group in (comps or {}).items() if isinstance(group, dict)
            for name, body in group.items()}


def changed_operations(old_docs, new_docs, all_docs):
    """Operations whose definition differs between the releases: edited, added or removed in a changed contract, or
    reaching (through `$ref`, nested, across files) a component that changed. old_docs / new_docs: the changed
    contract files at each release (None where the file did not exist); all_docs: every contract at the new release,
    searched only when a component changed."""
    hit = set()
    changed_comps = set()
    for path in set(old_docs) | set(new_docs):
        old, new = old_docs.get(path), new_docs.get(path)
        o_ops, n_ops = _operations(old, path), _operations(new, path)
        for k in set(o_ops) | set(n_ops):
            if _canon(o_ops.get(k)) != _canon(n_ops.get(k)):
                hit.add(k)
        o_c, n_c = _components(old, path), _components(new, path)
        changed_comps |= {k for k in set(o_c) | set(n_c) if _canon(o_c.get(k)) != _canon(n_c.get(k))}
    if not changed_comps:
        return hit
    docs = dict(all_docs() if callable(all_docs) else all_docs)     # read only now: a component changed
    docs.update({p: d for p, d in new_docs.items() if d is not None})
    comps = {}
    for path, doc in docs.items():
        comps.update({k: _refs(v, path) for k, v in _components(doc, path).items()})
    grew = True
    while grew:                                  # a component that reaches a changed one has changed too
        grew = False
        for k, refs in comps.items():
            if k not in changed_comps and refs & changed_comps:
                changed_comps.add(k)
                grew = True
    for path, doc in docs.items():
        for k, d in _operations(doc, path).items():
            if k not in hit and _refs(d, path) & changed_comps:
                hit.add(k)
    return hit


def changed_screens(old_doc, new_doc):
    """Screen ids whose definition differs between two copies of one screens/P*.yaml (None: no file)."""
    def by_id(doc):
        return {s["id"]: s for s in ((doc or {}).get("screens") or []) if isinstance(s, dict) and s.get("id")}
    o, n = by_id(old_doc), by_id(new_doc)
    return {i for i in set(o) | set(n) if _canon(o.get(i)) != _canon(n.get(i))}


def changed_tables(old_ref, new_ref):
    """Tables whose entry in any table-keyed section of handoff/schema-reference.json differs (cols, origin, storage,
    store, lineage ...); a list section (nomap) names no table."""
    out = set()
    old_ref, new_ref = old_ref or {}, new_ref or {}
    for sec in set(old_ref) | set(new_ref):
        o, n = old_ref.get(sec), new_ref.get(sec)
        o = o if isinstance(o, dict) else {}
        n = n if isinstance(n, dict) else {}
        out |= {t for t in set(o) | set(n) if _canon(o.get(t)) != _canon(n.get(t))}
    return out


def changed_files(paths):
    """File links (paths inside the package, as adam-links.json writes them) and ADRs from the changed paths."""
    files = {p[len("ticvai/"):] for p in paths if p.startswith("ticvai/")}
    adrs = {f"ADR-{m.group(1)}" for m in (ADR_FILE.match(p) for p in files) if m}
    return {"file": files, "adr": adrs}


# ---------------------------------------------------------------------------------------------------------------------
# Impact: the tickets whose links touch a changed artefact
# ---------------------------------------------------------------------------------------------------------------------

def bucket_of(status):
    if status in SKIPPED:
        return None
    if status in FINISHED:
        return "finished"
    if status in NOT_STARTED or not status:
        return "new"
    return "started"


def impact_tickets(links, artefacts, keys_by_id):
    """{tickets: [pull-direct rows + status, bucket, touches], skipped: [...]}: every ticket with a link (of a kind in
    IMPACT_KINDS) to a changed artefact, once, in id order. `role` is the bucket: new, started or finished."""
    want = {k: set(artefacts.get(k) or ()) for k in IMPACT_KINDS}
    hits, info = {}, {}
    for ln in links:
        kind = ln.get("kind")
        if kind in want and ln.get("id") in want[kind]:
            wp = str(ln["key"])
            hits.setdefault(wp, [])
            touch = f"{kind} {ln['id']}"
            if touch not in hits[wp]:
                hits[wp].append(touch)
            info.setdefault(wp, ln)
    tickets, skipped = [], []
    for wp in sorted(hits, key=lambda x: int(x) if x.isdigit() else 0):
        ln = info[wp]
        b = bucket_of(ln.get("status") or "")
        wid = int(wp) if wp.isdigit() else wp
        if b is None:
            skipped.append({"id": wid, "status": ln.get("status")})
            continue
        tickets.append({"id": wid, "key": keys_by_id.get(wp, wp), "role": b, "kind": ln.get("type") or "",
                        "bucket": b, "status": ln.get("status") or "", "subject": ln.get("subject") or "",
                        "assignee": ln.get("assignee") or "", "touches": sorted(hits[wp])})
    return {"tickets": tickets, "skipped": skipped}


# ---------------------------------------------------------------------------------------------------------------------
# Self-tests: made-up tags, contracts, screens, tables and links the functions must read right. No git, no network.
# ---------------------------------------------------------------------------------------------------------------------

def _op(summary, ref=None, params=None):
    op = {"operationId": None, "summary": summary, "responses": {"200": {"description": "ok"}}}
    if ref:
        op["responses"]["200"]["content"] = {"application/json": {"schema": {"$ref": ref}}}
    if params:
        op["parameters"] = params
    return op


def _contract(ops, schemas=None, path_params=None):
    paths = {}
    for i, (op_id, op) in enumerate(ops.items()):
        op = dict(op, operationId=op_id)
        item = {"get" if i % 2 == 0 else "post": op}
        if path_params and op_id in path_params:
            item["parameters"] = path_params[op_id]
        paths[f"/x/{op_id}"] = item
    return {"openapi": "3.0.3", "paths": paths, "components": {"schemas": schemas or {}}}


SELF_TESTS = [0]


def self_test() -> list:
    """Each rule against made-up input it must read right. Returns the failures."""
    fails = []

    def case(name, got, want):
        SELF_TESTS[0] += 1
        if got != want:
            fails.append(f"{name}: got {got!r}, expected {want!r}")

    # -- tag numbering --------------------------------------------------------------------------------------------
    try:
        case("only r<N> tags count, numerically", release_numbers(["r1", "r10", "r6-rc", "rx", "r2", "v3", "r06", "r6"]),
             [1, 2, 6, 10])
        case("next after r6 with an r6-rc beside it", next_release(["r1", "r6", "r6-rc", "r5"]), "r7")
        case("a remote ahead of the workstation wins", next_release(["r6"], ["r6", "r7"]), "r8")
        case("no tag at all", next_release([]), "r1")
        case("a gap is not filled", next_release(["r1", "r3"]), "r4")
    except Exception as e:  # noqa: BLE001
        fails.append(f"tag numbering raised {type(e).__name__}: {e}")

    # -- operations -----------------------------------------------------------------------------------------------
    try:
        a_old = _contract({"getA": _op("A"), "getB": _op("B", "#/components/schemas/Bee"), "gone": _op("G"),
                           "getC": _op("C", "#/components/schemas/Wrap"), "getP": _op("P")},
                          {"Bee": {"type": "object"}, "Wrap": {"properties": {"b": {"$ref": "#/components/schemas/Bee"}}},
                           "Other": {"type": "string"}},
                          path_params={"getP": [{"name": "p", "in": "query"}]})
        a_new = _contract({"getA": _op("A edited"), "getB": _op("B", "#/components/schemas/Bee"),
                           "getC": _op("C", "#/components/schemas/Wrap"), "getP": _op("P"), "added": _op("N")},
                          {"Bee": {"type": "object", "required": ["id"]},
                           "Wrap": {"properties": {"b": {"$ref": "#/components/schemas/Bee"}}},
                           "Other": {"type": "string"}},
                          path_params={"getP": [{"name": "p", "in": "header"}]})
        # an unchanged file whose operation reaches the changed shared schema across files
        shared_old = {"components": {"schemas": {"Problem": {"type": "object"}, "Money": {"type": "number"}}}}
        shared_new = {"components": {"schemas": {"Problem": {"type": "object", "title": "now"},
                                                 "Money": {"type": "number"}}}}
        b_doc = _contract({"getX": _op("X", "../shared/common.yaml#/components/schemas/Problem"),
                           "getY": _op("Y", "../shared/common.yaml#/components/schemas/Money")})
        old_docs = {"contracts/spine/a.yaml": a_old, "contracts/shared/common.yaml": shared_old}
        new_docs = {"contracts/spine/a.yaml": a_new, "contracts/shared/common.yaml": shared_new}
        all_docs = dict(new_docs, **{"contracts/satellite/b.yaml": b_doc})
        case("operations: edited, added, removed, through a component, through a nested component, a path "
             "parameter, and across files",
             sorted(changed_operations(old_docs, new_docs, all_docs)),
             ["a#added", "a#getA", "a#getB", "a#getC", "a#getP", "a#gone", "b#getX"])
        case("operations: a new file is all new", sorted(changed_operations(
            {"contracts/spine/n.yaml": None}, {"contracts/spine/n.yaml": _contract({"one": _op("1")})}, {})),
            ["n#one"])
        mixed = {"paths": {"/m": {"get": {"operationId": "m", "responses": {200: {"d": 1}, "default": {"d": 2}}}}}}
        mixed2 = {"paths": {"/m": {"get": {"operationId": "m", "responses": {200: {"d": 1}, "default": {"d": 3}}}}}}
        case("operations: response codes as numbers beside 'default' (YAML reads 200 as a number)",
             changed_operations({"contracts/spine/m.yaml": mixed}, {"contracts/spine/m.yaml": mixed2}, {}), {"m#m"})
        case("operations: nothing changed", changed_operations({"contracts/spine/a.yaml": a_old},
                                                               {"contracts/spine/a.yaml": a_old}, {}), set())
    except Exception as e:  # noqa: BLE001
        fails.append(f"changed_operations raised {type(e).__name__}: {e}")

    # -- screens, tables, files -------------------------------------------------------------------------------------
    try:
        s_old = {"screens": [{"id": "BO-1", "title": "a"}, {"id": "BO-2", "title": "b"}, {"id": "BO-3"}]}
        s_new = {"screens": [{"id": "BO-1", "title": "a"}, {"id": "BO-2", "title": "B"}, {"id": "BO-4"}]}
        case("screens: edited, removed, added", sorted(changed_screens(s_old, s_new)), ["BO-2", "BO-3", "BO-4"])
        case("screens: a new file", sorted(changed_screens(None, s_old)), ["BO-1", "BO-2", "BO-3"])
        r_old = {"cols": {"s.a": ["id"], "s.b": ["id"], "s.c": ["id"]}, "storage": {"s.a": "rls"},
                 "nomap": ["x"], "lineage": {"s.c": {"w": 1}}}
        r_new = {"cols": {"s.a": ["id"], "s.b": ["id", "name"], "s.c": ["id"], "s.d": ["id"]},
                 "storage": {"s.a": "rls+"}, "nomap": ["y"], "lineage": {"s.c": {"w": 1}}}
        case("tables: a column, a storage note, a new table; a list section is not a table",
             sorted(changed_tables(r_old, r_new)), ["s.a", "s.b", "s.d"])
        case("files: paths under ticvai/, ADRs by number, nothing outside the package",
             changed_files(["ticvai/docs/adr/0055-hosts.md", "ticvai/repos/ticvai-docs/setup/README.md",
                            "viewer/api/main.py", "ticvai/contracts/spine/a.yaml"]),
             {"file": {"docs/adr/0055-hosts.md", "repos/ticvai-docs/setup/README.md", "contracts/spine/a.yaml"},
              "adr": {"ADR-0055"}})
    except Exception as e:  # noqa: BLE001
        fails.append(f"screens/tables/files raised {type(e).__name__}: {e}")

    # -- impact: artefacts -> tickets, split by status --------------------------------------------------------------
    try:
        def L(key, kind, i, status, typ="Task", subject="s", assignee="Pat"):
            return {"key": key, "kind": kind, "id": i, "status": status, "type": typ, "subject": subject,
                    "assignee": assignee}
        links = [L("10", "operation", "a#getA", "New"), L("10", "table", "s.b", "New"),
                 L("11", "operation", "a#getA", "In progress"), L("12", "table", "s.b", "Ready for QA"),
                 L("13", "screen", "BO-2", "Closed", "Sub Task"), L("14", "operation", "a#getA", "Rejected"),
                 L("15", "service", "AService", "In progress"),          # a service link never selects a ticket
                 L("16", "operation", "a#untouched", "Ready for QA"), L("17", "adr", "ADR-0055", "On hold", "Feature"),
                 L("18", "file", "docs/adr/0055-hosts.md", "Developed")]
        arts = {"operation": {"a#getA"}, "table": {"s.b"}, "screen": {"BO-2"}, "service": {"AService"},
                "adr": {"ADR-0055"}, "file": {"docs/adr/0055-hosts.md"}}
        got = impact_tickets(links, arts, {"10": "T-10", "12": "T-12", "13": "T-12#ui"})
        by = {t["id"]: t for t in got["tickets"]}
        case("impact: the tickets hit, once each, in id order", [t["id"] for t in got["tickets"]],
             [10, 11, 12, 13, 17, 18])
        case("impact: a ticket hit twice lists both", by.get(10, {}).get("touches"),
             ["operation a#getA", "table s.b"])
        case("impact: buckets", {b: [t["id"] for t in got["tickets"] if t["bucket"] == b]
                                 for b in ("new", "started", "finished")},
             {"new": [10, 17], "started": [11, 18], "finished": [12, 13]})
        case("impact: Rejected is skipped, and said", got["skipped"], [{"id": 14, "status": "Rejected"}])
        case("impact: pull-direct shape", {k: by.get(13, {}).get(k) for k in ("id", "key", "role", "kind")},
             {"id": 13, "key": "T-12#ui", "role": "finished", "kind": "Sub Task"})
        case("impact: a ticket with no plan key keeps its id as key", by.get(11, {}).get("key"), "11")
    except Exception as e:  # noqa: BLE001
        fails.append(f"impact_tickets raised {type(e).__name__}: {e}")
    return fails


def run_self_tests(quiet=False) -> bool:
    fails = self_test()
    for f in fails:
        print(f"  SELF-TEST    {f}")
    if fails:
        print(f"FAIL {len(fails)} self-test(s)")
        return False
    if not quiet:
        print(f"PASS - {SELF_TESTS[0]} cr-release self-tests")
    return True


# ---------------------------------------------------------------------------------------------------------------------
# Git, the environment, and where a release's files go
# ---------------------------------------------------------------------------------------------------------------------

def git(*args, check=True, cwd=None):
    p = subprocess.run(["git", *args], cwd=str(cwd or REPO), capture_output=True, text=True, encoding="utf-8",
                       errors="replace")
    if check and p.returncode:
        sys.exit(f"cr-release: git {' '.join(args)}: {p.stderr.strip()}")
    return p.stdout


def git_show(ref, path):
    """A file's text at a ref, or None when the file is not there."""
    p = subprocess.run(["git", "show", f"{ref}:{path}"], cwd=str(REPO), capture_output=True)
    return p.stdout.decode("utf-8") if p.returncode == 0 else None


def load_yaml(text):
    if text is None:
        return None
    import yaml
    return yaml.load(text, Loader=getattr(yaml, "CSafeLoader", yaml.SafeLoader))


def load_env(path):
    """KEY=VALUE lines into the environment for the tools this one runs; a key already set wins. Values never printed."""
    p = Path(path)
    if not p.is_file():
        return []
    got = []
    for line in p.read_text(encoding="utf-8").splitlines():
        k, sep, v = line.strip().partition("=")
        if sep and k and not k.startswith("#") and k not in os.environ:
            os.environ[k] = v.strip().strip('"').strip("'")
            got.append(k)
    return got


def resolve_release(release, after_tag):
    """(base, release, head): the release before, the release being made, and the ref that holds it.
    Before the tag (check, impact, tag): base = the newest release tag, release = the next number, head = HEAD.
    After it (after-deploy, rework, settle): release = the newest tag, base = the one below it, head = that tag.
    --release rN names the release instead: base is the highest tag below it, head its tag if it exists, else HEAD."""
    local = git("tag", "-l", "r*").split()
    nums = release_numbers(local)
    if release:
        m = RELEASE_TAG.match(release)
        if not m:
            sys.exit(f"cr-release: --release takes r<N>, not {release}")
        n = int(m.group(1))
        below = [x for x in nums if x < n]
        if not below:
            sys.exit(f"cr-release: no release tag below {release} to compare with")
        return f"r{below[-1]}", release, (release if n in nums else "HEAD")
    if not nums:
        sys.exit("cr-release: no release tag r<N> here (git fetch --tags first)")
    if after_tag:
        if len(nums) < 2:
            sys.exit("cr-release: only one release tag: nothing to compare it with")
        return f"r{nums[-2]}", f"r{nums[-1]}", f"r{nums[-1]}"
    return f"r{nums[-1]}", next_release(local), "HEAD"


def out_dir(args, release):
    d = Path(args.out) if args.out else REPO / "audit" / "ticvai" / "releases" / release
    d.mkdir(parents=True, exist_ok=True)
    return d


def write_json(path, data):
    Path(path).write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")


def head_sha():
    return git("rev-parse", "HEAD").strip()


def show(cmd):
    return " ".join(c if c and not any(ch in c for ch in " \"'") else json.dumps(c) for c in cmd)


def run_shown(cmd, cwd=None, apply=True):
    """Print the command; run it only when apply. Returns the exit code (0 for a command only shown)."""
    print(f"    $ {show(cmd)}" + ("" if cwd is None else f"    (in {Path(cwd).relative_to(REPO).as_posix() or '.'})"))
    if not apply:
        return 0
    return subprocess.run(cmd, cwd=str(cwd or REPO)).returncode


# ---------------------------------------------------------------------------------------------------------------------
# check: the branch is main, clean and pushed, and the gate passes
# ---------------------------------------------------------------------------------------------------------------------

def scoped_flag():
    """Lane C's change-scoped checks, if this checkout has them: '--changed-from' (a file of paths), '--changed', or
    None (then the full refresh runs)."""
    src = (PKG / "tools" / "run-checks.py").read_text(encoding="utf-8")
    if '"--changed-from"' in src:
        return "--changed-from"
    if '"--changed"' in src:
        return "--changed"
    return None


def last_full_run_seconds():
    runs = Path(os.environ.get("TEMP") or os.environ.get("TMPDIR") or "/tmp") / "ticvai-refresh-safe" / "runs"
    try:
        for d in sorted(runs.iterdir(), key=lambda p: p.stat().st_mtime, reverse=True):
            tsv = d / "phases.tsv"
            if tsv.is_file():
                rows = dict(line.split("\t")[:2] for line in tsv.read_text().splitlines()[1:] if "\t" in line)
                if rows.get("total", "").isdigit():
                    return int(rows["total"]), d.name
    except OSError:
        pass
    return None, None


def gate_command(changed_file, json_out):
    flag = scoped_flag()
    if flag == "--changed-from":
        paths = [p for p in Path(changed_file).read_text(encoding="utf-8").split("\n") if p]
        return ("change-scoped checks (lane C's run-checks.py --changed): only the checks that read a changed file",
                [sys.executable, "tools/run-checks.py", "--changed-from", str(changed_file), "--json", str(json_out)],
                len(paths))
    if flag == "--changed":
        paths = [p for p in Path(changed_file).read_text(encoding="utf-8").split("\n") if p]
        return ("change-scoped checks (lane C's run-checks.py --changed): only the checks that read a changed file",
                [sys.executable, "tools/run-checks.py", "--changed", *paths, "--json", str(json_out)], len(paths))
    return ("the full refresh and gate (run-checks.py has no --changed yet: lane C has not merged)",
            ["bash", "tools/refresh-safe.sh", "--head-only", "--no-merge", "--parallel", "4"], None)


def cmd_check(args):
    base, release, _ = resolve_release(args.release, after_tag=False)
    out = out_dir(args, release)
    print(f"cr-release check: {base} -> {release} at HEAD {head_sha()[:9]}; "
          f"{'APPLY: the gate runs' if args.apply else 'dry run (--apply runs the gate)'}")
    refuse = []
    branch = git("rev-parse", "--abbrev-ref", "HEAD").strip()
    if branch != "main":
        refuse.append(f"the branch is {branch}, not main")
    status = git("status", "--porcelain", "--untracked-files=all").splitlines()
    tracked = [l for l in status if not l.startswith("??")]
    untracked_pkg = [l[3:] for l in status if l.startswith("?? ticvai/")]
    other = len(status) - len(tracked) - len(untracked_pkg)
    if tracked:
        refuse.append(f"{len(tracked)} tracked file(s) changed and not committed ({', '.join(l[3:] for l in tracked[:5])})")
    if untracked_pkg:
        refuse.append(f"{len(untracked_pkg)} untracked file(s) in the package ({', '.join(untracked_pkg[:5])})")
    head = head_sha()
    for remote in REMOTES:
        p = subprocess.run(["git", "ls-remote", remote, "refs/heads/main"], cwd=str(REPO), capture_output=True,
                           text=True)
        there = p.stdout.split()[0] if p.returncode == 0 and p.stdout.split() else None
        if there is None:
            refuse.append(f"cannot read main on {remote} ({(p.stderr or 'no answer').strip()[:120]})")
        elif there != head:
            refuse.append(f"HEAD is not what {remote} has on main ({remote} main is {there[:9]}): push first")
    if git("rev-parse", f"{base}^{{commit}}").strip() == head:
        refuse.append(f"HEAD is {base} itself: nothing to release")
    elif subprocess.run(["git", "merge-base", "--is-ancestor", base, "HEAD"], cwd=str(REPO)).returncode:
        refuse.append(f"{base} is not behind HEAD")
    changed = [p for p in git("diff", "--name-only", f"{base}..HEAD").split("\n") if p]
    changed_file = out / "changed.txt"
    changed_file.write_text("\n".join(changed) + "\n", encoding="utf-8")
    print(f"  {len(changed)} file(s) changed since {base} ({sum(p.startswith('ticvai/') for p in changed)} in the "
          f"package) -> {changed_file}")
    cl = subprocess.run([sys.executable, "tools/check-changelog.py", "--since", base], cwd=str(PKG),
                        capture_output=True, text=True, encoding="utf-8", errors="replace")
    last = (cl.stdout.strip().splitlines() or ["(no output)"])[-1]
    print(f"  change log since {base}: {last}")
    if cl.returncode:
        refuse.append(f"check-changelog --since {base} fails: {last}")
    if other:
        print(f"  note: {other} untracked file(s) outside the package (not part of the release)")
    which, cmd, n = gate_command(changed_file, out / "checks.json")
    secs, run = last_full_run_seconds()
    estimate = ("minutes: only what the change reaches" if n is not None else
                f"about {secs // 60} min (the last full run, {run}, took {secs} s)" if secs else "30 to 50 min")
    print(f"  gate: {which}; expect {estimate}")
    for r in refuse:
        print(f"  REFUSE  {r}")
    result = {"head": head, "base": base, "release": release, "gate": which, "command": show(cmd),
              "refused": refuse, "ran": False}
    if refuse:
        write_json(out / "check.json", result)
        run_shown(cmd, cwd=PKG, apply=False)
        print("cr-release check: NOT READY (fix the lines above, then run it again; the gate above runs then)")
        return 1
    started = time.time()
    rc = run_shown(cmd, cwd=PKG, apply=args.apply)
    took = round(time.time() - started)
    if args.apply:
        result.update(ran=True, rc=rc, seconds=took, passed=rc == 0)
        print(f"  gate {'PASSED' if rc == 0 else f'FAILED (exit {rc})'} in {took // 60} min {took % 60} s")
    write_json(out / "check.json", result)
    if not args.apply:
        print("cr-release check: ready to run the gate (--apply)")
        return 0
    return 0 if rc == 0 else 1


# ---------------------------------------------------------------------------------------------------------------------
# impact: the tickets the release touches
# ---------------------------------------------------------------------------------------------------------------------

def release_artefacts(base, head):
    """The changed files and the artefacts whose definitions changed between two refs."""
    changed = [p for p in git("diff", "--name-only", f"{base}..{head}").split("\n") if p]
    pkg = lambda p: p[len("ticvai/"):]
    contracts = [p for p in changed if p.startswith("ticvai/contracts/") and p.endswith((".yaml", ".yml"))]
    old_docs = {pkg(p): load_yaml(git_show(base, p)) for p in contracts}
    new_docs = {pkg(p): load_yaml(git_show(head, p)) for p in contracts}

    def all_docs():
        names = git("ls-tree", "-r", "--name-only", head, "--", "ticvai/contracts").split("\n")
        return {pkg(p): load_yaml(git_show(head, p)) for p in names if p.endswith((".yaml", ".yml"))}

    art = {"operation": changed_operations(old_docs, new_docs, all_docs), "screen": set(), "table": set()}
    for p in changed:
        if re.match(r"^ticvai/screens/P[^/]*\.yaml$", p):
            art["screen"] |= changed_screens(load_yaml(git_show(base, p)), load_yaml(git_show(head, p)))
    if SCHEMA_REF in changed:
        art["table"] = changed_tables(json.loads(git_show(base, SCHEMA_REF) or "{}"),
                                      json.loads(git_show(head, SCHEMA_REF) or "{}"))
    art.update(changed_files(changed))
    return changed, art


def live_statuses(links):
    """Subject, status, type and assignee read from OpenProject now (GET only; TICVAI_OP_TOKEN), over the cached ones."""
    import importlib.util
    spec = importlib.util.spec_from_file_location("adam_links", PKG / "tools" / "adam-links.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    snap = mod.snapshot(os.environ["TICVAI_OP_TOKEN"])
    return [dict(ln, **snap.get(int(ln["key"]), {})) if str(ln.get("key", "")).isdigit() else ln for ln in links]


def impact_md(base, release, art, imp, changed):
    lines = [f"# Light CR release {release}: what it touches", "",
             f"From {base}. {len(changed)} file(s) changed; artefacts whose definition changed: "
             + ", ".join(f"{len(v)} {k}(s)" for k, v in sorted(art.items())) + ".",
             "Service links are not used: every back-end task links its service.", ""]
    for b, title in (("new", "Not started (New, On hold): the next pull has the change"),
                     ("started", "Started: the pull shows what changed since the previous one"),
                     ("finished", "Finished (Ready for QA, Closed): a rework sub-task (`cr-release.py rework`)")):
        rows = [t for t in imp["tickets"] if t["bucket"] == b]
        lines += [f"## {title} ({len(rows)})", ""]
        lines += [f"- #{t['id']} {t['key']} ({t['kind']}, {t['status']}, {t['assignee'] or 'nobody'}): "
                  f"{'; '.join(t['touches'][:6])}{' ...' if len(t['touches']) > 6 else ''}" for t in rows]
        lines.append("")
    if imp["skipped"]:
        lines += [f"Skipped (Rejected): {', '.join('#%s' % s['id'] for s in imp['skipped'])}", ""]
    return "\n".join(lines)


def cmd_impact(args):
    base, release, head = resolve_release(args.release, after_tag=False)
    out = out_dir(args, release)
    started = time.time()
    changed, art = release_artefacts(base, head)
    links = (json.loads(git_show(head, LINKS) or "{}")).get("links") or []
    if args.live_status:
        if not os.environ.get("TICVAI_OP_TOKEN"):
            sys.exit("cr-release impact: --live-status needs TICVAI_OP_TOKEN")
        links = live_statuses(links)
    mp = json.loads(git_show(head, PMS_MAP) or "{}")
    keys_by_id = {str(v): k for k, v in mp.items() if isinstance(v, int) and not k.startswith(("_", "VERSION"))}
    imp = impact_tickets(links, art, keys_by_id)
    write_json(out / "impact.json", imp["tickets"])
    for b in ("new", "started", "finished"):
        write_json(out / f"impact-{b}.json", [t for t in imp["tickets"] if t["bucket"] == b])
    write_json(out / "artefacts.json", {"base": base, "release": release, "head": head,
                                        "head_sha": git("rev-parse", f"{head}^{{commit}}").strip(),
                                        "changed_files": changed, "skipped": imp["skipped"],
                                        "statuses": "live" if args.live_status else "cached in adam-links.json",
                                        **{k: sorted(v) for k, v in art.items()}})
    (out / "impact.md").write_text(impact_md(base, release, art, imp, changed), encoding="utf-8")
    count = {b: sum(t["bucket"] == b for t in imp["tickets"]) for b in ("new", "started", "finished")}
    print(f"cr-release impact: {base} -> {release} ({head}): {len(changed)} file(s) changed; "
          + ", ".join(f"{len(v)} {k}(s)" for k, v in sorted(art.items())) + " changed")
    print(f"  {len(imp['tickets'])} ticket(s): {count['new']} new, {count['started']} started, {count['finished']} "
          f"finished; {len(imp['skipped'])} rejected skipped; statuses "
          f"{'read from OpenProject now' if args.live_status else 'as cached in adam-links.json'} "
          f"({round(time.time() - started)} s)")
    print(f"  -> {out / 'impact.json'} (the pull list), impact-new/started/finished.json, impact.md")
    return 0


#@@MORE@@

def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if not run_self_tests(quiet=bool(argv) and argv[0] != "self-test"):
        return 1
    ap = argparse.ArgumentParser(prog="cr-release.py", description=__doc__.split("\n\n")[0])
    sub = ap.add_subparsers(dest="cmd")
    sub.add_parser("self-test", help="run the self-tests only")

    def common(p):
        p.add_argument("--release", help="the release, r<N> (default: see the module text)")
        p.add_argument("--out", help="where this release's files go (default audit/ticvai/releases/r<N>/)")
        p.add_argument("--apply", action="store_true", help="do it (without: print what would be done)")
        p.add_argument("--env-file", default=str(REPO / "audit" / "audit.env"),
                       help="KEY=VALUE secrets for the tools it runs (values never printed)")
        return p

    common(sub.add_parser("check", help="main, clean and pushed; the gate"))
    p = common(sub.add_parser("impact", help="the tickets the release touches, for the pull"))
    p.add_argument("--live-status", action="store_true", help="read statuses from OpenProject now (GET only)")
    #@@ARGS@@
    a = ap.parse_args(argv)
    if a.cmd in (None, "self-test"):
        return 0
    loaded = load_env(a.env_file)
    if loaded:
        print(f"  (environment: {', '.join(loaded)} from {a.env_file}; values not shown)")
    return COMMANDS[a.cmd](a)


COMMANDS = {"check": cmd_check, "impact": cmd_impact}


if __name__ == "__main__":
    sys.exit(main())
