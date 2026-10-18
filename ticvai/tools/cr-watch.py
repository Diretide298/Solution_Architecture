#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The CR watcher: new ADAM change requests sorted, drafted and put in front of the lead as one list.

**18 October 2026** (post-r6 plan, item 7, CHG-CRF-002; lead, 14 October: "Also faster way to respond to dev CRs";
council of 14 October). A request used to wait for the lead, then a manual audit, then an agent per request. This
gives it a first answer the same hour, on a schedule (every 30 minutes on the lead's machine):

  1. fetch   ADAM's change-request export (POST /api/auth/login, GET /api/export/changes, as ADAM_EMAIL and
             ADAM_PASSWORD), keeping the open requests of the project it has not seen yet (state.json: the highest
             export id seen).
  2. sort    with no AI: the known class (handoff/cr-classes.yaml: its artefacts, words and requests, and the checks
             whose baselined findings are its members), a duplicate (an open request on the same artefact), what blocks
             it (an open blocking request on its ticket, artefact or class, or one it names), the class's known members
             across the package (handoff/audit-baseline.json) and the tickets they touch (adam-links.json, the started
             ones named), and whether the class's fix branch exists.
  3. draft   one Claude Code turn per request (claude -p, read-only tools, in a worktree at the latest release tag):
             verdict, class, recommendation, the resolution the developer reads, who must decide.
  4. review  REVIEW.md: one block per request with a `decision:` line for the lead: approve, change or reject. The
             requests in a class with a written default ruling come first, under one line, "approve all default-ruled
             (n)", so the lead can clear them with one mark; each is still settled only by that mark.
  5. settle  only what the lead marked approve or change: a decisions file for viewer/api/settle_changes.py, dry run
             first, then --apply. A rejected draft is drafted again at the next run, with the lead's note.

  python3 tools/cr-watch.py run --seed                    # first time: start after every request ADAM has now
  python3 tools/cr-watch.py run [--no-draft] [--csv FILE] # 1-4: what the schedule runs
  python3 tools/cr-watch.py settle [--apply]              # 5: after the lead marks REVIEW.md
  python3 tools/cr-watch.py --self-test

`run` writes nothing to ADAM or OpenProject. Credentials come from the environment or --env-file and are never
printed. When ADAM cannot be read, REVIEW.md says so at the top and the run exits 2: a failed read is never reported
as "nothing new". Output goes to audit/ticvai/cr-watch/ (gitignored). The self-tests run first, every time.
"""
from __future__ import annotations

import argparse
import contextlib
import csv
import datetime
import http.cookiejar
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import audit_guard as g  # noqa: E402

ROOT = g.ROOT                                   # ticvai/
REPO = ROOT.parent                              # the ADAM repository
CLASSES = ROOT / "handoff" / "cr-classes.yaml"
OUT = REPO / "audit" / "ticvai" / "cr-watch"    # audit/ is gitignored: state, drafts, REVIEW.md stay on this machine
SETTLE = REPO / "viewer" / "api" / "settle_changes.py"
ADAM = os.environ.get("ADAM_API_URL", "https://adamapi.ainfinite.ai")   # adam.ainfinite.ai answers /api/export 404
RELEASE_DIR = os.environ.get("CR_WATCH_RELEASE_DIR", "D:/wt/cr-watch-release")
PROJECT = "ticvai"
UA = "curl/8.0"
# The export's columns the watcher reads (viewer/api/main.py _export_changes writes 27).
COLUMNS = ("id", "ref", "raised", "project", "status", "blocking", "kind", "artefact", "title", "raised by",
           "ticket", "problem", "evidence", "options", "recommendation")
OPEN = ("Open", "Accepted")          # not settled yet: what a duplicate or a blocker can be
VERDICTS = ("FIXED IN", "PARTLY FIXED", "NOT FIXED", "NOT A PROBLEM")
NEEDS = ("lead", "client", "none")
STATUSES = ("open", "accepted", "rejected", "done")   # settle_changes.py
LOCK_HOURS = 2
DRAFT_MINUTES = 15


def _now() -> str:
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


# ------------------------------------------------------------------------------------------------- 1. fetch
class AdamDown(RuntimeError):
    """ADAM could not be read. The message names the step and the HTTP status, never a credential."""


def fetch_export(base: str, email: str, password: str) -> str:
    """ADAM's change-request register as CSV text: log in, export, log out."""
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))

    def call(method, path, body=None):
        data = json.dumps(body).encode() if body is not None else None
        req = urllib.request.Request(base.rstrip("/") + path, data=data, method=method,
                                     headers={"content-type": "application/json", "user-agent": UA})
        try:
            with opener.open(req, timeout=120) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            raise AdamDown(f"{method} {path} answered HTTP {e.code}") from None
        except (urllib.error.URLError, OSError) as e:
            raise AdamDown(f"{method} {path} failed: {getattr(e, 'reason', e)}") from None

    call("POST", "/api/auth/login", {"email": email, "password": password})
    try:
        return call("GET", "/api/export/changes").decode("utf-8-sig")
    finally:
        with contextlib.suppress(AdamDown):
            call("POST", "/api/auth/logout", {})


