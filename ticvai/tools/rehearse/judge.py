#!/usr/bin/env python3
"""Judge a rehearsal pull, and the live re-pull against it (release runbook section 4 "The rehearsal pull" and
section 7; CHG-GRD-003, CHG-RHS-001).

A rehearsal passes only with all five at zero, over every ticket of the block:
  1. pull errors (a ticket with no row in the pull log was never pulled, and counts);
  2. tickets whose pull does not say release r<N> (`release.current`);
  3. tickets with nothing linked (`linked: 0`), features and tasks alike;
  4. dead links (`notFound` above 0);
  5. open tickets that keep someone who left (the bundle's `successors`) as assignee or Accountable, started tickets
     included. Read from the stand-in OpenProject's state, because a pull does not carry Accountable (P-25: on r6 the
     rehearsal checked assignees only, and 158 Ready for QA tickets kept a leaver as Accountable). When that state's
     Accountable came from the previous bundle and not from an OpenProject snapshot, criterion 5 is NOT JUDGED and the
     rehearsal does not pass (exit 2).
And the stand-in must have answered ADAM at all: a rehearsal whose ADAM read some other OpenProject proves nothing.
Tickets that left the block are pulled for the record and never judged.

It also compares every ticket with the last live pull (the developer impact list) and writes
<work>/rehearsal-report.json and <work>/rehearsal-summary.md. The live mode compares the live re-pull after the
release with the rehearsal, ticket by ticket by key (the created tickets have real ids by then): release, links, dead
links and what each ticket touches must match; status, owner and sprint changes since are listed, not failed.

    python tools/rehearse/judge.py --self-test
    python tools/rehearse/judge.py rehearsal --work <work folder> --release r7 --base <last live pull>
    python tools/rehearse/judge.py live --rehearsal <work folder> --live <live re-pull folder> --release r7

Exit 0 pass, 1 fail, 2 not judged. The self-tests run first, every time.
"""
from __future__ import annotations

import argparse
import collections
import json
import sys
import tempfile
from pathlib import Path

REL_LINE = "- Written at release "
LEFT = "left-block"
NEW = "new to the block's pull"


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


def read_log(pull_dir) -> dict:
    """Ticket id -> the last row pull-direct.mjs logged for it (a re-run after an error logs again; the last wins)."""
    rows = {}
    p = Path(pull_dir) / "pull-log.jsonl"
    if p.is_file():
        for line in p.read_text(encoding="utf-8").splitlines():
            if line.strip():
                r = json.loads(line)
                rows[str(r["id"])] = r
    return rows


def read_ticket(pull_dir, i):
    return load(Path(pull_dir) / "workspace" / ".adam" / "work" / str(i) / "ticket.json")


def touches(t) -> set:
    return {f"{x.get('kind')} {x.get('id')}" for x in ((t or {}).get("touches") or [])}


def norm(text) -> str:
    return "\n".join(l for l in str(text or "").replace("\r\n", "\n").split("\n") if not l.startswith(REL_LINE)).strip()


def names(rows, n=20) -> str:
    if not rows:
        return ""
    more = f", and {len(rows) - n} more" if len(rows) > n else ""
    return " (" + ", ".join(f"#{r['id']} {r.get('key') or '?'}" for r in rows[:n]) + more + ")"


# ------------------------------------------------------------------------------------------------- the criteria
def leaver_tickets(state) -> list:
    """Open tickets (by the stand-in's own isClosed) whose assignee or Accountable left (the bundle's successors)."""
    left = set(state.get("leavers") or [])
    closed = {s["name"] for s in state.get("statuses") or [] if s.get("isClosed")}
    key_of = state.get("key_of") or {}
    out = []
    for i, w in sorted((state.get("packages") or {}).items(), key=lambda x: int(x[0])):
        ln = w.get("_links") or {}
        status = (ln.get("status") or {}).get("title")
        if status in closed:
            continue
        for field, label in (("assignee", "assignee"), ("responsible", "Accountable")):
            who = (ln.get(field) or {}).get("title")
            if who in left:
                out.append({"id": int(i), "key": key_of.get(str(i)), "status": status, "field": label, "person": who})
    return out


