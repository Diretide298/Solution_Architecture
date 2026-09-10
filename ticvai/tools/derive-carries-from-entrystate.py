#!/usr/bin/env python3
"""Derive `transitions[].carries` from what the destination says it needs.

**`carries` is the field the whole transitions exercise exists for** — the state that travels with
a move, the thing a frontend developer cannot guess and otherwise finds by reading somebody's
JavaScript. It looked unobtainable: the flows do not record it, the boards do not, and inventing
it would be worse than leaving it blank.

**It was already written down, on the other end of the edge.** 420 screens declare
`entryState.params` with `from: navigation` — `WEB-004 Attraction Details` needs `eventId` and
`productId`; `POS-005 Payment` needs an order. That is not a guess about the journey, it is the
destination stating its own precondition, and **any edge arriving there must carry it or the
screen renders empty and blames the network.** 1,276 bare edges point at such a destination.

**What this does not claim.** The `trigger` written here is the destination's name, because that
is what a control leading to it reads on a rail or a row — the same convention the launcher and
board-hub labels use. It is not a claim to know the button. Where a screen already has a
transition for that edge from a flow, a board or a person, it is left alone: this only fills
blanks, and `provenance` leads with `derived ` so no reader mistakes it for an observation.

**The asymmetry worth knowing:** `carries` here is a *requirement*, not an observation. It says
what the destination cannot open without. If a real source later says the edge carries more, that
source is right and this is incomplete — never the other way round.

Idempotent. Run with no arguments to preview; `--apply` to write.
"""

from __future__ import annotations
import glob
import pathlib
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent


def params_of(screen: dict) -> list[str]:
    out = []
    for p in ((screen.get("entryState") or {}).get("params") or []):
        name = p.get("name") if isinstance(p, dict) else str(p)
        if name:
            out.append(name)
    return sorted(set(out))


def main() -> int:
    apply = "--apply" in sys.argv
    docs = {f: yaml.safe_load(open(f, encoding="utf-8"))
            for f in sorted(glob.glob(str(ROOT / "screens" / "P*.yaml")))}
    screens = {s["id"]: s for d in docs.values() for s in d["screens"]}

    written = 0
    touched = set()
    for d in docs.values():
        for s in d["screens"]:
            nav = s.get("navigation") or {}
            done = {str(t.get("to", "")).partition("#")[0]
                    for t in (nav.get("transitions") or [])}
            for e in (nav.get("exitTo") or []):
                if e in done or e not in screens:
                    continue
                needs = params_of(screens[e])
                if not needs:
                    continue
                written += 1
                touched.add(s["id"])
                if apply:
                    nav.setdefault("transitions", []).append({
                        "to": e,
                        "trigger": screens[e]["name"],
                        "carries": needs,
                        "provenance": (f"derived — {e} declares entryState.params "
                                       f"{', '.join(needs)}, so an edge into it must carry them"),
                    })

    if not written:
        print("nothing to do — every edge into a screen with entryState.params is labelled")
        return 0

    print(f"{written} edge(s) across {len(touched)} screen(s) "
          f"{'labelled with carries' if apply else 'pending (run with --apply)'}")
    if apply:
        for f, d in docs.items():
            pathlib.Path(f).write_text(
                yaml.safe_dump(d, sort_keys=False, allow_unicode=True, width=100),
                encoding="utf-8")
        print(f"written to {len(docs)} platform file(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
