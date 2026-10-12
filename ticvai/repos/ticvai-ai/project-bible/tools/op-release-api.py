#!/usr/bin/env python3
"""Apply a small release to OpenProject over its REST API: only the tickets that changed between two release tags.

**The fast path for a release that creates nothing** (12 October 2026, Chinmay: "we should have this functionality
for both adam and PMS to push CRs fixes quickly through the api"). `tools/op-release-server.sh` runs op-release.rb
inside the OpenProject container, on the server, over every one of ~8,000 tickets, which is right for a release
that creates tickets, re-parents, links or retires. A change-request release usually moves a few owners, sprints,
descriptions or titles; this compares the two bundles (`handoff/service-docs/op-release.json` at each tag) and
applies just that difference from any workstation, with the same rules as op-release.rb:

  * **New tickets** get assignee, accountable, sprint version, title and pointer description set to the plan's
    (the release line excluded from the comparison, as op-release.rb's `norm`).
  * **Started tickets** keep their assignee, sprint, title and text: they get one comment per release naming the
    plan's person ("Plan update (release rN)"), and the bundle's one pointer comment if they carry no pointer yet.
  * **Priority_No.** (the build order) is set on every ticket, started and closed ones too.
  * No mail unless --notify.

**It refuses, and names the server path, when the release needs what it does not do**: tickets to create, links that
changed, or tickets leaving the plan. Dry run unless --apply; safe to run again (a ticket already right is skipped, a
comment already there is not repeated).

  python3 tools/op-release-api.py --from r3 --to r4            # dry run
  python3 tools/op-release-api.py --from r3 --to r4 --apply    # TICVAI_OP_TOKEN in the environment
"""
from __future__ import annotations

import argparse
import base64
import json
import os
import subprocess
import sys
import threading
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUNDLE = "ticvai/handoff/service-docs/op-release.json"
PMS_MAP = "ticvai/handoff/service-docs/pms-map.json"
UA = "curl/8.0"  # the OpenProject host's firewall refuses Python's default agent
FIELDS = ("assignee", "responsible", "version", "sequence", "subject", "pointer")


def git_json(ref: str, path: str):
    out = subprocess.run(["git", "show", f"{ref}:{path}"], cwd=ROOT, capture_output=True)
    if out.returncode:
        sys.exit(f"op-release-api: git show {ref}:{path}: {out.stderr.decode().strip()}")
    return json.loads(out.stdout)


class OP:
    def __init__(self, base: str, token: str):
        self.base = base.rstrip("/") + "/api/v3"
        self.auth = "Basic " + base64.b64encode(f"apikey:{token}".encode()).decode()

    def req(self, method: str, path: str, body=None):
        data = json.dumps(body).encode() if body is not None else None
        r = urllib.request.Request(self.base + path, data=data, method=method, headers={
            "authorization": self.auth, "user-agent": UA, "content-type": "application/json"})
        try:
            with urllib.request.urlopen(r, timeout=120) as resp:
                return json.loads(resp.read() or b"null")
        except urllib.error.HTTPError as e:
            raise RuntimeError(f"{method} {path}: {e.code} {e.read().decode('utf-8', 'replace')[:300]}") from None

    def paged(self, path: str):
        out, offset = [], 1
        while True:
            sep = "&" if "?" in path else "?"
            got = self.req("GET", f"{path}{sep}pageSize=500&offset={offset}")
            els = got["_embedded"]["elements"]
            out += els
            if len(els) < 500 or offset > 50:
                return out
            offset += 1