def criteria(tickets, log, release, state, requests) -> dict:
    """The five criteria and the stand-in check over the block's tickets; tickets that left the block are not judged."""
    judged = [t for t in tickets if t.get("set") != LEFT]
    c = {"tickets": len(judged), "errors": [], "release": [], "empty": [], "dead": [],
         "leavers": leaver_tickets(state), "requests": requests, "accountableFrom": state.get("accountableFrom")}
    for t in judged:
        r = log.get(str(t["id"]))
        if r is None or r.get("error"):
            c["errors"].append({"id": t["id"], "key": t["key"], "error": (r or {}).get("error") or "not pulled"})
            continue
        res = r.get("result") or {}
        got = (res.get("release") or {}).get("current")
        if got != release:
            c["release"].append({"id": t["id"], "key": t["key"], "release": got})
        if not res.get("linked"):
            c["empty"].append({"id": t["id"], "key": t["key"], "type": t.get("type")})
        if (res.get("notFound") or 0) > 0:
            c["dead"].append({"id": t["id"], "key": t["key"], "notFound": res["notFound"]})
    return c


def verdict(c) -> tuple:
    """(exit code, one line per criterion). 0 when all five are zero and the stand-in answered; 2 when nothing else
    failed but Accountable came from no OpenProject snapshot (criterion 5 not judged); 1 otherwise."""
    def ok(rows):
        return "PASS" if not rows else "FAIL"
    feats = sum(1 for r in c["empty"] if r.get("type") == "Feature")
    lv = c["leavers"]
    snap = c.get("accountableFrom") == "openproject"
    by = collections.Counter(f"{r['person']} as {r['field']}" for r in lv)
    lines = [
        f"- Pull errors: {len(c['errors'])} -> {ok(c['errors'])}{names(c['errors'])}",
        f"- Release on every ticket: {c['tickets'] - len(c['errors']) - len(c['release'])}/"
        f"{c['tickets'] - len(c['errors'])} -> {ok(c['release'])}{names(c['release'])}",
        f"- Nothing linked: {feats} features, {len(c['empty']) - feats} tasks -> {ok(c['empty'])}{names(c['empty'])}",
        f"- Dead links (notFound): {len(c['dead'])} tickets, {sum(r['notFound'] for r in c['dead'])} links -> "
        f"{ok(c['dead'])}{names(c['dead'])}",
        f"- Open tickets with someone who left as assignee or Accountable: {len(lv)}"
        + (f" ({'; '.join(f'{k}: {n}' for k, n in by.most_common())})" if lv else "")
        + f" -> {ok(lv) if (snap or lv) else 'NOT JUDGED'}{names(lv)}"
        + ("" if snap else " (Accountable came from the previous bundle, not OpenProject: take a snapshot with "
                           "prepare.py snapshot and run again)"),
        f"- The stand-in OpenProject answered {c['requests']} calls -> "
        + ("PASS" if c["requests"] else "FAIL (ADAM read some other OpenProject)"),
    ]
    if not c["tickets"]:
        lines.append("- No ticket was judged (is --block right?) -> NOT JUDGED")
        return 2, lines
    failed = c["errors"] or c["release"] or c["empty"] or c["dead"] or lv or not c["requests"]
    return (1 if failed else (0 if snap else 2)), lines


