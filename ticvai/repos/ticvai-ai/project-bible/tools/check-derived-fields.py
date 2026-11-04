#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A refresh may write into an authored file only inside a field it declares it owns (r14 review finding E-03).

**Authored inputs change only with a change entry** -- contracts/, screens/, flows/, states/, events/, docs/adr/ --
and the refresh derives everything else. But seven refresh steps write into screens/ and contracts/, and one into
flows/: r13's derive commit a657374c rewrote a navigation edge's `provenance` in screens/P14-developer-portal.yaml
(and 411 more across thirteen files), and the r10 and r11 derive commits touched 25 and 6 contract and screen
files. Every one of those writes was meant, and nothing could tell them apart from a hand edit committed under a
derive message: the derive commit was the one place a change to an authored file needed no change entry, and so
the one place an unrecorded change could hide. The lead (r14): "The derive must stop writing authored files, or
declare exactly the derived fields it owns."

**The declaration is `tools/derived_fields.py`**: per file glob, the field paths each step writes (`[]` every list
item, `*` every map key, `[?filter]` the list items a step marks as its own), whole files that are entirely
derived, and the generator-only rules (fill a blank, grow a list, correct text it recognises). This check parses
both versions of every authored file the refresh changed and fails on any difference outside those fields.

**Parsed, not textual.** The derivers re-dump whole files (PyYAML safe_dump, width 100), so a refresh rewraps lines
and drops comments in files whose data it never touched: r11's a47956cb changed 294 lines of P08 and no value.
A text diff would fail every refresh; the data is what the package means.

    python3 tools/check-derived-fields.py --base <tree-ish>   the working tree against <tree-ish> (refresh-safe.sh
                                                              passes the commit the refresh started from)
    python3 tools/check-derived-fields.py --commit <sha>      <sha>~1 against <sha>, both from git (a derive commit)
    python3 tools/check-derived-fields.py                     the self-test only
    python3 tools/check-derived-fields.py --list              the declaration, one line per rule

The self-test runs first every time and proves the check can fail: a change inside a declared field passes, a
change to the undeclared field beside it fails, a list item a step owns passes where a hand-written one beside it
fails, and a deleted authored file fails. Exit 1 on any finding or a failed self-test.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
import time
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import derived_fields as DF  # noqa: E402

import yaml  # noqa: E402

AUTHORED = ["contracts", "screens", "flows", "states", "events", "docs/adr"]


# ── git ─────────────────────────────────────────────────────────────────────────────────────────────────────────────

def git(*args: str) -> str:
    r = subprocess.run(["git", "-C", str(ROOT), *args], capture_output=True)
    if r.returncode != 0:
        raise SystemExit(f"git {' '.join(args)}: {r.stderr.decode('utf-8', 'replace').strip()}")
    return r.stdout.decode("utf-8")


def blobs(requests: list) -> dict:
    """{(rev, package path): text or None} for many files in one `git cat-file --batch`."""
    if not requests:
        return {}
    prefix = git("rev-parse", "--show-prefix").strip()
    data = "".join(f"{rev}:{prefix}{p}\n" for rev, p in requests).encode("utf-8")
    out = subprocess.run(["git", "-C", str(ROOT), "cat-file", "--batch"], input=data, capture_output=True).stdout
    res, pos = {}, 0
    for req in requests:
        nl = out.index(b"\n", pos)
        head = out[pos:nl].decode("utf-8", "replace").split()
        pos = nl + 1
        if len(head) == 3 and head[1] == "blob":
            size = int(head[2])
            res[req] = out[pos:pos + size].decode("utf-8", "replace")
            pos += size + 1
        else:
            res[req] = None                      # missing, or not a file at that revision
    return res


def changed_files(a: str, b: str | None) -> list:
    """Package-relative paths under the authored directories that differ between a and b (None: the working tree,
    untracked files included, since a step that creates a file leaves it untracked)."""
    rng = [a] if b is None else [a, b]
    names = git("diff", "--name-only", "--no-renames", "--relative", *rng, "--", *AUTHORED).split("\n")
    if b is None:
        names += git("ls-files", "--others", "--exclude-standard", "--", *AUTHORED).split("\n")
    return sorted({n.strip() for n in names if n.strip()})


