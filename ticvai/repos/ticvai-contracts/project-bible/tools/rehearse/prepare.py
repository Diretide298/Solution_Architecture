#!/usr/bin/env python3
"""The rehearsal's inputs (release runbook section 4; CHG-RHS-001), each a subcommand rehearse.sh runs:

  sparse    the candidate clone's sparse-checkout patterns: everything but the mirrors under ticvai/repos/, of which
            only what ADAM's release export keeps (viewer/lib/export-keep.json), so a `file` link that adam-links.py
            checks on disk resolves as it does at the release.
  tickets   every Feature and Task of the block (tasks.csv `block`) by its OpenProject id, read from the candidate's
            pms-map.json after op-created-merge.py merged the stand-in ids (so a ticket the release creates is pulled
            by its stand-in id); and every ticket of the last live pull no longer in the block, as left-block (pulled
            for the record, never judged).
  registry  ADAM's project registry for the rehearsal: the clone's package only, its release exports in the work folder.
  served    waits until ADAM serves r<N> at the candidate's commit (served.json); fails if it serves anything else.
  account   the rehearsal's ADAM account (the first, an admin), its OpenProject token for the stand-in, and the
            project's OpenProject number. The password goes to run/account.env only; nothing prints it.
  pins      every ticket the last release had, pinned at r<N-1> for the rehearsal account, as a developer who pulled
            it then holds it: each pull then says what changed since, as it will for them.
  live      the rehearsal's list with each created ticket's real id (the apply's op-created-r<N>.json) in place of its
            stand-in id, for the live re-pull.
  snapshot  READS OpenProject (GET only, TICVAI_OP_TOKEN): every work package of the project with its owners, the
            statuses, and who can be assigned. The lead runs it before the rehearsal; rehearse.sh never does.

    python tools/rehearse/prepare.py --self-test
    python tools/rehearse/prepare.py <subcommand> --help

The self-tests run first, every time.
"""
from __future__ import annotations

import argparse
import base64
import csv
import http.cookiejar
import json
import os
import secrets
import sqlite3
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from simulate import STAND_IN_FROM  # noqa: E402

PMS = "https://pms.softlabsgroup.in"
LEFT = "left-block"
TRACK_ROLE = {"Frontend": "frontend", "Backend": "backend", "Database": "backend", "DevOps": "backend",
              "Onboarding": "backend", "Test": "other", "AI": "other"}


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


def write(path, text) -> None:
    """LF line ends on every platform: bash sources account.env, and a CR would end up in the password."""
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def sparse_patterns(keep: dict) -> list:
    out = ["/*", "!/ticvai/repos/", "/ticvai/repos/*/*", "!/ticvai/repos/*/*/"]
    out += [f"/ticvai/repos/*/{d}/" for d in keep.get("every_repo") or []]
    out += [f"/ticvai/repos/{repo}/{d}/" for repo, dirs in sorted((keep.get("per_repo") or {}).items()) for d in dirs]
    return out


def ticket_list(rows, ids, created, base_log, block) -> tuple:
    """(tickets, problems). `ids`: key -> OpenProject id (bundle ids, then pms-map after the merge)."""
    tickets, problems, keys, seen = [], [], set(), set()
    for r in rows:
        if r.get("block") != block or r.get("type") not in ("Feature", "Task"):
            continue
        k = r["key"]
        i = ids.get(k)
        if not isinstance(i, int):
            problems.append(f"{k}: no OpenProject id, and the release does not create it")
            continue
        tickets.append({"id": i, "key": k, "type": r["type"],
                        "role": "frontend" if r["type"] == "Feature" else TRACK_ROLE.get(r.get("track") or "", "other"),
                        "kind": "Feature" if r["type"] == "Feature" else (r.get("track") or "Task"),
                        "assignee": r.get("assignee") or "",
                        "set": "created" if k in created else ("in-base" if str(i) in base_log else "moved-in")})
        keys.add(k)
        seen.add(str(i))
    for i, row in sorted(base_log.items(), key=lambda x: int(x[0])):
        if i in seen or (row.get("key") or "") in keys:
            continue
        tickets.append({"id": int(i), "key": row.get("key") or "", "type": row.get("type") or "",
                        "role": row.get("role") or "other", "kind": row.get("kind") or "", "assignee": "",
                        "set": LEFT})
    return tickets, problems