def parse_export(text: str) -> list:
    """The export's rows as dicts with `id` an int. Refuses a file without the columns the watcher reads."""
    reader = csv.DictReader(io.StringIO(text.lstrip("﻿")))
    missing = [c for c in COLUMNS if c not in (reader.fieldnames or [])]
    if missing:
        raise ValueError(f"the export has no column {', '.join(missing)}")
    rows = []
    for r in reader:
        try:
            r["id"] = int(r["id"])
        except (TypeError, ValueError):
            raise ValueError(f"the export's row {r.get('ref') or '?'} has id {r.get('id')!r}, not a number") from None
        rows.append(r)
    return rows


def new_requests(rows: list, project: str, last_id: int) -> tuple:
    """(the open requests of `project` raised after `last_id`, the highest id of the project in the export)."""
    mine = [r for r in rows if r["project"] == project]
    top = max([last_id] + [r["id"] for r in mine])
    return [r for r in mine if r["id"] > last_id and r["status"] == "Open"], top


def read_env_file(path) -> dict:
    """KEY=VALUE lines; `export `, `set ` and `$env:` prefixes, quotes and # comments allowed. Never printed."""
    out = {}
    for line in Path(path).read_text(encoding="utf-8-sig").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        k = k.strip()
        for prefix in ("export ", "set ", "$env:"):
            if k.lower().startswith(prefix.lower()):
                k = k[len(prefix):].strip()
        v = v.strip()
        if len(v) >= 2 and v[0] == v[-1] and v[0] in "'\"":
            v = v[1:-1]
        out[k] = v
    return out


# ------------------------------------------------------------------------------------------------- 2. sort
def load_classes(path=None) -> list:
    raise NotImplementedError("Task 6")


def short_id(cr: dict) -> str:
    raise NotImplementedError("Task 6")


def key_tokens(key: str) -> set:
    raise NotImplementedError("Task 6")


def _members(baseline: dict, check: str, rule: str) -> list:
    raise NotImplementedError("Task 6")


def _has(text: str, word: str) -> bool:
    raise NotImplementedError("Task 6")


def classify(cr: dict, classes: list, baseline: dict) -> list:
    raise NotImplementedError("Task 6")


def _words(text: str) -> set:
    raise NotImplementedError("Task 6")


def related(cr: dict, rows: list, main) -> dict:
    raise NotImplementedError("Task 6")


def siblings(main, baseline: dict, idx: dict) -> dict:
    raise NotImplementedError("Task 6")


def sort_request(cr: dict, rows: list, classes: list, baseline: dict, idx: dict, branches: set) -> dict:
    raise NotImplementedError("Task 6")


def facts_lines(cr: dict, f: dict) -> list:
    raise NotImplementedError("Task 6")


# ------------------------------------------------------------------------------------------------- 3. draft
PROMPT = """You answer one change request a TICVAI developer raised in ADAM, against the package as released at
{release} (this folder: paths are relative to ticvai/ unless they start with viewer/). Read what you need. Change
nothing, run nothing.

The request
  {ref}, raised {raised} by {raised_by}, ticket #{ticket}, {kind} {artefact}{blocking}
  Title: {title}
  Problem: {problem}
  Evidence: {evidence}
  Options: {options}
  The developer recommends: {recommendation}

What the watcher found with no AI
{facts}
{note}
Do this
1. Check each point of the request against the package at {release}. Say which points it already has, which it does
   not, and which were misread; quote the file and the line.
2. Name the class: the known class above when it fits, else "new: <a name in plain words>". When the facts give no
   sibling count, search the package for the same pattern and say how many there are and where.
3. Verdict: FIXED IN {release}, PARTLY FIXED, NOT FIXED or NOT A PROBLEM.
4. Write the resolution the developer reads in ADAM, in plain words with no batch codes or acronyms as names of work:
   what was decided, what the next release ({next}) carries, and "Build now:" what they do today. Developers and
   agents are always on the latest release: never ask anyone to choose or pin a release. Client-approved screens never
   change visibly: fix the contract, binding or storage to fit the screen.
5. Who must decide: lead, client (a business rule, law or money question the package cannot settle), or none.

End with one JSON block and nothing after it:
```json
{{"verdict": "...", "class": "...", "recommendation": "...", "resolution": "...", "needs": "lead", "misread": "..."}}
```
"""


