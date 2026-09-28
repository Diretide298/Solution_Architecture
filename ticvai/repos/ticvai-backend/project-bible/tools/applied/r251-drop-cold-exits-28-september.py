#!/usr/bin/env python3
"""Remove the inferred exits that carry nothing (decided 28 September 2026, audit R251).

**The decision.** Navigation is re-derived so that a screen links only to screens it can pass the
needed ids to, and every "Returns to X" is mirrored on both screens. Inferred exits such as
`BO-079 Stock Count -> BO-001 Queue Directory` are removed.

**Where those exits came from.** Exit lists were seeded from module nav-sets (the menu of the
module a screen sits in), and `derive-carries-from-entrystate.py` then wrote each one a transition
whose provenance reads *"derived — X declares entryState.params … and Y holds none of them, so the
edge carries nothing and X opens cold"*. That sentence is the tool saying the link is not real.

**What this removes**, for each such transition, both the transition and the `exitTo` entry:

- the transition is the carries tool's own (provenance `derived — … declares entryState.params`),
  carries nothing, and its trigger is still the destination's name (a trigger a person renamed is
  somebody's decision and stays);
- the destination needs at least one id that is neither `from: session` nor `optional` (a
  destination that can open without one is a real link, cold or not);
- the destination does not list the source in `entryFrom` (that is a "Returns to X" pair, which
  R251 keeps and mirrors);
- no other transition from the source reaches the destination (a flow or board edge wins);
- the destination is in **another module**. That is the module-menu exit the decision names
  (`Stock & Supply` -> `Access & Venue`). A cold edge between siblings of one module, such as
  `WEB-012 Checkout -> WEB-010 Shopping Cart`, is usually a journey link whose ids the holds
  analysis missed, so it is left for review rather than removed blind.

**Text edits, not a YAML dump**, so the hand formatting of the screen files survives; every file is
re-parsed afterwards and the result compared with the intended change.

Idempotent. No arguments previews; `--apply` writes.
"""
from __future__ import annotations

import glob
import pathlib
import re
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[2]
MINE = "derived — "
MINE_MARK = "declares entryState.params"


def base(to) -> str:
    return str(to or "").partition("#")[0]


def must_carry(screen: dict) -> list[str]:
    out = []
    for p in ((screen.get("entryState") or {}).get("params") or []):
        if isinstance(p, str):
            p = {"name": p}
        if isinstance(p, dict) and p.get("name") and p.get("from") != "session" and not p.get("optional"):
            out.append(p["name"])
    return out


def candidates(screens: dict) -> dict[str, list[str]]:
    drop: dict[str, list[str]] = {}
    for sid, s in screens.items():
        nav = s.get("navigation") or {}
        trans = nav.get("transitions") or []
        for t in trans:
            dst = base(t.get("to"))
            prov = str(t.get("provenance", ""))
            if not (prov.startswith(MINE) and MINE_MARK in prov) or t.get("carries") or dst not in screens:
                continue
            if t.get("trigger") != screens[dst].get("name"):
                continue
            if not must_carry(screens[dst]):
                continue
            if sid in ((screens[dst].get("navigation") or {}).get("entryFrom") or []):
                continue
            if sum(1 for u in trans if base(u.get("to")) == dst) > 1:
                continue
            if s.get("module") == screens[dst].get("module"):
                # A sibling in the same module (Checkout back to Cart) is a journey link the
                # holds-analysis may simply have missed; left for review, not removed blind.
                continue
            drop.setdefault(sid, []).append(dst)
    # **Never strand a screen.** Where every way into a destination would go, its edges stay and
    # the screen is reported instead: an unreachable screen is a worse defect than a cold link.
    inbound: dict[str, set[str]] = {}
    for sid, s in screens.items():
        nav = s.get("navigation") or {}
        for d in set(nav.get("exitTo") or []) | {base(t.get("to")) for t in nav.get("transitions") or []}:
            inbound.setdefault(d, set()).add(sid)
        for p in nav.get("entryFrom") or []:
            inbound.setdefault(sid, set()).add(p)
    for dst in sorted({d for v in drop.values() for d in v}):
        losing = {sid for sid, v in drop.items() if dst in v}
        if inbound.get(dst) and inbound[dst] <= losing:
            STRANDED.append(dst)
            for sid in losing:
                drop[sid].remove(dst)
    return {k: v for k, v in drop.items() if v}


