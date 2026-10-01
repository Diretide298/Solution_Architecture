#!/usr/bin/env python3
"""Same-module links that carry nothing: a reason on each, or removed (1 October 2026, plan 2.6).

**Where they came from.** R251 (28 September) removed the inferred exits that carry nothing between
two *modules* and left the ones between siblings of one module for review (the note said 273; the
guest import brought it to 320), because a sibling link such as `WEB-012 Checkout -> WEB-010 Cart`
is usually a journey link whose ids the holds analysis missed. Each was a transition written by
`derive-carries-from-entrystate.py` whose provenance read *"... holds none of them, so the edge
carries nothing and X opens cold"*.

**What the review found.** Almost none of them open cold. The deriver now says why an edge carries
nothing (`why_nothing()`): the way back to the screen the source was opened from; the destination's
ids only pre-select (deep link or `optional`); the destination finds them itself; it opens on a list
it can read unaided; or the source is the module's hub and this is its menu entry. **That rule is
the fix for the class** -- it runs at every refresh. This script only brings the screen files to
where the next refresh would leave them, and does the one thing a deriver must not: it removes the
links that are still cold, since `exitTo` is authored.

**What it removes**, for each same-module edge of the R251 kind (the carries tool's own
transition, carrying nothing, trigger still the destination's name, the destination needing an id
that is neither `session` nor `optional`, no "Returns to" pair, no other transition to it) that the
rule still calls `cold`: both the transition and the `exitTo` entry. A cold link between two
screens of one module is redundant with the module's own menu. A screen whose only ways in would go
is never stranded; it keeps its edges and is reported.

**Text edits, not a YAML dump**, so the hand formatting survives; each file is re-parsed and compared
with the intended change. `--skip FILE` leaves a platform file alone (its provenance is then
rewritten by the next refresh). Idempotent. No arguments previews; `--apply` writes.
"""
from __future__ import annotations

import collections
import glob
import importlib.util
import pathlib
import re
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[2]
TOOLS = ROOT / "tools"