def draft_prompt(cr: dict, facts: list, release: str, nxt: str, note: str = "") -> str:
    raise NotImplementedError("Task 7")


def parse_draft(text: str, release: str) -> dict:
    raise NotImplementedError("Task 7")


def releases_from(tags) -> tuple:
    raise NotImplementedError("Task 7")


def settle_as(verdict: str, release: str, nxt: str) -> tuple:
    raise NotImplementedError("Task 7")


def run_claude(prompt: str, cwd: Path, claude: str, timeout: int = DRAFT_MINUTES * 60) -> str:
    raise NotImplementedError("Task 7")


# ------------------------------------------------------------------------------------------------- 4. review
BLOCK = re.compile(r"^## (CR-\d+)\b.*$", re.M)
# One line for the requests in a class with a written default ruling (controller ruling 4, 18 October): the lead
# writes `approve` after the colon and each of them that has no mark of its own is approved.
ALL_DEFAULT = re.compile(r"^approve all default-ruled \(\d+\):[ \t]*(.*)$", re.M)


def _item(r: dict) -> dict:
    raise NotImplementedError("Task 8")


def _default_ruled(p: dict) -> bool:
    raise NotImplementedError("Task 8")


def render_review(pending: dict, status_line: str) -> str:
    raise NotImplementedError("Task 8")


def parse_review(text: str) -> dict:
    raise NotImplementedError("Task 8")


def decisions_for(pending: dict, marks: dict, project: str, nxt: str) -> tuple:
    raise NotImplementedError("Task 8")


def settle_argv(decisions: Path, base: str, apply: bool) -> list:
    raise NotImplementedError("Task 8")


# ------------------------------------------------------------------------------------------------- state and git
def load_state(out: Path):
    raise NotImplementedError("Task 9")


def _write(path: Path, text: str):
    raise NotImplementedError("Task 9")


def save_state(out: Path, state: dict):
    raise NotImplementedError("Task 9")


def _log(out: Path, line: str):
    raise NotImplementedError("Task 9")


def _git(*args, cwd=REPO) -> str:
    raise NotImplementedError("Task 9")


def releases_live() -> tuple:
    raise NotImplementedError("Task 9")


def branches_live() -> set:
    raise NotImplementedError("Task 9")


def release_tree(path: Path, tag: str) -> Path:
    raise NotImplementedError("Task 9")


class Busy(RuntimeError):
    pass


@contextlib.contextmanager
def locked(out: Path):
    raise NotImplementedError("Task 9")


# ------------------------------------------------------------------------------------------------- run and settle
def _fetch_live(a) -> str:
    raise NotImplementedError("Task 9")


def _draft_file(out: Path, p: dict, text: str):
    raise NotImplementedError("Task 9")


def run(a, fetch=None, drafter=None, tree=None, rel=None, branches=None) -> int:
    raise NotImplementedError("Task 9")


def settle(a, runner=None, env=None, rel=None) -> int:
    raise NotImplementedError("Task 9")


# ------------------------------------------------------------------------------------------------- self-tests
HEADER = ["id", "ref", "raised", "date", "project", "status", "blocking", "side", "platform", "kind", "artefact",
          "title", "raised by", "email", "via", "ticket", "picked by", "picked on", "our decision", "because",
          "reference", "settled on", "settled by", "problem", "evidence", "options", "recommendation"]


def _row(i, **kw) -> dict:
    r = {h: "" for h in HEADER}
    r.update({"id": str(i), "ref": f"CR-{i:03d}", "raised": f"2026-10-18T0{i % 10}:00:00Z", "project": "ticvai",
              "status": "Open", "kind": "Operation", "artefact": f"orders#op{i}", "title": f"request {i}",
              "raised by": "Deep Khanvilkar", "ticket": str(27000 + i), "problem": "something"})
    r.update(kw)
    return r


