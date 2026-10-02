#!/usr/bin/env python3
"""Push the Block A task sheet into OpenProject: epics, features, tasks, sub-tasks, versions and relations.

**Resumable, never duplicating.** Every created work package is recorded in
`handoff/service-docs/pms-map.json` (local key -> OpenProject id) the moment it exists, and a key already
in the map is never created again. Re-running after an interruption continues where it stopped.

Reads:
  handoff/service-docs/tasks.csv    the hierarchy, subjects, descriptions, dependencies
  a schedule JSON                   who does each task and when (scratch output of the Block A scheduler)
  handoff/api-data-lineage.json     method and path for each operation's sub-task

  python3 tools/push-openproject.py --schedule <schedule.json> [--dry-run] [--delete-test]

The API key comes from the environment (TICVAI_OP_TOKEN), never from a file.

**Read handoff/service-docs/OPENPROJECT-PUSH.md first.** This makes the tickets, with full descriptions
(tools/op-descriptions.py). The "follows" links belong on the server (tools/op-bulk-links.*), and ADAM's links in
ADAM (tools/adam-links.py): through the API the links take a day.
"""
from __future__ import annotations

import argparse
import base64
import csv
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))    # tools/op-descriptions.py

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "handoff" / "service-docs"
MAP = DOCS / "pms-map.json"
BASE = "https://pms.softlabsgroup.in/api/v3"
PROJECT = 153
TYPES = {"Epic": 5, "Feature": 4, "Task": 1, "Sub Task": 10}   # Epic = Block, Feature = app-module (1 October)
LAST_SPRINT = 13                              # "Sprint 1" ... "Sprint 13": 5 October 2026 to 2 April 2027
PRIORITY = {"1": 9, "2": 8, "3": 7}          # wave 1 High, 2 Normal, 3 Low
PRIORITY_NO = "customField9"                  # "Priority_No." (integer): the build-order sequence
LEAD = {"POS": "Pradnya Yeram", "MOB": "Chitrangi Mestry", "WEB": "Chinmay Patkar", "WL": "Chinmay Patkar",
        "SETUP": "Pallavi Sawant", "VM": "Pallavi Sawant", "devops": "Hrushikant Patkar"}
FE_CHECK = ["Chitrangi Mestry", "Chinmay Patkar", "Pallavi Sawant", "Sanket Keluskar", "Pradnya Yeram"]
BE_CHECK = ["Pranay Shinde", "Tanmay Dukhande"]          # Hrushikant is never a checker


def reduce_links(edges):
    """Drop each link a longer chain already implies: A follows C is redundant when A follows B follows C.
    "follows" is transitive in OpenProject, so the order the links enforce is exactly the same."""
    after = defaultdict(set)
    for k, d in edges:
        after[k].add(d)
    memo = {}

    def before(k):
        if k not in memo:
            memo[k] = set()
            for d in after[k]:
                memo[k] |= {d} | before(d)
        return memo[k]

    sys.setrecursionlimit(10000)
    return [(k, d) for k, d in edges if not any(d in before(o) for o in after[k] if o != d)]


OP_ID = re.compile(r"^[a-z][A-Za-z0-9]+$")


