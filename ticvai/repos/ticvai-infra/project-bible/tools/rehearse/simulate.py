#!/usr/bin/env python3
"""OpenProject as the release's apply will leave it, for the stand-in (tools/rehearse/stand-in-openproject.mjs).

The apply is tools/op-release.rb on the server. This replays its phases that change what a pull reads, with the same
rules, on the project as it is now:
  now           OpenProject's snapshot (prepare.py snapshot: status, assignee, Accountable, sprint, parent of every
                ticket, as OpenProject holds them) over the last live pull (status, owner, sprint, parent, text,
                comments) over the previous release's bundle (New). Without a snapshot, Accountable comes from the
                previous bundle and the judge does not count the leaver criterion as judged.
  create        tickets with no id, parents first; an existing ticket with the same subject under the same parent and
                no key of its own is taken, as the apply does; the rest get stand-in ids from 990001, written to
                op-created-r<N>.json (the file the apply writes), so the rehearsal merges and links them as
                production does.
  priority      the build order on every plan ticket. New tickets are re-parented under the plan's parent first.
  assign        On hold and planned again: back to New with one comment. A New ticket gets the plan's assignee,
                Accountable and sprint, and a field still on someone who left goes to the successor when the plan's
                person has no account. A started, open ticket keeps its owners except a field on someone who left,
                which goes to the plan's person, else the successor (P-25); otherwise it gets one comment.
  retire        New tickets only: defer to On hold with no assignee or sprint; merge and regroup to Rejected (a
                regrouped one only once nothing is under it); each with its note.
  descriptions  a New ticket's text becomes its pointer and its subject the plan's; a started open one gets one comment.
The links and health phases change nothing a pull reads. PHASES must equal op-release.rb's list: a phase added to the
apply stops the rehearsal until it is replayed here (or shown to change nothing a pull reads).

    python tools/rehearse/simulate.py --self-test
    python tools/rehearse/simulate.py --bundle <op-release-rN.json> --release rN [--prev <op-release-rN-1.json>]
        [--base <last live pull>] [--op-snapshot <snapshot.json>] [--rules <op-release.rb>]
        --out <work>/op-state.json --created-out <work>/op-created-rN.json

The self-tests run first, every time.
"""
from __future__ import annotations

import argparse
import collections
import json
import re
import sys
from pathlib import Path

STAND_IN_FROM = 990001
# op-release.rb's PHASES, in its order. links and health change nothing a pull reads.
PHASES = ("create", "priority", "assign", "links", "retire", "descriptions", "health")
DEFAULT_STATUSES = [  # OpenProject 10 on the PMS server, the ids the bundle's `statuses` names
    {"id": 1, "name": "New", "isClosed": False, "isDefault": True},
    {"id": 7, "name": "In progress", "isClosed": False, "isDefault": False},
    {"id": 12, "name": "Closed", "isClosed": True, "isDefault": False},
    {"id": 13, "name": "On hold", "isClosed": False, "isDefault": False},
    {"id": 14, "name": "Rejected", "isClosed": True, "isDefault": False},
    {"id": 15, "name": "Ready for QA", "isClosed": False, "isDefault": False},
]
TYPES = {"Epic": 5, "Feature": 4, "Task": 1, "Sub Task": 6, "Bug": 7}
# Planned hires with no OpenProject account yet (the plan names them; nobody can be assigned under that name).
PLACEHOLDERS = ("New full-stack developer", "Second AI engineer")


def utf8() -> None:
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass


def load(path, default=None):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def rules_phases(text: str) -> list:
    m = re.search(r"PHASES\s*=\s*%w\[([^\]]*)\]", text)
    return m.group(1).split() if m else []


def phase_problem(text: str):
    got = rules_phases(text)
    if not got:
        return "op-release.rb names no PHASES list: the replay cannot tell which phases the apply runs"
    if tuple(got) != PHASES:
        return (f"op-release.rb runs {got}; simulate.py replays {list(PHASES)}: teach simulate.py the new phase (or "
                f"say why it changes nothing a pull reads) before the rehearsal can stand for the apply")
    return None


