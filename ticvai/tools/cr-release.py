#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The light change-request release: a merged class fix reaches developers in minutes (CHG-LCR-001).

Self-tests run first, every time; `self-test` runs only them.

    python3 tools/cr-release.py self-test
"""
from __future__ import annotations

import json
import posixpath
import re
import sys

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

def _canon(x) -> str:
    return json.dumps(x, sort_keys=True, default=str)


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
    docs = dict(all_docs)
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


def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    ok = run_self_tests(quiet=bool(argv) and argv[0] != "self-test")
    if not ok:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