def live_list(tickets, stand_in, real) -> tuple:
    """(the list with each created ticket's real id, problems). stand_in, real: op-created files {key: id}."""
    stand_ids = {v: k for k, v in stand_in.items() if isinstance(v, int) and v >= STAND_IN_FROM}
    others = {t["id"] for t in tickets if t["id"] not in stand_ids}
    out, problems = [], []
    for t in tickets:
        if t["id"] not in stand_ids:
            out.append(dict(t))
            continue
        k = stand_ids[t["id"]]
        i = real.get(k)
        if not isinstance(i, int):
            problems.append(f"{k}: the release's op-created file has no id for it (stand-in #{t['id']})")
        elif i in others:
            problems.append(f"{k}: real id #{i} is already another ticket on the list")
        else:
            out.append({**t, "id": i, "standIn": t["id"]})
    return out, problems


def registry(clone, releases) -> dict:
    return {"default": "ticvai", "projects": [{
        "id": "ticvai", "name": "TICVAI", "root": str(clone), "contracts": "contracts", "active": True,
        "releases": str(releases), "note": "The rehearsal's candidate (tools/rehearse/rehearse.sh)."}]}


def served_problem(releases, tag, commit):
    doc = load(Path(releases) / "served.json")
    if not doc:
        return f"no served.json under {releases} yet"
    if doc.get("mode") != "tag" or doc.get("tag") != tag:
        return f"ADAM serves {doc.get('mode')} {doc.get('tag')} ({doc.get('problem') or 'no problem given'}), not {tag}"
    got = str(doc.get("commit") or "")
    if not got or not (commit.startswith(got) or got.startswith(commit)):
        return f"ADAM serves {tag} at {got[:8]}, not the candidate {commit[:8]}"
    return None


def pins(db, email, tickets, tag, commit, project="ticvai") -> tuple:
    """(exit code, rows written or the problem). Every ticket but the created ones, pinned at `tag` for the account.
    Prints nothing: the self-tests call it, and `sparse` output must hold the patterns only."""
    conn = sqlite3.connect(db, timeout=30)
    try:
        acc = conn.execute("SELECT id FROM account WHERE email_folded = ?", (email.strip().lower(),)).fetchone()
        if not acc:
            return 1, f"no ADAM account for {email} in {db}"
        now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        rows = [(acc[0], project, str(t["id"]), tag, commit, now, now) for t in tickets if t.get("set") != "created"]
        with conn:
            conn.executemany("INSERT OR IGNORE INTO ticket_pin (account_id, project_id, external_key, tag, commit_sha, "
                             "pinned_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?)", rows)
        return 0, len(rows)
    finally:
        conn.close()


def account(api, origin, op, op_token, project_id, env_out) -> int:
    """The rehearsal account, through ADAM's own API, as a person setting up ADAM would."""
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))

    def call(method, path, body=None):
        req = urllib.request.Request(api + path, data=json.dumps(body).encode() if body is not None else None,
                                     method=method, headers={"content-type": "application/json", "origin": origin})
        try:
            with opener.open(req, timeout=120) as res:
                return res.status, json.loads(res.read() or b"null")
        except urllib.error.HTTPError as e:
            return e.code, e.read().decode("utf-8", "replace")[:300]

    code, st = call("GET", "/api/auth/state")
    if code != 200 or not isinstance(st, dict) or not st.get("needsBootstrap"):
        print(f"the rehearsal database already has accounts, or ADAM did not answer ({code}): use a new work folder")
        return 1
    domain = st.get("domain") if isinstance(st.get("domain"), str) and st.get("domain") else "softlabsgroup.com"
    email = f"rehearsal@{domain}"
    password = "Rh-" + secrets.token_urlsafe(18)
    for method, path, body in (
            ("POST", "/api/auth/bootstrap", {"email": email, "name": "Rehearsal Account", "password": password}),
            ("PUT", "/api/settings/openproject", {"token": op_token, "endpoint": op}),
            ("PUT", "/api/pms/projects/ticvai", {"pms_project_id": int(project_id)})):
        code, answer = call(method, path, body)
        print(f"  {method} {path}: {code}")
        if code >= 300:
            print(f"  {answer}")
            return 1
    write(env_out, f"ADAM_EMAIL={email}\nADAM_PASSWORD={password}\n")
    try:
        os.chmod(env_out, 0o600)
    except OSError:
        pass
    print(f"account {email}; its password is in {env_out} only")
    return 0