def _title(links, field):
    return ((links or {}).get(field) or {}).get("title") or None


def _int(x):
    try:
        return int(str(x).rstrip("/").rsplit("/", 1)[-1])
    except (TypeError, ValueError):
        return None


def read_pulls(base) -> dict:
    """OpenProject id -> ticket.json of the last live pull (workspace/.adam/work/<id>/ticket.json)."""
    out = {}
    for f in (Path(base) / "workspace" / ".adam" / "work").glob("*/ticket.json"):
        d = load(f)
        if not d:
            continue
        i = _int((d.get("workPackage") or {}).get("key") or f.parent.name)
        if i is not None:
            out[i] = d
    return out


def simulate(bundle, prev=None, pulls=None, snapshot=None) -> tuple:
    """(the stand-in's state, {created key: id}). `pulls`: id -> ticket.json; `snapshot`: prepare.py snapshot."""
    prev = prev or {}
    pulls = pulls or {}
    release = bundle["release"]
    author = bundle.get("author") or "Chinmay Parab"
    at = bundle.get("built_at") or "2026-01-01T00:00:00Z"
    field = bundle.get("field") or "customField9"
    aliases = bundle.get("aliases") or {}
    left = bundle.get("successors") or {}
    markers = bundle["markers"]

    def name(n):
        return aliases.get(n, n) if n else None

    def placeholder(n):
        return bool(n) and n.startswith(PLACEHOLDERS)

    statuses = [dict(s) for s in ((snapshot or {}).get("statuses") or DEFAULT_STATUSES)]
    closed = {s["name"] for s in statuses if s.get("isClosed")}
    versions = {v["id"]: v["name"] for v in bundle.get("sprint_versions") or [] if v.get("id")}
    for v in prev.get("sprint_versions") or []:
        if v.get("id"):
            versions.setdefault(v["id"], v["name"])
    ids = {k: v for k, v in (bundle.get("ids") or {}).items() if isinstance(v, int)}
    pids = {k: v for k, v in (prev.get("ids") or {}).items() if isinstance(v, int)}
    key_of = {v: k for k, v in {**pids, **ids}.items()}
    state, comments, basis = {}, {}, {}

    def fresh(i, t, parents):
        return {"id": i, "key": t["key"], "subject": t["subject"], "type": t["type"], "status": "New",
                "assignee": None if placeholder(name(t.get("assignee"))) else name(t.get("assignee")),
                "responsible": None if placeholder(name(t.get("responsible"))) else name(t.get("responsible")),
                "version": versions.get(t.get("version")) if t.get("set_version") else None,
                "parent": parents.get(t["parent"]) if t.get("parent") else None,
                "description": t["pointer"].replace("%ID%", str(i)), "sequence": t.get("sequence"),
                "priority": None, "startDate": None, "dueDate": None, "percentageDone": 0}

    # ---- now: the previous bundle, overlaid by the last live pull, overlaid by OpenProject's own snapshot
    for t in prev.get("tickets") or []:
        i = pids.get(t["key"])
        if i:
            state[i], comments[i], basis[i] = fresh(i, t, pids), [], "previous-bundle"
    for i, d in pulls.items():
        i = int(i)
        w = d.get("workPackage") or {}
        s = state.setdefault(i, {"id": i, "key": key_of.get(i), "responsible": None})
        s.update({"subject": w.get("subject"), "type": w.get("type"), "status": w.get("status") or "New",
                  "assignee": w.get("assignee") or None, "version": w.get("version") or None,
                  "parent": _int(w.get("parent")), "description": w.get("description"),
                  "sequence": w.get("buildOrder"), "priority": w.get("priority"), "startDate": w.get("startDate"),
                  "dueDate": w.get("dueDate"), "percentageDone": w.get("percentDone") or 0})
        comments[i] = [{"author": c.get("author"), "at": c.get("at"), "text": c.get("text")}
                       for c in (w.get("comments") or [])]
        basis[i] = "live-pull"
    for e in (snapshot or {}).get("work_packages") or []:
        ln = e.get("_links") or {}
        i = int(e["id"])
        s = state.setdefault(i, {"id": i, "key": key_of.get(i), "description": "", "priority": None})
        s.update({"subject": e.get("subject"), "type": _title(ln, "type"), "status": _title(ln, "status") or "New",
                  "assignee": _title(ln, "assignee"), "responsible": _title(ln, "responsible"),
                  "version": _title(ln, "version"), "parent": _int((ln.get("parent") or {}).get("href")),
                  "sequence": e.get(field), "startDate": e.get("startDate"), "dueDate": e.get("dueDate"),
                  "percentageDone": e.get("percentageDone") or 0})
        if not s.get("description"):
            s["description"] = (e.get("description") or {}).get("raw") or ""
        comments.setdefault(i, [])
        basis[i] = "openproject"

    # ---- who can hold a field: OpenProject's assignable people, else everyone named who is not a planned hire
    if snapshot and snapshot.get("assignable"):
        accounts = set(snapshot["assignable"])
    else:
        accounts = {n for s in state.values() for n in (s.get("assignee"), s.get("responsible"))
                    if n and not placeholder(n)}
        for t in list(bundle.get("tickets") or []) + list(prev.get("tickets") or []):
            for f in ("assignee", "responsible"):
                n = name(t.get(f))
                if n and not placeholder(n):
                    accounts.add(n)
        accounts |= set(left.values())

    def find_user(n):
        return n if n in accounts else None

    def hand_on(planned, current):
        if planned or current is None or current not in left:
            return planned
        return find_user(left[current])

    def note(i, text):
        comments.setdefault(i, []).append({"author": author, "at": at, "text": text})

    # ---- create (parents before children: the bundle lists them that way)
    by_key = {t["key"]: t for t in bundle["tickets"]}
    owned = set(ids.values())
    created, claimed = {}, set()
    nxt = max([STAND_IN_FROM] + [i + 1 for i in list(state) + list(ids.values())])
    for k in bundle.get("create") or []:
        t = by_key[k]
        pk = t.get("parent")
        parent = (ids.get(pk) or created.get(pk)) if pk else None
        if pk and parent is None:
            raise ValueError(f"{k}: its parent {pk} has no ticket and is not made earlier in this run")
        found = next((i for i in sorted(state) if state[i].get("subject") == t["subject"]
                      and state[i].get("parent") == parent and i not in owned and i not in claimed), None)
        if found is not None:
            claimed.add(found)
            created[k] = found
            state[found]["key"] = k
            continue
        i, nxt = nxt, nxt + 1
        s = fresh(i, t, {**ids, **created})
        s["assignee"], s["responsible"] = find_user(name(t.get("assignee"))), find_user(name(t.get("responsible")))
        state[i], comments[i], basis[i], created[k] = s, [], "created", i
    all_ids = {**ids, **created}
    tickets = [(t, all_ids.get(t["key"])) for t in bundle["tickets"]]
    tickets = [(t, i) for t, i in tickets if i in state]
    for t, i in tickets:                      # a New ticket goes under the plan's parent
        if state[i]["status"] == "New":
            state[i]["parent"] = all_ids.get(t["parent"]) if t.get("parent") else None
    # ---- priority
    for t, i in tickets:
        if t.get("sequence") is not None:
            state[i]["sequence"] = t["sequence"]
    # ---- assign
    reopen_marker = bundle.get("reopen_marker") or "Back in the plan"
    for t, i in tickets:
        if state[i]["status"] == "On hold":
            state[i]["status"] = "New"
            where = f"Sprint {t['sprint']}" if t.get("sprint") else "the plan"
            note(i, f"**{reopen_marker}** (release {release}): this work is planned again, in {where}; it was on hold.")
    marker = f"Plan update (release {release})"
    for t, i in tickets:
        s = state[i]
        a, r = find_user(name(t.get("assignee"))), find_user(name(t.get("responsible")))
        if s["status"] == "New":
            a, r = hand_on(a, s.get("assignee")), hand_on(r, s.get("responsible"))
        v = versions.get(t.get("version")) if t.get("set_version") else None
        want = {}
        if a and s.get("assignee") != a:
            want["assignee"] = a
        if r and s.get("responsible") != r:
            want["responsible"] = r
        if v and s.get("version") != v:
            want["version"] = v
        leaver = {}
        if s["status"] != "New" and s["status"] not in closed:
            for f, planned in (("assignee", a), ("responsible", r)):
                cur = s.get(f)
                if cur in left:
                    h = hand_on(planned, cur)
                    if h and h != cur:
                        leaver[f] = h
        if not want and not leaver:
            continue
        if s["status"] == "New":
            s.update(want)
        elif leaver:
            s.update(leaver)
        elif s["status"] not in closed and not any(marker in (c.get("text") or "") for c in comments.get(i, [])):
            note(i, f"**{marker}:** this ticket is now planned for **{a or t.get('assignee')}**"
                    + (f" in **{v}**" if v else "") + f", accountable **{r or t.get('responsible')}**. It is already "
                    f"{s['status']}, so its assignee was not changed; agree the handover with {author} if it should move.")
    # ---- retire (New tickets only)
    for e in bundle.get("retire") or []:
        s = state.get(e["id"])
        if not s:
            continue
        target = "On hold" if e["action"] == "defer" else "Rejected"
        if e["action"] == "regroup" and any(x.get("parent") == e["id"] for x in state.values()):
            continue
        if s["status"] == target or s["status"] != "New":
            continue
        s["status"] = target
        if e["action"] == "defer":
            s["assignee"], s["version"] = None, None
        note(e["id"], e["note"])
    # ---- descriptions
    def norm(x):
        return "\n".join(l for l in str(x or "").replace("\r\n", "\n").split("\n")
                         if not l.startswith(markers["release"])).strip()
    for t, i in sorted(tickets, key=lambda x: (x[0].get("sequence") or 999999, x[0]["key"])):
        s = state[i]
        want = t["pointer"].replace("%ID%", str(i))
        if s["status"] == "New":
            if norm(s.get("description")) != norm(want):
                s["description"] = want
            s["subject"] = t["subject"]
        elif markers["pointer"] in (s.get("description") or ""):
            pass
        elif any(markers["comment"] in (c.get("text") or "") for c in comments.get(i, [])):
            pass
        elif s["status"] not in closed:
            note(i, bundle["comment"].replace("%ID%", str(i)).replace("%KEY%", t["key"]))

    # ---- the stand-in's state (HAL as OpenProject 10 gives it)
    known = {s["name"] for s in statuses}
    for s in state.values():
        if s["status"] not in known:      # a status the last pull named that the default list lacks
            statuses.append({"id": 100 + len(statuses), "name": s["status"], "isClosed": False, "isDefault": False})
            known.add(s["status"])
    people = set(accounts) | {author, "Rehearsal Account"}
    for s in state.values():
        people |= {s.get("assignee"), s.get("responsible")}
    for c in comments.values():
        people |= {x.get("author") for x in c}
    users = {n: 100 + k for k, n in enumerate(sorted(n for n in people if n))}
    vid = {n: i for i, n in versions.items()}
    sid = {s["name"]: s["id"] for s in statuses}
    packages = {}
    for i, s in state.items():
        ln = {"self": {"href": f"/api/v3/work_packages/{i}", "title": s.get("subject") or ""},
              "project": {"href": f"/api/v3/projects/{bundle['project']}", "title": "TICVAI"},
              "type": {"href": f"/api/v3/types/{TYPES.get(s.get('type'), 1)}", "title": s.get("type") or "Task"},
              "status": {"href": f"/api/v3/statuses/{sid[s['status']]}", "title": s["status"]}}
        for f in ("assignee", "responsible"):
            if s.get(f):
                ln[f] = {"href": f"/api/v3/users/{users[s[f]]}", "title": s[f]}
        if s.get("priority"):
            ln["priority"] = {"href": "/api/v3/priorities/9", "title": s["priority"]}
        if s.get("version"):
            ln["version"] = {"href": f"/api/v3/versions/{vid.get(s['version'], 1)}", "title": s["version"]}
        if s.get("parent"):
            p = state.get(s["parent"])
            ln["parent"] = {"href": f"/api/v3/work_packages/{s['parent']}",
                            "title": (p or {}).get("subject") or f"#{s['parent']}"}
        packages[str(i)] = {"_type": "WorkPackage", "id": i, "subject": s.get("subject") or "", "lockVersion": 1,
                            "description": {"format": "markdown", "raw": s.get("description") or ""},
                            "startDate": s.get("startDate"), "dueDate": s.get("dueDate"),
                            "percentageDone": s.get("percentageDone") or 0, "scheduleManually": False,
                            field: s.get("sequence"), "createdAt": at, "updatedAt": at, "_links": ln}
    out = {"project": {"id": bundle["project"], "identifier": "ticvai", "name": "TICVAI"}, "release": release,
           "field": field, "statuses": statuses, "packages": packages,
           "comments": {str(i): c for i, c in comments.items()}, "users": users,
           "versions": [{"id": i, "name": n} for i, n in versions.items()],
           "basis": {str(i): b for i, b in basis.items()}, "key_of": {str(v): k for k, v in all_ids.items()},
           "leavers": sorted(left), "accountableFrom": "openproject" if snapshot else "previous-bundle"}
    return out, created


