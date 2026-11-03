#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The known-findings index ADAM's pull reads is complete and current (r14 lane k, CHG-R14PUL-001).

**Why.** The lead, 3 November 2026: "a ticket's pull lists the package checks it already fails, so developers stop
raising change requests for gaps we already know about". tools/build-known-findings.py writes
handoff/known-findings.json, every known (baselined, still found) finding of the gate's checks with the artefacts it is
about, and ADAM's pull lists the ones a ticket links. An index that misses a finding, or one written before the
baseline moved, tells a developer a gap is new when it is on the list (or known when it is fixed), and the change
requests come back. This holds it:

  KF-STALE      handoff/known-findings.json is missing, or is not what build-known-findings.py writes now (the
                package and the checks' baselines are read again; derive before check: the refresh runs the builder
                just before the checks)
  KF-SOURCE     a baseline the index was built from has moved since (its sha256 in `sources` differs)
  KF-COVERAGE   a finding handoff/audit-baseline.json holds is in the index neither as a finding, nor as unmapped,
                nor as gone (no longer found)
  KF-UNMAPPED   a known finding maps to no artefact a ticket links (its rule is not in build-known-findings.py
                RULE_MAP, or its key names nothing in the package), and NOT_AN_ARTEFACT gives no reason. Each is
                listed by name; the excused ones are listed too, never failed

Strict: a new finding fails whatever any baseline says, and nothing here is ever baselined. It shows what the
baselines hold and judges nothing about the findings themselves.

    python3 tools/check-known-findings.py               # the self-test, then the index
    python3 tools/check-known-findings.py --self-test   # the self-test alone
    python3 tools/check-known-findings.py --quick       # without the regeneration (KF-STALE not judged)
