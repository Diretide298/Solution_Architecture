#!/usr/bin/env python3
"""Label navigation edges from the flows, which have been half-writing them all along.

**94 flows hold 275 ordered screen pairs**, each step naming the screen, what the actor does and
which operations run. An edge that appears in a flow is an edge somebody walked; the screens have
never read them.

**99 of the 275 are already in an `exitTo` and get labelled.** The other 176 are not in any
`exitTo` at all — the flows and the screens disagree about what connects to what, and nothing had
ever compared them. `--adopt` resolves that disagreement, and **the two halves resolve
differently, because the package already has a convention and it is nearly absolute.**

**2,683 of the 2,684 existing `exitTo` edges stay inside one platform.** Exactly one crosses, and
it was added by hand yesterday. So `exitTo` means *navigation within an app* — not "any screen the
work reaches next".

- **107 of the 176 are same-platform.** A flow walked from one screen to another inside one app
  and the screen never declared the exit. That is a missing edge and it is adopted: added to
  `exitTo` and labelled.
- **69 are cross-platform** — a steward's app to the back office, a till to management. **Nobody
  navigates there; they pick the work up somewhere else, on another device, often as another
  person.** Adding those to `exitTo` would put 69 exceptions against a 2,683-to-1 convention and
  would make the reachability check read a handover as a click. They are recorded as transitions
  carrying `crossesDevice: true` — which is what that field, unused until now, exists for (the
  24 August rule) — and deliberately left out of `exitTo`.

**What it will not guess.** `carries` — the field the whole exercise exists for — is not in the
flows, and neither is the label on the control. A derived transition says *you get from A to B,
and here is the flow step where somebody did it*; a human still has to say what travels and what
the button reads. An `operation` is cited **only when exactly one of the departing step's
operations is declared on the departing screen**, because a citation that names the wrong call is
worse than no citation: it reads as fact.

Ownership follows the rule the rest of the package uses. Anything this tool writes leads with
`flow `; anything that does not is another source's and is left alone. A board-derived transition
outranks a flow-derived one and is never overwritten.

Idempotent. Run with no arguments to see what it would do; `--apply` to write.
"""

from __future__ import annotations
import collections
import glob
import pathlib
import re
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
MINE = "flow "


def first_sentence(text: str, limit: int = 110) -> str:
    """The action, as one clause. Flow actions are prose; a trigger has to be short."""
    t = " ".join(str(text or "").split())
    t = re.sub(r"\*\*(.+?)\*\*", r"\1", t)
    m = re.split(r"(?<=[.;])\s", t)
    out = m[0] if m else t
    if len(out) > limit:
        out = out[:limit].rsplit(" ", 1)[0] + "…"
    return out.rstrip(".")