def snapshot(token, project, out, pms=PMS) -> int:
    """READ ONLY: GETs of the project's work packages (all statuses), the statuses and the assignable people."""
    auth = "Basic " + base64.b64encode(f"apikey:{token}".encode()).decode()

    def get(path, params=None):
        url = f"{pms}/api/v3/{path}" + ("?" + urllib.parse.urlencode(params) if params else "")
        req = urllib.request.Request(url, method="GET", headers={"Authorization": auth, "User-Agent": "curl/8.0"})
        for attempt in range(4):
            try:
                with urllib.request.urlopen(req, timeout=600) as r:
                    return json.load(r)
            except urllib.error.HTTPError as e:
                # the proxy gives up after 100 seconds (524) or while OpenProject restarts (502); a read is safe to repeat
                if e.code not in (502, 503, 524) or attempt == 3:
                    raise
                time.sleep(30 * (attempt + 1))

    flt = json.dumps([{"status": {"operator": "*", "values": []}}])
    wps, off = [], 1
    while True:
        d = get(f"projects/{project}/work_packages", {"pageSize": 200, "offset": off, "filters": flt})
        els = d["_embedded"]["elements"]
        wps += els
        if len(wps) >= d["total"] or not els:
            break
        off += 1
    statuses = [{"id": s["id"], "name": s["name"], "isClosed": bool(s.get("isClosed")),
                 "isDefault": bool(s.get("isDefault"))} for s in get("statuses")["_embedded"]["elements"]]
    people = [u["name"] for u in get(f"projects/{project}/available_assignees",
                                     {"pageSize": 1000})["_embedded"]["elements"]]
    taken = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    Path(out).write_text(json.dumps({"takenAt": taken, "openproject": pms, "project": project, "statuses": statuses,
                                     "assignable": people, "work_packages": wps}, ensure_ascii=False),
                         encoding="utf-8")
    print(f"{len(wps)} work packages, {len(statuses)} statuses, {len(people)} assignable people at {taken} -> {out}")
    return 0


def main(argv=None) -> int:
    utf8()
    argv = sys.argv[1:] if argv is None else argv
    fails = self_test()
    for f in fails:
        print(f"  SELF-TEST    {f}")
    if fails:
        print(f"FAIL {len(fails)} self-test(s)")
        return 1
    if not argv or argv == ["--self-test"]:
        print("PASS - prepare.py self-tests")
        return 0
    ap = argparse.ArgumentParser(description="The rehearsal's inputs.")
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("sparse")
    s.add_argument("--keep", required=True)
    s = sub.add_parser("tickets")
    for x in ("--clone", "--bundle", "--created", "--base", "--out"):
        s.add_argument(x, required=True)
    s.add_argument("--block", default="A")
    s = sub.add_parser("registry")
    for x in ("--clone", "--releases", "--out"):
        s.add_argument(x, required=True)
    s = sub.add_parser("served")
    for x in ("--releases", "--tag", "--commit"):
        s.add_argument(x, required=True)
    s.add_argument("--wait", type=int, default=1800)
    s = sub.add_parser("account")
    for x in ("--api", "--origin", "--op", "--op-token", "--project", "--env-out"):
        s.add_argument(x, required=True)
    s = sub.add_parser("pins")
    for x in ("--db", "--email", "--tickets", "--tag", "--commit"):
        s.add_argument(x, required=True)
    s = sub.add_parser("live")
    for x in ("--tickets", "--stand-in", "--created", "--out"):
        s.add_argument(x, required=True)
    s = sub.add_parser("snapshot")
    s.add_argument("--out", required=True)
    s.add_argument("--project", type=int, default=153)
    s.add_argument("--openproject", default=PMS)
    a = ap.parse_args(argv)

    if a.cmd == "sparse":
        print("\n".join(sparse_patterns(load(a.keep, {}) or {})))
        return 0
    if a.cmd == "tickets":
        docs = Path(a.clone) / "handoff" / "service-docs"
        rows = list(csv.DictReader((docs / "tasks.csv").open(encoding="utf-8")))
        ids = {k: v for k, v in ((load(a.bundle, {}) or {}).get("ids") or {}).items() if isinstance(v, int)}
        ids.update({k: v for k, v in (load(docs / "pms-map.json", {}) or {}).items()
                    if isinstance(v, int) and not k.startswith(("_", "VERSION"))})
        base_log = {}
        for line in (Path(a.base) / "pull-log.jsonl").read_text(encoding="utf-8").splitlines():
            if line.strip():
                r = json.loads(line)
                base_log[str(r["id"])] = r
        tickets, problems = ticket_list(rows, ids, load(a.created, {}) or {}, base_log, a.block)
        for p in problems:
            print(f"  {p}")
        if problems:
            print(f"FAIL - {len(problems)} block ticket(s) with no id: the bundle neither has nor creates them")
            return 1
        Path(a.out).write_text(json.dumps(tickets, indent=1), encoding="utf-8")
        counts = {}
        for t in tickets:
            counts[t["set"]] = counts.get(t["set"], 0) + 1
        print(f"{len(tickets)} tickets to pull: {counts} -> {a.out}")
        return 0
    if a.cmd == "registry":
        write(a.out, json.dumps(registry(a.clone, a.releases), indent=1))
        return 0
    if a.cmd == "served":
        until = time.time() + a.wait
        while True:
            problem = served_problem(a.releases, a.tag, a.commit)
            if problem is None:
                print(f"ADAM serves {a.tag} at {a.commit[:8]}")
                return 0
            if not problem.startswith("no served.json") or time.time() > until:
                print(f"FAIL - {problem}")
                return 1
            time.sleep(5)
    if a.cmd == "account":
        return account(a.api, a.origin, a.op, a.op_token, a.project, a.env_out)
    if a.cmd == "pins":
        code, n = pins(a.db, a.email, load(a.tickets, []) or [], a.tag, a.commit)
        print(f"{n} tickets pinned at {a.tag}, as a developer who pulled them at that release holds them" if code == 0
              else f"FAIL - {n}")
        return code
    if a.cmd == "live":
        out, problems = live_list(load(a.tickets, []) or [], load(a.stand_in, {}) or {}, load(a.created, {}) or {})
        for p in problems:
            print(f"  {p}")
        if problems:
            print(f"FAIL - {len(problems)} created ticket(s) without a usable real id")
            return 1
        Path(a.out).write_text(json.dumps(out, indent=1), encoding="utf-8")
        print(f"{len(out)} tickets, {sum(1 for t in out if 'standIn' in t)} by their real ids now -> {a.out}")
        return 0
    token = os.environ.get("TICVAI_OP_TOKEN", "")
    if not token:
        print("FAIL - set TICVAI_OP_TOKEN (read only: the snapshot makes GET calls only)")
        return 1
    return snapshot(token, a.project, a.out, a.openproject)


