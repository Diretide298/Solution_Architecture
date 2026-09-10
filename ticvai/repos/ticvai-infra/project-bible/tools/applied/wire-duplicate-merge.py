#!/usr/bin/env python3
"""Wire the duplicate-match and merge process onto the two screens that were drawn for it.

**The process is fully decided, drawn on a client board, written into the contracts, and reachable
from no screen.** `matchGuest` and `mergeGuests` are declared by nothing in `screens/`, so a
designer reading the package cannot know the flow exists and a build would ship without it.

## What was already decided, and where

`marketing-crm.matchGuest` -- *"Is this the same person we already have?"*, cites **Board 4E**:

  *"A restaurant creates a duplicate guest every time somebody books by phone with a different
  number, and a CRM that cannot recognise them reports two visits as two guests forever."*

  **Returns candidates and a score. Never merges.** *"An automatic merge on a name and a birthday
  joins two families, and the join is far harder to undo than to make."*

  **Scores are explained.** *"Same mobile* and *similar name, same postcode* are different levels
  of certainty, and a host deciding at a podium needs to see which."*

`marketing-crm.mergeGuests` -- *"Two records, one person"*, cites **Board 4G**:

  **Always a person's decision**, acting on what `matchGuest` proposed. **The losing record is
  superseded, not deleted** -- orders, entitlements and consents already point at it.
  **Reversible for thirty days.** **Consent takes the narrower of the two**, because inheriting
  the more permissive consent is how a merge becomes a regulatory finding.

**Board 4E and 4G are `FnB Board 4`, not Marketing Board 4.** The Marketing frames at those
letters are *Multichannel Composer* and *Campaign Approval Workflow*; the FnB ones are
`fnb-4e` *Create / Edit Reservation* and `fnb-4g` *Guest Profile & Dining History*, which are the
screens the descriptions describe. Those two screens already declare `FnB Board 4` frames --
**the drawing and the contract agreed all along and the screen sat between them declaring
neither.**

Run: python3 tools/wire-duplicate-merge.py [--apply]
"""
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
P06 = ROOT / "screens" / "P06-staff-app.yaml"

# The operation lines to insert, and the component to add to `contentBody`. Indentation matches
# the file: screens are top-level list items, so their keys sit at two spaces.
ADD = {
    "EMP-055": {
        "apis": """  - operationId: matchGuest
    contract: marketing-crm
    purpose: Propose existing guests who may be the same person, before a second record is created
    trigger: onAction
""",
        "component": """      - kind: duplicateMatch
        label: Possible existing guest
        notes: >
          **Runs while the booking is being typed, not after it is saved.** A duplicate created at
          the podium is one somebody has to find later. Proposes only — `matchGuest` never merges,
          and the reason each candidate matched is shown beside it.
""",
    },
    "EMP-057": {
        "apis": """  - operationId: matchGuest
    contract: marketing-crm
    purpose: Find other records that may be this same person
    trigger: onAction
  - operationId: mergeGuests
    contract: marketing-crm
    purpose: Merge a proposed duplicate into this profile, once a person has decided
    trigger: onAction
""",
        "component": """      - kind: duplicateMatch
        label: Possible duplicates of this guest
        permission: GUEST_MANAGE
        notes: Candidates from `matchGuest`, each with the rule that matched it.
      - kind: confirmDialog
        label: Merge these two records
        permission: GUEST_MANAGE
        notes: >
          **The consequence, stated before the act.** The losing record is superseded rather than
          deleted so a year of orders and consents keeps resolving; the merge is reversible for
          thirty days; and **consent takes the narrower of the two positions**, which is the one
          thing about a merge that is a regulatory question rather than a data one.
""",
    },
}


def splice(text: str) -> str:
    """Insert the operations and components without disturbing anything else.

    Line-based rather than a YAML round-trip: dumping the document would reflow 66 screens of
    carefully written prose to change two of them.
    """
    # **Nothing here checked whether it had already run.** `splice` appended unconditionally,
    # so a second `--apply` added a second copy of every operation and component. Found on
    # 10 September with exactly one run on disk — one run short of a screen declaring
    # `duplicateMatch` six times. Same fault as `derive-transitions-from-flows --adopt`,
    # found the same day: **a tool that writes must be able to see what it wrote last time.**
    lines = text.split("\n")
    out, current, i = [], None, 0
    while i < len(lines):
        ln = lines[i]
        if ln.startswith("- id: "):
            current = ln[len("- id: "):].strip()
        # `apis:` is the screen's own key at two spaces; append after its last entry.
        if current in ADD and ln == "  apis:":
            out.append(ln)
            i += 1
            while i < len(lines) and (lines[i].startswith("  - ") or lines[i].startswith("    ")):
                out.append(lines[i])
                i += 1
            block = ADD[current]["apis"].rstrip("\n").split("\n")
            if not any(b.strip() in text for b in block
                       if b.strip().startswith("- operationId:")):
                out.extend(block)
            continue
        # The one region on these screens; append the component after the last existing one.
        if current in ADD and ln == "      components:":
            out.append(ln)
            i += 1
            while i < len(lines) and (lines[i].startswith("      - ") or lines[i].startswith("        ")):
                out.append(lines[i])
                i += 1
            block = ADD[current]["component"].rstrip("\n").split("\n")
            first = block[0].strip()
            if first and text.count(first) < 2:
                out.extend(block)
            continue
        out.append(ln)
        i += 1
    return "\n".join(out)


def main() -> int:
    apply = "--apply" in sys.argv
    before = P06.read_text(encoding="utf-8")
    after = splice(before)
    if after == before:
        print("  nothing to do")
        return 0

    a, b = yaml.safe_load(before), yaml.safe_load(after)
    assert len(a["screens"]) == len(b["screens"]), "screen count changed"
    for sa, sb in zip(a["screens"], b["screens"]):
        assert sa["id"] == sb["id"], "order changed at %s" % sa["id"]
        if sa["id"] not in ADD:
            assert sa == sb, "%s changed and should not have" % sa["id"]
            continue
        # **Only two things may move**, and everything else on the screen must be identical.
        ka = {k: v for k, v in sa.items() if k not in ("apis", "layout")}
        kb = {k: v for k, v in sb.items() if k not in ("apis", "layout")}
        assert ka == kb, "%s changed outside apis/layout" % sa["id"]
        old_ops = [x["operationId"] for x in sa.get("apis") or []]
        new_ops = [x["operationId"] for x in sb.get("apis") or []]
        assert new_ops[:len(old_ops)] == old_ops, "%s lost an operation" % sa["id"]
        print("  %-9s + %s" % (sa["id"], ", ".join(new_ops[len(old_ops):])))
        for ra, rb in zip(sa["layout"]["regions"], sb["layout"]["regions"]):
            ca = [c["kind"] for c in ra.get("components") or []]
            cb = [c["kind"] for c in rb.get("components") or []]
            assert cb[:len(ca)] == ca, "%s lost a component" % sa["id"]
            if len(cb) > len(ca):
                print("  %-9s + %s" % ("", ", ".join(cb[len(ca):])))

    if apply:
        P06.write_text(after, encoding="utf-8")
        print("\n  written")
    else:
        print("\n  dry run — pass --apply to write")
    return 0


if __name__ == "__main__":
    sys.exit(main())