def run(pairs: list) -> tuple:
    """[(path, before, after)] -> (findings, files changed)."""
    findings = []
    for path, before, after in pairs:
        diffs = DF.compare_all(path, before, after)
        for where, kind in diffs[:DF.LIMIT]:
            findings.append(f"FAIL {path} {where}: changed outside the fields the refresh owns ({kind})")
        if len(diffs) > DF.LIMIT:
            findings.append(f"FAIL {path} (and {len(diffs) - DF.LIMIT} more difference(s) in this file): changed "
                            f"outside the fields the refresh owns")
    return findings, len(pairs)


# ── self-test ───────────────────────────────────────────────────────────────────────────────────────────────────────

def _dump(doc) -> str:
    return yaml.safe_dump(doc, sort_keys=False, allow_unicode=True, width=100)


def _screens():
    return {"platform": {"code": "P08", "wireframeBoard": "wireframes/P08.dc.html"}, "screens": [
        {"id": "BO-1", "name": "Rules", "purpose": "See rules for this venue.",
         "apis": [{"operationId": "listRules", "contract": "tenancy", "purpose": "listRules", "trigger": "onLoad"},
                  {"operationId": "recordViewEvents", "contract": "reporting", "purpose": "Beacon",
                   "trigger": "onLoad"}],
         "entryState": {"params": [{"name": "venueId", "from": "session"}]},
         "navigation": {"exitTo": ["BO-2"], "entryFrom": [],
                        "transitions": [{"to": "BO-2", "trigger": "Open", "provenance": "board reading, 19 Sep"}]},
         "layout": {"regions": [{"name": "contentBody", "components": [{"kind": "dataTable", "label": "Rules"}]}]},
         "wireframe": {"status": "notStarted", "provenance": "generated", "board": "wireframes/P08.dc.html#bo-1"}},
        {"id": "BO-2", "name": "Rule", "purpose": "One rule, edited.", "navigation": {"entryFrom": ["BO-1"]}},
        {"id": "BO-3", "name": "Audit", "purpose": "The audit trail of rules."},
    ]}


def _contract():
    return {"openapi": "3.0.3", "info": {"title": "Tenancy", "version": "1", "x-ticvai-screen-count": 2},
            "paths": {"/rules": {"get": {"operationId": "listRules", "summary": "List rules",
                                         "x-ticvai-consumed-by": ["P08 BO-1 Rules"]}}}}


def _case(path, before, mutate, expect_pass):
    after = None
    if mutate is not None:
        doc = yaml.safe_load(before) if before is not None else None
        after = mutate(doc)
        after = after if isinstance(after, str) or after is None else _dump(after)
    return path, before, after, expect_pass


def _s(doc, sid):
    return next(s for s in doc["screens"] if s["id"] == sid)


def _set(fn):
    """A mutation that edits the doc in place and returns it."""
    def m(doc):
        fn(doc)
        return doc
    return m


