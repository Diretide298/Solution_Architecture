#!/usr/bin/env python3
"""Build the one release bundle the OpenProject push runs from: handoff/service-docs/op-release.json.

Until 1 October a release reached OpenProject through about ten steps: op-create.rb, op-created-merge.py,
op-descriptions.rb, op-order-sync.py/.rb, op-bulk-links.py/.rb, op-assign-sync.py/.rb, op-retire.py and
op-check.py/.rb, each with its own JSON. This writes everything those steps need into one file, keyed by
plan key, and tools/op-release.rb applies it on the server in phases (dry run first). Council item C6/C7,
audit/ticvai/TODO.md item 1E.

The bundle holds:

  ids          every pushed key -> its OpenProject id, straight from pms-map.json. It is authoritative: a key
               in it is never made again or given another id; a key not in it is new.
  tickets      every plan ticket (epics, features, tasks, then sub-tasks; parents first) with its parent key,
               subject, type, wave priority, Priority_No. (build order), assignee, accountable, its sprint (the
               OpenProject version "Sprint n"), the artefact ids it builds and its pointer body (C7)
  sprint_versions  "Sprint 1" ... "Sprint 13" with their dates and ids (made on the server when missing; the
               old "Block A · Week n" versions stay as they are and are no longer set)
  create       the plan keys with no ticket yet, parents before children
  links        the "follows" links to have (a longer chain's implied links left out, as op-bulk-links.py does)
  edges        every plan wait, unreduced: a direct link the plan no longer orders, even through a chain, is
               pruned (as op-order-sync.py does)
  retire       pushed tickets that left the plan, with op-retire.py's action (defer: on hold, merge: rejected)
               and its comment; and (1 October) the service and app epics and features the sprint plan replaced
               with Block epics and app-module features (regroup: rejected once nothing is under them)
  unexplained  pushed tickets that left the plan with no reason in op-retire.py: listed, never touched

**Pointer bodies (C7).** OpenProject holds who, when, state and order; the package, served by ADAM at a release
tag, holds what. A ticket's description becomes a pointer: a one-line summary, its key, the artefact ids it
builds, "Pull via ADAM: /ticket <id>" and the release it was written at. The id is written as %ID% here and
filled in on the server (a new ticket has no id until it is made).

Checks before writing: no OpenProject id is shared by two keys, every new ticket's parent is pushed or made
earlier in the bundle, the plan's waits have no cycle, and check-key-stability passes (no new key's work is
already on a pushed ticket). Any failure writes nothing.

    python3 tools/op-release.py --release r1            # writes handoff/service-docs/op-release.json
    python3 tools/op-release.py --release r1 --show SVC-ORDER-PAYMENT-1 APP-MOB-GST-043

Then the server: tools/op-release-server.sh (OPENPROJECT-PUSH.md, "The release push").
"""
from __future__ import annotations

import argparse
import csv
import importlib.util
import json
import re
import subprocess
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "handoff" / "service-docs"
OUT = DOCS / "op-release.json"
SCREEN = re.compile(r"([A-Z]+-\d{3})$")
TAG = re.compile(r"^r\d+$")
POINTER_PREFIX = "Pull via ADAM:"               # a description holding this line is already a pointer
RELEASE_PREFIX = "- Written at release "        # the one pointer line that may differ without a rewrite
COMMENT_MARKER = "The spec for this ticket lives in ADAM"   # the one comment a started ticket gets, found by it
REOPEN_MARKER = "Back in the plan"              # an On hold plan ticket set back to New, with one comment
MAX_BUILDS = 60
LAST_SPRINT = 13                                # Sprint 13 ends 2 April 2027; later work is planned into it
INPUTS = ("tasks.csv", "pms-map.json", "block-a-schedule.json")    # in handoff/service-docs; checked at the tag


def _load(name, file):
    spec = importlib.util.spec_from_file_location(name, ROOT / "tools" / file)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


push = _load("push_openproject", "push-openproject.py")
assign_sync = _load("op_assign_sync", "op-assign-sync.py")
OP_NAME = assign_sync.OP_NAME                   # plan name -> OpenProject name (Surendra -> Surendra Loke)


def pushed(mp):
    """{key: id} for the work packages in pms-map.json (not the versions, not the bookkeeping)."""
    return {k: v for k, v in mp.items() if not k.startswith(("_", "VERSION")) and isinstance(v, int)}