def _csv(rows) -> str:
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=HEADER)
    w.writeheader()
    for r in rows:
        w.writerow(r)
    return "﻿" + buf.getvalue()


def _links_file(folder: Path, rows) -> Path:
    path = folder / "adam-links.json"
    path.write_text(json.dumps({"project": "ticvai", "cached": True, "statusReadAt": "2026-10-18T09:00:00Z",
                                "links": [{"key": str(wp), "kind": k, "id": i, "status": s, "type": "Task",
                                           "assignee": "Deep Khanvilkar", "subject": "x"}
                                          for wp, k, i, s in rows]}), encoding="utf-8")
    return path


TEST_CLASSES = """classes:
- id: read-routes
  name: Read routes between modules
  artefacts: [ADR-0055]
  words: [x-ticvai-read-via, another module's]
  crs: [CR-096]
- id: row-security
  name: Row security fits its callers
  words: [row security, scope_path]
  crs: [CR-108]
  checks: {check-rls-scope-fit: [RF-TENANT-ROOT]}
- id: contract-storage
  name: Contract against storage
  words: [no column]
  checks: {check-stored-request-fields: [SR-STORED-NO-COLUMN]}
"""
TEST_BASELINE = {"check-rls-scope-fit": {"rules": {"RF-TENANT-ROOT": ["opA:sch.tab:write", "opB:sch.other:read"]}},
                 "check-stored-request-fields": {"rules": {"SR-STORED-NO-COLUMN": ["payByLink.linkToken"]}}}


def _expect(fails, name, got, want):
    if got != want:
        fails.append(f"{name}: got {got!r}, expected {want!r}")


def _t_export(fails):
    rows = parse_export(_csv([_row(4), _row(5), _row(6, problem="two\nlines"), _row(7, status="Done"),
                              _row(8, project="other")]))
    _expect(fails, "parse: ids are numbers", [r["id"] for r in rows], [4, 5, 6, 7, 8])
    _expect(fails, "parse: a cell keeps its new lines", rows[2]["problem"], "two\nlines")
    new, top = new_requests(rows, "ticvai", 5)
    _expect(fails, "new: open, after the last seen, this project", [r["ref"] for r in new], ["CR-006"])
    _expect(fails, "new: the highest id of the project", top, 7)
    try:
        parse_export("id,ref\n1,CR-001\n")
        fails.append("parse: an export without the columns was accepted")
    except ValueError as e:
        if "artefact" not in str(e):
            fails.append(f"parse: the refusal does not name the missing columns ({e})")
    with tempfile.TemporaryDirectory() as d:
        f = Path(d) / "a.env"
        f.write_text("# login\nADAM_EMAIL=a@b.c\nexport ADAM_PASSWORD=\"p w\"\n$env:TICVAI_OP_TOKEN='t'\nset X=1\n",
                     encoding="utf-8")
        _expect(fails, "env file", read_env_file(f),
                {"ADAM_EMAIL": "a@b.c", "ADAM_PASSWORD": "p w", "TICVAI_OP_TOKEN": "t", "X": "1"})