def self_test() -> list:
    S, C = _dump(_screens()), _dump(_contract())
    P, K = "screens/P08-venue-back-office.yaml", "contracts/spine/tenancy.yaml"
    flow_edge = {"to": "BO-3", "trigger": "Opens the audit", "provenance": "flow F12 step 2→3"}
    cases = [
        ("a reflowed file, the same data", _case(P, S, lambda d: "# a comment the dump dropped\n" + yaml.safe_dump(
            d, sort_keys=False, width=60), True)),
        # contracts: a declared field and the one beside it
        ("consumed-by recomputed", _case(K, C, _set(lambda d: d["paths"]["/rules"]["get"].update(
            {"x-ticvai-consumed-by": ["P08 BO-1 Rules", "P08 BO-3 Audit"]})), True)),
        ("screen count recomputed", _case(K, C, _set(lambda d: d["info"].update({"x-ticvai-screen-count": 3})), True)),
        ("the summary beside consumed-by", _case(K, C, _set(lambda d: d["paths"]["/rules"]["get"].update(
            {"summary": "List the rules"})), False)),
        ("the version beside the screen count", _case(K, C, _set(lambda d: d["info"].update({"version": "2"})),
                                                      False)),
        # screens: list items a step owns, and hand-written ones beside them
        ("a flow edge added with its exit (--adopt)", _case(P, S, _set(lambda d: (
            _s(d, "BO-1")["navigation"]["transitions"].append(dict(flow_edge)),
            _s(d, "BO-1")["navigation"]["exitTo"].append("BO-3"),
            _s(d, "BO-3").setdefault("navigation", {}).setdefault("entryFrom", []).append("BO-1"))), True)),
        ("an exit added with no flow behind it", _case(P, S, _set(lambda d: _s(d, "BO-1")["navigation"]["exitTo"]
                                                             .append("BO-3")), False)),
        ("an exit removed", _case(P, S, _set(lambda d: _s(d, "BO-1")["navigation"].update({"exitTo": []})), False)),
        ("a hand-written edge's trigger", _case(P, S, _set(lambda d: _s(d, "BO-1")["navigation"]["transitions"][0]
                                                          .update({"trigger": "Edit"})), False)),
        ("carries filled on a hand-written edge", _case(P, S, _set(lambda d: _s(d, "BO-1")["navigation"]
                                                                   ["transitions"][0].update({"carries": ["ruleId"]})),
                                                        True)),
        ("a hand-written edge's provenance made a flow's", _case(P, S, _set(lambda d: _s(d, "BO-1")["navigation"]
                                                                            ["transitions"][0].update(
            {"provenance": "flow F1 step 1→2"})), False)),
        ("a derived component added", _case(P, S, _set(lambda d: _s(d, "BO-1")["layout"]["regions"][0]["components"]
                                                       .append({"kind": "primaryButton", "derived": True,
                                                                "impliedBy": "createRule", "notes": "x"})), True)),
        ("a derived region made on a screen with no layout", _case(P, S, _set(lambda d: _s(d, "BO-3").update(
            {"layout": {"regions": [{"name": "contentBody", "components": [
                {"kind": "detailPanel", "derived": True, "impliedBy": "getAudit", "notes": "x"}]}]}})), True)),
        ("an authored component's label", _case(P, S, _set(lambda d: _s(d, "BO-1")["layout"]["regions"][0]
                                                          ["components"][0].update({"label": "All rules"})), False)),
        ("an operation bound to an unbound control", _case(P, S, _set(lambda d: _s(d, "BO-1")["layout"]["regions"][0]
                                                                     ["components"][0].update(
            {"operation": "listRules"})), True)),
        # fill, replace, grow
        ("a permission filled", _case(P, S, _set(lambda d: _s(d, "BO-1").update({"permission": "RULE_READ"})), True)),
        ("a contract written back", _case(P, S, _set(lambda d: _s(d, "BO-1")["apis"][0].update(
            {"contract": "identity"})), True)),
        ("an api's operationId", _case(P, S, _set(lambda d: _s(d, "BO-1")["apis"][0].update(
            {"operationId": "listRuleSets"})), False)),
        ("a beacon moved to the background", _case(P, S, _set(lambda d: _s(d, "BO-1")["apis"][1].update(
            {"trigger": "background"})), True)),
        ("a read moved to onAction", _case(P, S, _set(lambda d: _s(d, "BO-1")["apis"][0].update(
            {"trigger": "onAction"})), False)),
        ("a boilerplate purpose rewritten", _case(P, S, _set(lambda d: _s(d, "BO-1").update(
            {"purpose": "Rules: shows list rules (`listRules`)."})), True)),
        ("a real purpose rewritten", _case(P, S, _set(lambda d: _s(d, "BO-2").update({"purpose": "Edit a rule."})),
                                           False)),
        ("an entry param in param_for's shape", _case(P, S, _set(lambda d: _s(d, "BO-1")["entryState"]["params"]
                                                                 .append({"name": "ruleId", "from": "navigation",
                                                                          "optional": True,
                                                                          "notes": "Optional: opened without it."})),
                                                      True)),
        ("an entry param with prose no generator writes", _case(P, S, _set(lambda d: _s(d, "BO-1")["entryState"]
                                                                           ["params"].append(
            {"name": "ruleId", "from": "navigation", "description": "the rule"})), False)),
        ("an authored entry param removed", _case(P, S, _set(lambda d: _s(d, "BO-1")["entryState"].update(
            {"params": []})), False)),
        ("state views written", _case(P, S, _set(lambda d: _s(d, "BO-1")["wireframe"].update(
            {"stateViews": {"loading": "P08/skeleton"}})), True)),
        ("an existing board anchor changed", _case(P, S, _set(lambda d: _s(d, "BO-1")["wireframe"].update(
            {"board": "wireframes/P08.dc.html#bo-9"})), False)),
        ("a screen removed", _case(P, S, _set(lambda d: d["screens"].pop()), False)),
        # whole files, created files, deleted files, non-YAML
        ("an authored file deleted", _case(P, S, None, False)),
        ("the id register rewritten", _case("screens/_id-register.yaml", _dump({"prefixes": {"BO": {"nextFree": 4}}}),
                                            _set(lambda d: d["prefixes"]["BO"].update({"nextFree": 5})), True)),
        ("a board flow created", _case("flows/F900-board.yaml", None, lambda d: _dump(
            {"id": "F900", "provenance": "derived-from-board", "steps": []}), True)),
        ("an authored flow created", _case("flows/F901-new.yaml", None, lambda d: _dump(
            {"id": "F901", "steps": []}), False)),
        ("an existing board flow edited", _case("flows/F900-board.yaml", _dump(
            {"id": "F900", "provenance": "derived-from-board", "steps": []}), _set(lambda d: d.update(
                {"steps": [{"step": 1}]})), False)),
        ("a state model edited", _case("states/rule.yaml", _dump({"states": ["draft", "live"]}),
                                       _set(lambda d: d["states"].append("retired")), False)),
        ("an ADR edited", ("docs/adr/0001-x.md", "# ADR 1\n\nDecided.\n", "# ADR 1\n\nUndecided.\n", False)),
        ("an ADR only re-saved with CRLF", ("docs/adr/0001-x.md", "# ADR 1\n\nDecided.\n",
                                            "# ADR 1\r\n\r\nDecided.\r\n", True)),
    ]
    bad = []
    for name, (path, before, after, expect_pass) in cases:
        got = DF.compare_all(path, before, after)
        if (not got) != expect_pass:
            bad.append(f"self-test FAIL: {name}: expected {'PASS' if expect_pass else 'a finding'}, got "
                       f"{got[:3] or 'PASS'}")
    # strip() removes exactly the strip-mode fields
    st = DF.strip(P, yaml.safe_load(S))
    if "contract" in st["screens"][0]["apis"][0] or "board" not in st["screens"][0]["wireframe"]:
        bad.append("self-test FAIL: strip() did not remove apis[].contract alone")
    print(f"self-test: {len(cases) + 1} case(s), " + ("all as expected" if not bad else f"{len(bad)} wrong"))
    return bad