def summary_line(subject):
    """One line: the subject without its [track] tag."""
    s = " ".join(re.sub(r"^\[[^\]]+\]\s*", "", subject or "").split())
    return s if len(s) <= 200 else s[:197].rstrip() + "..."


def builds_of(r, part, lineage):
    """The artefact ids a ticket builds, as ADAM names them: operation contract#operationId, table schema.name,
    screen id, service. Setup, onboarding and AI tasks build nothing ADAM indexes by id: their key is enough."""
    def op_id(op):
        c = lineage.get(op, {}).get("contract")
        return f"{c}#{op}" if c else op

    if r["type"] == "Task" and r["track"] == "Backend":
        ops = [part] if part else (r["subject"].split(": ", 1)[1].split(", ") if ": " in r["subject"] else [])
        return [f"operation {op_id(op)}" for op in ops]
    if r["type"] == "Task" and r["track"] == "Database":
        if part:
            return [f"table {part}"]
        m = re.search(r"Tables: (.+?)\. Source", r["description"])
        return [f"table {t}" for t in (m.group(1).split(", ") if m else [])]
    if r["type"] == "Task" and r["track"] == "Frontend":
        m = SCREEN.search(r["key"])
        return [f"screen {m.group(1)}"] if m else []
    if r["type"] in ("Epic", "Feature") and r.get("service"):
        return [f"service {r['service']}"]
    return []


def pointer(key, summary, builds, release):
    """The description a ticket carries from this release on. %ID% is its OpenProject id, filled in on the server."""
    shown = builds[:MAX_BUILDS]
    more = f" and {len(builds) - MAX_BUILDS} more (all listed in ADAM)" if len(builds) > MAX_BUILDS else ""
    lines = [f"**{summary}**", "",
             f"- Key: `{key}`",
             "- Builds: " + (", ".join(f"`{b}`" for b in shown) + more if shown else "see the key; nothing indexed by id"),
             f"- {POINTER_PREFIX} `/ticket %ID%`",
             f"{RELEASE_PREFIX}`{release}`",
             "",
             "The spec (contract, tables, screens, done-when) lives in ADAM at the release tag, not in this ticket. "
             "OpenProject holds who, when, state and order."]
    return "\n".join(lines) + "\n"


def comment(release):
    """The one comment a started ticket gets instead of a rewrite. %ID% and %KEY% are filled in on the server."""
    return (f"**{COMMENT_MARKER} from release {release}.** The description above is what this work started "
            "against, so it is left as it is. The current spec (contract, tables, screens, done-when) is in ADAM: "
            "pull it with `/ticket %ID%` (key `%KEY%`). OpenProject keeps who, when, state and order.")


def find_cycle(edges):
    after = defaultdict(list)
    for k, d in edges:
        after[k].append(d)
    state = {}
    for start in list(after):
        if state.get(start):
            continue
        stack = [(start, iter(after[start]))]
        path = [start]
        state[start] = 1
        while stack:
            node, it = stack[-1]
            nxt = next(it, None)
            if nxt is None:
                state[node] = 2
                stack.pop()
                path.pop()
                continue
            if state.get(nxt) == 1:
                return path[path.index(nxt):] + [nxt]
            if not state.get(nxt):
                state[nxt] = 1
                stack.append((nxt, iter(after[nxt])))
                path.append(nxt)
    return None


def shared_ids(ids):
    by_id = defaultdict(list)
    for k, v in ids.items():
        by_id[v].append(k)
    return {v: sorted(ks) for v, ks in by_id.items() if len(ks) > 1}