# --------------------------------------------------------------------------------------------------- self-tests
def self_test() -> list:
    fails = []
    keep = {"every_repo": [".github", "openapi"], "per_repo": {"ticvai-docs": ["setup"]}}
    want = ["/*", "!/ticvai/repos/", "/ticvai/repos/*/*", "!/ticvai/repos/*/*/", "/ticvai/repos/*/.github/",
            "/ticvai/repos/*/openapi/", "/ticvai/repos/ticvai-docs/setup/"]
    if sparse_patterns(keep) != want:
        fails.append(f"sparse patterns {sparse_patterns(keep)}")
    rows = [{"key": "F-1", "type": "Feature", "block": "A", "track": "", "assignee": "Pranay Shinde"},
            {"key": "T-1", "type": "Task", "block": "A", "track": "Database", "assignee": "Hrushikant Patkar"},
            {"key": "T-NEW", "type": "Task", "block": "A", "track": "Frontend", "assignee": ""},
            {"key": "T-LOST", "type": "Task", "block": "A", "track": "Backend", "assignee": ""},
            {"key": "T-B", "type": "Task", "block": "B", "track": "Backend", "assignee": ""},
            {"key": "E-A", "type": "Epic", "block": "A", "track": "", "assignee": ""}]
    ids = {"F-1": 100, "T-1": 101, "T-NEW": STAND_IN_FROM, "T-B": 103, "E-A": 99}
    base = {"100": {"id": 100, "key": "F-1"}, "101": {"id": 101, "key": "T-1"},
            "150": {"id": 150, "key": "T-GONE", "role": "backend", "kind": "Backend"}}
    got, problems = ticket_list(rows, ids, {"T-NEW": STAND_IN_FROM}, base, "A")
    sets = {t["key"]: (t["id"], t["set"]) for t in got}
    if sets != {"F-1": (100, "in-base"), "T-1": (101, "in-base"), "T-NEW": (STAND_IN_FROM, "created"),
                "T-GONE": (150, LEFT)}:
        fails.append(f"the block's list was {sets}")
    if problems != ["T-LOST: no OpenProject id, and the release does not create it"]:
        fails.append(f"a block ticket with no id gave {problems}")
    if [t["role"] for t in got[:3]] != ["frontend", "backend", "frontend"]:
        fails.append(f"roles {[t['role'] for t in got[:3]]}")
    got2, _ = ticket_list(rows[:2], {"F-1": 100, "T-1": 555}, {}, base, "A")
    if [(t["key"], t["set"]) for t in got2] != [("F-1", "in-base"), ("T-1", "moved-in"), ("T-GONE", LEFT)]:
        fails.append(f"a block ticket with a new id, and its old id, gave {[(t['key'], t['set']) for t in got2]}")
    tickets = [{"id": 100, "key": "F-1", "set": "in-base"}, {"id": STAND_IN_FROM, "key": "T-NEW", "set": "created"},
               {"id": 200, "key": "T-TAKEN", "set": "created"}, {"id": 150, "key": "T-GONE", "set": LEFT}]
    stand = {"T-NEW": STAND_IN_FROM, "T-TAKEN": 200}
    out, problems = live_list(tickets, stand, {"T-NEW": 31000, "T-TAKEN": 200})
    if [t["id"] for t in out] != [100, 31000, 200, 150] or problems or out[1].get("standIn") != STAND_IN_FROM:
        fails.append(f"the live list was {out} / {problems}")
    _, problems = live_list(tickets, stand, {})
    if problems != [f"T-NEW: the release's op-created file has no id for it (stand-in #{STAND_IN_FROM})"]:
        fails.append(f"a created ticket with no real id gave {problems}")
    _, problems = live_list(tickets, stand, {"T-NEW": 100})
    if problems != ["T-NEW: real id #100 is already another ticket on the list"]:
        fails.append(f"a real id another ticket has gave {problems}")
    reg = registry("C:/w/rc/ticvai", "C:/w/run/releases")
    p = reg["projects"][0]
    if (reg["default"], p["id"], p["root"], p["releases"]) != ("ticvai", "ticvai", "C:/w/rc/ticvai", "C:/w/run/releases"):
        fails.append(f"registry {reg}")
    with tempfile.TemporaryDirectory() as tmp:
        if "no served.json" not in (served_problem(tmp, "r7", "abcdef1234") or ""):
            fails.append("no served.json was not a problem")
        Path(tmp, "served.json").write_text(json.dumps({"mode": "working", "tag": None}), encoding="utf-8")
        if "not r7" not in (served_problem(tmp, "r7", "abcdef1234") or ""):
            fails.append("a viewer serving its working tree passed")
        Path(tmp, "served.json").write_text(json.dumps({"mode": "tag", "tag": "r7", "commit": "abcdef1234aa"}),
                                            encoding="utf-8")
        if served_problem(tmp, "r7", "abcdef1234aa") is not None:
            fails.append("the candidate served as r7 was a problem")
        if "not the candidate" not in (served_problem(tmp, "r7", "0123456789") or ""):
            fails.append("r7 at another commit passed")
        db = Path(tmp, "t.db")
        conn = sqlite3.connect(db)
        conn.executescript(
            "CREATE TABLE account (id INTEGER PRIMARY KEY, email_folded TEXT);"
            "INSERT INTO account VALUES (7, 'rehearsal@softlabsgroup.com');"
            "CREATE TABLE ticket_pin (id INTEGER PRIMARY KEY AUTOINCREMENT, account_id INTEGER, project_id TEXT, "
            "external_key TEXT, tag TEXT, commit_sha TEXT, pinned_at TEXT, updated_at TEXT, "
            "UNIQUE (account_id, project_id, external_key));")
        conn.commit()
        conn.close()
        for _ in range(2):
            code, n = pins(db, "Rehearsal@softlabsgroup.com", tickets, "r6", "abc")
        conn = sqlite3.connect(db)
        got = sorted(r[0] for r in conn.execute("SELECT external_key FROM ticket_pin WHERE tag = 'r6'"))
        conn.close()
        if code != 0 or got != ["100", "150"]:
            fails.append(f"pins gave {got} (a created ticket has no earlier pull to pin)")
        code, _ = pins(db, "nobody@softlabsgroup.com", tickets, "r6", "abc")
        if code == 0:
            fails.append("pins for an account that does not exist passed")
    return fails


if __name__ == "__main__":
    sys.exit(main())
