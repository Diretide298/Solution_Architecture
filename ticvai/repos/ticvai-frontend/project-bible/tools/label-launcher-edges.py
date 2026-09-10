#!/usr/bin/env python3
"""Label the edges leaving a platform's home screen, and stop there.

**A platform home screen is a launcher.** `BO-100 Venue Home`, `ADM-002 Platform Dashboard`,
`WEB-001` — their exits are tiles or rail entries, and the words on the control are the
destination's name. That is a claim about the control, not a guess about the journey, so it can
be written down.

**Where this deliberately stops.** 1,457 of the remaining bare edges are one half of a reciprocal
pair — `A → B` and `B → A` both declared. It is tempting to call one the drill-down and the other
"Back to A", and it would raise the coverage figure by half. **Nothing in the package says which
direction is which.** Guessing would put a plausible sentence where a fact should be, and a
labelled edge that is wrong is worse than a bare one: bare says *nobody has written this down*,
and wrong says *somebody did*.

The other 1,055 have no structural story at all. Both groups need a real source — a board, a
prototype, a workshop minute — and this tool leaves them alone.

Idempotent. Run with no arguments to preview; `--apply` to write.
"""

from __future__ import annotations
import glob
import pathlib
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent


def main() -> int:
    apply = "--apply" in sys.argv
    docs = {f: yaml.safe_load(open(f, encoding="utf-8"))
            for f in sorted(glob.glob(str(ROOT / "screens" / "P*.yaml")))}
    screens = {s["id"]: s for d in docs.values() for s in d["screens"]}

    written = 0
    for d in docs.values():
        code = d["platform"]["code"]
        for s in d["screens"]:
            nav = s.get("navigation") or {}
            if not nav.get("isEntryPoint"):
                continue
            done = {str(t.get("to", "")).partition("#")[0]
                    for t in (nav.get("transitions") or [])}
            for e in (nav.get("exitTo") or []):
                if e in done or e not in screens:
                    continue
                written += 1
                if apply:
                    nav.setdefault("transitions", []).append({
                        "to": e,
                        "trigger": screens[e]["name"],
                        "provenance": (f"structural — {s['id']} is {code}'s home screen and its "
                                       f"exits are its launcher"),
                    })

    if not written:
        print("nothing to do — every home-screen exit is already labelled")
        return 0
    print(f"{written} launcher edge(s) {'labelled' if apply else 'pending (run with --apply)'}")
    if apply:
        for f, d in docs.items():
            pathlib.Path(f).write_text(
                yaml.safe_dump(d, sort_keys=False, allow_unicode=True, width=100),
                encoding="utf-8")
        print(f"written to {len(docs)} platform file(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
