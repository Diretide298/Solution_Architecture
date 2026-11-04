#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The baselines only shrink between releases, unless the lead approves the growth by name (r14, CHG-R14I-001).

**Why.** The r13 system review (finding E-04, 3 November 2026) measured handoff/audit-baseline.json, the known
members of every audit class, at each release tag: 5,592 known findings at r6, 5,961 at r13. A guard fails only on
a finding the baseline does not list, and `--update-baseline` lists today's findings, new ones included: one
command cleared a new member of a class, and check-request-fields-stored arrived at r8 with 364 findings
baselined instead of blocking, against the lead's rule of 25 October ("a new check blocks in the release it
arrives"). Nothing compared the file with the last tag. tools/refresh-safe-baseline.json, the release gate's
allowlist, had no dates at all (E-02).

**What fails here:**

    BR-GROWTH     a guard's known set at HEAD holds a key it did not hold at the last release tag (r*), and no
                  change entry approves it: an entry's `baseline_growth` names the guard and the key (or
                  `RULE|*` for a rule), with `approved_by` the lead. A guard that is new since the tag counts
                  in full (it blocks in the release it arrives).
    BR-APPROVAL   a `baseline_growth` approval that names no guard, no keys, or no approver.
    BR-ALLOWLIST  an entry of tools/refresh-safe-baseline.json that is undated, unapproved, past its expiry,
                  more than 14 days long (CLAUDE.md rule 15), or a count pin (tools/gate_allowlist.py rules 1-2).
    BR-TAG        no r* tag in a package that has been released (release_baseline.released()): the comparison
                  would silently be skipped, so it fails instead (review E-05).

A change entry approves growth like this (changes/entries/CHG-XXX-nnn-*.yaml):

    baseline_growth:
      approved_by: Chinmay
      guards:
        check-request-fields-stored: ["RF-NOT-STORED|tenancy#setVenueHours.foo", "RF-READONLY|*"]

The 5,961 entries already known at r13 carry no expiry: they are the tracked debt of each class, and a known
finding a started ticket builds on already fails (CHG-CRF-001). Whether they should expire is the lead's call
(r14 lane i report).

    python3 tools/check-baseline-ratchet.py              # against the latest r* tag
    python3 tools/check-baseline-ratchet.py --tag r12    # against another tag
"""
import glob
import json
import os
import re
import subprocess
import sys

import yaml

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import gate_allowlist  # noqa: E402
from release_baseline import released  # noqa: E402

AUDIT = "handoff/audit-baseline.json"


def git(*args):
    p = subprocess.run(["git", *args], cwd=ROOT, capture_output=True)
    return p.returncode, p.stdout.decode("utf-8", "replace")


def latest_tag():
    rc, out = git("tag", "--merged", "HEAD", "-l", "r*")
    tags = [t for t in out.split() if re.fullmatch(r"r\d+", t)]
    return max(tags, key=lambda t: int(t[1:])) if tags else None


def at_tag(tag, path):
    rc, prefix = git("rev-parse", "--show-prefix")
    rc, out = git("show", "%s:%s%s" % (tag, prefix.strip(), path))
    return json.loads(out) if rc == 0 and out.strip() else {}


def keys(doc):
    """guard -> {"RULE|key"} for an audit-baseline document."""
    return {g: {"%s|%s" % (r, k) for r, ks in ((v or {}).get("rules") or {}).items() for k in ks or ()}
            for g, v in (doc or {}).items() if g != "_about" and isinstance(v, dict)}


def approvals(entries_dir=None):
    """(guard -> [(pattern, change id)], problems) from every change entry's baseline_growth."""
    out, bad = {}, []
    for f in sorted(glob.glob(os.path.join(entries_dir or os.path.join(ROOT, "changes", "entries"), "*.yaml"))):
        try:
            doc = yaml.safe_load(open(f, encoding="utf-8")) or {}
        except Exception as e:  # noqa: BLE001
            bad.append(("BR-APPROVAL", os.path.basename(f), "does not parse: %s" % e))
            continue
        g = doc.get("baseline_growth")
        if g is None:
            continue
        cid = doc.get("id") or os.path.basename(f)
        if not isinstance(g, dict) or not str(g.get("approved_by") or "").strip():
            bad.append(("BR-APPROVAL", cid, "baseline_growth needs approved_by (the lead)"))
            continue
        guards = g.get("guards")
        if not isinstance(guards, dict) or not guards or not all(isinstance(v, list) and v for v in guards.values()):
            bad.append(("BR-APPROVAL", cid, "baseline_growth.guards must map each guard to the keys it approves"))
            continue
        for guard, ks in guards.items():
            out.setdefault(guard, []).extend((str(k), cid) for k in ks)
    return out, bad


