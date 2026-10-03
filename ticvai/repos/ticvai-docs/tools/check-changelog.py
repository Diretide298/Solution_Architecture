#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Every change is logged with its decision and why, and an entry closes only on a prevention that exists.

**Council of 2 October 2026** (`docs/active/council/council-report-2026-10-02-opus.html`): *"a change closes only when it ships a
check, a generator rule or a schema field. A prose 'lesson' doesn't close anything."* And Chinmay, the
same night: *"all the changes and fixes: log them, also the decision and why."* The log is
`changes/entries/*.yaml`, one file per change; the rules are `changes/schema.yaml`; the README explains
them with an example. This enforces them, so nobody has to remember to read them.

**Every run** validates every entry file:

  - the file name is `<id>-<slug>.yaml`; the id matches `^CHG-[A-Z][A-Z0-9]{1,5}-\\d{3}$`; ids are unique, and
    numbered 001, 002, ... with no gap inside a batch (one batch per branch, so branches never collide);
  - every required field is there, every enum holds, dates are dates; `decision` says what, by whom and
    when; `why` cites a source a reader can open (a MoM, a DI, an R-root, an ADR, the council, a finding,
    a commit, a CR ...);
  - a minutes-sourced entry carries `client_signoff` (who and when, or `pending`); from 5 October every
    entry names its ADAM CR and its triage (`blocker`, `fix-forward`, `defer`);
  - **the closing rule:** a `closed` entry names the commit that closed it (known to git), and its
    prevention exists: a `check` is `tools/<name>.py`, present and run by `run-checks.py`; a
    `generator-rule` or `template-field` is `<path>[::<symbol>]`, present (and naming the symbol); a
    `none` carries the reason and the lead's approval.

**With `--since [REF]`** (default: the latest `r*` tag) it also applies **the commit rule**: every non-merge
commit in REF..HEAD that touches an authored package input (`changes/schema.yaml` `authored_roots` and
`authored_files`, less anything `tools/refresh-manifest.py` classifies as derived) names an existing entry
id in its message. Commits dated before `commit_rule_from` (5 October) are grandfathered; a release refresh
commit may carry `CHG-exempt: <reason>`, and every exemption is printed. Without `--since` (the normal
`run-checks.py` run, where no range is given) only the files are validated.

Self-tests run every time: entries and commits built in memory that must pass, and ones that must fail.

    python3 tools/check-changelog.py                 # validate changes/entries/
    python3 tools/check-changelog.py --since         # ... and the commit rule since the latest r* tag
    python3 tools/check-changelog.py --since r2      # ... since r2