def sub_tasks(r, lineage):
    """The sub-tasks under a task row: one per operation, one per table, three per screen.
    [(key, parent key, subject, short text)]. tools/op-release.py reads the same list."""
    key, out = r["key"], []
    if r["type"] != "Task":
        return out
    if r["track"] == "Backend" and ": " in r["subject"]:
        # Only operation ids become sub-tasks: a task written by hand (docs/active/block-a-extra-tasks.json) may have
        # a colon in its title, and the words after it are not operations (1 October: 16 such fragments were pushed).
        for op in [x for x in r["subject"].split(": ", 1)[1].split(", ") if OP_ID.match(x)]:
            ln = lineage.get(op, {})
            out.append((f"{key}#{op}", key, f"[BE] {op}: {ln.get('verb', '')} {ln.get('path', '')}".strip(),
                        f"Build `{op}` to its contract, with tests for success and every listed error. "
                        f"{ln.get('summary', '')}"))
    elif r["track"] == "Database":
        m = re.search(r"Tables: (.+?)\. Source", r["description"])
        for t in (m.group(1).split(", ") if m else []):
            out.append((f"{key}#{t}", key, f"[DB] {t}", f"Create `{t}` in this migration with its keys, "
                        "indexes and row-level security; include it in ROLLBACK."))
    elif r["track"] == "Frontend":
        name = r["subject"].split("] ", 1)[-1]
        for part, text in (("build", "Build the screen with every state (loading, empty, error, offline) against the mock API."),
                           ("wire", "Connect the screen to the real API once its backend tasks are done."),
                           ("test", "Component tests for the states and the main flows; lint and typecheck pass.")):
            label = {"build": "build with all states", "wire": "connect to API", "test": "tests"}[part]
            out.append((f"{key}#{part}", key, f"[FE] {name}: {label}", text))
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--schedule", required=True)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--delete-test", action="store_true", help="delete the old 'test:' work packages first")
    ap.add_argument("--workers", type=int, default=1, help="links sent at once")
    ap.add_argument("--batch", type=int, default=5, help="links between server-idle checks")
    ap.add_argument("--all-links", action="store_true",
                    help="also send links another chain already implies (A>C when A>B>C); same effect, more calls")
    ap.add_argument("--idle-seconds", type=float, default=3.0, help="a read slower than this means the server is busy")
    ap.add_argument("--idle-wait", type=int, default=60, help="seconds to wait before checking again")
    ap.add_argument("--export", metavar="JSON",
                    help="write the work packages still to make to this file instead of making them; "
                         "tools/op-create.rb makes them on the server, without Cloudflare's 100-second limit")
    a = ap.parse_args()
    token = os.environ.get("TICVAI_OP_TOKEN", "")
    if not token and not a.dry_run and not a.export:
        print("TICVAI_OP_TOKEN is not set")
        return 2
    auth = "Basic " + base64.b64encode(f"apikey:{token}".encode()).decode()

    def call(method, path, body=None, tries=4):
        for i in range(tries):
            req = urllib.request.Request(BASE + path, json.dumps(body).encode() if body is not None else None,
                                         {"Content-Type": "application/json", "Authorization": auth,
                                          "User-Agent": "curl/8.0"}, method=method)
            try:
                with urllib.request.urlopen(req, timeout=180) as r:
                    txt = r.read().decode("utf-8") or "{}"
                    return json.loads(txt)
            except urllib.error.HTTPError as e:
                msg = e.read().decode("utf-8", "replace")
                if e.code in (429, 500, 502, 503, 504) and i < tries - 1:
                    time.sleep(2 * (i + 1))
                    continue
                raise RuntimeError(f"{method} {path} -> {e.code}: {msg[:400]}")
            except (urllib.error.URLError, ConnectionError, TimeoutError):
                # A create that timed out may still have been made on the server: retrying it made four copies
                # of one sub-task on 28 September. Stop instead, and check the project before running again.
                if method == "POST":
                    raise RuntimeError(f"{method} {path} timed out; it may have been created. Check the project "
                                       "for the newest work packages (tools/op-recent.py) before running again")
                if i < tries - 1:
                    time.sleep(2 * (i + 1))
                    continue
                raise

    rows = list(csv.DictReader((DOCS / "tasks.csv").open(encoding="utf-8")))
    by_key = {r["key"]: r for r in rows}
    sched = json.load(open(a.schedule, encoding="utf-8"))
    lineage = json.loads((ROOT / "handoff" / "api-data-lineage.json").read_text(encoding="utf-8"))
    who = sched["assign"]
    # **Two-week sprints** (1 October): a task's version is "Sprint n", the sprint it starts in (1-13; later work
    # is planned into Sprint 13). The old "Block A · Week n" versions stay in the project and are no longer set.
    week = {k: max(1, min(int(v), LAST_SPRINT)) for k, v in (sched.get("sprint") or {}).items()}
    for k, v in sched["start"].items():
        week.setdefault(k, max(1, min(int(v // 10) + 1, LAST_SPRINT)))
    sprint_cal = {int(x["n"]): x for x in sched.get("sprints") or []}
    svc_owner = {r["service"]: r["assignee"] for r in rows if r["type"] == "Epic" and r["key"].startswith("SVC-")}
    mp = json.loads(MAP.read_text(encoding="utf-8")) if MAP.exists() else {}

    def save():
        MAP.write_text(json.dumps(mp, indent=1), encoding="utf-8")

    users = {}
    if not a.dry_run and not a.export:
        for u in call("GET", f"/projects/{PROJECT}/available_assignees?pageSize=200")["_embedded"]["elements"]:
            users[u["name"]] = u["id"]

    def user_link(name):
        return {"href": f"/api/v3/users/{users[name]}"} if name in users else None

    # ---- 1. the old test tickets
    if a.delete_test and not a.export:
        old = [] if a.dry_run else call("GET", f'/projects/{PROJECT}/work_packages?pageSize=200&filters='
                                        + urllib.request.quote(json.dumps([{"status": {"operator": "*", "values": []}}])))["_embedded"]["elements"]
        old = [w for w in old if w["subject"].startswith("test:")]
        for w in old:
            call("DELETE", f"/work_packages/{w['id']}")
            print(f"deleted #{w['id']} {w['subject']}")

    # ---- 2. versions: one per sprint ("Sprint 1" ... "Sprint 13", 1 October; the week versions are left alone)
    for n in range(1, LAST_SPRINT + 1):
        k = f"VERSION-S{n}"
        if k in mp or a.dry_run or a.export:
            continue
        body = {"name": f"Sprint {n}", "_links": {"definingProject": {"href": f"/api/v3/projects/{PROJECT}"}}}
        if sprint_cal.get(n):
            body.update({"startDate": sprint_cal[n]["start"], "endDate": sprint_cal[n]["end"]})
        v = call("POST", "/versions", body)
        mp[k] = v["id"]
        save()
        print(f"version Sprint {n} -> {v['id']}")

    # ---- 3. work packages, parents first (tasks.csv is written parents first)
    def checker(key, track):
        w = week.get(key, 1) - 1
        return (BE_CHECK[w % len(BE_CHECK)] if track in ("Backend", "Database")
                else FE_CHECK[w % len(FE_CHECK)])

    def accountable(r):
        if r.get("accountable"):                 # written by the sprint plan (1 October)
            return r["accountable"]
        if r["track"] in ("Backend", "Database"):
            return svc_owner.get(r["service"]) or LEAD["devops"]
        area = "VM" if r["area"] == "VM" else r["area"]
        return LEAD.get(area) or r["assignee"]

    exported = []

    def create(key, typ, subject, desc, parent_key, assignee, acct, prio, version_week, seq):
        if key in mp:
            return
        if a.export:
            exported.append({"key": key, "type_id": TYPES[typ], "subject": subject[:255],
                             "description": full.get(key, desc), "parent_key": parent_key,
                             "parent_id": mp.get(parent_key) if parent_key else None,
                             "assignee": assignee, "responsible": acct, "priority_id": prio,
                             "version_id": mp.get(f"VERSION-S{version_week}") if version_week else None,
                             "sequence": int(seq) if seq else None, "priority_no_field": PRIORITY_NO})
            return
        links = {"type": {"href": f"/api/v3/types/{TYPES[typ]}"},
                 "priority": {"href": f"/api/v3/priorities/{prio}"}}
        if parent_key:
            links["parent"] = {"href": f"/api/v3/work_packages/{mp[parent_key]}"}
        for field, name in (("assignee", assignee), ("responsible", acct)):
            if name and user_link(name):
                links[field] = user_link(name)
        if version_week and f"VERSION-S{version_week}" in mp:
            links["version"] = {"href": f"/api/v3/versions/{mp[f'VERSION-S{version_week}']}"}
        body = {"subject": subject[:255], "description": {"format": "markdown", "raw": full.get(key, desc)},
                "_links": links}
        if seq:
            body[PRIORITY_NO] = int(seq)
        try:
            wp_id = call("POST", f"/projects/{PROJECT}/work_packages", body)["id"]
        except RuntimeError as e:
            # Cloudflare gives up after 100 s (524) while OpenProject goes on and makes the work package: a new
            # sub-task under a big migration task took longer than that on 28 September. Find it, don't remake it.
            if "-> 524" not in str(e) and "timed out" not in str(e):
                raise
            wp_id = made_late(subject[:255], mp[parent_key] if parent_key else None)
            print(f"  {key}: the server answered late; found it as #{wp_id}", flush=True)
        mp[key] = wp_id
        save()      # every one: a run stopped part-way must not leave made tickets unrecorded

    def made_late(subject, parent_id, wait=600):
        known = {v for v in mp.values() if isinstance(v, int)}
        query = ("/projects/%d/work_packages?pageSize=40&sortBy=%s&filters=%s" % (
            PROJECT, urllib.request.quote('[["id","desc"]]'),
            urllib.request.quote(json.dumps([{"status": {"operator": "*", "values": []}}]))))
        until = time.time() + wait
        while time.time() < until:
            for w in call("GET", query)["_embedded"]["elements"]:
                parent = ((w["_links"].get("parent") or {}).get("href") or "").rsplit("/", 1)[-1]
                if w["id"] not in known and w["subject"] == subject and parent == (str(parent_id) if parent_id else ""):
                    return w["id"]
            time.sleep(20)
        raise RuntimeError(f"'{subject}' was not made within {wait}s; check the project before running again")

    def small(r, assignee, wk):
        """The sub-tasks under a task: one per operation, one per table, three per screen."""
        return [(k, p, s, d, assignee, r, wk) for k, p, s, d in sub_tasks(r, lineage)]

    # The full description for every ticket (tools/op-descriptions.py): contract, tables, screens, done-when and
    # plan. The short text built below is only the fallback for a key the builder does not know.
    keys = [r["key"] for r in rows] + [s[0] for r in rows if r["type"] == "Task" for s in small(r, None, None)]
    full = __import__("op-descriptions").build(a.schedule, keys)

    counts = defaultdict(int)
    subs = []
    for r in rows:
        key, typ = r["key"], r["type"]
        assignee = who.get(key) or r["assignee"]
        wk = week.get(key)
        extra = [f"Build order: #{r['sequence']}" + (f" · {assignee}'s queue" if assignee else "")]
        if typ == "Task":
            extra.append(f"Planned: Sprint {wk}" + (f" (Block {r['block']})" if r.get("block") else "") if wk else "")
            extra.append(f"Checker (sprint {wk}): {checker(key, r['track'])}" if wk else "")
            if r["dependsOn"]:
                extra.append("Follows: " + ", ".join(r["dependsOn"].split()))
        desc = (r["description"] or "") + "\n\n" + "\n".join(f"- {x}" for x in extra if x) + f"\n\nKey: `{key}` · Track: {r['track']} · Points: {r['points']}"
        counts[typ] += 1
        if not a.dry_run:
            create(key, typ, r["subject"], desc, r["parent"] or None, assignee if typ == "Task" else (r["assignee"] or None),
                   accountable(r), PRIORITY.get(r["wave"] or "2", 8), wk if typ == "Task" else None, r["sequence"])
        if typ == "Task":
            subs += small(r, assignee, wk)
    counts["Sub Task"] = len(subs)
    if a.dry_run:
        print(dict(counts), "relations:", sum(1 for r in rows if r["type"] == "Task" and r["dependsOn"]))
        return 0
    if not a.export:
        save()
    print("work packages:", {k: v for k, v in counts.items()}, flush=True)
    for i, (key, parent, subject, desc, assignee, r, wk) in enumerate(subs, 1):
        create(key, "Sub Task", subject, desc, parent, assignee, accountable(r), PRIORITY.get(r["wave"] or "2", 8),
               wk, r["sequence"])
        if i % 100 == 0:
            save()
            print(f"  sub-tasks {i}/{len(subs)}", flush=True)
    if a.export:
        Path(a.export).write_text(json.dumps(exported, indent=1, ensure_ascii=False), encoding="utf-8")
        print(f"exported {len(exported)} work packages to make -> {a.export}")
        return 0
    save()

    # ---- 4. relations: a task follows each task it depends on. Several at once: each one makes OpenProject
    # reschedule the chain behind it, so a single stream gets slower as the chains grow. Only a link that exists
    # (created now, or found already there) is recorded; a failed one is retried on the next run.
    done_rel = set(mp.get("_relations", []))
    edges = [(r["key"], d) for r in rows if r["type"] == "Task" and r["dependsOn"] for d in r["dependsOn"].split()]
    if not a.all_links:
        edges = reduce_links(edges)
    todo = [(k, d) for k, d in edges if f"{k}>{d}" not in done_rel and d in mp]

    def link(pair):
        k, d = pair
        for i in range(6):
            try:
                call("POST", f"/work_packages/{mp[k]}/relations",
                     {"_links": {"from": {"href": f"/api/v3/work_packages/{mp[k]}"},
                                 "to": {"href": f"/api/v3/work_packages/{mp[d]}"}}, "type": "follows"})
                return pair, "made"
            except (RuntimeError, OSError) as e:
                msg = str(e)
                if "422" in msg and re.search(r"already|taken|exists", msg, re.I):
                    return pair, "there"
                if ("409" in msg or "lock" in msg.lower() or "422" not in msg) and i < 5:
                    time.sleep(3 * (i + 1))      # a clash with a neighbouring link, or the server: try again
                    continue
                return pair, "failed: " + msg[:160]

    def idle():
        """Wait until a plain read is quick again: the server is shared, and these links load it."""
        probe = f"/work_packages/{next(iter(v for k, v in mp.items() if not k.startswith(('_', 'VERSION'))))}"
        while True:
            t = time.time()
            try:
                call("GET", probe)
            except (RuntimeError, OSError):
                pass
            took = time.time() - t
            if took <= a.idle_seconds:
                return
            print(f"  server busy (a read took {took:.1f}s); waiting {a.idle_wait}s", flush=True)
            time.sleep(a.idle_wait)

    failed = n = 0
    print(f"relations: {len(todo)} to make, in batches of {a.batch}, {a.workers} at a time", flush=True)
    with ThreadPoolExecutor(a.workers) as pool:
        for b in range(0, len(todo), a.batch):
            idle()
            t = time.time()
            for fut in as_completed([pool.submit(link, p) for p in todo[b:b + a.batch]]):
                (k, d), outcome = fut.result()
                n += 1
                if outcome.startswith("failed"):
                    failed += 1
                    print("  relation failed:", f"{k}>{d}", outcome, flush=True)
                else:
                    done_rel.add(f"{k}>{d}")
            mp["_relations"] = sorted(done_rel)
            save()
            print(f"  relations {n}/{len(todo)} ({time.time() - t:.0f}s for the batch)", flush=True)
    mp["_relations"] = sorted(done_rel)
    save()
    print("done:", len([k for k in mp if not k.startswith(("_", "VERSION"))]), "work packages,",
          len(done_rel), "relations,", failed, "failed (re-run to retry)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