# --------------------------------------------------------------------------------------------- the impact list
def impact(tickets, base_log, base_dir, log, work_dir) -> list:
    """Ticket by ticket against the last live pull: what a developer will see change (the developer impact list)."""
    report = []
    for t in tickets:
        i = str(t["id"])
        a, b = base_log.get(i), log.get(i)
        ta, tb = read_ticket(base_dir, i), read_ticket(work_dir, i)
        wa, wb = (ta or {}).get("workPackage") or {}, (tb or {}).get("workPackage") or {}
        xa, xb = touches(ta), touches(tb)
        ops_a = {x for x in xa if x.startswith("operation ")}
        ops_b = {x for x in xb if x.startswith("operation ")}
        ra, rb = (a or {}).get("result") or {}, (b or {}).get("result") or {}
        rel = rb.get("release") or {}
        row = {
            "id": t["id"], "key": t["key"], "type": t.get("type"), "set": t.get("set"),
            "error": (b or {}).get("error") if b else "not pulled",
            "release": rel.get("current"), "movedFrom": rel.get("movedFrom"),
            "changedArtefacts": rel.get("changed"), "breaking": rel.get("breaking"),
            "status": {"before": wa.get("status"), "after": wb.get("status")},
            "links": {"before": ra.get("linked") if a else None, "after": rb.get("linked")},
            "notFound": {"before": ra.get("notFound") if a else None, "after": rb.get("notFound")},
            "operations": {"added": sorted(x[10:] for x in ops_b - ops_a),
                           "removed": sorted(x[10:] for x in ops_a - ops_b)},
            "otherLinks": {"added": sorted((xb - xa) - ops_b), "removed": sorted((xa - xb) - ops_a)},
            "assignee": {"before": wa.get("assignee") if ta else None, "after": wb.get("assignee")},
            "subject": {"before": wa.get("subject"), "after": wb.get("subject")}
            if ta and wa.get("subject") != wb.get("subject") else None,
            "sprint": {"before": wa.get("version"), "after": wb.get("version")}
            if ta and wa.get("version") != wb.get("version") else None,
            "parent": {"before": wa.get("parent"), "after": wb.get("parent")}
            if ta and wa.get("parent") != wb.get("parent") else None,
            "descriptionChanged": bool(ta) and norm(wa.get("description")) != norm(wb.get("description")),
            "releaseLineOnly": bool(ta) and wa.get("description") != wb.get("description")
            and norm(wa.get("description")) == norm(wb.get("description")),
            "newComments": max(0, len(wb.get("comments") or []) - len(wa.get("comments") or []))
            if ta else len(wb.get("comments") or []),
        }
        row["ownerChanged"] = bool(ta) and row["assignee"]["before"] != row["assignee"]["after"]
        row["changed"] = sorted(k for k, v in {
            "links": row["links"]["before"] != row["links"]["after"], "operations": bool(ops_a ^ ops_b),
            "otherLinks": bool((xa ^ xb) - ops_a - ops_b), "owner": row["ownerChanged"],
            "description": row["descriptionChanged"], "subject": bool(row["subject"]), "sprint": bool(row["sprint"]),
            "parent": bool(row["parent"]), "status": bool(ta) and wa.get("status") != wb.get("status"),
            "comments": row["newComments"] > 0}.items() if v) if ta else [NEW]
        report.append(row)
    return report