def _load(name: str, path: pathlib.Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


d = _load("derive_carries", TOOLS / "derive-carries-from-entrystate.py")
base = d.base


def must_carry(screen: dict) -> list[str]:
    return [p["name"] for p in d.entry_params(screen)
            if p.get("from") != d.SESSION and not p.get("optional")]


def render_provenance(text: str) -> list[str]:
    """The provenance lines exactly as `yaml.safe_dump` writes them at a transition's depth."""
    out = yaml.safe_dump({"screens": [{"navigation": {"transitions": [
        {"to": "X", "provenance": text}]}}]}, sort_keys=False, allow_unicode=True, width=100)
    lines = out.rstrip("\n").split("\n")
    return lines[lines.index("    - to: X") + 1:]


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass
    apply = "--apply" in sys.argv
    skip = {a for i, a in enumerate(sys.argv) if i and sys.argv[i - 1] == "--skip"}
    files = sorted(glob.glob(str(ROOT / "screens" / "P*.yaml")))
    docs = {f: yaml.safe_load(open(f, encoding="utf-8")) for f in files}
    screens = {s["id"]: s for doc in docs.values() for s in doc["screens"]}
    platform = {s["id"]: f for f, doc in docs.items() for s in doc["screens"]}
    contracts = d.Contracts()
    held = {sid: d.holds(s, contracts) for sid, s in screens.items()}
    reads = {sid: d.contracts_of(s, contracts) for sid, s in screens.items()}

    def carries_for(src: str, dst: str) -> list[str]:
        ok = reads[dst] | {d.ANY} if reads[dst] else None
        return [n for n in d.needed(screens[dst])
                if n in held[src] and (ok is None or held[src][n] & ok)]

    reprov: dict[str, dict[str, str]] = collections.defaultdict(dict)   # sid -> {to: provenance}
    drop: dict[str, list[str]] = collections.defaultdict(list)
    split: collections.Counter = collections.Counter()
    for sid, s in screens.items():
        trans = (s.get("navigation") or {}).get("transitions") or []
        for t in trans:
            dst = base(t.get("to"))
            if not d.is_mine(t) or t.get("carries") or dst not in screens or carries_for(sid, dst):
                continue
            kind, why = d.why_nothing(sid, dst, screens, contracts)
            new = d.provenance(sid, dst, d.needed(screens[dst]), [], why)
            the_class = (t.get("trigger") == screens[dst].get("name") and must_carry(screens[dst])
                         and sid not in ((screens[dst].get("navigation") or {}).get("entryFrom") or [])
                         and sum(1 for u in trans if base(u.get("to")) == dst) == 1
                         and s.get("module") == screens[dst].get("module"))
            if the_class:
                split[kind] += 1
                if kind == "cold":
                    drop[sid].append(dst)
                    continue
            if new != t.get("provenance"):
                reprov[sid][t.get("to")] = new

    # Never strand a screen (the R251 rule).
    inbound: dict[str, set[str]] = collections.defaultdict(set)
    for sid, s in screens.items():
        nav = s.get("navigation") or {}
        for e in set(nav.get("exitTo") or []) | {base(t.get("to")) for t in nav.get("transitions") or []}:
            inbound[e].add(sid)
        for p in nav.get("entryFrom") or []:
            inbound[sid].add(p)
    stranded = []
    for dst in sorted({x for v in drop.values() for x in v}):
        losing = {sid for sid, v in drop.items() if dst in v}
        if inbound[dst] <= losing:
            stranded.append(dst)
            for sid in losing:
                drop[sid].remove(dst)
    drop = {k: v for k, v in drop.items() if v}

    per_file: dict[str, list[int]] = {}
    for f in files:
        name = pathlib.Path(f).name
        mine = {sid for sid in set(reprov) | set(drop) if platform[sid] == f}
        if not mine or name in skip:
            if mine:
                print(f"  {name}: skipped ({sum(len(reprov.get(x, {})) for x in mine)} provenance, "
                      f"{sum(len(drop.get(x, [])) for x in mine)} removal(s) left)")
            continue
        raw = open(f, "rb").read().decode("utf-8")
        crlf = "\r\n" in raw
        text = raw.replace("\r\n", "\n")
        want = yaml.safe_load(text)
        want_s = {s["id"]: s for s in want["screens"]}
        for sid in sorted(mine):
            start = text.index(f"\n- id: {sid}\n") + 1
            nxt = text.find("\n- id: ", start)
            end = nxt + 1 if nxt >= 0 else len(text)
            nav_at = text.find("\n  navigation:\n", start - 1, end)
            m = re.compile(r"\n  [A-Za-z]").search(text, nav_at + 1, end)
            nav_end = m.start() + 1 if m else end
            lines = text[nav_at + 1:nav_end].split("\n")
            out, i, sect = [], 0, None
            gone = set(drop.get(sid, []))
            while i < len(lines):
                ln = lines[i]
                if re.match(r"^    [A-Za-z]+:", ln):
                    sect = ln.strip().rstrip(":")
                if sect == "exitTo" and ln.startswith("    - ") and ln[6:].strip() in gone:
                    i += 1
                    continue
                mt = re.match(r"^    - to: (\S+)$", ln)
                if sect == "transitions" and mt:
                    j = i + 1
                    while j < len(lines) and lines[j].startswith("      "):
                        j += 1
                    block = lines[i:j]
                    to = mt.group(1)
                    flat = re.sub(r"\s+", " ", "\n".join(block))
                    if base(to) in gone and d.MINE_MARK in flat:
                        i = j
                        continue
                    if to in reprov.get(sid, {}):
                        k = next(n for n, x in enumerate(block) if x.startswith("      provenance:"))
                        e = k + 1
                        while e < len(block) and block[e].startswith("        "):
                            e += 1
                        block = block[:k] + render_provenance(reprov[sid][to]) + block[e:]
                    out.extend(block)
                    i = j
                    continue
                out.append(ln)
                i += 1
            seg = re.sub(r"\n    (exitTo|transitions):\n(?!    - )", "\n", "\n".join(out))
            text = text[:nav_at + 1] + seg + text[nav_end:]
            # the intended result, in memory
            nav = want_s[sid].get("navigation") or {}
            if gone:
                nav["exitTo"] = [x for x in nav.get("exitTo") or [] if x not in gone]
                nav["transitions"] = [t for t in nav.get("transitions") or []
                                      if not (base(t.get("to")) in gone and d.is_mine(t))]
                for k in ("exitTo", "transitions"):
                    if not nav[k]:
                        del nav[k]
            for t in nav.get("transitions") or []:
                if t.get("to") in reprov.get(sid, {}):
                    t["provenance"] = reprov[sid][t["to"]]
        if yaml.safe_load(text) != want:
            raise SystemExit(f"{name}: the edited text does not parse to the intended change")
        per_file[name] = [sum(len(reprov.get(x, {})) for x in mine),
                          sum(len(drop.get(x, [])) for x in mine)]
        if apply:
            open(f, "wb").write((text.replace("\n", "\r\n") if crlf else text).encode("utf-8"))

    for name, (p, r) in per_file.items():
        print(f"  {name}: {p} provenance line(s) rewritten, {r} link(s) removed")
    for sid, v in sorted(drop.items()):
        for dst in v:
            print(f"  removed  {sid} {screens[sid]['name']} -> {dst} {screens[dst]['name']}")
    if stranded:
        print(f"kept, because removing them would leave the screen unreachable: {stranded}")
    total = sum(split.values())
    print(f"{total} same-module link(s) of the R251 kind that carry nothing: "
          + ", ".join(f"{k} {v}" for k, v in split.most_common())
          + f" -- {'written' if apply else 'pending (run with --apply)'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