def _t_sort(fails):
    with tempfile.TemporaryDirectory() as d:
        (Path(d) / "c.yaml").write_text(TEST_CLASSES, encoding="utf-8")
        classes = load_classes(Path(d) / "c.yaml")
        idx = g.link_index(_links_file(Path(d), [(10, "table", "sch.tab", "Ready for QA"),
                                                 (11, "operation", "svc#opB", "New"),
                                                 (27941, "operation", "orders#op1", "In progress")]))
        rows = parse_export(_csv([
            _row(1, kind="Decision", artefact="ADR-0055", title="reads another module's data with no x-ticvai-read-via",
                 ticket="27941"),
            _row(2, artefact="orders#payByLink", title="payByLink has no column for its token"),
            _row(3, kind="Table", artefact="sch.tab", title="scope_path is wrong, row security shuts callers out",
                 blocking="yes", ticket="27941"),
            _row(4, kind="Table", artefact="sch.tab", title="scope_path is wrong, row security shuts callers out too"),
            _row(5, title="follows CR-003 on the same rows", problem="see CR-003"),
            _row(6, title="nothing anyone has seen before", artefact="orders#zz"),
            _row(7, kind="Table", artefact="sch.tab", title="settled already", status="Done", blocking="yes")]))
        by = {r["ref"]: r for r in rows}
        f1 = sort_request(by["CR-001"], rows, classes, TEST_BASELINE, idx, {"fix/read-routes"})
        _expect(fails, "class by artefact and words", f1["class"], "read-routes")
        _expect(fails, "reason names the artefact", f1["class_why"][0], "artefact ADR-0055")
        _expect(fails, "fix branch found", (f1["branch"], f1["branch_exists"]), ("fix/read-routes", True))
        _expect(fails, "ticket status from the cached links", f1["ticket_status"], "In progress, Deep Khanvilkar")
        _expect(fails, "blocked by the open blocking request on its ticket",
                [(b["ref"], b["why"]) for b in f1["blocked_by"]], [("CR-003", "the same ticket")])
        f2 = sort_request(by["CR-002"], rows, classes, TEST_BASELINE, idx, set())
        _expect(fails, "class by baselined membership", f2["class"], "contract-storage")
        if not any("payByLink is a known member of SR-STORED-NO-COLUMN" in w for w in f2["class_why"]):
            fails.append(f"membership reason missing: {f2['class_why']}")
        f4 = sort_request(by["CR-004"], rows, classes, TEST_BASELINE, idx, set())
        _expect(fails, "duplicate on the same artefact", [(x["ref"], x["likely"]) for x in f4["duplicates"]],
                [("CR-003", True)])
        _expect(fails, "blocked by the same artefact", [b["why"] for b in f4["blocked_by"]], ["the same artefact"])
        _expect(fails, "siblings of the class", (f4["siblings"]["members"], f4["siblings"]["tickets"],
                                                 [t["wp"] for t in f4["siblings"]["started"]]), (2, 2, [10]))
        f5 = sort_request(by["CR-005"], rows, classes, TEST_BASELINE, idx, set())
        _expect(fails, "names an open request", f5["follows"], ["CR-003"])
        _expect(fails, "blocked by the request it names", [b["why"] for b in f5["blocked_by"]], ["it names it"])
        f6 = sort_request(by["CR-006"], rows, classes, TEST_BASELINE, idx, set())
        _expect(fails, "no class", f6["class"], "")
        if "none matched" not in " ".join(facts_lines(by["CR-006"], f6)):
            fails.append("facts of an unclassed request do not say no class matched")
        if any("CR-007" in str(v) for v in f4.values()):
            fails.append("a settled request was counted as a duplicate or a blocker")


ANSWER = ("The points check out.\n```json\n{\"verdict\": \"not fixed\", \"class\": \"Read routes between modules\", "
          "\"recommendation\": \"Option A\", \"resolution\": \"Accepted.\\n  Build now: read through the query.\", "
          "\"needs\": \"lead\", \"misread\": \"\"}\n```\n")


def _t_draft(fails):
    d = parse_draft(ANSWER, "r6")
    _expect(fails, "draft verdict", d["verdict"], "NOT FIXED")
    _expect(fails, "draft resolution on one line", d["resolution"], "Accepted. Build now: read through the query.")
    for bad, why in (("no json here", "does not end with a JSON block"),
                     ("```json\n{\"verdict\": \"maybe\", \"resolution\": \"x\"}\n```", "is not FIXED IN r6"),
                     ("```json\n{\"verdict\": \"NOT FIXED\"}\n```", "no resolution"),
                     ("```json\n{\"verdict\": \"NOT FIXED\", \"resolution\": \"x\", \"needs\": \"boss\"}\n```",
                      "not lead, client or none")):
        try:
            parse_draft(bad, "r6")
            fails.append(f"a bad draft was accepted: {bad[:40]!r}")
        except ValueError as e:
            if why not in str(e):
                fails.append(f"bad draft refused for the wrong reason: {e}")
    _expect(fails, "settle as: fixed", settle_as("FIXED IN R6", "r6", "r7"), ("done", "r6"))
    _expect(fails, "settle as: not a problem", settle_as("NOT A PROBLEM", "r6", "r7"), ("rejected", "r6"))
    _expect(fails, "settle as: partly", settle_as("PARTLY FIXED", "r6", "r7"), ("accepted", "r7"))
    _expect(fails, "releases", releases_from(["r1", "r6", "r6-rc", "r10x", "r5"]), ("r6", "r7"))
    p = draft_prompt(_row(9, blocking="yes", **{"raised by": "Pranay Shinde"}), ["Known class: X"], "r6", "r7",
                     "wrong class")
    for want in ("CR-009", "at\nr6", "Pranay Shinde", ", blocking", "  - Known class: X", "rejected the last draft: "
                 "wrong class", "(r7)", "Build now:", "never ask anyone to choose or pin"):
        if want not in p:
            fails.append(f"the prompt lacks {want!r}")