def summary(meta, c, lines, report) -> str:
    """rehearsal-summary.md: what ran, the five criteria, and the impact list in words and per developer."""
    rel, prev = meta.get("release") or "r<N>", meta.get("previous") or "the last release"
    block = [r for r in report if r["set"] != LEFT]
    gone = [r for r in report if r["set"] == LEFT]
    both = [r for r in block if r["set"] == "in-base"]
    C = collections.Counter
    snap = c.get("accountableFrom") == "openproject"
    now = (f"OpenProject's snapshot (`{meta.get('snapshot')}`)" if snap
           else f"the last live pull, with Accountable from the {prev} bundle (no OpenProject snapshot)")
    L = [f"# {rel} rehearsal pull: summary", "",
         f"Candidate `{meta.get('candidate')}` = {str(meta.get('commit') or '')[:8]}, served by a local ADAM as `{rel}` "
         f"(a clone with no remote; `{rel}` is tagged there only). Stand-in OpenProject: `{rel}`'s bundle "
         f"({meta.get('bundle') or 'committed'}) applied with op-release.rb's rules to {now}. Ticket links loaded as "
         f"production loads them (op-created-merge.py, adam-links.py, load_links.py --prune). Connector: the "
         f"candidate's viewer/mcp. Pins seeded at {prev}, so each pull reports the move a developer's will. Last live "
         f"pull: `{meta.get('base')}`.", "",
         f"Tickets pulled: {len(report)} = {len(block)} of Block {meta.get('block') or 'A'} "
         f"({dict(C(r['set'] for r in block))}) + {len(gone)} that left it.", "",
         "## Pass criteria", "", *lines, ""]
    L += [f"## {prev} -> {rel}, tickets in both pulls", "", f"Of {len(both)} tickets:", ""]
    L += [f"- {k}: {n}" for k, n in C(x for r in both for x in r["changed"]).most_common()]
    L += [f"- unchanged: {sum(1 for r in both if not r['changed'])}",
          f"- description changed only in the 'Written at release' line: "
          f"{sum(1 for r in both if r['releaseLineOnly'])}",
          f"- links {sum(r['links']['before'] or 0 for r in both)} -> {sum(r['links']['after'] or 0 for r in both)}; "
          f"tickets with nothing linked {sum(1 for r in both if not r['links']['before'])} -> "
          f"{sum(1 for r in both if not r['links']['after'])}",
          f"- operations added {sum(len(r['operations']['added']) for r in both)}, removed "
          f"{sum(len(r['operations']['removed']) for r in both)}",
          f"- linked artefacts changed since {prev} (the pull's 'what changed'): "
          f"{sum(1 for r in both if r['changedArtefacts'])} tickets; with a breaking change: "
          f"{sum(1 for r in both if r['breaking'])}"]
    moves = C(f"{r['assignee']['before']} -> {r['assignee']['after']}" for r in both if r["ownerChanged"])
    L += ["", "Owner changes: " + ("; ".join(f"{k}: {n}" for k, n in moves.most_common()) or "none"),
          "", "## Per developer (owner after the apply)", "",
          "| Developer | Tickets | Changed | Links changed | Operations changed | Description changed | Owner moved in "
          "| Owner moved out | New to the block |", "|---|---|---|---|---|---|---|---|---|"]
    devs = sorted({r["assignee"]["after"] or "(none)" for r in block}
                  | {r["assignee"]["before"] or "(none)" for r in both})
    for d in devs:
        mine = [r for r in block if (r["assignee"]["after"] or "(none)") == d]
        out_ = [r for r in both if (r["assignee"]["before"] or "(none)") == d and r["ownerChanged"]]
        L.append(f"| {d} | {len(mine)} | {sum(1 for r in mine if r['changed'])} | "
                 f"{sum(1 for r in mine if 'links' in r['changed'])} | "
                 f"{sum(1 for r in mine if 'operations' in r['changed'])} | "
                 f"{sum(1 for r in mine if 'description' in r['changed'])} | "
                 f"{sum(1 for r in mine if r['ownerChanged'])} | {len(out_)} | "
                 f"{sum(1 for r in mine if r['set'] != 'in-base')} |")
    L += ["", "## Left the block (pulled for the record, not judged)", ""]
    L += [f"- #{r['id']} {r['key']}: status {r['status']['before']} -> {r['status']['after']}, links "
          f"{r['links']['before']} -> {r['links']['after']}" + (f", error {r['error']}" if r["error"] else "")
          for r in gone]
    L += ["", "## New to the block's pull", ""]
    L += [f"- #{r['id']} {r['key']} ({r['type']}, {r['set']}): links {r['links']['after']}, "
          f"owner {r['assignee']['after']}" for r in block if r["set"] != "in-base"]
    return "\n".join(L) + "\n"


