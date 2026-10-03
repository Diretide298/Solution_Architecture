#!/usr/bin/env python3
"""What each OpenProject ticket touches, for ADAM: the rows `adam_pull` reads to fill a ticket's folder.

ADAM keeps its ticket-to-artefact links in its own table (artefact_link on the ADAM server), not in OpenProject,
so tickets pushed straight into OpenProject arrive with none and every pull says "nothing is linked". This builds
them from the package:

  backend task or sub-task   its operations (contract#operationId), its service, the tables they read or write,
                             and the screens in this plan that call them
  database task / sub-task   its tables
  frontend task / sub-task   its screen and the operations the screen calls
  service epic or feature    its service

Writes handoff/service-docs/adam-links.json, loaded on the ADAM server by viewer/api/load_links.py. With
TICVAI_OP_TOKEN set it also reads each ticket's subject, status, type and assignee from OpenProject, the cached
columns ADAM shows on a board (a copy, labelled as one; OpenProject stays the truth).

  python3 tools/adam-links.py
"""
from __future__ import annotations

import base64
import collections
import csv
import json
import os
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "handoff" / "service-docs"
PMS = "https://pms.softlabsgroup.in"
PROJECT = 153
sys.path.insert(0, str(ROOT / "tools"))
import ticket_done  # noqa: E402  (what a ticket builds: shared with op-release.py and build-service-docs.py)

# A screen task's key ends in its screen id, three or four digits, "-REST" on the rest of a setup screen (CHG-RONEP-003:
# the three-digit pattern gave BO-1065 and the other four-digit setup screens no links at all).
SCREEN = ticket_done.SCREEN
SLICE = re.compile(r"In the slice: ([A-Za-z0-9, ]+?)(?:\)|\.|;|$)")
REST_OF = re.compile(r"Block A built only its setup operations \(([A-Za-z0-9, ]+?)\)")


def snapshot(token):
    """Subject, status, type and assignee of every work package in the project: three paged reads."""
    auth = "Basic " + base64.b64encode(f"apikey:{token}".encode()).decode()
    flt = urllib.parse.quote(json.dumps([{"status": {"operator": "*", "values": []}}]))
    out, off = {}, 1
    while True:
        req = urllib.request.Request(f"{PMS}/api/v3/projects/{PROJECT}/work_packages?pageSize=1000&offset={off}"
                                     f"&filters={flt}", headers={"Authorization": auth, "User-Agent": "curl/8.0"})
        d = json.load(urllib.request.urlopen(req, timeout=600))
        for e in d["_embedded"]["elements"]:
            ln = e["_links"]
            out[e["id"]] = {"subject": e["subject"], "status": ln["status"]["title"], "type": ln["type"]["title"],
                            "assignee": (ln.get("assignee") or {}).get("title") or ""}
        if len(out) >= d["total"] or not d["_embedded"]["elements"]:
            return out
        off += 1


def main() -> int:
    rows = {r["key"]: r for r in csv.DictReader((DOCS / "tasks.csv").open(encoding="utf-8"))}
    mp = json.loads((DOCS / "pms-map.json").read_text(encoding="utf-8"))
    lineage = json.loads((ROOT / "handoff" / "api-data-lineage.json").read_text(encoding="utf-8"))

    screen_ops = {}
    for f in sorted((ROOT / "screens").glob("P*.yaml")):
        for s in yaml.safe_load(f.read_text(encoding="utf-8"))["screens"]:
            screen_ops[s["id"]] = [a["operationId"] for a in s.get("apis") or [] if a.get("operationId")]
    touches = touches_from(rows, lineage, screen_ops)
    token = os.environ.get("TICVAI_OP_TOKEN", "")
    snap = snapshot(token) if token else {}
    links, per_kind, bare = [], collections.Counter(), 0
    for key, wp in mp.items():
        if key.startswith(("_", "VERSION")):
            continue
        seen = set()
        got = [t for t in touches(key) if not (t in seen or seen.add(t))]
        bare += not got
        for kind, target in got:
            per_kind[kind] += 1
            links.append({"key": str(wp), "kind": kind, "id": target, "url": f"{PMS}/work_packages/{wp}",
                          **snap.get(wp, {})})
    out = {"project": "ticvai", "openproject": PMS, "cached": bool(snap), "links": links}
    (DOCS / "adam-links.json").write_text(json.dumps(out, indent=0), encoding="utf-8")
    tickets = len([k for k in mp if not k.startswith(("_", "VERSION"))])
    print(f"{len(links)} links for {tickets - bare} of {tickets} tickets ({bare} with nothing to link: setup, "
          f"onboarding and frontend/VM groupings); {dict(per_kind)}; cached columns: {bool(snap)}")
    return 0


def touches_from(rows, lineage, screen_ops):
    """key -> [(kind, id)] for a ticket (a task, or "TASK#part" a sub-task). Imported by tools/check-ticket-builds.py."""
    screen_of = {k: m.group(1) for k, r in rows.items()
                 if r["type"] == "Task" and r["track"] == "Frontend" and (m := SCREEN.search(k))}
    planned = set(screen_of.values())
    callers = collections.defaultdict(set)          # operation -> screens in this plan that call it
    for sid in planned:
        for op in screen_ops.get(sid, []):
            callers[op].add(sid)

    def op_id(op):
        c = lineage.get(op, {}).get("contract")
        return f"{c}#{op}" if c else op

    def backend(ops):
        out = []
        for op in ops:
            ln = lineage.get(op, {})
            out.append(("operation", op_id(op)))
            if ln.get("service"):
                out.append(("service", ln["service"]))
            # `cache:idempotency` and the like are Redis keys, not tables adam_table can find
            out += [("table", t) for t in ln.get("reads", []) + ln.get("writes", []) if ":" not in t]
            out += [("screen", s) for s in sorted(callers.get(op, ()))]
        return out

    def listed(rx, text):
        m = rx.search(text or "")
        return [x.strip() for x in m.group(1).split(",") if x.strip()] if m else None

    def touches(key):
        base, _, part = key.partition("#")
        if base not in rows:  # out of the plan (tools/op-retire.py closes or parks it): nothing to link
            return []
        r = rows[base]
        if r["track"] == "Frontend" and base in screen_of:
            sid, ops = screen_of[base], list(screen_ops.get(screen_of[base], []))
            # **A setup ticket links only its slice's operations, the rest-of-the-screen ticket the others**
            # (r1 gate G4, CHG-RONEP-003): APP-SETUP-BO-1162 said "2 of its 6 operations" and linked all 6.
            if base.startswith("APP-SETUP-") and not base.endswith("-REST"):
                sl = listed(SLICE, r["description"])
                ops = [o for o in ops if o in sl] if sl is not None else ops
            elif base.endswith("-REST"):
                done = listed(REST_OF, r["description"]) or []
                ops = [o for o in ops if o not in done]
            return [("screen", sid)] + [("operation", op_id(op)) for op in ops]
        out = []
        for b in ticket_done.builds_of(r, part, lineage):
            kind, _, name = b.partition(" ")
            if kind == "operation":
                out += backend([name.split("#")[-1]])
            else:
                out.append((kind, name))
        return out

    return touches


if __name__ == "__main__":
    sys.exit(main())
