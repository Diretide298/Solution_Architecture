#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The one allowlist the release gate reads: `tools/refresh-safe-baseline.json` (r14, CHG-R14I-001).

**Why this module exists.** The r13 system review (findings E-01, E-02, E-11, F-12; 3 November 2026) found that "gate
PASS" at r13 was refresh-safe.sh's judgement against an allowlist with no dates, while three gating checkers failed
when run on their own:

  * the allowlist had no `added`, `expires` or `approved_by`, so CLAUDE.md rule 15 ("allowlist entries expire within
    14 days") never reached it; its entries were 14 to 33 days old;
  * check-screen-patterns was pinned by its summary line (`^28 finding\\(s\\): NP 1, P8 20, READ 7$`), so a finding
    could be swapped for another of the same rule, and the later-sprint NP count grew from 191 to 312 as "NP 1";
  * run-checks.py never read it, so `python tools/run-checks.py` and the release gate gave different verdicts;
  * a baselined checker that printed its known lines and then crashed was judged a pass.

So the rules live here, once, and both `tools/run-checks.py` (its gate) and `tools/refresh-safe.sh` (its judge, which
now takes run-checks.py's verdict instead of running checkers of its own) apply them:

  1. An entry carries `added` and `expires` (YYYY-MM-DD, at most EXPIRY_DAYS after `added`), `approved_by` (the
     lead), `change` (the CHG-/CR- id that records why) and `why`. An entry without them, or past its expiry, is
     itself a gate failure (`ALLOWLIST <checker>: ...`), whatever the checker prints.
  2. A `known` pattern names one finding. A pattern that matches a count or a verdict line (`28 finding(s)`,
     `FAIL - 7 stale`) is refused: a count is not a finding, and a count pin lets findings swap.
  3. A failing checker is let through only when it ran to its end (no traceback, and its last line is its own
     verdict: FAIL / STALE / ISSUE / ERROR), it printed at least one finding line, and every finding line it printed
     matches a pattern of a valid entry. Anything else is a gate failure.
  4. A pass with allowlisted failures is printed as `PASS with N allowlisted failure(s)`, never as a bare PASS.

`tools/check-baseline-ratchet.py` applies rules 1 and 2 to the file on its own (so a bad entry fails every run,
not only a release run), and compares the file with the last release tag (no entry may appear without the
approval fields).
"""
import datetime
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH = os.path.join(ROOT, "tools", "refresh-safe-baseline.json")
EXPIRY_DAYS = 14                    # CLAUDE.md rule 15
REQUIRED = ("added", "expires", "approved_by", "change", "why")
CHANGE_ID = re.compile(r"\b(CHG-[A-Z][A-Z0-9]{1,5}-\d{3}|CR-\d+)\b")
# A finding line in the forms the checkers print; the closing verdict (`FAIL - ...`) is not a finding.
FINDING = re.compile(r"^\s*(FAIL|STALE|ISSUE|ERROR)\s+(?!-)(.*\S)\s*$", re.M)
# The last line of a checker that ran to its end and failed.
VERDICT = re.compile(r"^\s*(FAIL|STALE|ISSUE|ERROR)\b")
# A pattern that is a count or a verdict rather than one finding (rule 2).
COUNT_PATTERN = re.compile(r"\\d|\d+\s*(?:\\s[*+]?\s*)?(?:finding|stale|issue|problem|error|failure|new|known)"
                           r"|finding\\?\(s\\?\)|^\^?\s*(?:FAIL|PASS)\s*(?:\\s[*+]?)?\s*-", re.I)


def _date(v):
    try:
        return datetime.date.fromisoformat(str(v))
    except ValueError:
        return None


def load(path=PATH):
    if not os.path.exists(path):
        return {"checkers": {}}
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def entry_problems(name, e, today=None):
    """Why an allowlist entry is not valid today (rules 1 and 2); [] when it is."""
    today = today or datetime.date.today()
    out = []
    if not isinstance(e, dict):
        return ["the entry is not an object"]
    for f in REQUIRED:
        if not str(e.get(f) or "").strip():
            out.append("no `%s`" % f)
    added, expires = _date(e.get("added")), _date(e.get("expires"))
    if e.get("added") and added is None:
        out.append("`added` is not a date (YYYY-MM-DD)")
    if e.get("expires") and expires is None:
        out.append("`expires` is not a date (YYYY-MM-DD)")
    if added and expires:
        if (expires - added).days > EXPIRY_DAYS:
            out.append("`expires` %s is more than %d days after `added` %s (CLAUDE.md rule 15)"
                       % (expires, EXPIRY_DAYS, added))
        if expires < today:
            out.append("expired on %s: fix the finding, or the lead approves a new entry" % expires)
        if added > today:
            out.append("`added` %s is in the future" % added)
    if e.get("change") and not CHANGE_ID.search(str(e.get("change"))):
        out.append("`change` names no CHG-XXX-nnn or CR-nnn id")
    known = e.get("known")
    if not isinstance(known, list) or not known:
        out.append("no `known` patterns: an entry lets through named findings only")
    else:
        for pt in known:
            try:
                re.compile(pt)
            except re.error as x:
                out.append("pattern %r does not compile: %s" % (pt, x))
                continue
            if COUNT_PATTERN.search(pt):
                out.append("pattern %r is a count or a verdict, not one finding (rule 2, review E-01)" % pt)
    return out


def all_problems(doc, today=None):
    """[(checker, problem)] for every entry of the file (rules 1 and 2)."""
    out = []
    for name, e in sorted((doc.get("checkers") or {}).items()):
        out += [(name, p) for p in entry_problems(name, e, today)]
    cov = doc.get("refresh_tools_coverage") or {}
    for n in cov.get("known_unexcused") or []:
        if not isinstance(n, dict):
            out.append(("refresh_tools_coverage", "%r has no dates or approval: give it the fields of rule 1" % n))
        else:
            out += [("refresh_tools_coverage", p) for p in entry_problems("refresh_tools_coverage", dict(n, known=[".+"]),
                                                                           today)]
    return out


def findings(out):
    return [m.group(2).strip() for m in FINDING.finditer(out or "")]


def ran_to_end(out):
    """A failing checker ran to its end: no traceback, and its last line is its own verdict."""
    text = out or ""
    if "Traceback (most recent call last)" in text:
        return False
    lines = [l for l in text.splitlines() if l.strip()]
    return bool(lines) and bool(VERDICT.match(lines[-1]))


def judge(name, rc, out, doc, today=None):
    """('pass'|'allowlisted'|'fail', [reasons]) for one gating checker's run."""
    if rc == 0:
        return "pass", []
    e = (doc.get("checkers") or {}).get(name)
    if e is None:
        return "fail", []
    bad = entry_problems(name, e, today)
    if bad:
        return "fail", ["allowlist entry not valid: %s" % "; ".join(bad)]
    if not ran_to_end(out):
        return "fail", ["rc=%d and the run did not end on its own verdict (a crash is never allowlisted)" % rc]
    errs = findings(out)
    if not errs:
        return "fail", ["rc=%d with no finding line to compare with the allowlist" % rc]
    unknown = [x for x in errs if not any(re.search(pt, x) for pt in e["known"])]
    if unknown:
        return "fail", ["not in the allowlist: %s" % x for x in unknown]
    return "allowlisted", ["%d finding(s), every one allowlisted until %s (%s, approved by %s)"
                           % (len(errs), e["expires"], e["change"], e["approved_by"])]


def gone(name, out, doc):
    """Patterns of an entry that matched nothing in this run (remove them)."""
    e = (doc.get("checkers") or {}).get(name) or {}
    errs = findings(out)
    return [pt for pt in e.get("known") or [] if not any(re.search(pt, x) for x in errs)]


def verdict_line(n_fail, n_allow):
    if n_fail:
        return "FAIL"
    return "PASS with %d allowlisted failure(s)" % n_allow if n_allow else "PASS"


def self_test():
    """The rules on made-up entries: [] when every case holds."""
    t = datetime.date(2026, 11, 3)
    good = {"added": "2026-11-01", "expires": "2026-11-10", "approved_by": "Chinmay", "change": "CHG-R14I-001",
            "why": "x", "known": [r"^SP-NOACCESS\s+P14 DEV-001: "]}
    doc = {"checkers": {"c": good}}
    bad = []
    cases = [
        (entry_problems("c", good, t) == [], "a dated, approved, named entry is valid"),
        (any("expired" in p for p in entry_problems("c", dict(good, expires="2026-11-02"), t)), "an expired entry"),
        (any("more than" in p for p in entry_problems("c", dict(good, expires="2026-11-30"), t)), "over 14 days"),
        (any("approved_by" in p for p in entry_problems("c", {k: v for k, v in good.items() if k != "approved_by"}, t)),
         "no approver"),
        (any("count" in p for p in entry_problems("c", dict(good, known=[r"^28 finding\(s\): NP 1, P8 20, READ 7$"]), t)),
         "the r13 count pin (E-01)"),
        (any("count" in p for p in entry_problems("c", dict(good, known=[r"FAIL - \d+ stale"]), t)), "a verdict pin"),
        (judge("c", 1, "  FAIL SP-NOACCESS   P14 DEV-001: x\nFAIL - 1 finding(s)\n", doc, t)[0] == "allowlisted",
         "a named finding is let through"),
        (judge("c", 1, "  FAIL SP-NOACCESS   P14 DEV-001: x\n  FAIL SP-NOACCESS BO-293: y\nFAIL - 2\n", doc, t)[0]
         == "fail", "a second finding is new"),
        (judge("c", 1, "  FAIL SP-NOACCESS   P14 DEV-001: x\nTraceback (most recent call last):\n  KeyError\n", doc,
               t)[0] == "fail", "a crash after the known line (E-11)"),
        (judge("c", 1, "  FAIL SP-NOACCESS   P14 DEV-001: x\nFAIL - 1\n",
               {"checkers": {"c": dict(good, expires="2026-11-02")}}, t)[0] == "fail", "an expired entry lets nothing"),
        (judge("d", 1, "  FAIL x\nFAIL - 1\n", doc, t)[0] == "fail", "a checker with no entry"),
        (verdict_line(0, 2) == "PASS with 2 allowlisted failure(s)", "the verdict names the allowlisted"),
    ]
    for ok, what in cases:
        if not ok:
            bad.append(what)
    return bad
