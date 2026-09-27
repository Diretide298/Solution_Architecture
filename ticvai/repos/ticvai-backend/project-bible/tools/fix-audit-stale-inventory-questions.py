#!/usr/bin/env python3
"""Delete the pre-contract `openQuestions` residue from the screen records (audit root R266).

**41 `P02` screens still ask a question the contracts answered.** Each reads *"Inventory cites
`GET /wallet` -- no matching operation. Written before the contracts existed."* The page inventory
invented those paths before there were contracts; 40 of the 41 screens now declare the real
operations (`GST-011` `getWallet`, `GST-022` `getWaitTimes` on `/queues/wait-times`, ...) and
`GST-043` declares none and cites nothing. `tools/retire-answered-questions.py` names them as
residue, but it is excluded from refresh and was never applied, so every reader took them as live.

This does only that one thing: it removes each list item carrying the stale sentence, item by item,
and drops an `openQuestions:` header left with no items. Every other question -- open or answered
-- is left exactly where it is; moving answers to `resolvedQuestions` stays the retire tool's job.

Idempotent: a second run finds nothing. Dry run by default; `--apply` writes.

Run: python3 tools/fix-audit-stale-inventory-questions.py [--apply]
"""
import importlib.util
import sys
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("retire", HERE / "retire-answered-questions.py")
retire = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(retire)

SCREENS = retire.SCREENS
STALE = retire.STALE


def is_stale(text):
    # The sentence is folded across lines in 9 of the 41 items; compare on normalised whitespace.
    return STALE in " ".join(str(text).split())


def main():
    apply = "--apply" in sys.argv
    total = 0
    for f in sorted(SCREENS.glob("P*.yaml")):
        before = f.read_text(encoding="utf-8")
        lines = before.split("\n")
        out, i, gone = [], 0, []
        while i < len(lines):
            if lines[i] == "  openQuestions:":
                blk, nxt = retire.block_lines(lines, i)
                keep = []
                for chunk in retire.split_items(blk[1:]):
                    text = retire.item_text(chunk)
                    if is_stale(text):
                        gone.append(" ".join(text.split()))
                    else:
                        keep.extend(chunk)
                if keep:
                    out.append(lines[i])
                    out.extend(keep)
                i = nxt
                continue
            out.append(lines[i])
            i += 1
        if not gone:
            continue
        after = "\n".join(out)

        # Structural check: only stale openQuestions items differ, nothing else on any screen.
        a, b = yaml.safe_load(before), yaml.safe_load(after)
        assert len(a["screens"]) == len(b["screens"]), f"{f.name}: screen count changed"
        for sa, sb in zip(a["screens"], b["screens"]):
            assert sa["id"] == sb["id"], f"{f.name}: order changed at {sa['id']}"
            ka = {k: v for k, v in sa.items() if k != "openQuestions"}
            kb = {k: v for k, v in sb.items() if k != "openQuestions"}
            assert ka == kb, f"{f.name}: {sa['id']} changed outside openQuestions"
            want = [q for q in (sa.get("openQuestions") or []) if not is_stale(q)]
            assert (sb.get("openQuestions") or []) == want, f"{f.name}: {sa['id']} lost a live question"
            if not want:
                assert "openQuestions" not in sb, f"{f.name}: {sa['id']} left an empty openQuestions"

        for s in a["screens"]:
            for q in s.get("openQuestions") or []:
                if is_stale(q):
                    print("  %-10s %s" % (s["id"], " ".join(str(q).split())[:100]))
        total += len(gone)
        if apply:
            f.write_text(after, encoding="utf-8")
        print("  %-38s %d stale question(s) %s\n" % (f.name, len(gone), "deleted" if apply else "would be deleted"))

    print("  total stale questions: %d" % total)
    if not apply:
        print("  dry run - pass --apply to write")
    return 0


if __name__ == "__main__":
    sys.exit(main())