def _t_review(fails):
    pend = {}
    for i in (1, 2, 3):
        p = _item(dict(_row(i), id=i))
        p.update(facts={"class_name": "Row security fits its callers"}, facts_lines=["Ticket #27001"],
                 draft={"verdict": "NOT FIXED", "needs": "lead"}, status="accepted", ref_to="r7",
                 resolution=f"Accepted {i}. Build now: x.")
        pend[p["ref"]] = p
    text = render_review(pend, "status")
    blocks = text.split("\n## ")
    edited = []
    for b in blocks:
        if b.startswith("CR-001"):
            b = b.replace("decision: \n", "decision: approve\n")
        elif b.startswith("CR-002"):
            b = b.replace("decision: \n", "decision: change\n").replace("status: accepted", "status: rejected") \
                 .replace("resolution: Accepted 2. Build now: x.", "resolution: Not in the package.")
        elif b.startswith("CR-003"):
            b = b.replace("decision: \n", "decision: reject: wrong class\n")
        edited.append(b)
    marks = parse_review("\n## ".join(edited))
    _expect(fails, "review marks", {k: (v["decision"], v["note"]) for k, v in marks.items()},
            {"CR-001": ("approve", ""), "CR-002": ("change", ""), "CR-003": ("reject", "wrong class")})
    spec, problems = decisions_for(pend, marks, "ticvai", "r7")
    _expect(fails, "decisions", spec["items"],
            [{"cr": "CR-001", "status": "accepted", "resolution": "Accepted 1. Build now: x.", "ref": "r7"},
             {"cr": "CR-002", "status": "rejected", "resolution": "Not in the package.", "ref": "r7"}])
    _expect(fails, "no problems", problems, [])
    marks["CR-001"]["status"] = "maybe"
    _expect(fails, "a bad status is refused", decisions_for(pend, marks, "ticvai", "r7")[1],
            ["CR-001: status 'maybe' is not one of open, accepted, rejected, done"])
    argv = settle_argv(Path("d.json"), "https://adam.example", False)
    _expect(fails, "settle dry run argv", argv[1:], [str(SETTLE), "d.json", "--adam", "https://adam.example"])
    _expect(fails, "settle apply argv", settle_argv(Path("d.json"), "https://adam.example", True)[-1], "--apply")


def _t_default(fails):
    """Requests in a class with a written default ruling come first under one line the lead marks once (ruling 4)."""
    pend = {}
    for i, ruled in ((1, False), (2, True), (3, True), (4, True)):
        p = _item(dict(_row(i), id=i, blocking="yes" if i == 1 else ""))
        p.update(facts={"class_name": "Money currency", "default_ruling": "Rule X" if ruled else ""},
                 facts_lines=["Ticket #1"], draft={"verdict": "NOT FIXED", "needs": "client"}, status="accepted",
                 ref_to="r7", resolution=f"Accepted {i}. Build now: x.")
        pend[p["ref"]] = p
    text = render_review(pend, "status")
    heads = re.findall(r"^## (CR-\d+)", text, re.M)
    _expect(fails, "default-ruled requests come first, blocking next", heads, ["CR-002", "CR-003", "CR-004", "CR-001"])
    _expect(fails, "one line to approve them all", re.findall(r"^approve all default-ruled \((\d+)\):", text, re.M),
            ["3"])
    if text.index("approve all default-ruled") > text.index("| Request |"):
        fails.append("the approve-all line is not above the list")
    _expect(fails, "nothing marked, nothing approved",
            [m["decision"] for m in parse_review(text).values()], ["", "", "", ""])
    # the lead marks the one line, and gives CR-003 a mark of its own
    marked = text.replace("approve all default-ruled (3): ", "approve all default-ruled (3): approve", 1)
    marked = re.sub(r"(## CR-003[^\n]*\n[^\n]*\n)decision: \n", r"\1decision: reject: not this one\n", marked)
    marks = parse_review(marked)
    _expect(fails, "approve-all reaches the default-ruled only",
            {k: v["decision"] for k, v in marks.items()},
            {"CR-001": "", "CR-002": "approve", "CR-003": "reject", "CR-004": "approve"})
    spec, problems = decisions_for(pend, marks, "ticvai", "r7")
    _expect(fails, "settled: CR-002 and CR-004 only", [i["cr"] for i in spec["items"]], ["CR-002", "CR-004"])
    _expect(fails, "no problems with the approve-all", problems, [])
    # a default-ruled request with no draft is a problem, never settled by the one mark
    pend["CR-004"].update(status="", resolution="", draft=None)
    marks = parse_review(marked.replace("resolution: Accepted 4. Build now: x.", "resolution: "))
    _expect(fails, "no draft, no settle", decisions_for(pend, marks, "ticvai", "r7")[1],
            ["CR-004: no resolution to settle with"])