# ── main ────────────────────────────────────────────────────────────────────────────────────────────────────────────

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--base", help="tree-ish the refresh started from; compares the working tree with it")
    g.add_argument("--commit", help="a commit; compares it with its first parent, both from git")
    ap.add_argument("--list", action="store_true", help="print the declaration and exit")
    a = ap.parse_args()

    if a.list:
        for line in DF.summary():
            print(line)
        return 0

    bad = self_test()
    for line in bad:
        print(line)
    if bad:
        print(f"FAIL - the self-test failed ({len(bad)} case(s)); the check cannot be trusted")
        return 1

    t0 = time.time()
    if a.base:
        names = changed_files(a.base, None)
        before = blobs([(a.base, n) for n in names])
        pairs = []
        for n in names:
            p = ROOT / n
            after = p.read_text(encoding="utf-8") if p.is_file() else None
            pairs.append((n, before[(a.base, n)], after))
        what = f"the working tree against {a.base}"
    elif a.commit:
        parent = a.commit + "~1"
        names = changed_files(parent, a.commit)
        got = blobs([(parent, n) for n in names] + [(a.commit, n) for n in names])
        pairs = [(n, got[(parent, n)], got[(a.commit, n)]) for n in names]
        what = f"{a.commit} against its parent"
    else:
        print("self-test only: no refresh to compare (refresh-safe.sh passes --base)")
        return 0

    findings, n = run(pairs)
    for line in findings:
        print(line)
    secs = time.time() - t0
    if findings:
        print(f"FAIL - {len(findings)} finding(s) ({what}, {n} authored file(s) changed, {secs:.1f}s)")
        return 1
    print(f"PASS - {n} authored file(s) changed by the refresh, every change inside a declared derived field "
          f"({what}, {secs:.1f}s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