# ------------------------------------------------------------------------------------------- the live re-pull
def live_compare(reh_tickets, reh_log, reh_dir, live_tickets, live_log, live_dir, release) -> dict:
    """The live re-pull against the rehearsal, by key. Release, links, dead links and touches must match."""
    by_key = {t["key"]: t for t in live_tickets}
    out = {"compared": 0, "mismatch": [], "info": collections.Counter()}
    for t in reh_tickets:
        if t.get("set") == LEFT:
            continue
        lt = by_key.get(t["key"])
        if not lt:
            out["mismatch"].append({"key": t["key"], "why": "not on the live list"})
            continue
        out["compared"] += 1
        a, b = reh_log.get(str(t["id"])), live_log.get(str(lt["id"]))
        if b is None or b.get("error"):
            out["mismatch"].append({"key": t["key"], "id": lt["id"],
                                    "why": f"live pull: {(b or {}).get('error') or 'not pulled'}"})
            continue
        ra, rb = (a or {}).get("result") or {}, b.get("result") or {}
        why = []
        got = (rb.get("release") or {}).get("current")
        if got != release:
            why.append(f"live release {got}")
        if ra.get("linked") != rb.get("linked"):
            why.append(f"linked {ra.get('linked')} in the rehearsal, {rb.get('linked')} live")
        if (rb.get("notFound") or 0) > 0 or (ra.get("notFound") or 0) != (rb.get("notFound") or 0):
            why.append(f"dead links {ra.get('notFound') or 0} in the rehearsal, {rb.get('notFound') or 0} live")
        ta, tb = read_ticket(reh_dir, t["id"]), read_ticket(live_dir, lt["id"])
        xa, xb = touches(ta), touches(tb)
        if xa != xb:
            why.append(f"touches differ ({len(xb - xa)} only live, {len(xa - xb)} only in the rehearsal: "
                       f"{', '.join(sorted(xa ^ xb)[:4])})")
        if why:
            out["mismatch"].append({"key": t["key"], "id": lt["id"], "why": "; ".join(why)})
        wa, wb = (ta or {}).get("workPackage") or {}, (tb or {}).get("workPackage") or {}
        for f in ("status", "assignee", "version"):
            if wa.get(f) != wb.get(f):
                out["info"][f] += 1
    return out


# ------------------------------------------------------------------------------------------------------ the runs
def run_rehearsal(work: Path, release: str, base: Path) -> int:
    tickets, state = load(work / "tickets.json"), load(work / "op-state.json")
    if tickets is None or state is None:
        print(f"NOT JUDGED - {work} has no tickets.json or op-state.json (run rehearse.sh)")
        return 2
    meta = load(work / "rehearsal.json", {}) or {}
    stats = load(work / "run" / "op-stats.json", {}) or {}
    log, base_log = read_log(work / "direct"), read_log(base)
    c = criteria(tickets, log, release, state, int(stats.get("total") or 0))
    code, lines = verdict(c)
    report = impact(tickets, base_log, base, log, work / "direct")
    (work / "rehearsal-report.json").write_text(
        json.dumps({"criteria": c, "tickets": report}, indent=1, ensure_ascii=False), encoding="utf-8")
    text = summary({**meta, "release": release}, c, lines, report)
    (work / "rehearsal-summary.md").write_text(text, encoding="utf-8")
    print("\n".join(text.splitlines()[:14]))
    print({0: "PASS", 1: "FAIL", 2: "NOT JUDGED"}[code] + f" - {release} rehearsal: {work / 'rehearsal-summary.md'}")
    return code


def live_verdict(out) -> int:
    """1 on any mismatch, 2 when nothing was compared, else 0."""
    if out["mismatch"]:
        return 1
    return 0 if out["compared"] else 2