def _t_pipeline(fails):
    with tempfile.TemporaryDirectory() as d:
        d = Path(d)
        (d / "c.yaml").write_text(TEST_CLASSES, encoding="utf-8")
        (d / "b.json").write_text(json.dumps(TEST_BASELINE), encoding="utf-8")
        links = _links_file(d, [(10, "table", "sch.tab", "Ready for QA")])
        csv_text = _csv([_row(1, kind="Table", artefact="sch.tab", title="row security shuts callers out",
                              blocking="yes"), _row(2), _row(3)])
        a = argparse.Namespace(out=str(d / "out"), csv=None, project="ticvai", seed=False, start_id=None,
                               no_draft=False, classes=d / "c.yaml", baseline=d / "b.json", links=links, claude="",
                               release_dir="", adam="https://adam.example", apply=False)
        calls = []

        def drafter(prompt, cwd):
            calls.append(prompt)
            return ANSWER

        kw = dict(fetch=lambda _a: csv_text, drafter=drafter, tree=d, rel=("r6", "r7"), branches=set())
        quiet = io.StringIO()
        with contextlib.redirect_stdout(quiet):
            _expect(fails, "first run without state refuses", run(a, **kw), 2)
            a.start_id = 0
            _expect(fails, "run", run(a, **kw), 0)
        review = (d / "out" / "REVIEW.md").read_text(encoding="utf-8")
        _expect(fails, "three blocks", len(BLOCK.findall(review)), 3)
        _expect(fails, "blocking first", re.findall(r"^## .*$", review, re.M)[0],
            "## CR-001 · NOT FIXED · Row security fits its callers · blocking")
        _expect(fails, "three drafts", (len(calls), sorted(p.name for p in (d / "out" / "drafts").iterdir())),
                (3, ["CR-001.md", "CR-002.md", "CR-003.md"]))
        with contextlib.redirect_stdout(quiet):
            run(a, **kw)
        _expect(fails, "a second run drafts nothing again", len(calls), 3)
        marked = review.replace("decision: \nstatus: accepted\nref: r7\nresolution: Accepted. Build now: read through "
                                "the query.\nfacts: Ticket #27001", "decision: approve\nstatus: accepted\nref: r7\n"
                                "resolution: Accepted. Build now: read through the query.\nfacts: Ticket #27001", 1)
        marked = re.sub(r"(## CR-002[^\n]*\n[^\n]*\n)decision: \n", r"\1decision: reject: wrong class\n", marked)
        (d / "out" / "REVIEW.md").write_text(marked, encoding="utf-8")
        with contextlib.redirect_stdout(quiet):
            run(a, **kw)
        _expect(fails, "a rejected draft is drafted again with the note", (len(calls), "wrong class" in calls[-1]),
                (4, True))
        marks = parse_review((d / "out" / "REVIEW.md").read_text(encoding="utf-8"))
        _expect(fails, "the lead's approve survives a run", marks["CR-001"]["decision"], "approve")
        _expect(fails, "the redraft is waiting again", marks["CR-002"]["decision"], "")

        def down(_a):
            raise AdamDown("GET /api/export/changes answered HTTP 502")

        with contextlib.redirect_stdout(quiet):
            _expect(fails, "ADAM down exits 2", run(a, **dict(kw, fetch=down)), 2)
        top = (d / "out" / "REVIEW.md").read_text(encoding="utf-8")
        if "could not be read (GET /api/export/changes answered HTTP 502)" not in top:
            fails.append("REVIEW.md does not say ADAM could not be read")
        _expect(fails, "nothing lost when ADAM is down", len(BLOCK.findall(top)), 3)
        secrets = {"ADAM_EMAIL": "lead@x", "ADAM_PASSWORD": "s3cret-pw", "TICVAI_OP_TOKEN": "tok-123"}
        ran = []
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            _expect(fails, "settle dry run", settle(a, runner=lambda argv, e: ran.append(argv) or 0, env=secrets,
                                                    rel=("r6", "r7")), 0)
            a.apply = True
            _expect(fails, "settle apply", settle(a, runner=lambda argv, e: ran.append(argv) or 0, env=secrets,
                                                  rel=("r6", "r7")), 0)
        _expect(fails, "settle runs settle_changes twice, --apply last", [x[-1] == "--apply" for x in ran],
                [False, True])
        spec = json.loads(Path(ran[-1][2]).read_text(encoding="utf-8"))
        _expect(fails, "decisions file", [(i["cr"], i["status"], i["ref"]) for i in spec["items"]],
                [("CR-001", "accepted", "r7")])
        state = load_state(d / "out")
        _expect(fails, "settled request leaves the list", sorted(state["pending"]), ["CR-002", "CR-003"])
        _expect(fails, "measure written", len((d / "out" / "settled.jsonl").read_text(encoding="utf-8").splitlines()),
                1)
        if any(v in out.getvalue() + quiet.getvalue() for v in secrets.values()):
            fails.append("a credential was printed")
        a.apply = False
        with contextlib.redirect_stdout(io.StringIO()):
            _expect(fails, "settle without credentials", settle(a, runner=lambda argv, e: 0, env={},
                                                                rel=("r6", "r7")), 0)
        a.seed, a.start_id = True, None
        (d / "out" / "state.json").unlink()
        with contextlib.redirect_stdout(io.StringIO()):
            _expect(fails, "seed", run(a, **kw), 0)
        _expect(fails, "seed starts after the last id", (load_state(d / "out")["last_id"],
                                                         load_state(d / "out")["pending"]), (3, {}))