"""
from __future__ import annotations

import argparse
import copy
import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import audit_guard as g  # noqa: E402

INDEX = ROOT / "handoff" / "known-findings.json"
SOURCES = {"handoff/audit-baseline.json": ROOT / "handoff" / "audit-baseline.json",
           "tools/refresh-safe-baseline.json": ROOT / "tools" / "refresh-safe-baseline.json"}


def builder():
    spec = importlib.util.spec_from_file_location("build_known_findings", ROOT / "tools" / "build-known-findings.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def judge(index: dict | None, audit: dict, shas: dict, fresh_text: str | None = None,
          index_text: str | None = None) -> list:
    """[(rule, message)] for the index against the audit baseline, the baselines' current sha256 (`shas`), and, when
    given, the text the builder writes now (`fresh_text`, against `index_text`)."""
    out = []
    if index is None:
        return [("KF-STALE", "handoff/known-findings.json is missing: run tools/build-known-findings.py "
                             "(the refresh does)")]
    if fresh_text is not None and fresh_text != index_text:
        try:
            fresh = json.loads(fresh_text)
            a = {(f["check"], f["rule"], f["key"]): f for f in index.get("findings") or []}
            b = {(f["check"], f["rule"], f["key"]): f for f in fresh.get("findings") or []}
            moved = sorted(k for k in a.keys() | b.keys() if a.get(k) != b.get(k))
            what = (f"{len(moved)} finding(s) differ, e.g. {' '.join('/'.join(k) for k in moved[:3])}" if moved
                    else "the findings agree; the rest of the file differs")
        except ValueError:
            what = "the builder's output would not parse"
        out.append(("KF-STALE", f"handoff/known-findings.json is not what tools/build-known-findings.py writes now "
                                f"({what}): run it (the refresh does), never edit it by hand"))
    for rel, now in sorted(shas.items()):
        had = ((index.get("sources") or {}).get(rel) or {}).get("sha256")
        if had != now:
            out.append(("KF-SOURCE", f"{rel} moved since the index was built (sha256 {str(had)[:12]} in the index, "
                                     f"{str(now)[:12]} now): run tools/build-known-findings.py"))
    held = {(f["check"], f["rule"], f["key"]) for f in (index.get("findings") or []) + (index.get("unmapped") or [])}
    gone = {(c, *rk.split("|", 1)) for c, keys in (index.get("gone") or {}).items() for rk in keys}
    for check, entry in sorted((k, v) for k, v in audit.items() if k != "_about" and isinstance(v, dict)):
        missing = [(check, r, k) for r, keys in sorted((entry.get("rules") or {}).items()) for k in keys or ()
                   if (check, r, k) not in held and (check, r, k) not in gone]
        if missing:
            out.append(("KF-COVERAGE", f"{check}: {len(missing)} baselined finding(s) in the index neither as a "
                                       f"finding, unmapped nor gone, e.g. {', '.join(m[1] + ' ' + m[2] for m in missing[:3])}"))
    for u in index.get("unmapped") or []:
        if not u.get("excused"):
            out.append(("KF-UNMAPPED", f"{u['check']} {u['rule']} {u['key']}: {u.get('why')} ({u.get('message', '')[:120]})"))
    return out


# ---- self-test ---------------------------------------------------------------------------------------------------

def self_test() -> list:
    b = builder()
    pkg = b.Package.of(
        ops={"createOrder": "orders#createOrder", "getCart": "orders#getCart"},
        screens={"POS-001", "WEB-010", "GST-010"}, tables={"orders.sales_order"},
        schema_tables={"orders.Order": {"orders.sales_order"}}, schema_ops={"orders.Order": {"orders#createOrder"}},
        schema_file={"orders.Orphan": "contracts/spine/orders.yaml"},
        groups={"cart": ["WEB-010", "GST-010"]}, files={"docs/active/a.md"})
    exports = {
        "check-screen-wiring": {"check": "check-screen-wiring", "rules": {"S-X": "x"}, "known": [
            {"rule": "S-X", "key": "POS-001:createOrder", "message": "POS-001: createOrder unreached"},
            {"rule": "S-X", "key": "POS-999:createOrder", "message": "a screen gone, the operation stays"}],
            "gone": {"S-X": ["POS-001:getCart"]}},
        "check-contract-shapes": {"check": "check-contract-shapes", "rules": {}, "known": [
            {"rule": "C-ENUM", "key": "orders.Order.kind", "message": "enum"},
            {"rule": "C-ENUM", "key": "orders.Orphan.kind", "message": "a schema nothing reaches"},
            {"rule": "C-ENUM", "key": "orders.Nothing.kind", "message": "names nothing"}]},
        "check-navigation": {"check": "check-navigation", "rules": {}, "known": [
            {"rule": "N-TWIN-OPS", "key": "cart", "message": "guest group cart"}]},
        "check-rls-scope-fit": {"check": "check-rls-scope-fit", "rules": {}, "known": [
            {"rule": "RF", "key": "createOrder:orders.sales_order:write", "message": "rls"}]},
        "check-cited-sources": {"check": "check-cited-sources", "rules": {}, "known": [
            {"rule": "CS", "key": "docs/active/a.md|scratchpad/x", "message": "cites"}]},
        "check-new-guard": {"check": "check-new-guard", "rules": {}, "known": [
            {"rule": "Z", "key": "POS-001", "message": "a guard RULE_MAP does not name"}]},
    }
    audit = {"_about": "", **{n: {"rules": {}} for n in exports}}
    audit["check-screen-wiring"]["rules"] = {"S-X": ["POS-001:createOrder", "POS-999:createOrder", "POS-001:getCart"]}
    audit["check-contract-shapes"]["rules"] = {"C-ENUM": ["orders.Order.kind", "orders.Orphan.kind", "orders.Nothing.kind"]}
    audit["check-navigation"]["rules"] = {"N-TWIN-OPS": ["cart"]}
    audit["check-rls-scope-fit"]["rules"] = {"RF": ["createOrder:orders.sales_order:write"]}
    audit["check-cited-sources"]["rules"] = {"CS": ["docs/active/a.md|scratchpad/x"]}
    audit["check-new-guard"]["rules"] = {"Z": ["POS-001"]}
    safe = {"checkers": {"check-screen-patterns": {"known": ["^1 finding"]}, "check-package": {"known": []}}}

    def lines(name, patterns):
        assert name == "check-screen-patterns", name
        return {"known": [{"rule": "P8", "key": "WEB-010", "message": "WEB-010: wave 2"},
                          {"rule": "NP", "key": "NP-ceiling", "message": "312 over the ceiling"}]}

    doc = b.build(pkg, {"guard": lambda n: copy.deepcopy(exports[n]), "lines": lines}, audit, safe)
    arts = {(f["check"], f["key"]): f["artefacts"] for f in doc["findings"]}
    un = {(u["check"], u["key"]): u for u in doc["unmapped"]}
    fails = []

    def case(name, ok):
        if not ok:
            fails.append(name)

    case("a screen key maps to the screen and the operation it names",
         arts.get(("check-screen-wiring", "POS-001:createOrder")) == ["operation:orders#createOrder", "screen:POS-001"])
    case("a key whose screen is gone still maps to its operation",
         arts.get(("check-screen-wiring", "POS-999:createOrder")) == ["operation:orders#createOrder"])
    case("a gone baseline entry is not a finding, and is listed as gone",
         ("check-screen-wiring", "POS-001:getCart") not in arts
         and doc["gone"].get("check-screen-wiring") == ["S-X|POS-001:getCart"])
    case("a schema field maps to the tables built from it and the operations reaching it",
         arts.get(("check-contract-shapes", "orders.Order.kind")) == ["operation:orders#createOrder", "table:orders.sales_order"])
    case("a schema nothing reaches maps to its contract file",
         arts.get(("check-contract-shapes", "orders.Orphan.kind")) == ["file:contracts/spine/orders.yaml"])
    case("a key naming nothing is unmapped, by name, not excused",
         ("check-contract-shapes", "orders.Nothing.kind") in un and not un[("check-contract-shapes", "orders.Nothing.kind")]["excused"])
    case("a guest pair maps to its web and app screens",
         arts.get(("check-navigation", "cart")) == ["screen:GST-010", "screen:WEB-010"])
    case("operation:table:write maps to both",
         arts.get(("check-rls-scope-fit", "createOrder:orders.sales_order:write")) == ["operation:orders#createOrder", "table:orders.sales_order"])
    case("a citing document maps to itself, not to what it cites",
         arts.get(("check-cited-sources", "docs/active/a.md|scratchpad/x")) == ["file:docs/active/a.md"])
    case("a guard RULE_MAP does not name is unmapped and says so",
         "RULE_MAP" in (un.get(("check-new-guard", "POS-001")) or {}).get("why", ""))
    case("a refresh-safe line finding maps to its screen", arts.get(("check-screen-patterns", "WEB-010")) == ["screen:WEB-010"])
    case("NOT_AN_ARTEFACT excuses the count over a ceiling", (un.get(("check-screen-patterns", "NP-ceiling")) or {}).get("excused") is True)
    case("a checker with no accepted lines is not run", "check-package" not in doc["sources"]["tools/refresh-safe-baseline.json"]["checks"])

    shas = {k: v["sha256"] for k, v in doc["sources"].items() if "sha256" in v}
    text = b.dump(doc)
    case("the dump parses back to the same index", json.loads(text) == doc)
    verdict = {r for r, _ in judge(doc, audit, shas, text, text)}
    case("the unmapped findings fail by name (and only they)", verdict == {"KF-UNMAPPED"})
    n_un = sum(1 for r, _ in judge(doc, audit, shas) if r == "KF-UNMAPPED")
    case("each unexcused unmapped finding is its own line", n_un == 2)
    clean = dict(doc, unmapped=[u for u in doc["unmapped"] if u["excused"]])
    clean_audit = copy.deepcopy(audit)
    clean_audit["check-contract-shapes"]["rules"]["C-ENUM"].remove("orders.Nothing.kind")
    del clean_audit["check-new-guard"]
    case("a complete, current index passes", judge(clean, clean_audit, shas, b.dump(clean), b.dump(clean)) == [])
    case("an index that is not the builder's output is STALE",
         [r for r, _ in judge(clean, clean_audit, shas, b.dump(doc), b.dump(clean))] == ["KF-STALE"])
    case("a moved baseline is KF-SOURCE",
         [r for r, _ in judge(clean, clean_audit, dict(shas, **{"handoff/audit-baseline.json": "0" * 64}))] == ["KF-SOURCE"])
    more = copy.deepcopy(clean_audit)
    more["check-screen-wiring"]["rules"]["S-X"].append("POS-002:createOrder")
    case("a baselined finding the index lacks is KF-COVERAGE",
         [r for r, _ in judge(clean, more, shas)] == ["KF-COVERAGE"])
    case("a missing index is KF-STALE", [r for r, _ in judge(None, clean_audit, shas)] == ["KF-STALE"])
    print(f"check-known-findings self-test: {21 - len(fails)} of 21 passed")
    for f in fails:
        print(f"  FAIL self-test: {f}")
    return fails


def main() -> int:
    g.force_utf8()
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--self-test", action="store_true", help="the self-test alone")
    ap.add_argument("--quick", action="store_true", help="skip the regeneration (KF-STALE is not judged)")
    a = ap.parse_args()
    fails = self_test()
    if a.self_test or fails:
        print(f"{'FAIL' if fails else 'PASS'} - check-known-findings self-test")
        return 1 if fails else 0
    text = INDEX.read_text(encoding="utf-8") if INDEX.exists() else None
    index = json.loads(text) if text else None
    audit = g.load_json(SOURCES["handoff/audit-baseline.json"], {}) or {}
    b = builder()
    shas = {rel: b.sha(path) for rel, path in SOURCES.items()}
    fresh = None if a.quick or index is None else b.dump(b.build())
    found = judge(index, audit, shas, fresh, text)
    c = (index or {}).get("counts") or {}
    excused = [u for u in (index or {}).get("unmapped") or [] if u.get("excused")]
    for rule, msg in found:
        print(f"  FAIL {rule:<12} {msg}")
    for u in excused:
        print(f"  listed {u['check']} {u['rule']} {u['key']}: names no artefact ({u.get('why')})")
    if found:
        print(f"FAIL - {len(found)} finding(s) on handoff/known-findings.json")
        return 1
    print(f"PASS - handoff/known-findings.json {'current and ' if fresh is not None else ''}complete: "
          f"{c.get('findings', 0)} known finding(s) by artefact, {len(excused)} listed as naming no artefact")
    return 0


if __name__ == "__main__":
    sys.exit(main())
