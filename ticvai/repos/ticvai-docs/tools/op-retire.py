#!/usr/bin/env python3
"""Take tickets out of the plan when their screen is deferred or merged, after a decision says so.

Added 28 September for the audit decisions. R187 and R242 deferred seven guest screens to a later release,
and R276 merged five duplicate screens into others. Their tickets exist in OpenProject, and push-openproject.py
only creates, so nothing else could move them.

A ticket is moved only if nobody has started it (status New). A started ticket is listed and left alone:
work in progress is a conversation, not a script.
- **Deferred:** the ticket and its sub-tasks go On hold, lose their Block A week (version) and their
  assignee, so they leave the developer's board. They get one comment saying why.
- **Merged:** the ticket and its sub-tasks go to Rejected (closed), with a comment naming the ticket that
  carries the screen now.
Sent with notify=false, so nobody is mailed. Dry run unless --apply. Token from TICVAI_OP_TOKEN.

    python tools/op-retire.py [--apply]
"""
import argparse
import base64
import json
import os
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAP = ROOT / "handoff" / "service-docs" / "pms-map.json"
BASE = "https://pms.softlabsgroup.in/api/v3"
ON_HOLD, REJECTED, NEW = 13, 14, 1

DEFERRED = {sid: "R187" for sid in ("GST-051", "GST-052", "GST-053", "GST-054", "GST-059")}
DEFERRED.update({sid: "R242" for sid in ("GST-030", "WEB-046")})
MERGED = {"BO-127": "BO-036", "BO-472": "BO-141", "CMS-020": "CMS-015", "BO-320": "BO-027", "BO-652": "BO-027"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()
    auth = "Basic " + base64.b64encode(f"apikey:{os.environ['TICVAI_OP_TOKEN']}".encode()).decode()
    head = {"Authorization": auth, "User-Agent": "curl/8.0", "Content-Type": "application/json"}

    def call(method, path, body=None):
        req = urllib.request.Request(BASE + path, json.dumps(body).encode() if body is not None else None,
                                     head, method=method)
        with urllib.request.urlopen(req, timeout=120) as r:
            return json.loads(r.read().decode() or "{}")

    mp = json.loads(MAP.read_text(encoding="utf-8"))

    def keys_for(sid):
        top = [k for k in mp if "#" not in k and re.search(rf"-{re.escape(sid)}$", k)]
        return [(k, [s for s in mp if s.startswith(k + "#")]) for k in top]

    def ticket_of(sid):
        return next((f"#{mp[k]}" for k in mp if "#" not in k and re.search(rf"-{re.escape(sid)}$", k)), sid)

    plan = []
    for sid, why in DEFERRED.items():
        note = (f"**Deferred to a later release** (decided 28 September, audit {why}). This screen is out of "
                "Block A, so the ticket is on hold and off the board. It comes back when its release is planned.")
        for k, subs in keys_for(sid):
            plan += [(x, "defer", note) for x in [k] + subs]
    for sid, into in MERGED.items():
        note = (f"**Merged into {into}** (decided 28 September, audit R276). {into}'s ticket "
                f"({ticket_of(into)}) now carries this screen's operations, so this ticket is closed.")
        for k, subs in keys_for(sid):
            plan += [(x, "merge", note) for x in [k] + subs]

    skipped = 0
    for key, kind, note in plan:
        wp = call("GET", f"/work_packages/{mp[key]}")
        status = wp["_links"]["status"]["href"].rsplit("/", 1)[-1]
        if status != str(NEW):
            skipped += 1
            print(f"  leave  #{mp[key]} {key}: status is {wp['_links']['status']['title']}, not New")
            continue
        body = {"lockVersion": wp["lockVersion"], "_links": {"status": {"href": f"/api/v3/statuses/"
                                                                              f"{ON_HOLD if kind == 'defer' else REJECTED}"}}}
        if kind == "defer":
            body["_links"].update({"assignee": {"href": None}, "version": {"href": None}})
        print(f"  {kind:5}  #{mp[key]} {key}")
        if a.apply:
            call("PATCH", f"/work_packages/{mp[key]}?notify=false", body)
            call("POST", f"/work_packages/{mp[key]}/activities?notify=false", {"comment": {"raw": note}})
    moved = len(plan) - skipped
    print(f"{moved} to move, {skipped} left alone (already started)" + ("" if a.apply else "; dry run, pass --apply"))


if __name__ == "__main__":
    sys.exit(main())
