#!/usr/bin/env python3
"""Mark the Block A and B design-note corrections of the moved workshop-pack screens (2 October 2026).

The companion of move-adm049-2-october.py. Every open correction (no `status`) on a moved screen in Block A or
B gets `status` and `by` (handoff/design-notes/README.md):

  fixed      the move, the merge or a screen edit changed the screen (CHG-MOV-001 .. -007)
  withdrawn  the screen is a full-merge anchor: it is not built, so what its layout got wrong is moot (CHG-MOV-002)
  logged     the fix needs a contract change, an operation that does not exist, a plan decision or a component
             kind the library lacks: an open entry lists it (CHG-MOV-008, CHG-MOV-009)

Blocks C and D stay open (they are fixed before their own sprints). The edit is textual, two lines appended to
each correction, so the hand-written notes keep their layout.

    python3 tools/applied/move-adm049-design-notes-2-october.py [--apply]
"""
import argparse
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
NOTES = ROOT / "handoff" / "design-notes"

FULL = {"ADM-097", "ADM-242", "ADM-249", "ADM-252", "ADM-611"}
SECTION_READ = {"ADM-119", "ADM-121"}   # a section of a venue screen that reads the record
KEEP = {"ADM-068", "ADM-619"}


def in_range(sid: str) -> bool:
    m = re.fullmatch(r"ADM-(\d+)", sid or "")
    return bool(m) and (48 <= int(m.group(1)) <= 317 or 559 <= int(m.group(1)) <= 698)


def dispose(sid: str, what: str):
    """(status, CHG id) for one open correction, or None when this run does not decide it."""
    w = what.strip()
    if sid in FULL:
        return "withdrawn", "CHG-MOV-002"
    if w.startswith("Calls tenant-permission operations with no tenant picker"):
        return "fixed", "CHG-MOV-001"
    if w.startswith("requiresModule is 'marketing' on a TICVAI Console screen"):
        return "fixed", "CHG-MOV-001"
    if w.startswith("emptyFirstRun says it 'carries the create action'"):
        return "fixed", "CHG-MOV-003"
    if w.startswith("Name ends with a tab") or w.startswith("The screen name ends in an escaped tab"):
        return "fixed", "CHG-MOV-004"
    if sid == "ADM-048" and "PLATFORM_TENANT_VIEW" in w:
        return "fixed", "CHG-MOV-007"
    if sid == "ADM-145" and w.startswith('"Delegate" is a decision button'):
        return "fixed", "CHG-MOV-005"
    if sid == "ADM-157" and w.startswith("The purpose text is shared"):
        return "fixed", "CHG-MOV-005"
    if sid == "ADM-241" and w.startswith("No canvas component"):
        return "logged", "CHG-MOV-009"
    if sid == "ADM-241" and w.startswith("Fields drawn as drop-downs"):
        return "fixed", "CHG-MOV-005"
    if (sid, w[:12]) in {("ADM-245", "Action types"), ("ADM-251", "Error types "), ("ADM-257", "The table ha")}:
        return "fixed", "CHG-MOV-005"
    if sid == "ADM-247" and w.startswith("Reaches approveVersioningGovernance (step-up"):
        return "fixed", "CHG-MOV-006"
    if sid == "ADM-141" and w.startswith("No write operation"):
        return "fixed", "CHG-MOV-002"
    if sid in SECTION_READ and w.startswith("No read operation"):
        return "fixed", "CHG-MOV-002"
    # the rest need the contract, an operation that does not exist, or a plan decision
    if (w.startswith("Pack actions with no operation") or w.startswith("List operation(s)")
            or w.startswith("No read operation") or w.startswith("No write operation")):
        return "logged", "CHG-MOV-008"
    return "logged", "CHG-MOV-008"


def blocks(lines):
    """screen id -> (start, end) line range of its entry under `screens:`."""
    out, cur, start = {}, None, None
    for i, ln in enumerate(lines):
        m = re.match(r"^  ([A-Z]{2,4}-\d+):\s*$", ln)
        if m or (cur and re.match(r"^\S", ln)):
            if cur:
                out[cur] = (start, i)
            cur, start = (m.group(1), i) if m else (None, None)
    if cur:
        out[cur] = (start, len(lines))
    return out


def correction_items(lines, a, b):
    """[(start, end)] of each item under `    corrections:` within lines[a:b]."""
    idx = next((k for k in range(a, b) if lines[k] == "    corrections:"), None)
    if idx is None:
        return []
    items, k = [], idx + 1
    while k < b:
        ln = lines[k]
        if ln.startswith("    - "):
            items.append([k, None])
        elif ln.strip() and not ln.startswith("      "):
            break
        k += 1
    for n, it in enumerate(items):
        it[1] = items[n + 1][0] if n + 1 < len(items) else k
        while it[1] > it[0] + 1 and not lines[it[1] - 1].strip():
            it[1] -= 1
    return [tuple(x) for x in items]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()
    tally = {}
    for f in sorted(NOTES.glob("*.yaml")):
        raw = f.read_bytes().decode("utf-8")
        crlf = "\r\n" in raw
        text = raw.replace("\r\n", "\n")
        doc = yaml.load(text, Loader=getattr(yaml, "CSafeLoader", yaml.SafeLoader)) or {}
        screens = doc.get("screens") or {}
        lines = text.split("\n")
        rng = blocks(lines)
        inserts = []   # (line index, [new lines]) applied bottom-up
        for sid, v in screens.items():
            if not in_range(sid) or sid in KEEP or v.get("block") not in ("A", "B"):
                continue
            cs = v.get("corrections") or []
            items = correction_items(lines, *rng[sid])
            if len(items) != len(cs):
                print(f"  ! {f.name} {sid}: {len(cs)} corrections parsed, {len(items)} found in the text")
                continue
            for (s0, e0), c in zip(items, cs):
                if sid == "ADM-603" and c.get("by") == "CHG-WIR-027" and c.get("status") == "logged":
                    for k in range(s0, e0):
                        if lines[k] == "      status: logged":
                            lines[k] = "      status: fixed"
                        if lines[k] == "      by: CHG-WIR-027":
                            lines[k] = "      by: CHG-MOV-007"
                    tally[("fixed", "CHG-MOV-007")] = tally.get(("fixed", "CHG-MOV-007"), 0) + 1
                    continue
                if c.get("status"):
                    continue
                st, by = dispose(sid, str(c.get("what") or ""))
                tally[(st, by)] = tally.get((st, by), 0) + 1
                inserts.append((e0, [f"      status: {st}", f"      by: {by}"]))
        for at, new in sorted(inserts, reverse=True):
            lines[at:at] = new
        body = "\n".join(lines)
        if body != text:
            chk = yaml.load(body, Loader=getattr(yaml, "CSafeLoader", yaml.SafeLoader))
            assert set(chk["screens"]) == set(screens), f.name
            print(f"  {f.name}: {len(inserts)} correction(s) marked")
            if a.apply:
                f.write_bytes((body.replace("\n", "\r\n") if crlf else body).encode("utf-8"))
    for (st, by), n in sorted(tally.items()):
        print(f"  {st:9} {by}  {n}")
    print("applied" if a.apply else "dry run: --apply writes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