def approved(guard, key, appr):
    for pat, cid in appr.get(guard, []):
        if pat == key or (pat.endswith("|*") and key.startswith(pat[:-1])):
            return cid
    return None


def growth(old, new, appr):
    """[(rule, where, detail)] for every key gained since the tag and not approved."""
    out = []
    a, b = keys(old), keys(new)
    for g in sorted(b):
        gained = sorted(b[g] - a.get(g, set()))
        unapproved = [k for k in gained if not approved(g, k, appr)]
        for k in unapproved[:20]:
            out.append(("BR-GROWTH", g, "%s is known now and was not at the tag%s; fix it, or the lead approves it "
                                        "in a change entry's baseline_growth" % (k, "" if g in a else " (a guard new since the tag)")))
        if len(unapproved) > 20:
            out.append(("BR-GROWTH", g, "... and %d more unapproved key(s)" % (len(unapproved) - 20)))
    return out


def self_test():
    old = {"g": {"rules": {"R": ["a", "b"]}}}
    appr = {"g": [("R|c", "CHG-X-001")], "h": [("S|*", "CHG-X-002")]}
    cases = [
        (growth(old, {"g": {"rules": {"R": ["a"]}}}, {}) == [], "a shrinking baseline passes"),
        (len(growth(old, {"g": {"rules": {"R": ["a", "b", "z"]}}}, {})) == 1, "an unapproved key fails"),
        (growth(old, {"g": {"rules": {"R": ["a", "c"]}}}, appr) == [], "an approved key passes"),
        (len(growth(old, {"g": {"rules": {"R": ["a"]}}, "n": {"rules": {"S": ["x"]}}}, appr)) == 1,
         "a guard new since the tag counts in full"),
        (growth({}, {"h": {"rules": {"S": ["x", "y"]}}}, appr) == [], "a rule-wide approval"),
    ]
    return [what for ok, what in cases if not ok]


def main():
    args = sys.argv[1:]
    bad_tests = self_test()
    if bad_tests:
        for b in bad_tests:
            print("  FAIL self-test: %s" % b)
        print("FAIL - %d self-test(s)" % len(bad_tests))
        return 1
    found = []
    for c, why in gate_allowlist.all_problems(gate_allowlist.load()):
        found.append(("BR-ALLOWLIST", c, why))
    tag = args[args.index("--tag") + 1] if "--tag" in args else latest_tag()
    appr, abad = approvals()
    found += abad
    if not tag:
        why = released()
        if why:
            found.append(("BR-TAG", "-", "no r* release tag in this clone, but %s: fetch the tags "
                                         "(git fetch --tags origin)" % why))
        else:
            print("  note: no release yet; nothing to compare with")
    else:
        old = at_tag(tag, AUDIT)
        new = json.load(open(os.path.join(ROOT, AUDIT), encoding="utf-8"))
        if not old:
            found.append(("BR-TAG", tag, "%s has no %s to compare with" % (tag, AUDIT)))
        else:
            found += growth(old, new, appr)
            n_old, n_new = sum(map(len, keys(old).values())), sum(map(len, keys(new).values()))
            print("  %s: %d known finding(s) at %s, %d now" % (AUDIT, n_old, tag, n_new))
    for rule, where, detail in found:
        print("  FAIL %-12s %s: %s" % (rule, where, detail))
    if found:
        print("FAIL - %d finding(s)" % len(found))
        return 1
    print("PASS - no baseline grew since %s without the lead's approval; the gate's allowlist is dated and "
          "valid; %d self-test(s) pass" % (tag or "the first release", 5))
    return 0


if __name__ == "__main__":
    sys.exit(main())
