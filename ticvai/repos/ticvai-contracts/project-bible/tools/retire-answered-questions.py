#!/usr/bin/env python3
"""Separate answers from questions in `openQuestions`, and un-collide screen-level `provenance`.

**`openQuestions` reads as 74 open items and 24 of them are open.** The field accumulated three
different things and nothing separated them:

  **41 are pre-contract residue**, all `P02`, all the same sentence -- *"Inventory cites
  `GET /tickets` -- no matching operation. Written before the contracts existed."* The operation
  exists; it is not called `GET /tickets`. `GST-012` declares `listMyEntitlements`,
  `getEntitlement`, `transferOrderTickets` and three more. **The note records a path the page
  inventory invented before there were contracts** and was never retired when they arrived. 40 of
  the 41 screens declare operations; `GST-043 Arabic / RTL Experience` declares none and cites
  nothing, so its question is vacuously true rather than open.

  **9 are answers**, written into the question they answer on 8 September -- `BO-006` from the
  14 August minute, and eight `P11` screens from the 7 September workshop. They move to
  `resolvedQuestions`, because **a decision and its provenance are worth more than a deleted
  line**, and losing which minute settled a thing is how it gets asked again.

  **24 are open.** That is the number.

## The third `provenance` collision

`provenance` at screen level holds prose -- *"client board, specified"*, *"MoM 10 August 2026
§4.8"* -- on 128 screens, while `wireframe.provenance` is the enum `generated|designed`. **Same
word, two meanings, and 128 screens carry both.** This is the third instance of one word doing two
jobs, after `release` (a hold, and a publication) and `generatedPack` (the client drew it, against
`generated` meaning nobody did).

Renamed to `sourceNote`, which is what it is: the prose form of `source`, the structured pack
citation on 590 screens. **The two are disjoint** -- no screen carries both -- so they are one
concept written two ways, and the name should say so. Nothing reads the field.

Run: python3 tools/retire-answered-questions.py [--apply]
"""
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SCREENS = ROOT / "screens"

STALE = "Written before the contracts existed"
ANSWERED = re.compile(r"^(Answered|Unblocked|Resolved|Decided) by", re.M)


def block_lines(lines, i):
    """The lines belonging to the `openQuestions:` block that starts at `i`.

    A block is its own header plus every following list item and continuation. **Indentation is the
    only structure YAML gives here**, so the block ends at the next line indented two spaces that
    is not a list item -- which is the next sibling key."""
    out = [lines[i]]
    j = i + 1
    while j < len(lines):
        ln = lines[j]
        if ln.startswith("  - ") or ln.startswith("    ") or not ln.strip():
            out.append(ln)
            j += 1
            continue
        break
    while out and not out[-1].strip():
        out.pop()
    return out, i + len(out)


def main():
    apply = "--apply" in sys.argv
    tally = {"deleted": 0, "resolved": 0, "kept": 0, "renamed": 0}

    for f in sorted(SCREENS.glob("P*.yaml")):
        before = f.read_text(encoding="utf-8")
        lines = before.split("\n")
        out, i = [], 0
        while i < len(lines):
            ln = lines[i]
            if ln == "  openQuestions:":
                blk, nxt = block_lines(lines, i)
                # **The raw block is line-wrapped and the sentence is not.** YAML folds a long
                # scalar across lines, so `Written before the contracts existed` appears intact in
                # 32 items and split across a newline in 9 more. Matching the raw text found 32 of
                # 41 and would have left nine pieces of residue behind reporting success.
                body = " ".join(" ".join(blk[1:]).split())
                n = sum(1 for b in blk[1:] if b.startswith("  - "))
                if STALE in body:
                    tally["deleted"] += n
                elif ANSWERED.search(body.strip().lstrip("- ").lstrip("'")):
                    out.append("  resolvedQuestions:")
                    out.extend(blk[1:])
                    tally["resolved"] += 1
                else:
                    out.extend(blk)
                    tally["kept"] += n
                i = nxt
                continue
            if ln.startswith("  provenance: "):
                out.append("  sourceNote: " + ln[len("  provenance: "):])
                tally["renamed"] += 1
                i += 1
                continue
            out.append(ln)
            i += 1

        after = "\n".join(out)
        if after == before:
            continue

        # **The edit is text and the check is structural.** Re-parse both sides and assert that the
        # only differences are the three keys this tool is allowed to touch -- otherwise a stray
        # indent silently rewrites a neighbouring screen, which is exactly how
        # `P11-accreditation-portal.yaml` was broken once already.
        a, b = yaml.safe_load(before), yaml.safe_load(after)
        assert len(a["screens"]) == len(b["screens"]), f"{f.name}: screen count changed"
        touch = {"openQuestions", "resolvedQuestions", "provenance", "sourceNote"}
        for sa, sb in zip(a["screens"], b["screens"]):
            assert sa["id"] == sb["id"], f"{f.name}: order changed at {sa['id']}"
            ka = {k: v for k, v in sa.items() if k not in touch}
            kb = {k: v for k, v in sb.items() if k not in touch}
            assert ka == kb, f"{f.name}: {sa['id']} changed outside the permitted keys"
            assert sb.get("sourceNote") == sa.get("provenance"), f"{f.name}: {sa['id']} sourceNote"
            moved = sa.get("openQuestions") or []
            if sb.get("resolvedQuestions"):
                assert sb["resolvedQuestions"] == moved, f"{f.name}: {sa['id']} resolved text"

        if apply:
            f.write_text(after, encoding="utf-8")
        print("  %-38s %s" % (f.name, "written" if apply else "would change"))

    print("\n  stale questions deleted   : %d" % tally["deleted"])
    print("  screens moved to resolved : %d" % tally["resolved"])
    print("  questions left open       : %d" % tally["kept"])
    print("  provenance -> sourceNote  : %d" % tally["renamed"])
    if not apply:
        print("\n  dry run — pass --apply to write")
    return 0


if __name__ == "__main__":
    sys.exit(main())