STRANDED: list[str] = []


def edit_segment(seg: str, targets: list[str]) -> str:
    lines = seg.split("\n")
    out, i = [], 0
    in_exit = in_trans = False
    while i < len(lines):
        ln = lines[i]
        if ln == "    exitTo:":
            in_exit, in_trans = True, False
        elif ln == "    transitions:":
            in_trans, in_exit = True, False
        elif not ln.startswith("    - ") and not ln.startswith("      ") and ln.strip():
            in_exit = in_trans = False
        if in_exit and ln.startswith("    - ") and ln[6:].strip() in targets:
            i += 1
            continue
        m = re.match(r"^    - to: (\S+)$", ln)
        if in_trans and m and base(m.group(1)) in targets:
            j = i + 1
            while j < len(lines) and lines[j].startswith("      "):
                j += 1
            block = "\n".join(lines[i:j])
            if MINE_MARK in re.sub(r"\s+", " ", block):
                i = j
                continue
        out.append(ln)
        i += 1
    # A list emptied by the removal must not stay as a null key: check-screens iterates it.
    return re.sub(r"\n    (exitTo|transitions):\n(?!    - )", "\n", "\n".join(out))


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass
    apply = "--apply" in sys.argv
    files = sorted(glob.glob(str(ROOT / "screens" / "P*.yaml")))
    docs = {f: yaml.safe_load(open(f, encoding="utf-8")) for f in files}
    screens = {s["id"]: s for d in docs.values() for s in d["screens"]}
    drop = candidates(screens)
    total = sum(len(v) for v in drop.values())
    per_file: dict[str, int] = {}
    for f in files:
        mine = {sid: v for sid, v in drop.items() if any(s["id"] == sid for s in docs[f]["screens"])}
        if not mine:
            continue
        raw = open(f, "rb").read().decode("utf-8")
        crlf = "\r\n" in raw
        text = raw.replace("\r\n", "\n")
        for sid, targets in mine.items():
            start = text.index(f"\n- id: {sid}\n") + 1
            nxt = text.find("\n- id: ", start)
            end = nxt + 1 if nxt >= 0 else len(text)
            nav_at = text.find("\n  navigation:\n", start - 1, end)
            if nav_at < 0:
                raise SystemExit(f"{sid}: no navigation block")
            nav_end = nav_at + 1
            m = re.compile(r"\n  [A-Za-z]").search(text, nav_at + 1, end)
            nav_end = m.start() + 1 if m else end
            text = text[:nav_at + 1] + edit_segment(text[nav_at + 1:nav_end], targets) + text[nav_end:]
        after = yaml.safe_load(text)
        # verify: exactly the intended exits and transitions are gone, nothing else moved
        before_s = {s["id"]: s for s in docs[f]["screens"]}
        for s in after["screens"]:
            b = before_s[s["id"]]
            gone = set(mine.get(s["id"], []))
            nb, na = b.get("navigation") or {}, s.get("navigation") or {}
            want_exit = [e for e in (nb.get("exitTo") or []) if e not in gone]
            want_tr = [t for t in (nb.get("transitions") or [])
                       if not (base(t.get("to")) in gone and MINE_MARK in str(t.get("provenance", "")))]
            if (na.get("exitTo") or []) != want_exit or (na.get("transitions") or []) != want_tr:
                raise SystemExit(f"{f}: {s['id']} navigation did not come out as intended")
            if {k: v for k, v in s.items() if k != "navigation"} != {k: v for k, v in b.items() if k != "navigation"}:
                raise SystemExit(f"{f}: {s['id']} changed outside navigation")
        per_file[pathlib.Path(f).name] = sum(len(v) for v in mine.values())
        if apply:
            open(f, "wb").write((text.replace("\n", "\r\n") if crlf else text).encode("utf-8"))
    for name, n in per_file.items():
        print(f"  {name}: {n}")
    if STRANDED:
        print(f"kept, because removing them would leave the screen unreachable: {STRANDED}")
    print(f"{total} inferred exit(s) that carry nothing across {len(drop)} screen(s) — "
          + ("removed" if apply else "pending (run with --apply)"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
