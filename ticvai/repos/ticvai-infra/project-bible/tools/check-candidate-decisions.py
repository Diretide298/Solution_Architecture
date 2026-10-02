#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A design import that differs from the spec is decided: every candidate frame's differences carry a decision.

**2 October 2026** (CHG-SEED-005). POS v2 arrived on 1 October as a design build
(`sources/designs/TICVAI_POS_Terminal_v2.html`), was imported as candidate frames on sixteen P04 screens
(`wireframe.candidate`, each with the `differences` between the build and the spec), and needed eight
decisions (POSV2-1..8, `docs/registers/pos-v2-decisions.md`) before Claude Design could use it. Chinmay:
*"there should be a prevention against a repeat"*: a design import that changes behaviour cannot sit on a
screen undecided, where a designer draws from it and a developer builds from the spec.

So every `wireframe.candidate` with `differences` must say how each was settled, in one of these ways:

  - **decided:** the differences (or a `decisions` list on the candidate) cite a decision: a design-return
    decision (`POSV2-n`, checked against `handoff/pos-v2-decisions.json`), an audit root (`R123`, checked
    against `docs/active/root-classes.md`) or a change (`CHG-XXX-nnn`, checked against `changes/entries/`);
  - **applied:** the candidate carries `applied: <CHG id or commit>`: the spec was changed to match the
    build, so nothing is left to decide;
  - **none:** `differences` is empty or says there are none.

    CD-UNDECIDED    a candidate whose differences carry no decision, no `applied` and are not empty
    CD-UNKNOWN-REF  a candidate citing a decision that does not exist

**Report-only until the five P04 candidates POS v2 left undecided (POS-000, -003, -004, -012, -023) are
decided**; the lead then records the baseline and makes it gate.

    python3 tools/check-candidate-decisions.py [--all] [--update-baseline]
"""
import json
import re
import sys

import audit_guard as g

ROOT = g.ROOT
RULES = {
    "CD-UNDECIDED": "a design candidate differs from the spec and carries no decision",
    "CD-UNKNOWN-REF": "a design candidate cites a decision that does not exist",
}
REF = re.compile(r"\b(POSV2-\d+|R\d{3}|CHG-[A-Z]{2,6}-\d{3})\b")
NONE = re.compile(r"^\s*(none|no differences?|identical|matches the spec)\b", re.I)


def known_refs() -> set:
    out = set()
    try:
        for d in json.loads((ROOT / "handoff" / "pos-v2-decisions.json").read_text(encoding="utf-8")):
            if d.get("ref"):
                out.add(d["ref"])
    except Exception:
        pass
    rc = ROOT / "docs" / "active" / "root-classes.md"
    if rc.exists():
        out |= set(re.findall(r"\bR\d{3}\b", rc.read_text(encoding="utf-8", errors="replace")))
    for p in (ROOT / "changes" / "entries").glob("CHG-*.yaml"):
        m = re.match(r"(CHG-[A-Z]{2,6}-\d{3})-", p.name)
        if m:
            out.add(m.group(1))
    return out


def main() -> int:
    g.force_utf8()
    guard = g.Guard("check-candidate-decisions", RULES)
    refs = known_refs()
    n = 0
    for _stem, s in g.screens():
        c = (s.get("wireframe") or {}).get("candidate")
        if not isinstance(c, dict):
            continue
        n += 1
        sid = s["id"]
        diff = str(c.get("differences") or "")
        cited = set(REF.findall(diff)) | {str(x) for x in (c.get("decisions") or [])}
        for r in sorted(cited - refs):
            guard.add("CD-UNKNOWN-REF", f"{sid}:{r}", f"{sid}: cites {r}, which is not a recorded decision")
        if cited or c.get("applied") or not diff.strip() or NONE.match(diff):
            continue
        guard.add("CD-UNDECIDED", sid, f"{sid} {s.get('name', '')[:40]}: candidate from {c.get('file')} "
                                       f"differs and carries no decision: {diff[:140]}")
    guard.note(f"{n} screen(s) carry a design candidate; {len(refs)} decision id(s) known")
    return guard.finish()


if __name__ == "__main__":
    sys.exit(main())