def main(argv=None) -> int:
    utf8()
    ap = argparse.ArgumentParser(description="Replay the release's apply for the stand-in OpenProject.")
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--bundle")
    ap.add_argument("--release")
    ap.add_argument("--prev")
    ap.add_argument("--base")
    ap.add_argument("--op-snapshot")
    ap.add_argument("--rules")
    ap.add_argument("--out")
    ap.add_argument("--created-out")
    a = ap.parse_args(argv)
    fails = self_test()
    for f in fails:
        print(f"  SELF-TEST    {f}")
    if fails:
        print(f"FAIL {len(fails)} self-test(s)")
        return 1
    if a.self_test or not a.bundle:
        print("PASS - simulate.py self-tests")
        return 0
    if not (a.out and a.created_out):
        ap.error("--out and --created-out are needed with --bundle")
    bundle = load(a.bundle)
    if not bundle:
        print(f"FAIL - no bundle at {a.bundle}")
        return 1
    if a.release and bundle.get("release") != a.release:
        print(f"FAIL - the bundle is release {bundle.get('release')}, not {a.release}")
        return 1
    if a.rules:
        problem = phase_problem(Path(a.rules).read_text(encoding="utf-8"))
        if problem:
            print(f"FAIL - {problem}")
            return 1
    snapshot = load(a.op_snapshot) if a.op_snapshot else None
    if a.op_snapshot and not snapshot:
        print(f"FAIL - no snapshot at {a.op_snapshot}")
        return 1
    try:
        state, created = simulate(bundle, load(a.prev) if a.prev else None, read_pulls(a.base) if a.base else {},
                                  snapshot)
    except ValueError as exc:
        print(f"FAIL - {exc}")
        return 1
    Path(a.out).write_text(json.dumps(state, ensure_ascii=False), encoding="utf-8")
    Path(a.created_out).write_text(json.dumps(created, indent=1), encoding="utf-8")
    C = collections.Counter
    stand_in = sum(1 for v in created.values() if v >= STAND_IN_FROM)
    print(f"{len(state['packages'])} work packages, now from {dict(C(state['basis'].values()))}; statuses after the "
          f"apply {dict(C(p['_links']['status']['title'] for p in state['packages'].values()))}")
    print(f"created {len(created)}: {len(created) - stand_in} taken by subject, {stand_in} stand-in ids from "
          f"{STAND_IN_FROM} -> {a.created_out}; Accountable from {state['accountableFrom']}; "
          f"who left: {', '.join(state['leavers']) or 'nobody'}")
    return 0