def link_id(wp: dict, rel: str):
    href = ((wp.get("_links") or {}).get(rel) or {}).get("href")
    return int(href.rstrip("/").rsplit("/", 1)[-1]) if href else None


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--from", dest="old", required=True, help="the release OpenProject is at (a tag)")
    ap.add_argument("--to", dest="new", required=True, help="the release to apply (a tag)")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--notify", action="store_true")
    ap.add_argument("--jobs", type=int, default=8, help="tickets read and written at a time")
    ap.add_argument("--pms", default=os.environ.get("TICVAI_PMS_URL", "https://pms.softlabsgroup.in"))
    a = ap.parse_args()
    if not os.environ.get("TICVAI_OP_TOKEN"):
        sys.exit("op-release-api: TICVAI_OP_TOKEN is not set")

    old, new = git_json(a.old, BUNDLE), git_json(a.new, BUNDLE)
    if new.get("release") != a.new:
        sys.exit(f"op-release-api: the bundle at {a.new} is for {new.get('release')}: build it with "
                 f"tools/op-release.py --release {a.new} and commit it before tagging")
    ids = git_json(a.new, PMS_MAP)
    rel_prefix = new["markers"]["release"]
    norm = lambda s: "\n".join(l for l in str(s or "").replace("\r\n", "\n").split("\n")
                               if not l.startswith(rel_prefix)).strip()

    # **What this path does not do**, checked before anything is read from OpenProject.
    edges = lambda b: {tuple(e) for e in b.get("edges") or []}
    retire = lambda b: {r["key"] for r in b.get("retire") or []}
    refuse = []
    if new.get("create"):
        refuse.append(f"{len(new['create'])} ticket(s) to create")
    if edges(new) != edges(old):
        refuse.append(f"links changed (+{len(edges(new) - edges(old))} -{len(edges(old) - edges(new))})")
    if retire(new) - retire(old):
        refuse.append(f"{len(retire(new) - retire(old))} ticket(s) leaving the plan")
    if refuse:
        print("op-release-api: this release needs the server path: " + "; ".join(refuse) + ".\n"
              f"  run on the OpenProject server: tools/op-release-server.sh dry-run {a.new}, then apply {a.new}")
        return 2

    before = {t["key"]: t for t in old["tickets"]}
    changed = []
    for t in new["tickets"]:
        p = before.get(t["key"])
        if p is None or any((norm(p.get(f)) if f == "pointer" else p.get(f)) !=
                            (norm(t.get(f)) if f == "pointer" else t.get(f)) for f in FIELDS):
            changed.append(t)
    print(f"op-release-api: {a.old} -> {a.new}: {len(changed)} of {len(new['tickets'])} plan tickets differ; "
          f"{'APPLY' if a.apply else 'dry run (--apply to change)'}")
    if not changed:
        return 0

    op = OP(a.pms, os.environ["TICVAI_OP_TOKEN"])
    project = new["project"]
    aliases = new.get("aliases") or {}
    users = {u["name"]: u["id"] for u in op.paged(f"/projects/{project}/available_assignees")}
    user = lambda n: users.get(aliases.get(n, n)) or users.get(n) if n else None
    new_status, field = new["statuses"]["new"], new["field"]
    assign_marker = f"Plan update (release {a.new})"
    pointer_marker, comment_marker = new["markers"]["pointer"], new["markers"]["comment"]

    schemas, schema_lock = {}, threading.Lock()

    def has_field(w) -> bool:
        href = w["_links"]["schema"]["href"]
        with schema_lock:
            if href not in schemas:
                schemas[href] = field in op.req("GET", href.replace("/api/v3", "", 1))
        return schemas[href]

    def one(t):
        """(line or None, patched, commented, failure or None) for one plan ticket."""
        wp_id = ids.get(t["key"])
        if not wp_id:
            return None, 0, 0, f"{t['key']}: no OpenProject id in pms-map.json"
        try:
            w = op.req("GET", f"/work_packages/{wp_id}")
            status = link_id(w, "status")
            closed = bool(((w.get("_embedded") or {}).get("status") or {}).get("isClosed"))
            want_pointer = t["pointer"].replace("%ID%", str(wp_id))
            patch, links, notes = {}, {}, []
            # Priority_No. only where the ticket's type has the field: OpenProject has it on Task and Feature, not
            # Sub Task, where op-release.rb writes the value behind the API's back and the API reads null.
            if t.get("sequence") is not None and has_field(w) and str(w.get(field)) != str(t["sequence"]):
                patch[field] = t["sequence"]
            a_id, r_id = user(t.get("assignee")), user(t.get("responsible"))
            v_id = t.get("version") if t.get("set_version") else None
            moves = ((a_id and link_id(w, "assignee") != a_id) or (r_id and link_id(w, "responsible") != r_id)
                     or (v_id and link_id(w, "version") != v_id))
            if status == new_status:
                if a_id and link_id(w, "assignee") != a_id:
                    links["assignee"] = {"href": f"/api/v3/users/{a_id}"}
                if r_id and link_id(w, "responsible") != r_id:
                    links["responsible"] = {"href": f"/api/v3/users/{r_id}"}
                if v_id and link_id(w, "version") != v_id:
                    links["version"] = {"href": f"/api/v3/versions/{v_id}"}
                if w.get("subject") != t["subject"]:
                    patch["subject"] = t["subject"]
                if norm((w.get("description") or {}).get("raw")) != norm(want_pointer):
                    patch["description"] = {"raw": want_pointer}
            elif not closed:
                said = None
                if moves or pointer_marker not in str((w.get("description") or {}).get("raw")):
                    acts = op.req("GET", f"/work_packages/{wp_id}/activities")["_embedded"]["elements"]
                    said = " ".join(((x.get("comment") or {}).get("raw") or "") for x in acts)
                if moves and assign_marker not in said:
                    notes.append(f"**{assign_marker}:** this ticket is now planned for **{t.get('assignee')}**"
                                 + (f" in **Sprint {t['sprint']}**" if t.get("sprint") else "")
                                 + f", accountable **{t.get('responsible')}**. It is already started, so its assignee "
                                 f"was not changed; agree the handover with {new.get('author')} if it should move.")
                if said is not None and pointer_marker not in str((w.get("description") or {}).get("raw"))                         and comment_marker not in said:
                    notes.append(new["comment"].replace("%ID%", str(wp_id)).replace("%KEY%", t["key"]))
            what = list(patch) + list(links) + (["comment"] * len(notes))
            if not what:
                return None, 0, 0, None
            line = (f"  #{wp_id} {t['key']} ({'New' if status == new_status else 'closed' if closed else 'started'}): "
                    + ", ".join(what))
            patched = commented = 0
            if a.apply:
                if patch or links:
                    body = dict(patch, lockVersion=w["lockVersion"])
                    if links:
                        body["_links"] = links
                    op.req("PATCH", f"/work_packages/{wp_id}?notify={'true' if a.notify else 'false'}", body)
                    patched = 1
                for text in notes:
                    op.req("POST", f"/work_packages/{wp_id}/activities?notify={'true' if a.notify else 'false'}",
                           {"comment": {"raw": text}})
                    commented += 1
            return line, patched, commented, None
        except Exception as e:  # one ticket must not stop the rest
            return None, 0, 0, f"#{wp_id} {t['key']}: {e}"

    n_patch = n_comment = n_same = 0
    failed = []
    with ThreadPoolExecutor(max_workers=max(1, a.jobs)) as pool:
        for line, p_, c_, err in pool.map(one, changed):
            if err:
                failed.append(err)
            elif line:
                print(line)
                n_patch += p_; n_comment += c_
            else:
                n_same += 1
    print(f"op-release-api: {n_same} already right" + (f", {n_patch} changed, {n_comment} commented" if a.apply else "")
          + f", {len(failed)} failed")
    for f in failed:
        print(f"  FAILED {f}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