def run_live(reh: Path, live: Path, release: str) -> int:
    rt, lt = load(reh / "tickets.json"), load(live / "tickets-live.json")
    if rt is None or lt is None:
        print(f"NOT JUDGED - no tickets.json in {reh} or tickets-live.json in {live}")
        return 2
    out = live_compare(rt, read_log(reh / "direct"), reh / "direct", lt, read_log(live / "direct"),
                       live / "direct", release)
    lines = [f"# {release} live re-pull against the rehearsal", "",
             f"Compared {out['compared']} tickets by key (the tickets the release created by their real ids). "
             f"Release, links, dead links and what each ticket touches must match.", "",
             f"- Mismatches: {len(out['mismatch'])} -> {'PASS' if not out['mismatch'] else 'FAIL'}"]
    lines += [f"  - {m['key']}" + (f" #{m['id']}" if m.get("id") else "") + f": {m['why']}"
              for m in out["mismatch"][:200]]
    lines += ["", "Changed since the rehearsal (listed, not failed): "
              + ("; ".join(f"{k}: {n}" for k, n in out["info"].most_common()) or "nothing")]
    text = "\n".join(lines) + "\n"
    (live / "live-repull-summary.md").write_text(text, encoding="utf-8")
    (live / "live-repull-report.json").write_text(
        json.dumps({**out, "info": dict(out["info"])}, indent=1, ensure_ascii=False), encoding="utf-8")
    print("\n".join(lines[:12]))
    if not out["compared"]:
        print("NOT JUDGED - the live re-pull compared no tickets")
    return live_verdict(out)


def main(argv=None) -> int:
    utf8()
    ap = argparse.ArgumentParser(description="Judge a rehearsal pull or a live re-pull.")
    ap.add_argument("mode", nargs="?", choices=["rehearsal", "live"])
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--work")
    ap.add_argument("--release")
    ap.add_argument("--base")
    ap.add_argument("--rehearsal")
    ap.add_argument("--live")
    a = ap.parse_args(argv)
    fails = self_test()
    for f in fails:
        print(f"  SELF-TEST    {f}")
    if fails:
        print(f"FAIL {len(fails)} self-test(s)")
        return 1
    if a.self_test or not a.mode:
        print("PASS - judge.py self-tests")
        return 0
    if a.mode == "rehearsal":
        if not (a.work and a.release and a.base):
            ap.error("rehearsal needs --work, --release and --base")
        return run_rehearsal(Path(a.work), a.release, Path(a.base))
    if not (a.rehearsal and a.live and a.release):
        ap.error("live needs --rehearsal, --live and --release")
    return run_live(Path(a.rehearsal), Path(a.live), a.release)