# --------------------------------------------------------------------------------------------------- self-tests
def self_test() -> list:
    """The apply's rules on a made-up project. Returns the failures."""
    fails = []
    pointer = "**{k}**\n\n- Key: `{k}`\n- Pull via ADAM: `/ticket %ID%`\n- Written at release `r7`\n"

    def tk(key, parent="F-1", assignee="Pranay Shinde", responsible="Hrushikant Patkar", typ="Task", seq=2):
        return {"key": key, "type": typ, "parent": parent, "subject": f"[BE] {key}", "assignee": assignee,
                "responsible": responsible, "sequence": seq, "sprint": 1, "version": 77, "set_version": True,
                "pointer": pointer.format(k=key)}

    bundle = {"release": "r7", "project": 153, "field": "customField9", "author": "Chinmay Parab",
              "built_at": "2026-10-20T09:00:00Z", "aliases": {"Surendra": "Surendra Loke"},
              "successors": {"Tanmay Dukhande": "Narayan Gaonkar"},
              "markers": {"pointer": "Pull via ADAM:", "release": "- Written at release ",
                          "comment": "The spec for this ticket lives in ADAM"},
              "comment": "The spec for this ticket lives in ADAM: `/ticket %ID%` (%KEY%).",
              "reopen_marker": "Back in the plan",
              "sprint_versions": [{"key": "VERSION-S1", "name": "Sprint 1", "id": 77}],
              "ids": {"F-1": 100, "T-NEW": 101, "T-QA": 102, "T-QA2": 103, "T-HOLD": 104, "T-STARTED": 105},
              "tickets": [tk("F-1", parent=None, typ="Feature", seq=1), tk("T-NEW", assignee="New full-stack developer 1"),
                          tk("T-QA"), tk("T-QA2", responsible="New full-stack developer 2"), tk("T-HOLD"),
                          tk("T-STARTED", assignee="Surendra"), tk("T-MADE"), tk("T-SAME")],
              "create": ["T-MADE", "T-SAME"],
              "retire": [{"key": "T-OLD", "id": 106, "action": "merge", "note": "Merged into T-NEW."},
                         {"key": "T-OLD2", "id": 107, "action": "defer", "note": "Deferred."}]}

    def hal(i, status, subject, assignee=None, responsible=None, parent=100):
        ln = {"status": {"title": status}, "type": {"title": "Task"}}
        if assignee:
            ln["assignee"] = {"title": assignee}
        if responsible:
            ln["responsible"] = {"title": responsible}
        if parent:
            ln["parent"] = {"href": f"/api/v3/work_packages/{parent}"}
        return {"id": i, "subject": subject, "_links": ln}

    snapshot = {"statuses": DEFAULT_STATUSES,
                "assignable": ["Pranay Shinde", "Hrushikant Patkar", "Narayan Gaonkar", "Chinmay Parab",
                               "Surendra Loke"],
                "work_packages": [hal(100, "New", "[BE] F-1", parent=None),
                                  hal(101, "New", "[BE] T-NEW", "Tanmay Dukhande", "Tanmay Dukhande"),
                                  hal(102, "Ready for QA", "[BE] T-QA", "Narayan Gaonkar", "Tanmay Dukhande"),
                                  hal(103, "Ready for QA", "[BE] T-QA2", "Pranay Shinde", "Tanmay Dukhande"),
                                  hal(104, "On hold", "[BE] T-HOLD"),
                                  hal(105, "In progress", "[BE] T-STARTED", "Pranay Shinde", "Hrushikant Patkar"),
                                  hal(106, "New", "[BE] T-OLD"),
                                  hal(107, "In progress", "[BE] T-OLD2", "Pranay Shinde"),
                                  hal(200, "New", "[BE] T-SAME")]}
    state, created = simulate(bundle, None, {}, snapshot)
    P = state["packages"]

    def who(i, f):
        return ((P[str(i)]["_links"].get(f) or {}).get("title"))

    def status(i):
        return P[str(i)]["_links"]["status"]["title"]

    def notes(i):
        return [c["text"] for c in state["comments"].get(str(i), [])]

    # a New ticket on a leaver: the plan's hire has no account, so the successor holds it; Accountable is the plan's
    if (who(101, "assignee"), who(101, "responsible")) != ("Narayan Gaonkar", "Hrushikant Patkar"):
        fails.append(f"New #101 on a leaver: {who(101, 'assignee')} / {who(101, 'responsible')}")
    # P-25: a started open ticket keeps its owners except a field on someone who left: the plan's person, else the
    # successor
    if (who(102, "assignee"), who(102, "responsible")) != ("Narayan Gaonkar", "Hrushikant Patkar"):
        fails.append(f"Ready for QA #102 with a leaver as Accountable: {who(102, 'assignee')} / {who(102, 'responsible')}")
    if (who(103, "assignee"), who(103, "responsible")) != ("Pranay Shinde", "Narayan Gaonkar"):
        fails.append(f"Ready for QA #103, plan's Accountable a hire: {who(103, 'assignee')} / {who(103, 'responsible')}")
    # a started ticket whose plan owner moved (through an alias) keeps its owner and gets one comment
    plan_notes = [n for n in notes(105) if "Plan update (release r7)" in n]
    if who(105, "assignee") != "Pranay Shinde" or len(plan_notes) != 1 or "Surendra Loke" not in plan_notes[0]:
        fails.append(f"started #105: owner {who(105, 'assignee')}, plan comments {plan_notes}")
    # On hold and planned again: back to New with one comment, then assigned and given its pointer like any New one
    if (status(104) != "New" or not any("Back in the plan" in n for n in notes(104))
            or who(104, "assignee") != "Pranay Shinde" or "/ticket 104" not in P["104"]["description"]["raw"]):
        fails.append(f"On hold #104 planned again: {status(104)}, {notes(104)}, {who(104, 'assignee')}")
    # created: a stand-in id from 990001 under its parent, its pointer naming the id; an existing ticket with the same
    # subject under the same parent and no key is taken
    if created != {"T-MADE": STAND_IN_FROM, "T-SAME": 200}:
        fails.append(f"created {created}")
    made = P.get(str(STAND_IN_FROM)) or {}
    if (not made.get("_links", {}).get("parent", {}).get("href", "").endswith("/100")
            or f"/ticket {STAND_IN_FROM}" not in made.get("description", {}).get("raw", "")
            or state["basis"].get(str(STAND_IN_FROM)) != "created" or state["key_of"].get("200") != "T-SAME"):
        fails.append(f"the made ticket or the taken one is wrong: {made}")
    # retire: a New ticket leaving the plan is rejected with its note; a started one is left alone
    if status(106) != "Rejected" or "Merged into T-NEW." not in notes(106) or status(107) != "In progress":
        fails.append(f"retire: #106 {status(106)} {notes(106)}, #107 {status(107)}")
    # who left, and where Accountable came from
    if state["leavers"] != ["Tanmay Dukhande"] or state["accountableFrom"] != "openproject":
        fails.append(f"leavers {state['leavers']}, Accountable from {state['accountableFrom']}")
    prev = {"ids": {"T-QA": 102}, "tickets": [tk("T-QA", responsible="Tanmay Dukhande")], "sprint_versions": []}
    state2, _ = simulate(bundle, prev, {}, None)
    if state2["accountableFrom"] != "previous-bundle":
        fails.append("a replay with no snapshot did not say its Accountable came from the previous bundle")
    # an unknown parent stops the replay as it stops the apply
    bad = json.loads(json.dumps(bundle))
    bad["tickets"].append(tk("T-ORPHAN", parent="NOPE"))
    bad["create"].append("T-ORPHAN")
    try:
        simulate(bad, None, {}, snapshot)
        fails.append("a created ticket with no parent ticket did not stop the replay")
    except ValueError:
        pass
    # the apply's phases, read from op-release.rb
    if phase_problem('PHASES = %w[create priority assign links retire descriptions health].freeze') is not None:
        fails.append("op-release.rb's phase list as it is was refused")
    if "notify" not in (phase_problem('PHASES = %w[create priority assign links retire descriptions notify '
                                      'health].freeze') or ""):
        fails.append("a phase the replay does not know was not named")
    if phase_problem("nothing here") is None:
        fails.append("a script with no PHASES passed")
    return fails


if __name__ == "__main__":
    sys.exit(main())
