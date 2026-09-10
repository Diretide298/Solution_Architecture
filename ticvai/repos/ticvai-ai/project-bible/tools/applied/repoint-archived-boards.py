#!/usr/bin/env python3
"""Repoint the screens whose drawn frame was archived, and keep the fact that it existed.

**133 screens pointed `wireframe.board` at a Claude Design board that is no longer in the package.**
They were archived on 9 September to `_dump/wireframes-3-september/` because Claude Design will
redraw them, and a pointer to a file nobody ships is a broken link however good the reason.

**Every one of these screens already has a generated frame.** All 1,229 are on their platform
board — 69 of the 133 even name it in `generatedFallback`, which exists for exactly this case:
*"the generated frame kept alongside a drawn one, so a board that stops opening does not take the
screen's only frame with it."* This promotes that fallback to `board` and computes it for the 64
that never had one.

**What is deliberately not thrown away.** `provenance` becomes `generated`, because that is what
the frame it now points at actually is — but the note records which board drew it and where that
board went. **A screen that was designed and a screen that never was are different facts**, and
the redraw needs to know which is which.

Idempotent. Run with no arguments to preview; `--apply` to write.
"""

from __future__ import annotations
import glob
import pathlib
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[2]
ARCHIVE = "_dump/wireframes-3-september/"


def main() -> int:
    apply = "--apply" in sys.argv
    docs = {f: yaml.safe_load(open(f, encoding="utf-8"))
            for f in sorted(glob.glob(str(ROOT / "screens" / "P*.yaml")))}

    # Every board file the package still ships, so "missing" means missing rather than misspelt.
    live = {p.name for p in (ROOT / "wireframes").glob("*.html")}
    plat_board = {}
    for d in docs.values():
        for s in d["screens"]:
            fb = (s.get("wireframe") or {}).get("generatedFallback") or ""
            if fb:
                plat_board[d["platform"]["code"]] = fb.split("#")[0]

    moved, no_target = [], []
    for d in docs.values():
        code = d["platform"]["code"]
        for s in d["screens"]:
            w = s.get("wireframe") or {}
            board = w.get("board") or ""
            name = pathlib.Path(board.split("#")[0]).name
            if not name or name in live:
                continue

            target = w.get("generatedFallback")
            if not target:
                pb = plat_board.get(code)
                if not pb:
                    no_target.append(s["id"])
                    continue
                target = f"{pb}#{s['id'].lower()}"

            moved.append((s["id"], name))
            if apply:
                w["board"] = target
                w["provenance"] = "generated"
                w.pop("generatedFallback", None)
                w["note"] = (
                    f"**Drawn by Claude Design on `{name}`, archived 9 September 2026 to "
                    f"`{ARCHIVE}`.** The frame it points at now is the generated one. This screen "
                    f"has been designed once and is not starting from nothing.")

    if not moved and not no_target:
        print("nothing to do — every wireframe.board resolves to a board in the package")
        return 0

    print(f"{len(moved)} screen(s) point at an archived board")
    for sid, name in moved[:8]:
        print(f"  {sid:<10} {name}")
    if len(moved) > 8:
        print(f"  … and {len(moved) - 8} more")
    if no_target:
        print(f"\n{len(no_target)} screen(s) have no platform board to fall back to: "
              f"{', '.join(no_target[:6])}")

    if apply:
        for f, d in docs.items():
            pathlib.Path(f).write_text(
                yaml.safe_dump(d, sort_keys=False, allow_unicode=True, width=100),
                encoding="utf-8")
        print(f"\nwritten to {len(docs)} platform file(s)")
    else:
        print("\nrun with --apply to write")
    return 0


if __name__ == "__main__":
    sys.exit(main())