TESTS = [_t_export, _t_sort, _t_draft, _t_review, _t_default, _t_pipeline]


def self_test() -> list:
    fails = []
    for t in TESTS:
        try:
            t(fails)
        except Exception as e:  # a test that crashes is a failing test, never a pass
            fails.append(f"{t.__name__}: raised {e.__class__.__name__}: {e}")
    return fails


def main(argv=None) -> int:
    g.force_utf8()
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("command", nargs="?", choices=("run", "settle"))
    ap.add_argument("--self-test", action="store_true", help="run the self-tests only")
    ap.add_argument("--csv", help="read a saved export instead of ADAM's")
    ap.add_argument("--env-file", help="KEY=VALUE file with ADAM_EMAIL, ADAM_PASSWORD, TICVAI_OP_TOKEN")
    ap.add_argument("--out", default=str(OUT))
    ap.add_argument("--adam", default=ADAM)
    ap.add_argument("--project", default=PROJECT)
    ap.add_argument("--classes", default=str(CLASSES))
    ap.add_argument("--baseline", default=str(g.BASELINE))
    ap.add_argument("--links", default=str(g.LINKS))
    ap.add_argument("--no-draft", action="store_true", help="sort and list only; no Claude Code turn")
    ap.add_argument("--seed", action="store_true", help="first run: treat every request ADAM has now as seen")
    ap.add_argument("--start-id", type=int, help="first run: draft every open request after this export id")
    ap.add_argument("--claude", default="", help="path of the claude command (default: found on PATH)")
    ap.add_argument("--release-dir", default=RELEASE_DIR, help="the watcher's worktree at the latest release")
    ap.add_argument("--apply", action="store_true", help="settle: really settle (default: dry run)")
    a = ap.parse_args(argv)
    fails = self_test()
    for f in fails:
        print(f"  SELF-TEST    {f}")
    if fails:
        print(f"FAIL {len(fails)} self-test(s)")
        return 1
    if a.self_test or not a.command:
        print(f"PASS - {len(TESTS)} self-test groups")
        return 0
    if a.env_file:
        os.environ.update(read_env_file(a.env_file))
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    try:
        with locked(out):
            return run(a) if a.command == "run" else settle(a)
    except Busy as e:
        print(f"cr-watch: {e}; not run")
        return 0


if __name__ == "__main__":
    sys.exit(main())
