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
SCREEN = re.compile(r"([A-Z]+-\d{3})$")


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

    def touches(key):
        base, _, part = key.partition("#")
        if base not in rows:  # out of the plan (tools/op-retire.py closes or parks it): nothing to link
            return []
        r = rows[base]
        if r["track"] == "Backend" and r["type"] == "Task":
            ops = [part] if part else (r["subject"].split(": ", 1)[1].split(", ") if ": " in r["subject"] else [])
            return backend(ops)
        if r["track"] == "Database" and r["type"] == "Task":
            if part:
                return [("table", part)]
            m = re.search(r"Tables: (.+?)\. Source", r["description"])
            return [("table", t) for t in (m.group(1).split(", ") if m else [])]
        if r["track"] == "Frontend" and base in screen_of:
            sid = screen_of[base]
            return [("screen", sid)] + [("operation", op_id(op)) for op in screen_ops.get(sid, [])]
        if r["type"] in ("Epic", "Feature") and r["service"]:
            return [("service", r["service"])]
        return []

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


if __name__ == "__main__":
    sys.exit(main())
