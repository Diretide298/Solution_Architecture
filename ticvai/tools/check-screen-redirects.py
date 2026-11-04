#!/usr/bin/env python3
"""A screen merged into another says so in a field, and the field names a screen that is built.

**3 November 2026, the r13 system review F-14** (the lead, "All four, one release"; CHG-R14J-030). Nineteen
back-office screens were merged into another on 2 October (CHG-WIR-001, CHG-WIR-008, CHG-WIR-021, CHG-SBO-021,
CHG-MOV-002, CHG-CLN-003): "One implementation, both ids kept ... this id stays for traceability and routes to X, and
nothing on it is built separately". Only their notes said it, in prose ("**Merged into X**", which
tools/ticket_done.py read to hold their tasks), while each still carried a component path of its own, so the frontend
manifest gave a developer a component to build for a screen whose only job is a redirect, and BO-031 and BO-365 were
counted as the package's two unreachable screens. Each now carries `implementation.redirect: X` and no component
(screens/_schema.yaml), and ticket_done.merged_into reads the field first.

    SR-MERGED      a screen whose notes lead with "**Merged into X**" is neither `implementation.redirect: X` nor
                   `implementation.sectionOf: X` (a section renders inside X; a redirect only routes to it), or one
                   whose apisNote says it has no operations of its own because it was merged has no redirect
    SR-TARGET      a redirect names no screen, itself, a screen on another app, a screen that is itself a redirect,
                   or a section of another screen
    SR-COMPONENT   a redirect still names a component of its own (nothing is built for it), or has no route

    python tools/check-screen-redirects.py [--self-test]
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import audit_guard as g  # noqa: E402
from ticket_done import MERGED_NOTE  # noqa: E402

RULES = {
    "SR-MERGED": "a merged screen (notes '**Merged into X**', or apisNote 'merged into') with neither "
                 "implementation.redirect nor implementation.sectionOf naming X (review F-14, CHG-R14J-030)",
    "SR-TARGET": "a redirect to no screen, itself, another app's screen, a redirect or a section (CHG-R14J-030)",
    "SR-COMPONENT": "a redirect that still names a component, or has no route (CHG-R14J-030)",
}
APIS_MERGED = re.compile(r"No operations of its own.*?merged into ([A-Z]+-\d{3,4})\b", re.S)


def findings(screens: dict) -> list:
    """[(rule, screen id, message)] over {screen id: screen dict}."""
    out = []
    for sid, s in sorted(screens.items()):
        imp = s.get("implementation") or {}
        to, sec = imp.get("redirect"), imp.get("sectionOf")
        m = MERGED_NOTE.search(str(s.get("notes") or ""))
        a = APIS_MERGED.search(str(s.get("apisNote") or ""))
        said = (m.group(1) if m else None) or (a.group(1) if a else None)
        if said and to != said and sec != said:
            out.append(("SR-MERGED", sid, f"{sid} is merged into {said} (its notes or apisNote say so) and carries "
                                          f"neither implementation.redirect nor sectionOf {said}"))
        if a and not to:
            out.append(("SR-MERGED", sid, f"{sid}'s apisNote says it has no operations of its own because it was "
                                          f"merged into {a.group(1)}; a screen that only routes there is a redirect"))
        if not to:
            continue
        t = screens.get(to)
        timp = (t or {}).get("implementation") or {}
        if t is None:
            out.append(("SR-TARGET", sid, f"{sid} redirects to {to}, which is no screen"))
        elif to == sid:
            out.append(("SR-TARGET", sid, f"{sid} redirects to itself"))
        elif timp.get("app") != imp.get("app"):
            out.append(("SR-TARGET", sid, f"{sid} ({imp.get('app')}) redirects to {to} on another app "
                                          f"({timp.get('app')}); a route cannot cross apps"))
        elif timp.get("redirect") or timp.get("sectionOf"):
            out.append(("SR-TARGET", sid, f"{sid} redirects to {to}, which is itself a "
                                          f"{'redirect' if timp.get('redirect') else 'section'}: name the screen "
                                          "that is built"))
        if imp.get("component"):
            out.append(("SR-COMPONENT", sid, f"{sid} redirects to {to} and still names a component "
                                             f"({imp['component']}): nothing is built for a redirect"))
        if not imp.get("route"):
            out.append(("SR-COMPONENT", sid, f"{sid} redirects to {to} and has no route of its own to redirect"))
        if sec:
            out.append(("SR-TARGET", sid, f"{sid} is both a redirect to {to} and a section of {sec}"))
    return out


def self_test() -> int:
    host = {"id": "BO-102", "implementation": {"app": "a", "route": "/b2", "component": "src/B2.tsx"}}

    def red(**imp):
        return {"id": "BO-101", "notes": "**Merged into BO-102** (decided).",
                "implementation": dict({"app": "a", "route": "/b1"}, **imp)}

    cases = [
        ("a redirect to the built screen passes", {"BO-101": red(redirect="BO-102"), "BO-102": host}, []),
        ("a merged screen with no field fails", {"BO-101": red(component="src/B1.tsx"), "BO-102": host},
         ["SR-MERGED"]),
        ("a section of the host passes", {"BO-101": red(sectionOf="BO-102", component="src/B2.tsx"), "BO-102": host}, []),
        ("an apisNote merge without a redirect fails",
         {"BO-101": {"id": "BO-101", "apisNote": "No operations of its own since 2 October 2026: merged into BO-102, whose "
                                             "operations it routes to.",
                   "implementation": {"app": "a", "route": "/b1", "sectionOf": "BO-102"}}, "BO-102": host},
         ["SR-MERGED"]),
        ("a redirect to nothing fails", {"BO-101": red(redirect="BO-109"), "BO-102": host}, ["SR-MERGED", "SR-TARGET"]),
        ("a redirect still naming a component fails",
         {"BO-101": red(redirect="BO-102", component="src/B1.tsx"), "BO-102": host}, ["SR-COMPONENT"]),
        ("a redirect across apps fails",
         {"BO-101": red(redirect="BO-102"), "BO-102": dict(host, implementation={"app": "z", "route": "/b2"})},
         ["SR-TARGET"]),
        ("a redirect to a redirect fails",
         {"BO-101": red(redirect="BO-102"), "BO-102": dict(host, implementation={"app": "a", "route": "/b2",
                                                                            "redirect": "BO-103"}),
          "BO-103": dict(host, id="BO-103")}, ["SR-TARGET"]),
        ("an unmerged screen is left alone", {"BO-102": host}, []),
    ]
    fails = []
    for name, scr, want in cases:
        got = sorted(r for r, _, _ in findings(scr))
        if got != sorted(want):
            fails.append(f"{name}: got {got}, expected {sorted(want)}")
    for f in fails:
        print("  FAIL", f)
    print(f"check-screen-redirects self-test: {len(cases) - len(fails)} of {len(cases)} passed")
    return 1 if fails else 0


def main() -> int:
    g.force_utf8()
    if "--self-test" in sys.argv[1:]:
        return self_test()
    if self_test():
        return 1
    guard = g.Guard("check-screen-redirects", RULES)
    screens = {s["id"]: s for _, s in g.screens()}
    for rule, sid, msg in findings(screens):
        guard.add(rule, sid, msg)
    n = sum(1 for s in screens.values() if (s.get("implementation") or {}).get("redirect"))
    guard.note(f"{len(screens)} screens, {n} redirect(s)")
    return guard.finish()


if __name__ == "__main__":
    sys.exit(main())