# --------------------------------------------------------------------------------------------------- self-tests
def self_test() -> list:
    """Each rule against made-up pulls and states it must pass and fail. Returns the failures."""
    fails = []

    def wp(status, assignee=None, accountable=None):
        ln = {"status": {"title": status}}
        if assignee:
            ln["assignee"] = {"title": assignee}
        if accountable:
            ln["responsible"] = {"title": accountable}
        return {"_links": ln}

    def row(i, key, linked=3, nf=0, rel="r7", error=None):
        r = {"id": i, "key": key, "result": {"linked": linked, "notFound": nf, "release": {"current": rel}}}
        if error:
            r["error"] = error
        return r

    statuses = [{"name": "New", "isClosed": False}, {"name": "Ready for QA", "isClosed": False},
                {"name": "Rejected", "isClosed": True}]
    state = {"statuses": statuses, "leavers": ["Tanmay Dukhande"], "accountableFrom": "openproject",
             "key_of": {"1": "T-1", "2": "F-2"},
             "packages": {"1": wp("New", "Pranay Shinde", "Hrushikant Patkar"), "2": wp("New", "Pranay Shinde")}}
    tickets = [{"id": 1, "key": "T-1", "type": "Task", "set": "in-base"},
               {"id": 2, "key": "F-2", "type": "Feature", "set": "in-base"},
               {"id": 9, "key": "OLD-9", "type": "Task", "set": LEFT}]
    clean = {"1": row(1, "T-1"), "2": row(2, "F-2"), "9": row(9, "OLD-9", linked=0, rel="r6")}

    def judge(log, st=state, requests=12):
        c = criteria(tickets, log, "r7", st, requests)
        return c, verdict(c)[0]

    c, code = judge(clean)
    if code != 0:
        fails.append(f"a clean rehearsal did not pass (exit {code}): {verdict(c)[1]}")
    # 1. pull errors: an error row, and a ticket never pulled; a ticket that left the block is never judged
    c, code = judge({"1": row(1, "T-1", error="502 Bad Gateway")})
    if [e["key"] for e in c["errors"]] != ["T-1", "F-2"] or code != 1:
        fails.append(f"an error and a ticket never pulled gave {c['errors']} (exit {code})")
    with tempfile.TemporaryDirectory() as tmp:
        (Path(tmp) / "pull-log.jsonl").write_text(
            "".join(json.dumps(r) + "\n" for r in (row(1, "T-1", error="timeout"), row(1, "T-1"))), encoding="utf-8")
        if read_log(tmp)["1"].get("error"):
            fails.append("a re-run after an error did not replace the error row")
    # 2. a ticket still on the previous release
    c, code = judge({**clean, "1": row(1, "T-1", rel="r6")})
    if [r["key"] for r in c["release"]] != ["T-1"] or code != 1:
        fails.append(f"a ticket at r6 gave {c['release']} (exit {code})")
    # 3. nothing linked, a feature and a task alike
    c, code = judge({**clean, "1": row(1, "T-1", linked=0), "2": row(2, "F-2", linked=0)})
    if [r["key"] for r in c["empty"]] != ["T-1", "F-2"] or code != 1 or "1 features, 1 tasks" not in verdict(c)[1][2]:
        fails.append(f"nothing linked gave {c['empty']} / {verdict(c)[1][2]} (exit {code})")
    # 4. dead links
    c, code = judge({**clean, "2": row(2, "F-2", nf=2)})
    if c["dead"] != [{"id": 2, "key": "F-2", "notFound": 2}] or code != 1:
        fails.append(f"two dead links gave {c['dead']} (exit {code})")
    # 5. a leaver kept as Accountable on a started ticket (P-25) and as assignee on a New one; a closed one is no finding
    st5 = json.loads(json.dumps(state))
    st5["packages"]["3"] = wp("Ready for QA", "Narayan Gaonkar", "Tanmay Dukhande")
    st5["packages"]["4"] = wp("New", "Tanmay Dukhande", "Hrushikant Patkar")
    st5["packages"]["5"] = wp("Rejected", "Tanmay Dukhande", "Tanmay Dukhande")
    c, code = judge(clean, st5)
    got = sorted((r["id"], r["field"]) for r in c["leavers"])
    if got != [(3, "Accountable"), (4, "assignee")] or code != 1:
        fails.append(f"leavers gave {got} (exit {code}); want #3 Accountable and #4 assignee, never the rejected #5")
    # Accountable from the previous bundle, not OpenProject: not judged, so no pass
    c, code = judge(clean, {**state, "accountableFrom": "previous-bundle"})
    if code != 2 or "NOT JUDGED" not in verdict(c)[1][4]:
        fails.append(f"a state with no OpenProject snapshot was judged (exit {code})")
    # the stand-in answered nothing: ADAM read some other OpenProject
    c, code = judge(clean, requests=0)
    if code != 1:
        fails.append("a rehearsal whose stand-in answered nothing passed")
    # the impact list: the release line alone is no text change; an owner move is; a created ticket is new
    with tempfile.TemporaryDirectory() as tmp:
        base, now = Path(tmp) / "base", Path(tmp) / "now"

        def put(d, i, w, links=()):
            p = d / "workspace" / ".adam" / "work" / str(i)
            p.mkdir(parents=True)
            (p / "ticket.json").write_text(json.dumps(
                {"workPackage": w, "touches": [{"kind": k, "id": x} for k, x in links]}), encoding="utf-8")
        put(base, 1, {"description": "Build it.\n- Written at release `r6`", "assignee": "Tanmay Dukhande"},
            [("operation", "a#b")])
        put(now, 1, {"description": "Build it.\n- Written at release `r7`", "assignee": "Narayan Gaonkar"},
            [("operation", "a#b"), ("table", "x.y")])
        put(now, 7, {"description": "New.", "assignee": "Pranay Shinde"})
        two = [{"id": 1, "key": "T-1", "type": "Task", "set": "in-base"},
               {"id": 7, "key": "T-7", "type": "Task", "set": "created"}]
        rep = impact(two, {"1": row(1, "T-1")}, base, {"1": row(1, "T-1"), "7": row(7, "T-7")}, now)
        a, b = rep
        if (not a["releaseLineOnly"] or a["descriptionChanged"] or not a["ownerChanged"]
                or a["otherLinks"]["added"] != ["table x.y"]):
            fails.append(f"the impact row for a moved ticket was {a}")
        if b["changed"] != [NEW]:
            fails.append(f"a created ticket's impact row said {b['changed']}")
        c = criteria(two, {"1": row(1, "T-1"), "7": row(7, "T-7")}, "r7", state, 5)
        text = summary({"release": "r7", "previous": "r6", "candidate": "r7-rc", "commit": "abcdef1234", "block": "A"},
                       c, verdict(c)[1], rep)
        if "## Pass criteria" not in text or "| Narayan Gaonkar |" not in text or "Tanmay Dukhande -> Narayan" not in text:
            fails.append("the summary lost its criteria, its per-developer table or its owner changes")
    # the live re-pull: matched by key; a link count or a release that differs fails; an owner change is listed
    with tempfile.TemporaryDirectory() as tmp:
        reh, live = Path(tmp) / "reh", Path(tmp) / "live"
        for d, i, who in ((reh, 990001, "Pranay Shinde"), (live, 31000, "Sanket Keluskar")):
            p = d / "workspace" / ".adam" / "work" / str(i)
            p.mkdir(parents=True)
            (p / "ticket.json").write_text(json.dumps({"workPackage": {"assignee": who},
                                                       "touches": [{"kind": "operation", "id": "a#b"}]}),
                                           encoding="utf-8")
        rt = [{"id": 990001, "key": "T-NEW", "set": "created"}]
        lt = [{"id": 31000, "key": "T-NEW", "set": "created", "standIn": 990001}]
        rlog = {"990001": row(990001, "T-NEW")}
        same = live_compare(rt, rlog, reh, lt, {"31000": row(31000, "T-NEW")}, live, "r7")
        if same["mismatch"] or same["info"].get("assignee") != 1:
            fails.append(f"a matching live re-pull gave {same['mismatch']} / {dict(same['info'])}")
        off = live_compare(rt, rlog, reh, lt, {"31000": row(31000, "T-NEW", linked=0)}, live, "r7")
        if len(off["mismatch"]) != 1 or "linked" not in off["mismatch"][0]["why"]:
            fails.append(f"a live ticket with fewer links gave {off['mismatch']}")
        old = live_compare(rt, rlog, reh, lt, {"31000": row(31000, "T-NEW", rel="r6")}, live, "r7")
        if len(old["mismatch"]) != 1 or "release" not in old["mismatch"][0]["why"]:
            fails.append(f"a live ticket still on r6 gave {old['mismatch']}")
        gone = live_compare(rt, rlog, reh, [], {}, live, "r7")
        if len(gone["mismatch"]) != 1:
            fails.append("a ticket missing from the live list was not a mismatch")
    return fails


if __name__ == "__main__":
    sys.exit(main())