def main() -> int:
    apply = "--apply" in sys.argv
    adopt = "--adopt" in sys.argv

    files = sorted(glob.glob(str(ROOT / "screens" / "P*.yaml")))
    docs = {f: yaml.safe_load(open(f, encoding="utf-8")) for f in files}
    screens = {s["id"]: s for d in docs.values() for s in d["screens"]}
    platform = {s["id"]: d["platform"]["code"] for d in docs.values() for s in d["screens"]}

    # pair -> {"triggers": [...], "cites": [...], "ops": [set per flow]}
    found: dict[tuple, dict] = collections.defaultdict(
        lambda: {"triggers": [], "cites": [], "ops": []})

    for f in sorted(glob.glob(str(ROOT / "flows" / "F*.yaml"))):
        d = yaml.safe_load(open(f, encoding="utf-8")) or {}
        steps = d.get("steps") or []
        for a, b in zip(steps, steps[1:]):
            sa, sb = a.get("screen"), b.get("screen")
            if not sa or not sb or sa == sb:
                continue
            rec = found[(sa, sb)]
            rec["triggers"].append(first_sentence(b.get("action")))
            rec["cites"].append(f"{d.get('id')} step {a.get('step')}→{b.get('step')}")
            rec["ops"].append(list(a.get("operations") or []))

    labellable, disagree = {}, []
    for (sa, sb), rec in found.items():
        exits = ((screens.get(sa) or {}).get("navigation") or {}).get("exitTo") or []
        if sb in exits:
            labellable[(sa, sb)] = rec
        else:
            disagree.append((sa, sb, rec))

    written = 0
    stronger = 0
    touched: set[str] = set()
    for (sa, sb), rec in sorted(labellable.items()):
        screen = screens[sa]
        nav = screen.setdefault("navigation", {})
        existing = nav.get("transitions") or []

        # **A transition another source wrote outranks this one.** Board- and hand-written
        # entries lead with something other than `flow `, and are never touched.
        if any(str(t.get("to", "")).partition("#")[0] == sb
               and not str(t.get("provenance", "")).startswith(MINE)
               for t in existing):
            stronger += 1
            continue

        own_ops = {a.get("operationId") for a in (screen.get("apis") or [])}
        cands = {o for ops in rec["ops"] for o in ops} & own_ops
        entry = {
            "to": sb,
            "trigger": rec["triggers"][0],
            "provenance": MINE + ", ".join(sorted(set(rec["cites"]))),
        }
        if len(cands) == 1:
            entry["operation"] = next(iter(cands))

        rest = [t for t in existing if str(t.get("to", "")).partition("#")[0] != sb]
        if existing == rest + [entry] or entry in existing:
            continue
        written += 1
        touched.add(sa)
        if apply:
            nav["transitions"] = rest + [entry]

    print(f"{len(found)} distinct screen pair(s) in the flows")
    current = len(labellable) - written - stronger
    print(f"  {len(labellable)} already in an exitTo  — {written} to write, {current} already "
          f"current, {stronger} owned by a stronger source (board- or hand-written)")
    print(f"  {len(disagree)} NOT in any exitTo — reported, not acted on\n")

    adopted = handovers = 0
    if adopt:
        for sa, sb, rec in sorted(disagree):
            screen = screens.get(sa)
            if screen is None:
                continue
            nav = screen.setdefault("navigation", {})
            existing = nav.get("transitions") or []
            if any(str(t.get("to", "")).partition("#")[0] == sb
                   and not str(t.get("provenance", "")).startswith(MINE)
                   for t in existing):
                continue

            own_ops = {a.get("operationId") for a in (screen.get("apis") or [])}
            cands = {o for ops in rec["ops"] for o in ops} & own_ops
            entry = {
                "to": sb,
                "trigger": rec["triggers"][0],
                "provenance": MINE + ", ".join(sorted(set(rec["cites"]))),
            }
            if len(cands) == 1:
                entry["operation"] = next(iter(cands))

            same = platform.get(sa) == platform.get(sb)
            if not same:
                # **A handover, not a link.** No `exitTo` entry: the operator does not click here.
                entry["crossesDevice"] = True
                entry["back"] = False

            # **Already current is not the same as absent**, and the entry has to be complete
            # before it can be compared — the handover fields are added above. Without this the
            # 69 handovers were rewritten on every run: identical content, but all fifteen files
            # marked dirty, and the report read "69 labelled" whether anything had happened or
            # not. A rebuild that changes nothing must say so.
            if any(t == entry for t in existing):
                continue

            if same:
                # A missing edge inside one app. The flow is the evidence it exists.
                adopted += 1
                if apply:
                    exits = nav.setdefault("exitTo", [])
                    if sb not in exits:
                        exits.append(sb)
                        exits.sort()
                    entered = (screens[sb].setdefault("navigation", {})
                               .setdefault("entryFrom", []))
                    if sa not in entered:
                        entered.append(sa)
                        entered.sort()
            else:
                handovers += 1
            if apply:
                nav["transitions"] = [t for t in existing
                                      if str(t.get("to", "")).partition("#")[0] != sb] + [entry]
                touched.add(sa)
                if same:
                    touched.add(sb)
        print(f"  --adopt: {adopted} same-platform edge(s) added to exitTo and labelled, "
              f"{handovers} cross-platform handover(s) labelled with crossesDevice\n")

    if apply and (written or adopted or handovers):
        for f, d in docs.items():
            if any(s["id"] in touched for s in d["screens"]):
                pathlib.Path(f).write_text(
                    yaml.safe_dump(d, sort_keys=False, allow_unicode=True, width=100),
                    encoding="utf-8")
        print(f"written to {sum(1 for f, d in docs.items() if any(s['id'] in touched for s in d['screens']))} platform file(s)\n")
    elif written:
        print("run with --apply to write\n")

    if not adopt:
        print("The flows and the screens disagree about these — run --adopt to resolve them:")
        for sa, sb, rec in sorted(disagree)[:12]:
            print(f"  {sa} → {sb:9} {rec['cites'][0]:18} {rec['triggers'][0][:52]}")
        if len(disagree) > 12:
            print(f"  … and {len(disagree) - 12} more")
    return 0


if __name__ == "__main__":
    sys.exit(main())