def build(rows, mp, sched, lineage, retire_plan, unexplained, release):
    """The bundle, from the plan rows, the map and the schedule. No files read or written: tests call this."""
    ids = pushed(mp)
    errors = []
    for i, ks in sorted(shared_ids(ids).items()):
        errors.append(f"id #{i} is mapped to {len(ks)} keys: {', '.join(ks)} (repair pms-map.json first)")
    by_key = {r["key"]: r for r in rows}
    who = sched["assign"]
    # **Two-week sprints** (1 October): a ticket's version is the sprint it starts in, "Sprint 1" to "Sprint 13"
    # (a later start is planned into Sprint 13, past 2 April); the schedule gives it (sprint), else its start day.
    sprint_of = {k: max(1, min(int(v), LAST_SPRINT)) for k, v in (sched.get("sprint") or {}).items()}
    for k, v in sched["start"].items():
        sprint_of.setdefault(k, max(1, min(int(v // 10) + 1, LAST_SPRINT)))
    cal = {int(s["n"]): s for s in sched.get("sprints") or []}
    sprint_versions = [{"key": f"VERSION-S{n}", "name": f"Sprint {n}", "id": mp.get(f"VERSION-S{n}"),
                        "start": (cal.get(n) or {}).get("start"), "end": (cal.get(n) or {}).get("end")}
                       for n in range(1, LAST_SPRINT + 1)]
    svc_owner = {r["service"]: r["assignee"] for r in rows if r["type"] == "Epic" and r["key"].startswith("SVC-")}

    def accountable(r):
        if r.get("accountable"):                 # the sprint plan writes it on the row (1 October)
            return r["accountable"]
        if r["track"] in ("Backend", "Database"):
            return svc_owner.get(r["service"]) or push.LEAD["devops"]
        return push.LEAD.get(r["area"]) or r["assignee"]

    def name(n):
        return OP_NAME.get(n, n) if n else None

    tickets = []

    def add(key, typ, parent, subject, r, part):
        task = r["type"] == "Task"
        base = r["key"]
        if task:
            assignee = who.get(base) or r["assignee"] or None
            n = sprint_of.get(base)
        else:
            assignee, n = r["assignee"] or None, None
        summ = summary_line(subject)
        builds = builds_of(r, part, lineage)
        tickets.append({
            "key": key, "type": typ, "type_id": push.TYPES[typ], "parent": parent or None,
            "subject": subject[:255], "priority_id": push.PRIORITY.get(r["wave"] or "2", 8),
            "sequence": int(r["sequence"]) if r["sequence"] else None,
            "assignee": name(assignee), "responsible": name(accountable(r)),
            "sprint": n, "version_key": f"VERSION-S{n}" if n else None,
            "version": mp.get(f"VERSION-S{n}") if n else None, "set_version": task,
            "summary": summ, "builds": builds, "pointer": pointer(key, summ, builds, release)})

    for r in rows:
        add(r["key"], r["type"], r["parent"], r["subject"], r, "")
    for r in rows:
        for k, parent, subject, _ in push.sub_tasks(r, lineage):
            add(k, "Sub Task", parent, subject, r, k.partition("#")[2])

    known = set(ids)
    create = []
    for t in tickets:
        if t["key"] in ids:
            continue
        if t["parent"] and t["parent"] not in known:
            errors.append(f"{t['key']}: its parent {t['parent']} is neither pushed nor made earlier in the bundle")
        create.append(t["key"])
        known.add(t["key"])

    task_keys = [r["key"] for r in rows if r["type"] == "Task"]
    edges = sorted({(r["key"], d) for r in rows if r["type"] == "Task" for d in r["dependsOn"].split()})
    unknown = sorted({d for _, d in edges if d not in by_key})
    if unknown:
        errors.append(f"waits on keys that are not in the plan: {', '.join(unknown[:15])}")
    cycle = find_cycle(edges)
    if cycle:
        errors.append("the plan's waits have a cycle: " + " > ".join(cycle))
        links = []
    else:
        links = push.reduce_links(edges)

    retire = [{"key": k, "id": ids[k], "action": kind, "note": note}
              for k, kind, note in retire_plan if k in ids]
    planned = {t["key"] for t in tickets}
    clash = sorted(r["key"] for r in retire if r["key"] in planned)
    if clash:
        errors.append(f"in the plan and in the retire list at once: {', '.join(clash[:15])}")
    unexp = [{"key": k, "id": ids.get(k), "why": "out of tasks.csv with no reason in op-retire.py"}
             for k in unexplained]
    # A pushed sub-task whose task is still planned but whose operation or table is no longer under it (the task
    # was split or regrouped). op-retire.py reasons about tasks only, so these have no reason either: listed.
    home = defaultdict(list)
    for k in planned:
        if "#" in k:
            home[k.partition("#")[2]].append(k)
    retired = {r["key"] for r in retire} | set(unexplained)
    for k in sorted(ids):
        if "#" not in k or k in planned or k in retired or k.partition("#")[0] in retired:
            continue
        other = [h for h in home.get(k.partition("#")[2], []) if h != k]
        why = (f"sub-task stale: its work is on {other[0]}" + (f" (#{ids[other[0]]})" if other[0] in ids else " (new)")
               if other else "sub-task stale: its operation or table is no longer in the plan")
        unexp.append({"key": k, "id": ids[k], "why": why})

    bundle = {
        "release": release, "project": push.PROJECT, "field": push.PRIORITY_NO,
        "statuses": {"new": 1, "on_hold": 13, "rejected": 14},
        "reopen_marker": REOPEN_MARKER,
        "author": "Chinmay Parab", "aliases": OP_NAME,
        "markers": {"pointer": POINTER_PREFIX, "release": RELEASE_PREFIX, "comment": COMMENT_MARKER},
        "comment": comment(release),
        "sprint_versions": sprint_versions,
        "ids": dict(sorted(ids.items())),
        "tickets": tickets, "create": create, "tasks": task_keys,
        "links": [list(e) for e in links], "edges": [list(e) for e in edges],
        "retire": retire, "unexplained": unexp,
    }
    return bundle, errors


def unexplained_kind(u):
    if "work is on" in u["why"]:
        return "stale sub-task, work on another ticket"
    if "no longer in the plan" in u["why"]:
        return "stale sub-task, work left the plan"
    return "task with no reason"


def counts(b):
    by_type = Counter(t["type"] for t in b["tickets"])
    new_by_type = Counter(t["type"] for t in b["tickets"] if t["key"] in set(b["create"]))
    return {
        "tickets": len(b["tickets"]), "by_type": dict(by_type), "pushed_ids": len(b["ids"]),
        "create": len(b["create"]), "create_by_type": dict(new_by_type),
        "with_builds": sum(1 for t in b["tickets"] if t["builds"]),
        "links": len(b["links"]), "edges": len(b["edges"]), "tasks": len(b["tasks"]),
        "retire": dict(Counter(r["action"] for r in b["retire"])), "unexplained": len(b["unexplained"]),
    }


def git(*args):
    try:
        return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, check=True).stdout.decode().strip()
    except Exception:
        return ""


def previous_structure(release):
    """The epics and features of the last release before `release` (its tasks.csv at the tag), and its tests."""
    tags = sorted((t for t in git("tag", "--list", "r*").split() if TAG.match(t)), key=lambda t: int(t[1:]))
    prev = [t for t in tags if int(t[1:]) < int(release[1:])]
    if not prev:
        return set()
    prefix = git("rev-parse", "--show-prefix")
    text = git("show", f"{prev[-1]}:{prefix}handoff/service-docs/tasks.csv")
    if not text:
        return set()
    return {r["key"] for r in csv.DictReader(text.splitlines()) if r["type"] in ("Epic", "Feature")
            or r["key"].startswith("TEST-")}


def regroup(rows, mp, retire_plan, unexplained, release, structure=None):
    """**The hierarchy of 1 October** (Epic = Block, Feature = app-module): the epics and features of the previous
    release that left the plan grouped tickets by service and app; their tickets move under the new parents in the
    same push, and they are closed (Rejected) with a comment once nothing is under them (op-release.rb checks).
    A module or block test whose app-module or block was renamed goes the same way. Returns the retire plan and the
    unexplained list without them."""
    structure = previous_structure(release) if structure is None else structure
    planned = {r["key"] for r in rows}
    gone = [k for k in unexplained if k in structure and k not in planned]
    note = ("**Replaced by the sprint plan** (release " + release + ", decided 1 October): tickets are grouped by "
            "Block (epic) and app-module (feature, e.g. Ticketing · Guest Web) now. Every ticket that was under this "
            "one has moved under its app-module, so this one is closed.")
    return (list(retire_plan) + [(k, "regroup", note) for k in gone],
            [k for k in unexplained if k not in set(gone)])


# What the server's OpenProject (10.0.2, Rails 5.2, Ruby 2.6) cannot run, found in tools/op-release.rb before a
# bundle is written (CHG-REL-001: the r2 dry run stopped in the retire phase on a parent_id query).
OP10_FORBIDDEN = [
    (re.compile(r"\.where\([^)]*parent_id\s*:"), "OpenProject 10 keeps parents in the relations table and has no "
     "work_packages.parent_id column: use w.children / w.parent"),
]


def op10_problems():
    rb = (ROOT / "tools" / "op-release.rb").read_text(encoding="utf-8")
    return [f"tools/op-release.rb:{n}: {why}" for n, line in enumerate(rb.splitlines(), 1)
            for rx, why in OP10_FORBIDDEN if rx.search(line) and not line.lstrip().startswith("#")]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--release", help="the tag the pointers are written at (r1, r2, ...); default: the tag on HEAD")
    ap.add_argument("--out", default=str(OUT))
    ap.add_argument("--show", nargs="*", default=[], help="print these keys' bundle entries")
    ap.add_argument("--no-key-check", action="store_true", help="skip check-key-stability (never for a real push)")
    a = ap.parse_args()
    release = a.release or git("describe", "--tags", "--exact-match", "HEAD")
    if not TAG.match(release or ""):
        print(f"--release must be a release tag like r1 (got {release!r}); HEAD carries no rN tag")
        return 2

    rows = list(csv.DictReader((DOCS / "tasks.csv").open(encoding="utf-8")))
    mp = json.loads((DOCS / "pms-map.json").read_text(encoding="utf-8"))
    sched = json.loads((DOCS / "block-a-schedule.json").read_text(encoding="utf-8"))
    lineage = json.loads((ROOT / "handoff" / "api-data-lineage.json").read_text(encoding="utf-8"))
    _, retire_plan, unexplained = _load("op_retire", "op-retire.py").build_plan()
    retire_plan, unexplained = regroup(rows, mp, retire_plan, unexplained, release)

    bundle, errors = build(rows, mp, sched, lineage, retire_plan, unexplained, release)
    errors += op10_problems()
    if not a.no_key_check:
        ks = _load("check_key_stability", "check-key-stability.py")
        if hasattr(ks, "retired_keys"):      # the 1C version (1 October): a rename of a pushed key blocks too
            k_errors, _ = ks.check(rows, mp, ks.gen.closed_keys(), ks.retired_keys(mp))
        else:
            k_errors, _ = ks.check(rows, mp, ks.gen.closed_keys())
        errors += [f"check-key-stability: {e}" for e in k_errors]
    if errors:
        for e in errors[:40]:
            print("  refuse:", e)
        print(f"FAIL: {len(errors)} problem(s); {a.out} not written")
        return 1

    commit = git("rev-parse", "HEAD")
    dirty = bool(git("status", "--porcelain", "--", *(f"handoff/service-docs/{f}" for f in INPUTS)))
    # The git blob id each input will have once committed (hash-object applies the same line-ending filter a
    # commit does). op-release-server.sh compares them with the files at the tag and refuses a stale bundle.
    inputs = {f: git("hash-object", f"handoff/service-docs/{f}") for f in INPUTS}
    bundle = {"release": bundle.pop("release"), "built_from": commit + ("+local-changes" if dirty else ""),
              "built_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "inputs": inputs, **bundle}
    Path(a.out).write_text(json.dumps(bundle, indent=0, ensure_ascii=False), encoding="utf-8")
    c = counts(bundle)
    print(f"op-release.json for {release} (from {bundle['built_from'][:12]}{' with local changes' if dirty else ''}):")
    print(f"  tickets {c['tickets']} {c['by_type']}; {c['pushed_ids']} pushed ids")
    print(f"  to create {c['create']} {c['create_by_type']}")
    print(f"  pointers {c['tickets']} ({c['with_builds']} name artefact ids)")
    print(f"  links {c['links']} to have ({c['edges']} plan waits over {c['tasks']} tasks, for pruning)")
    print(f"  leaving the plan {sum(c['retire'].values())} {c['retire']}; unexplained {c['unexplained']} (not touched)")
    print(f"  -> {a.out}")
    kinds = Counter(unexplained_kind(u) for u in bundle["unexplained"])
    if kinds:
        print(f"  unexplained, left alone: {dict(kinds)}")
    for u in bundle["unexplained"][:20]:
        print(f"  ?? #{u['id']} {u['key']}: {u['why']}")
    if len(bundle["unexplained"]) > 20:
        print(f"  ?? ... and {len(bundle['unexplained']) - 20} more (the bundle's 'unexplained' list)")
    by_key = {t["key"]: t for t in bundle["tickets"]}
    for k in a.show:
        t = by_key.get(k)
        print(f"\n=========== {k} ===========")
        if not t:
            print("(not a plan key)")
            continue
        print(json.dumps({x: y for x, y in t.items() if x != "pointer"}, indent=1, ensure_ascii=False))
        print("--- pointer ---\n" + t["pointer"].replace("%ID%", str(bundle["ids"].get(k, "<new>"))))
    return 0


if __name__ == "__main__":
    sys.exit(main())