"""
from __future__ import annotations

import argparse
import datetime
import importlib.util
import json
import pathlib
import re
import subprocess
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
CHANGES = ROOT / "changes"
ENTRIES = CHANGES / "entries"
SCHEMA = CHANGES / "schema.yaml"
INDEX = CHANGES / "CHANGELOG.md"
MANIFEST = ROOT / "handoff" / "refresh-manifest.json"
ID_IN_TEXT = re.compile(r"\bCHG-[A-Z][A-Z0-9]{1,5}-\d{3}\b")
EXEMPT = re.compile(r"(?mi)^CHG-exempt:\s*\S")
SHA = re.compile(r"^[0-9a-f]{7,40}$")


def _utf8():
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass


def _load(path: pathlib.Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _date(x):
    if isinstance(x, datetime.date):
        return x
    try:
        return datetime.date.fromisoformat(str(x))
    except Exception:
        return None


def _when(x):
    """A date or a date and time -> datetime (a bare date is its midnight)."""
    if isinstance(x, datetime.datetime):
        return x.replace(tzinfo=None)
    if isinstance(x, datetime.date):
        return datetime.datetime(x.year, x.month, x.day)
    try:
        return datetime.datetime.fromisoformat(str(x)).replace(tzinfo=None)
    except Exception:
        return None


def _git(*args) -> tuple[int, str]:
    try:
        p = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, encoding="utf-8",
                           errors="replace")
        return p.returncode, p.stdout
    except Exception:
        return 127, ""


def registered_checks() -> tuple[set, set]:
    """(CHECKS, REPORT_ONLY) from tools/run-checks.py."""
    try:
        spec = importlib.util.spec_from_file_location("run_checks", ROOT / "tools" / "run-checks.py")
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return set(mod.CHECKS), set(mod.REPORT_ONLY)
    except Exception:
        return set(), set()


class Context:
    """What validation asks of the world: files, registered checks, commits. Replaced in the self-tests."""

    def __init__(self):
        self.checks, self.report_only = registered_checks()
        self._git = _git("rev-parse", "--git-dir")[0] == 0

    def exists(self, rel: str) -> pathlib.Path | None:
        for base in (ROOT, ROOT.parent):
            p = base / rel
            if p.exists():
                return p
        return None

    def has_symbol(self, rel: str, symbol: str) -> bool:
        p = self.exists(rel)
        if not p or p.is_dir():
            return False
        try:
            return symbol in p.read_text(encoding="utf-8", errors="replace")
        except Exception:
            return False

    def commit_known(self, sha: str) -> bool | None:
        if not self._git:
            return None
        return _git("cat-file", "-e", f"{sha}^{{commit}}")[0] == 0


# ------------------------------------------------------------------------------------------ entries
def validate(entries: list[tuple[str, dict]], schema: dict, ctx) -> tuple[list[str], list[str]]:
    """entries: [(file name, entry)] -> (errors, warnings)."""
    errs, warns = [], []
    id_re = re.compile(schema["id_pattern"])
    slug_re = re.compile(schema["slug_pattern"])
    enums = schema["enums"]
    cites = [re.compile(c, re.I) for c in schema["why_cites"]]
    cr_from = _date(schema.get("adam_cr_required_from"))
    seen: dict = {}
    batches: dict = {}
    for fname, e in entries:
        where = fname
        if not isinstance(e, dict):
            errs.append(f"{where}: not a mapping")
            continue
        eid = str(e.get("id") or "")
        if not id_re.match(eid):
            errs.append(f"{where}: id {eid!r} does not match {schema['id_pattern']}")
        else:
            stem = fname[:-5] if fname.endswith(".yaml") else fname
            if not stem.startswith(eid + "-") or not slug_re.match(stem[len(eid) + 1:]):
                errs.append(f"{where}: the file name must be {eid}-<slug>.yaml (lowercase slug)")
            if eid in seen:
                errs.append(f"{where}: id {eid} is also {seen[eid]}")
            seen[eid] = fname
            b, n = eid.rsplit("-", 1)
            batches.setdefault(b, []).append(int(n))
        where = f"{eid or fname}"
        for f in schema["required"]:
            if e.get(f) in (None, "", [], {}) and f not in ("keys_touched", "tickets"):
                errs.append(f"{where}: missing {f}")
        for f, enum in (("source", "source"), ("kind", "kind"), ("status", "status")):
            if e.get(f) is not None and e.get(f) not in enums[enum]:
                errs.append(f"{where}: {f} {e.get(f)!r} is not one of {', '.join(enums[enum])}")
        d = _date(e.get("date"))
        if e.get("date") is not None and not d:
            errs.append(f"{where}: date {e.get('date')!r} is not YYYY-MM-DD")
        dec = e.get("decision")
        if dec is not None:
            if not isinstance(dec, dict) or not all(dec.get(k) for k in ("what", "by", "date")):
                errs.append(f"{where}: decision needs what, by and date")
            elif not _when(dec.get("date")):
                errs.append(f"{where}: decision date {dec.get('date')!r} is not YYYY-MM-DD[THH:MM]")
        why = str(e.get("why") or "")
        if why and not any(c.search(why) for c in cites):
            errs.append(f"{where}: why cites no source (a MoM, DI-, R-root, ADR-, council, finding, commit, CR ...)")
        kt = e.get("keys_touched")
        if not isinstance(kt, dict):
            errs.append(f"{where}: keys_touched must be a mapping of lists ({', '.join(schema['keys_touched_lists'])})")
        else:
            bad = [k for k in kt if k not in schema["keys_touched_lists"]]
            if bad:
                errs.append(f"{where}: keys_touched has unknown list(s) {', '.join(bad)}")
            if any(v is not None and not isinstance(v, list) for v in kt.values()):
                errs.append(f"{where}: every keys_touched value is a list")
            if e.get("kind") not in ("process", "plan") and not any(kt.values()):
                errs.append(f"{where}: keys_touched is empty for a {e.get('kind')} change")
        tk = e.get("tickets")
        if not isinstance(tk, dict) or not isinstance(tk.get("started", []), list) \
                or not isinstance(tk.get("unstarted", []), list) or set(tk) - {"started", "unstarted"}:
            errs.append(f"{where}: tickets must be {{started: [...], unstarted: [...]}}")
        rt = str(e.get("release_tag") or "")
        if rt and not re.match(r"^(r\d+|pending)$", rt):
            errs.append(f"{where}: release_tag {rt!r} is not r<N> or pending")
        if e.get("source") in schema.get("signoff_required_for", []):
            so = e.get("client_signoff")
            if not (so == "pending" or (isinstance(so, dict) and so.get("by") and _date(so.get("date")))):
                errs.append(f"{where}: a minutes-sourced change needs client_signoff {{by, date}} or 'pending'")
        if cr_from and d and d >= cr_from:
            if not e.get("adam_cr"):
                errs.append(f"{where}: from {cr_from} every change names its ADAM CR (adam_cr)")
            if e.get("triage") not in enums["triage"]:
                errs.append(f"{where}: from {cr_from} triage is one of {', '.join(enums['triage'])}")
        elif e.get("triage") is not None and e.get("triage") not in enums["triage"]:
            errs.append(f"{where}: triage {e.get('triage')!r} is not one of {', '.join(enums['triage'])}")
        pv = e.get("prevention")
        if pv is not None:
            if not isinstance(pv, dict) or pv.get("type") not in enums["prevention_type"]:
                errs.append(f"{where}: prevention.type is one of {', '.join(enums['prevention_type'])}")
                pv = None
            elif pv["type"] == "none":
                if not pv.get("reason"):
                    errs.append(f"{where}: prevention none needs a reason")
                elif e.get("status") == "closed" and not pv.get("approved_by"):
                    errs.append(f"{where}: closed on prevention none, which needs approved_by (the lead)")
            elif not pv.get("ref"):
                errs.append(f"{where}: prevention {pv['type']} needs a ref")
        if e.get("status") == "closed":
            sha = str(e.get("closed_by_commit") or "")
            if not SHA.match(sha):
                errs.append(f"{where}: closed, but closed_by_commit {sha!r} is not a commit id")
            elif ctx.commit_known(sha) is False:
                errs.append(f"{where}: closed_by_commit {sha} is not a commit git knows")
            if pv and pv.get("type") != "none" and pv.get("ref"):
                ref = str(pv["ref"])
                path, _, sym = ref.partition("::")
                if pv["type"] == "check":
                    name = pathlib.PurePosixPath(path).stem
                    if not ctx.exists(path if path.endswith(".py") else f"tools/{name}.py"):
                        errs.append(f"{where}: closed on check {ref}, which does not exist")
                    elif name not in ctx.checks:
                        errs.append(f"{where}: closed on check {name}, which run-checks.py does not run")
                    elif name in ctx.report_only:
                        warns.append(f"{where}: its prevention {name} is report-only for now")
                else:
                    if not ctx.exists(path):
                        errs.append(f"{where}: closed on {pv['type']} {ref}, and {path} does not exist")
                    elif sym and not ctx.has_symbol(path, sym):
                        errs.append(f"{where}: closed on {pv['type']} {ref}, and {path} does not name {sym}")
        elif e.get("status") == "open" and e.get("closed_by_commit"):
            warns.append(f"{where}: open, but names closed_by_commit")
    # **The plan-change rule** (council of 2 October: five reversals in one day happened because nothing stopped
    # them). From commit_rule_from, a plan change records when it was proposed and is decided at least 24 hours
    # later; one that reverses an earlier change says which, and that one was decided at least 48 hours before;
    # a closed plan change names the release that carried it.
    start = _date(schema.get("commit_rule_from"))
    by_id = {e.get("id"): e for _f, e in entries if isinstance(e, dict)}
    for _f, e in entries:
        if not isinstance(e, dict) or e.get("kind") != "plan":
            continue
        d = _date(e.get("date"))
        if not (start and d and d >= start):
            continue
        where = e.get("id")
        dec = _when((e.get("decision") or {}).get("date"))
        prop = _when(e.get("proposed"))
        if not prop:
            errs.append(f"{where}: a plan change records when it was proposed (proposed: YYYY-MM-DD[THH:MM])")
        elif dec and (dec - prop).total_seconds() < 24 * 3600:
            errs.append(f"{where}: decided {dec:%Y-%m-%d %H:%M}, less than 24 hours after it was proposed "
                        f"({prop:%Y-%m-%d %H:%M}): plan changes cool off for a day")
        rev = e.get("reverses")
        if rev:
            old = by_id.get(rev)
            if not old:
                errs.append(f"{where}: reverses {rev}, which is not in the log")
            else:
                odec = _when((old.get("decision") or {}).get("date"))
                if dec and odec and (dec - odec).total_seconds() < 48 * 3600:
                    errs.append(f"{where}: reverses {rev} less than 48 hours after it was decided")
        if e.get("status") == "closed" and not re.match(r"^r\d+$", str(e.get("release_tag") or "")):
            errs.append(f"{where}: a closed plan change names the release that carried it (release_tag r<N>)")
    for b, ns in sorted(batches.items()):
        ns = sorted(ns)
        if ns != list(range(1, len(ns) + 1)):
            errs.append(f"{b}: ids are not 001..{len(ns):03d} without gaps (have {', '.join(f'{n:03d}' for n in ns)})")
    return errs, warns


# ------------------------------------------------------------------------------------- commit rule
def authored(paths: list[str], schema: dict, classify=None) -> list[str]:
    """The package-relative paths a commit touched that are authored inputs."""
    roots = tuple(schema["authored_roots"])
    files = set(schema["authored_files"]) | set(schema.get("plan_files") or [])
    hit = [p for p in paths if p in files or p.startswith(roots)]
    if classify and hit:
        kinds = classify([p for p in hit if p not in files])
        hit = [p for p in hit if p in files or kinds.get(p) != "derived"]
    return hit


def commit_rule(commits: list[dict], ids: set, schema: dict, classify=None,
                kinds: dict | None = None) -> tuple[list[str], list[str], int]:
    """commits: [{sha, date (datetime.date), message, paths (package-relative)}] -> (errors, exemptions,
    grandfathered)."""
    errs, exempt, old = [], [], 0
    start = _date(schema.get("commit_rule_from"))
    for c in commits:
        hit = authored(c["paths"], schema, classify)
        if not hit:
            continue
        subject = c["message"].strip().splitlines()[0][:90] if c["message"].strip() else ""
        if start and c["date"] < start:
            old += 1
            continue
        cited = set(ID_IN_TEXT.findall(c["message"]))
        plan_hit = [p for p in hit if p in set(schema.get("plan_files") or [])]
        if plan_hit and kinds is not None and not any(kinds.get(i) == "plan" for i in cited & ids):
            errs.append(f"{c['sha'][:9]} changes the plan ({', '.join(plan_hit)}) and names no plan change "
                        f"(kind: plan)  ({subject})")
            continue
        if cited & ids:
            unknown = cited - ids
            if unknown:
                errs.append(f"{c['sha'][:9]} cites {', '.join(sorted(unknown))}, not in changes/entries/  ({subject})")
            continue
        if EXEMPT.search(c["message"]):
            exempt.append(f"{c['sha'][:9]} {subject}")
            continue
        what = ", ".join(hit[:3]) + (f" and {len(hit) - 3} more" if len(hit) > 3 else "")
        errs.append(f"{c['sha'][:9]} touches {what} and names no change id"
                    + (f" (cites unknown {', '.join(sorted(cited))})" if cited else "") + f"  ({subject})")
    return errs, exempt, old


def latest_tag() -> str | None:
    rc, out = _git("tag", "-l", "r*", "--sort=-v:refname")
    for t in out.split():
        if re.match(r"^r\d+$", t):
            return t
    return None


def git_commits(since: str) -> list[dict]:
    rc, prefix = _git("rev-parse", "--show-prefix")
    prefix = prefix.strip()
    rc, out = _git("log", "--no-merges", "--format=\x1e%H\x1f%cI\x1f%B\x1f", "--name-only", f"{since}..HEAD")
    if rc != 0:
        raise SystemExit(f"git log {since}..HEAD failed")
    commits = []
    for chunk in out.split("\x1e")[1:]:
        sha, date, msg, files = (chunk.split("\x1f") + ["", "", "", ""])[:4]
        paths = [f.strip()[len(prefix):] for f in files.splitlines()
                 if f.strip() and f.strip().startswith(prefix)]
        commits.append({"sha": sha, "date": datetime.date.fromisoformat(date[:10]), "message": msg,
                        "paths": paths})
    return commits


def manifest_classifier():
    if not MANIFEST.exists():
        return None
    try:
        spec = importlib.util.spec_from_file_location("refresh_manifest", ROOT / "tools" / "refresh-manifest.py")
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        m = mod.load_manifest(str(MANIFEST))
        return lambda paths: mod.classify(m, paths)
    except Exception:
        return None


# --------------------------------------------------------------------------------------- self-tests
class FakeCtx:
    def __init__(self):
        self.checks = {"check-audience-match", "check-key-stability"}
        self.report_only = {"check-audience-match"}

    def exists(self, rel):
        return rel in {"tools/check-audience-match.py", "tools/check-key-stability.py", "tools/check-unrun.py",
                       "tools/design_spec.py"} or None

    def has_symbol(self, rel, sym):
        return rel == "tools/design_spec.py" and sym == "render_screen"

    def commit_known(self, sha):
        return sha.startswith("abc")


def self_test(schema: dict) -> list[tuple[str, bool, str]]:
    good = {"id": "CHG-TST-001", "date": "2026-10-02", "source": "audit", "kind": "contract",
            "summary": "s", "decision": {"what": "w", "by": "Chinmay", "date": "2026-10-02"},
            "why": "R123 found it", "keys_touched": {"operations": ["getX"]}, "root_class": "CR-3",
            "tickets": {"started": [], "unstarted": []}, "release_tag": "pending", "decision_owner": "Chinmay",
            "prevention": {"type": "check", "ref": "tools/check-key-stability.py"}, "status": "closed",
            "closed_by_commit": "abc1234"}
    ctx = FakeCtx()
    out = []

    def case(name, entries, want_ok, want=None):
        errs, _w = validate(entries, schema, ctx)
        ok = (not errs) if want_ok else any((want or "") in e for e in errs)
        out.append((name, ok, "; ".join(errs[:2]) or "no error"))

    f = "CHG-TST-001-good.yaml"
    case("a complete closed entry passes", [(f, good)], True)
    case("a second batch numbered from 001 passes",
         [(f, good), ("CHG-ABC-001-x.yaml", dict(good, id="CHG-ABC-001"))], True)
    case("a gap in a batch fails", [(f, good), ("CHG-TST-003-x.yaml", dict(good, id="CHG-TST-003"))], False, "without gaps")
    case("a duplicate id fails", [(f, good), ("CHG-TST-001-y.yaml", good)], False, "also")
    case("a bad id fails", [("CHG-1-x.yaml", dict(good, id="CHG-1"))], False, "does not match")
    case("a file name that is not the id fails", [("CHG-TST-001.yaml", good)], False, "file name")
    case("no decision fails", [(f, dict(good, decision=None))], False, "missing decision")
    case("a decision without who fails", [(f, dict(good, decision={"what": "w", "date": "2026-10-02"}))], False, "decision needs")
    case("a why with no citation fails", [(f, dict(good, why="because it was wrong"))], False, "cites no source")
    case("a minutes change without sign-off fails", [(f, dict(good, source="mom"))], False, "client_signoff")
    case("a minutes change pending sign-off passes", [(f, dict(good, source="mom", client_signoff="pending"))], True)
    case("closed on an unregistered check fails",
         [(f, dict(good, prevention={"type": "check", "ref": "tools/check-unrun.py"}))], False, "does not run")
    case("closed on a missing check fails",
         [(f, dict(good, prevention={"type": "check", "ref": "tools/check-gone.py"}))], False, "does not exist")
    case("closed on a generator rule that exists passes",
         [(f, dict(good, prevention={"type": "generator-rule", "ref": "tools/design_spec.py::render_screen"}))], True)
    case("closed on a generator rule naming a missing symbol fails",
         [(f, dict(good, prevention={"type": "generator-rule", "ref": "tools/design_spec.py::nothing"}))], False, "does not name")
    case("none without approval fails", [(f, dict(good, prevention={"type": "none", "reason": "r"}))], False, "approved_by")
    case("closed without a commit fails", [(f, dict(good, closed_by_commit=""))], False, "not a commit id")
    case("closed on an unknown commit fails", [(f, dict(good, closed_by_commit="def5678"))], False, "git knows")
    case("an open entry with no prevention ref passes",
         [(f, dict(good, status="open", closed_by_commit=None, prevention={"type": "template-field", "ref": "x::y"}))], True)
    case("from 5 October an entry without its ADAM CR fails", [(f, dict(good, date="2026-10-05"))], False, "adam_cr")
    case("from 5 October an entry with CR and triage passes",
         [(f, dict(good, date="2026-10-05", adam_cr="CR-41", triage="fix-forward"))], True)
    case("an unknown source fails", [(f, dict(good, source="hallway"))], False, "not one of")
    case("an open entry may wait for the lead's approval of none",
         [(f, dict(good, status="open", closed_by_commit=None, prevention={"type": "none", "reason": "r"}))], True)
    case("a closed entry on none without approval fails",
         [(f, dict(good, prevention={"type": "none", "reason": "r"}))], False, "approved_by")
    plan = dict(good, kind="plan", source="plan", date="2026-10-06", adam_cr="CR-50", triage="defer",
                keys_touched={}, release_tag="r4", proposed="2026-10-05T09:00",
                decision={"what": "w", "by": "Chinmay", "date": "2026-10-06T10:00"})
    pf = "CHG-TST-001-plan.yaml"
    case("a plan change decided a day after it was proposed passes", [(pf, plan)], True)
    case("a plan change without proposed fails", [(pf, dict(plan, proposed=None))], False, "proposed")
    case("a plan change decided within 24 hours fails",
         [(pf, dict(plan, proposed="2026-10-06T08:00"))], False, "cool off")
    case("a closed plan change without its release fails", [(pf, dict(plan, release_tag="pending"))], False, "release")
    plan2 = dict(plan, id="CHG-TST-002", proposed="2026-10-06T11:00", reverses="CHG-TST-001",
                 decision={"what": "back", "by": "Chinmay", "date": "2026-10-07T12:00"})
    case("a reversal within 48 hours fails", [(pf, plan), ("CHG-TST-002-back.yaml", plan2)], False, "48 hours")
    plan3 = dict(plan2, proposed="2026-10-07T11:00",
                 decision={"what": "back", "by": "Chinmay", "date": "2026-10-09T12:00"})
    case("a reversal after 48 hours passes", [(pf, plan), ("CHG-TST-002-back.yaml", plan3)], True)
    case("before 5 October the plan rule is not applied", [(pf, dict(plan, date="2026-10-01", proposed=None,
                                                                    adam_cr=None, triage=None))], True)

    d = datetime.date
    commits = [
        {"sha": "a" * 40, "date": d(2026, 10, 6), "message": "TICVAI fix (CHG-TST-001)", "paths": ["screens/P01.yaml"]},
        {"sha": "b" * 40, "date": d(2026, 10, 6), "message": "TICVAI fix", "paths": ["contracts/spine/orders.yaml"]},
        {"sha": "c" * 40, "date": d(2026, 10, 6), "message": "TICVAI derived only", "paths": ["handoff/api-list.md"]},
        {"sha": "d" * 40, "date": d(2026, 10, 1), "message": "TICVAI old", "paths": ["flows/F01.yaml"]},
        {"sha": "e" * 40, "date": d(2026, 10, 6), "message": "TICVAI r3 refresh\n\nCHG-exempt: release refresh",
         "paths": ["screens/P02.yaml"]},
        {"sha": "f" * 40, "date": d(2026, 10, 6), "message": "TICVAI fix (CHG-TST-009)", "paths": ["docs/adr/0070.md"]},
        {"sha": "9" * 40, "date": d(2026, 10, 6), "message": "TICVAI team (CHG-TST-002)", "paths": ["docs/active/team.json"]},
        {"sha": "8" * 40, "date": d(2026, 10, 6), "message": "TICVAI derived screen", "paths": ["screens/generated.yaml"]},
        {"sha": "7" * 40, "date": d(2026, 10, 6), "message": "TICVAI plan (CHG-TST-001)", "paths": ["tools/sprint_plan.py"]},
        {"sha": "6" * 40, "date": d(2026, 10, 6), "message": "TICVAI plan (CHG-TST-002)", "paths": ["tools/sprint_plan.py"]},
    ]
    cls = lambda ps: {p: ("derived" if p == "screens/generated.yaml" else "authored") for p in ps}
    errs, exempt, old = commit_rule(commits, {"CHG-TST-001", "CHG-TST-002"}, schema, cls,
                                    {"CHG-TST-001": "contract", "CHG-TST-002": "plan"})
    flagged = {e[:9] for e in errs}
    out.append(("commit rule: a cited id passes", "aaaaaaaaa" not in flagged, ""))
    out.append(("commit rule: an authored change with no id fails", "bbbbbbbbb" in flagged, ""))
    out.append(("commit rule: a derived-only commit is not asked", "ccccccccc" not in flagged, ""))
    out.append(("commit rule: a commit before 5 October is grandfathered", old == 1 and "ddddddddd" not in flagged, ""))
    out.append(("commit rule: a refresh exemption is printed, not failed", len(exempt) == 1 and "eeeeeeeee" not in flagged, ""))
    out.append(("commit rule: an id not in the log fails", "fffffffff" in flagged, ""))
    out.append(("commit rule: team.json is authored, and a plan change cites it", "999999999" not in flagged, ""))
    out.append(("commit rule: a file the manifest calls derived is not asked", "888888888" not in flagged, ""))
    out.append(("commit rule: a plan file cited with a non-plan change fails", "777777777" in flagged, ""))
    out.append(("commit rule: a plan file cited with a plan change passes", "666666666" not in flagged, ""))
    return out


# --------------------------------------------------------------------------------------------- main
def load_entries() -> list[tuple[str, dict]]:
    out = []
    for p in sorted(ENTRIES.glob("*.yaml")):
        try:
            out.append((p.name, _load(p)))
        except Exception as ex:
            out.append((p.name, f"unreadable: {ex}"))
    return out


def index_is_current(entries) -> bool | None:
    try:
        spec = importlib.util.spec_from_file_location("cl_index", ROOT / "tools" / "build-changelog-index.py")
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        want = mod.render([e for _f, e in entries if isinstance(e, dict)])
    except Exception:
        return None
    return INDEX.exists() and INDEX.read_text(encoding="utf-8") == want


def main() -> int:
    _utf8()
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--since", nargs="?", const="", default=None, metavar="REF",
                    help="also apply the commit rule to REF..HEAD (default REF: the latest r* tag)")
    a = ap.parse_args()
    schema = _load(SCHEMA)
    entries = load_entries()
    errs, warns = validate(entries, schema, Context())
    ids = {e.get("id") for _f, e in entries if isinstance(e, dict)}
    st = {}
    for _f, e in entries:
        if isinstance(e, dict):
            st[e.get("status")] = st.get(e.get("status"), 0) + 1
    print(f"change log: {len(entries)} entr{'y' if len(entries) == 1 else 'ies'} "
          f"({st.get('open', 0)} open, {st.get('closed', 0)} closed) in {ENTRIES.relative_to(ROOT).as_posix()}/")

    if a.since is not None:
        ref = a.since or latest_tag()
        if not ref:
            errs.append("--since: no r* tag to start from")
        else:
            commits = git_commits(ref)
            kinds = {e.get("id"): e.get("kind") for _f, e in entries if isinstance(e, dict)}
            c_errs, exempt, old = commit_rule(commits, ids, schema, manifest_classifier(), kinds)
            print(f"commit rule since {ref}: {len(commits)} commit(s); {old} grandfathered "
                  f"(before {schema.get('commit_rule_from')}); {len(exempt)} exempt")
            for x in exempt:
                print(f"  exempt  {x}")
            errs += c_errs

    cur = index_is_current(entries)
    if cur is False:
        warns.append("changes/CHANGELOG.md is not current: python3 tools/build-changelog-index.py "
                     "(the refresh does it; do not commit it from a branch)")
    for w in warns:
        print(f"  note  {w}")
    for e in errs:
        print(f"  FAIL  {e}")
    tests = self_test(schema)
    bad = [t for t in tests if not t[1]]
    for name, ok, detail in tests:
        if not ok:
            print(f"  test FAIL {name}: {detail}")
    if errs or bad:
        print(f"FAIL - {len(errs)} problem(s), {len(bad)} self-test(s) failed")
        return 1
    print(f"PASS - every entry valid, every closed entry's prevention exists; {len(tests)} self-tests pass")
    return 0


if __name__ == "__main__":
    sys.exit(main())
